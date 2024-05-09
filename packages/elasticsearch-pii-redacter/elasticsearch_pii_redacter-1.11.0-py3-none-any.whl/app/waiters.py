"""The function that waits

...and its helpers
"""

import logging
from time import localtime, sleep, strftime
from datetime import datetime
from app.exceptions import (
    ConfigurationException,
    FailedReindex,
    MissingArgument,
    ResultNotExpected,
    TimeoutException,
)
from app.helpers import chunk_index_list


def health_check(client, **kwargs):
    """
    This function calls :py:meth:`~.elasticsearch.client.ClusterClient.health`
    and, based on the params provided, will return ``True`` or ``False`` depending on
    whether that particular keyword appears in the output, and has the expected value.

    If multiple keys are provided, all must match for a ``True`` response.

    :param client: A client connection object

    :type client: :py:class:`~.elasticsearch.Elasticsearch`

    :rtype: bool
    """
    logger = logging.getLogger(__name__)
    logger.debug('KWARGS= "%s"', kwargs)
    klist = list(kwargs.keys())
    if not klist:
        raise MissingArgument("Must provide at least one keyword argument")
    hc_data = client.cluster.health()
    response = True

    for k in klist:
        # First, verify that all kwargs are in the list
        if k not in list(hc_data.keys()):
            raise ResultNotExpected('Key "{0}" not in cluster health output')
        if not hc_data[k] == kwargs[k]:
            msg = (
                f'NO MATCH: Value for key "{kwargs[k]}", health check data: '
                f"{hc_data[k]}"
            )
            logger.debug(msg)
            response = False
        else:
            msg = f'MATCH: Value for key "{kwargs[k]}", health check data: {hc_data[k]}'
            logger.debug(msg)
    if response:
        logger.debug("Health Check for all provided keys passed.")
    return response


def relocate_check(client, index):
    """
    This function calls :py:meth:`~.elasticsearch.client.ClusterClient.state`
    with a given index to check if all of the shards for that index are in the
    ``STARTED`` state. It will return ``True`` if all primary and replica shards are in
    the ``STARTED`` state, and it will return ``False`` if any shard is in a different
    state.

    :param client: A client connection object
    :param index: The index name

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index: str

    :rtype: bool
    """
    logger = logging.getLogger(__name__)
    shard_state_data = client.cluster.state(index=index)["routing_table"]["indices"][
        index
    ]["shards"]
    finished_state = all(
        all(shard["state"] == "STARTED" for shard in shards)
        for shards in shard_state_data.values()
    )
    if finished_state:
        logger.debug('Relocate Check for index: "%s" has passed.', index)
    return finished_state


def restore_check(client, index_list):
    """
    This function calls :py:meth:`~.elasticsearch.client.IndicesClient.recovery`
    with the list of indices to check for complete recovery.  It will return ``True``
    if recovery of those indices is complete, and ``False`` otherwise.  It is designed
    to fail fast: if a single shard is encountered that is still recovering (not in
    ``DONE`` stage), it will immediately return ``False``, rather than complete
    iterating over the rest of the response.

    :param client: A client connection object
    :param index_list: The list of indices to verify having been restored.

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type index_list: list

    :rtype: bool
    """
    logger = logging.getLogger(__name__)
    response = {}
    for chunk in chunk_index_list(index_list):
        try:
            chunk_response = client.indices.recovery(index=chunk, human=True)
        except Exception as err:
            msg = (
                f"Unable to obtain recovery information for specified indices. Error: "
                f"{err}"
            )
            raise ResultNotExpected(msg) from err
        if chunk_response == {}:
            logger.debug("_recovery returned an empty response. Trying again.")
            return False
        response.update(chunk_response)
    logger.debug("Provided indices: %s", index_list)
    logger.debug("Found indices: %s", list(response.keys()))
    # pylint: disable=consider-using-dict-items
    for index in response:
        for shard in range(0, len(response[index]["shards"])):
            stage = response[index]["shards"][shard]["stage"]
            if stage != "DONE":
                logger.debug('Index "%s" is still in stage "%s"', index, stage)
                return False

    # If we've gotten here, all of the indices have recovered
    return True


