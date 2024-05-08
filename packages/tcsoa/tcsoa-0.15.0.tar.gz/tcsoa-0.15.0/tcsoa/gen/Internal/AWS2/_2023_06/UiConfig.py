from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2020_05.UiConfig import FilterCriteria
from typing import List, Dict
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
    :var serviceData: ServiceData structure containing errors and command, command collection and icon objects. If
    there is an error retrieving the configuration information, the error added to the ServiceData as a partial error.
    """
    clientName: str = ''
    columnConfigurations: List[ColumnConfigData] = ()
    serviceData: ServiceData = None


@dataclass
class SaveColumnConfigData(TcBaseObj):
    """
    This structure contains column configuration details and a list of column definition information.
    
    :var scope: The scope value is used to apply the UI configurations for that scope. 
    The Valid values are :
    "LoginUser" - Returns the current configuration defined for the current login user. 
    "scopeName" should be empty when scope is set for LoginUser.
    Note: Other scope values "Site", "Group" and "Role" are not supported.
    :var scopeName: The name of a valid Teamcneter scope. For "Site" and "LoginUser" scope, this value should be empty.
    Note: Added this for future. To be used when code starts supporting saving of column configurations for "Site",
    "Group" and "Role" scopes.
    :var clientScopeURI: The unique name of the client scope containing configurations.
    :var columnConfigId: The unique identifier for the column configuration.
    :var columns: Ordered list of column information.
    """
    scope: str = ''
    scopeName: str = ''
    clientScopeURI: str = ''
    columnConfigId: str = ''
    columns: List[ColumnDefInfo] = ()


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
    The Valid values are:
    "LoginUser" - Returns the current configuration defined for the current login user. 
    "scopeName" should be empty when scope is set for LoginUser.
    Note: Other scope values: "Site", "Group" and "Role" are not supported.
    :var scopeName: The scope name for which the column data is applicable. For "Site" and "LoginUser" scope, this
    value should be empty.
    Note: Added this for future use. To be used when code starts supporting saving of column configurations for:
    "Site", "Group" and "Role" scopes.
    :var hostingClient: The name of hosting client for which the list of column configurations is applicable. This
    value must correspond to the value of the property fnd0ClientName for an Fnd0Client object in the Teamcenter
    database.
    :var clientScopeURI: The client scope for which the list of column configurations is applicable. This value must
    correspond to the value of the property fnd0ClientScopeURI which is the unique identifier of a client scope
    (Fnd0ClientScope) in the Teamcenter database.
    :var columnConfigurations: List of column configuration details.
    """
    scope: str = ''
    scopeName: str = ''
    hostingClient: str = ''
    clientScopeURI: str = ''
    columnConfigurations: List[ColumnConfig] = ()


@dataclass
class ColumnDefInfo(TcBaseObj):
    """
    Contains details about a specific column. This includes the type of object for which the column is applicable, the
    name of the property displayed in the column, a flag indicating if the column should be used to order information
    displayed in the client, pixel width of the column, a flag indicating if the column should be text wrapped, a flag
    indicating if the column should be hidden and the column sort order, filters applied on a column, filter definition
    for the type of custom column filter to display in the client and the datatype of the property.
    
    :var hiddenFlag: If true, the column will be hidden on the client user interface.
    :var isFilteringEnabled: If true, column filtering is enabled on this column; otherwise, column filtering is not
    supported on this column.
    :var displayName: The display name for the value displayed in the column header.
    :var sortDirection: How the columns are sorted. Supported values are: "Ascending" and "Descending". This value will
    be empty if the column is not marked for sorting.
    :var filterDefinitionKey: This string that represents a custom filter definition which the clients can define in
    the client view model.
    :var filters: A list of filter criteria that is applied on the column.
    :var isFrozen: If true, the table has columns frozen until this column; otherwise, this column is not frozen.
    :var isTextWrapped: If true, the text of the column will be wrapped; otherwise, the text of the column will not be
    wrapped.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between 1 and 500.
    :var columnOrder: The column order value is used to arrange the columns in order.
    :var sortPriority: Sort priority set on column helps identify the order in which the columns should be used during
    sort. Sort priority value will be zero for columns not marked for sorting.
    :var propertyName: The property name for the value displayed in the column.
    :var associatedTypeName: The business object type for the value displayed in the column. This can be any valid
    Teamcenter business object type.
    :var dataType: The data type of the property for the given column. Valid values are: "String", "Integer", "Double",
    "Date", "Typed_Reference", and "Untyped_Reference".
    """
    hiddenFlag: bool = False
    isFilteringEnabled: bool = False
    displayName: str = ''
    sortDirection: str = ''
    filterDefinitionKey: str = ''
    filters: List[FilterCriteria] = ()
    isFrozen: bool = False
    isTextWrapped: bool = False
    pixelWidth: int = 0
    columnOrder: int = 0
    sortPriority: int = 0
    propertyName: str = ''
    associatedTypeName: str = ''
    dataType: str = ''


"""
Map from string to string.
"""
StringMap2 = Dict[str, str]
