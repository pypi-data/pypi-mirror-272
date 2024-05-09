##################################################################################
#                       Auto-generated Metaflow stub file                        #
# MF version: 2.11.15                                                            #
# Generated on 2024-05-08T22:46:02.409401                                        #
##################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

class MetaflowException(Exception, metaclass=type):
    def __init__(self, msg = "", lineno = None):
        ...
    def __str__(self):
        ...
    ...

class MetaflowAzureAuthenticationError(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowAzureResourceError(metaflow.exception.MetaflowException, metaclass=type):
    ...

class MetaflowAzurePackageError(metaflow.exception.MetaflowException, metaclass=type):
    ...

