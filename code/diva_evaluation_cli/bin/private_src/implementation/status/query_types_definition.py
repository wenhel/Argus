"""Status module: query types definition

Dictionary of system types:
    * key: name of the query type
    * value: command to get status
"""

from diva_evaluation_cli.bin.commands.actev_status_subcommands.chunk_query_command import ActevStatusChunkQuery
from diva_evaluation_cli.bin.commands.actev_status_subcommands.experiment_query_command import ActevStatusExperimentQuery
from diva_evaluation_cli.bin.commands.actev_status_subcommands.system_query_command import ActevStatusSystemQuery


query_types = {
    'chunk-query': ActevStatusChunkQuery,
    'experiment-query': ActevStatusExperimentQuery,
    'system-query': ActevStatusSystemQuery
}