def snapshot_check(client, snapshot=None, repository=None):
    """
    This function calls :py:meth:`~.elasticsearch.client.SnapshotClient.get` and
    tests to see whether the snapshot is complete, and if so, with what status.  It
    will log errors according to the result. If the snapshot is still ``IN_PROGRESS``,
    it will return ``False``. ``SUCCESS`` will be an ``INFO`` level message,
    ``PARTIAL`` nets a ``WARNING`` message, ``FAILED`` is an ``ERROR``, message, and
    all others will be a ``WARNING`` level message.

    :param client: A client connection object
    :param snapshot: The snapshot name
    :param repository: The repository name

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type snapshot: str
    :type repository: str

    :rtype: bool
    """
    logger = logging.getLogger(__name__)
    logger.debug("SNAPSHOT: %s", snapshot)
    logger.debug("REPOSITORY: %s", repository)
    try:
        result = client.snapshot.get(repository=repository, snapshot=snapshot)
        logger.debug("RESULT: %s", result)
    except Exception as err:
        raise ResultNotExpected(
            f'Unable to obtain information for snapshot "{snapshot}" in repository '
            f'"{repository}". Error: {err}'
        ) from err
    state = result["snapshots"][0]["state"]
    logger.debug("Snapshot state = %s", state)
    retval = True
    if state == "IN_PROGRESS":
        logger.debug("Snapshot %s still in progress.", snapshot)
        retval = False
    elif state == "SUCCESS":
        logger.info("Snapshot %s successfully completed.", snapshot)
    elif state == "PARTIAL":
        logger.warning("Snapshot %s completed with state PARTIAL.", snapshot)
    elif state == "FAILED":
        logger.error("Snapshot %s completed with state FAILED.", snapshot)
    else:
        logger.warning("Snapshot %s completed with state: %s", snapshot, state)
    return retval


def task_check(client, task_id=None):
    """
    This function calls :py:meth:`~.elasticsearch.client.TasksClient.get` with the
    provided ``task_id``.  If the task data contains ``'completed': True``, then it
    will return ``True``. If the task is not completed, it will log some information
    about the task and return ``False``

    :param client: A client connection object
    :param task_id: The task id

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type task_id: str

    :rtype: bool
    """
    logger = logging.getLogger(__name__)
    try:
        task_data = client.tasks.get(task_id=task_id)
    except Exception as err:
        msg = (
            f'Unable to obtain task information for task_id "{task_id}". Exception '
            f"{err}"
        )
        raise ResultNotExpected(msg) from err
    task = task_data["task"]
    completed = task_data["completed"]
    if task["action"] == "indices:data/write/reindex":
        logger.debug("It's a REINDEX TASK")
        logger.debug("TASK_DATA: %s", task_data)
        logger.debug("TASK_DATA keys: %s", list(task_data.keys()))
        if "response" in task_data:
            response = task_data["response"]
            if response["failures"]:
                msg = f'Failures found in reindex response: {response["failures"]}'
                raise FailedReindex(msg)
    running_time = 0.000000001 * task["running_time_in_nanos"]
    logger.debug("Running time: %s seconds", running_time)
    descr = task["description"]

    if completed:
        completion_time = (running_time * 1000) + task["start_time_in_millis"]
        time_string = strftime("%Y-%m-%dT%H:%M:%S", localtime(completion_time / 1000))
        logger.debug('Task "%s" completed at %s.', descr, time_string)
        retval = True
    else:
        # Log the task status here.
        logger.debug("Full Task Data: %s", task_data)
        msg = (
            f'Task "{descr}" with task_id "{task_id}" has been running for '
            f"{running_time} seconds"
        )
        logger.debug(msg)
        retval = False
    return retval


