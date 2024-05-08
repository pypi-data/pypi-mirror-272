from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2020_05.UiConfig import ColumnDefInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetOrResetUIColumnConfigResponse(TcBaseObj):
    """
    This structure returns information to the client about column configurations. The ServiceData contains information
    about errors encountered during processing.
    
    :var clientName: The client for which the configurations are applicable.
    :var columnConfigurations: List of column configurations data.
    :var serviceData:  ServiceData structure containing errors and command, command collection and icon objects. If
    there is an error retrieving the configuration information, the error added to the ServiceData as a partial error.
    """
    clientName: str = ''
    columnConfigurations: List[ColumnConfigData] = ()
    serviceData: ServiceData = None


@dataclass
class ColumnConfig(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI. It contains a unique
    column config id, a list of column definition information, and the default sort direction.
    
    :var columnConfigId: The unique identifier of the column.
    :var operationType: The operation that was used to identify the columns to be returned.
    Valid values are: "Intersection", "Union" and "Configured".
    :var columns: Ordered list of column details.
    """
    columnConfigId: str = ''
    operationType: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class ColumnConfigData(TcBaseObj):
    """
    This structure returns information about the column configuration definitions for a scope, hosting client and
    client scope.
    
    :var scope: The scope for which the column data is applicable.
    :var scopeName: The scope name for which the column data is applicable.
    :var hostingClient: The name of hosting client for which the list of column configurations is applicable. This
    value must correspond to the value of the property fnd0ClientName for an Fnd0Client object in the Teamcenter
    database.
    :var clientScopeURI: The client scope for which the list of column configurations is applicable. This value must
    correspond to the value of the property  fnd0ClientScopeURI which is the unique identifier of a client scope
    (Fnd0ClientScope) in the Teamcenter database.
    :var columnConfigurations: List of column configuration details.
    """
    scope: str = ''
    scopeName: str = ''
    hostingClient: str = ''
    clientScopeURI: str = ''
    columnConfigurations: List[ColumnConfig] = ()
