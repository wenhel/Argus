"""Status module: check status

Contains methods to check status of each type of queries: system, experiment and chunks

"""
import json
import os

###### Check chunk ############################################################

def check_status_chunk(query_type, command_history_dict, status_dict, **kwargs):
    """Check status of a specific chunk id during experiment processing.

    Use the process-chunk state to get the status of a given chunk id.

    Args:
        query_type (str): Type of status query, chunk in this case
        command_history_dict (:obj: `dict`): Dictionary of this form::

            {'command name': [{'status': 'start', id: '98', args: {...}} ...], ...}

        status_dict (:obj: `dict`): Dictionary of status according to a query type, a command name and a state
        **kwargs: Arbitrary keyword arguments

    Return:
        str: status of the chunk id

    """
    chunk_id = kwargs.get('chunk_id', None)
    status = 'Not processed'

    process_chunk_command = 'process-chunk'
    process_chunk = command_history_dict[process_chunk_command].pop()
    process_chunk_status = process_chunk['status']
    experiment_init_id = command_history_dict['experiment-init'].pop()['id']
    while process_chunk['status'] != 'not defined':
        if chunk_id == process_chunk['args']['chunk_id']:
            if process_chunk['id'] > experiment_init_id:
                status = get_status(query_type, process_chunk_command, process_chunk_status, status_dict)
                break
        process_chunk = command_history_dict['process-chunk'].pop()
        process_chunk_status = process_chunk['status']

    return status

###### Check experiment #######################################################

def check_status_experiment(query_type, command_history_dict, status_dict, **kwargs):
    """Check status of the experiment during the process.

    Use the experiment-init and cleanup and commands between (except pre/post/reset/process-chunk) to
    get status of the experiment.

    Args:
        query_type (str): Type of status query, chunk in this case
        command_history_dict (:obj: `dict`): Dictionary of this form::

            {'command name': [{'status': 'start', id: '98', args: {...}} ...], ...}

        status_dict (:obj: `dict`): Dictionary of status according to a query type, a command name and a state
        **kwargs: Arbitrary keyword arguments

    Return:
        str: status of the experiment

    """
    experiment_init_command = 'experiment-init'
    experiment_cleanup_command = 'experiment-cleanup'

    # Determine status of experiment-init first
    experiment_init = command_history_dict[experiment_init_command].pop()
    experiment_init_status = experiment_init['status']
    experiment_init_id = experiment_init['id']

    # Determine status of experiment cleanup
    experiment_cleanup = command_history_dict[experiment_cleanup_command].pop()
    experiment_cleanup_status = experiment_cleanup['status']
    experiment_cleanup_id = experiment_cleanup['id']

    status = get_status(query_type, experiment_init_command, experiment_init_status, status_dict)

    max_id = experiment_init_id
    # Determine status of all the commands between experiment-init and cleanup
    if status == 'In progress':

        commands_between_dict = command_history_dict.copy()
        # Remove commands not involved in the experiment status
        not_involved_commands = [experiment_init_command,
                                 experiment_cleanup_command,
                                 'system-setup',
                                 'design-chunks',
                                 'pre-process-chunk',
                                 'process-chunk',
                                 'post-process-chunk',
                                 'id']
        for not_involved_command in not_involved_commands:
            del commands_between_dict[not_involved_command]

        for command_name in commands_between_dict:
            command = commands_between_dict[command_name].pop()
            command_status = command['status']
            command_id = command['id']
            if max_id < command_id:
                max_id = command_id

            if experiment_init_id < command_id:
                status = get_status(query_type, 'others', command_status, status_dict)
                if status == 'Failed':
                    break

    if status != 'Not defined' and experiment_cleanup_id > max_id and max_id >= experiment_init_id:
        status = get_status(query_type, experiment_cleanup_command, experiment_cleanup_status, status_dict)
    return status

###### Check system ###########################################################

def check_status_system(query_type, command_history_dict, status_dict, **kwargs):
    """ Check status of the system.

    Use the system-setup state to get the status of the system.

    Args:
        query_type (str): Type of status query, chunk in this case
        command_history_dict (:obj: `dict`): Dictionary of this form::

            {'command name': [{'status': 'start', id: '98', args: {...}} ...], ...}

        status_dict (:obj: `dict`): Dictionary of status according to a query type, a command name and a state
        **kwargs: Arbitrary keyword arguments

    Return:
        str: status of the system

    """
    command = 'system-setup'
    system_status = command_history_dict[command].pop()['status']
    status = get_status(query_type, command, system_status, status_dict)
    return status

###### Main check function ####################################################

def check_status(query_type, **kwargs):
    """ Check status of a component of the system to know wether it is running properly.

    Args:
        query_type (str): Type of the component whose status has to be checked
    """
    status_methods = {'chunk-query': check_status_chunk,
                      'experiment-query': check_status_experiment,
                      'system-query': check_status_system}

    path = os.path.dirname(__file__)
    command_history_json = os.path.join(path, './command_state_monitoring.json')
    status_json = os.path.join(path, './status.json')


    with open(command_history_json) as f:
        command_history_dict = json.load(f)
    with open(status_json) as f:
        status_dict = json.load(f)

    status = status_methods[query_type](query_type, command_history_dict, status_dict, **kwargs)
    print(status)

def get_status(query_type, command, execution_status, status_dict):
    """ Get the status code of a command according to a query

    Args:
        query_type (str): Type of status query, chunk in this case
        command (str): Command name
        execution_status: State of the last given command execution
        status_dict (:obj: `dict`): Dictionary of status according to a query type, a command name and a state

    Return:
        str: status according to query type, command and execution status
    """
    return  status_dict[query_type][command][execution_status]