# pylint: disable=too-many-locals, too-many-arguments
def wait_for_it(
    client,
    action,
    task_id=None,
    snapshot=None,
    repository=None,
    index=None,
    index_list=None,
    wait_interval=9,
    max_wait=-1,
):
    """
    This function becomes one place to do all ``wait_for_completion`` type behaviors

    :param client: A client connection object
    :param action: The action name that will identify how to wait
    :param task_id: If the action provided a task_id, this is where it must be declared.
    :param snapshot: The name of the snapshot.
    :param repository: The Elasticsearch snapshot repository to use
    :param wait_interval: Seconds to wait between completion checks.
    :param max_wait: Maximum number of seconds to ``wait_for_completion``

    :type client: :py:class:`~.elasticsearch.Elasticsearch`
    :type action: str
    :type task_id: str
    :type snapshot: str
    :type repository: str
    :type wait_interval: int
    :type max_wait: int
    :rtype: None
    """
    logger = logging.getLogger(__name__)
    task_actions = ["forcemerge", "reindex", "update_by_query"]
    action_map = {
        "allocation": {"function": health_check, "args": {"relocating_shards": 0}},
        "cluster_routing": {"function": health_check, "args": {"relocating_shards": 0}},
        "forcemerge": {"function": task_check, "args": {"task_id": task_id}},
        "mount": {"function": health_check, "args": {"status": "green"}},
        "reindex": {"function": task_check, "args": {"task_id": task_id}},
        "relocate": {"function": relocate_check, "args": {"index": index}},
        "replicas": {"function": health_check, "args": {"status": "green"}},
        "restore": {"function": restore_check, "args": {"index_list": index_list}},
        "shrink": {"function": health_check, "args": {"status": "green"}},
        "snapshot": {
            "function": snapshot_check,
            "args": {"snapshot": snapshot, "repository": repository},
        },
        "update_by_query": {"function": task_check, "args": {"task_id": task_id}},
    }
    wait_actions = list(action_map.keys())

    if action not in wait_actions:
        raise ConfigurationException(f'"action" must be one of {wait_actions}')
    if action in task_actions and task_id is None:
        raise MissingArgument(f'A task_id must accompany "action" {action}')
    if action == "snapshot" and ((snapshot is None) or (repository is None)):
        raise MissingArgument(
            f'A snapshot and repository must accompany "action" {action}. snapshot: '
            f"{snapshot}, repository: {repository}"
        )
    if action == "restore" and index_list is None:
        raise MissingArgument(f'An index_list must accompany "action" {action}')
    if action in task_actions:
        try:
            _ = client.tasks.get(task_id=task_id)
        except Exception as err:
            # This exception should only exist in API usage.
            raise ResultNotExpected(
                f"Unable to find task_id {task_id}. Exception: {err}"
            ) from err

    # Now with this mapped, we can perform the wait as indicated.
    start_time = datetime.now()
    result = False
    while True:
        elapsed = int((datetime.now() - start_time).total_seconds())
        logger.debug("Elapsed time: %s seconds", elapsed)
        response = action_map[action]["function"](client, **action_map[action]["args"])
        # logger.debug('Response: %s', response)
        # Success
        if response:
            logger.debug(
                'Action "%s" finished executing (may or may not have been successful)',
                action,
            )
            result = True
            break
        # Not success, and reached maximum wait (if defined)
        if (max_wait != -1) and (elapsed >= max_wait):
            msg = (
                f'Unable to complete action "{action}" within max_wait ({max_wait}) '
                f"seconds."
            )
            logger.error(msg)
            break
        # Not success, so we wait.
        msg = (
            f'Action "{action}" not yet complete, {elapsed} total seconds elapsed. '
            f"Waiting {wait_interval} seconds before checking again."
        )
        logger.debug(msg)
        sleep(wait_interval)

    logger.debug("Result: %s", result)
    if not result:
        raise TimeoutException(
            f'Action "{action}" failed to complete in the max_wait period of '
            f"{max_wait} seconds"
        )
