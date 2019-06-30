"""Status module

"""
import json
import os
import logging

class StatusFactory():
    """Generate state of a given command each time it is called.
    """

    @staticmethod
    def generate_status(command, status, args):
        """Generate a dictionary inside a json file containing states of the commands

        Args:
            command (str): Command name
            status (str): State of the command ('Starting', 'Done', 'Not defined', 'Issue')

        """
        from diva_evaluation_cli.bin.cli import public_subcommands

        states_filename = './command_state_monitoring.json'
        path = os.path.dirname(__file__)
        command_states_log = os.path.join(path, states_filename)
        json_command_states = {}

        if os.path.isfile(command_states_log) and os.stat(command_states_log).st_size != 0:
            with open(command_states_log, 'r') as f:
                try:
                    json_command_states = json.load(f)
                    if command in public_subcommands:
                        json_command_states['id'] += 1
                        json_command_states[command.command].append({'status': status, 'id': json_command_states['id'], 'args': args})
                except:
                    logging.warning("Status monitoring improperly terminated: status reset")
                    if os.path.isfile(command_states_log):
                        os.remove(command_states_log)
			#os.remove(states_filename)

        if not os.path.isfile(command_states_log) or os.stat(command_states_log).st_size == 0:
            StatusFactory.generate_file(command_states_log, public_subcommands, json_command_states)
        

        with open(command_states_log, 'w+') as f:
            json.dump(json_command_states, f)



    @staticmethod
    def generate_file(filename, subcommands, json_command_states):
        """Initialize json file containing states of the commands

        Args:
            filename (str): Name of the json file
            subcommands (str): List of subcommands to monitor
            json_command_states (:obj:`dict`): Dictionary of command states to initialize
        """
        status_id = 0
        for subcommand in subcommands:
            json_command_states[subcommand.command] = [{'status': 'not defined', 'id': status_id, 'args': None}]
            status_id += 1
        json_command_states['id'] = status_id

