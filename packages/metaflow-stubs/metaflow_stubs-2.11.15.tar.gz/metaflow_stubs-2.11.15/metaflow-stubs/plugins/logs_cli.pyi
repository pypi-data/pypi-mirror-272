##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.15                                                            #
# Generated on 2024-05-08T22:46:02.362748                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception
    import metaflow._vendor.click.core
    import metaflow.plugins.logs_cli

LOGGER_TIMESTAMP: str

class CommandException(metaflow.exception.MetaflowException, metaclass=type):
    ...

LOG_SOURCES: list

class CustomGroup(metaflow._vendor.click.core.Group, metaclass=type):
    def __init__(self, name = None, commands = None, default_cmd = None, **attrs):
        ...
    def get_command(self, ctx, cmd_name):
        ...
    def parse_args(self, ctx, args):
        ...
    def resolve_command(self, ctx, args):
        ...
    def format_commands(self, ctx, formatter):
        ...
    ...

class CustomFormatter(object, metaclass=type):
    def __init__(self, default_cmd, original_formatter):
        ...
    def __getattr__(self, name):
        ...
    def write_dl(self, rows):
        ...
    ...

logs: CustomGroup

