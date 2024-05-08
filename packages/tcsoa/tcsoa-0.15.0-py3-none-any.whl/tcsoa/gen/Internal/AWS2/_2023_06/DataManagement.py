from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FilterCriteria(TcBaseObj):
    """
    A structure representing the filter criteria applied on a column.
    
    :var operation: This operation specifies the type of column filter operation applied. The supported operations are
    "CONTAINS", "EQUAL", "GREATER THAN", "LESS THAN" and "BETWEEN".
    :var values: These are the filter values saved in the database from the previous filter use case executed by the
    user.
    """
    operation: str = ''
    values: List[str] = ()


@dataclass
class GetTableViewModelPropsOut(TcBaseObj):
    """
    Output containing the JSON string representation for the objects for which the properties were fetched and the
    column configuration data.
    
    :var viewModelPropertiesJsonString: JSON string that contains the view model properties, the schema of JSON string
    is defined in getDeclarativeStyleSheet service operation.
    :var columnConfig: The column configuration data.
    """
    viewModelPropertiesJsonString: str = ''
    columnConfig: ColumnConfig = None


@dataclass
class GetTableViewModelPropsResp(TcBaseObj):
    """
    The getTableViewModelProperties2 response structure.
    
    :var output: The model objects with the dynamic compound properties inflated and the column configuration
    applicable for the input objects.
    :var serviceData: The Service Data object.
    """
    output: GetTableViewModelPropsOut = None
    serviceData: ServiceData = None


@dataclass
class ColumnConfig(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI. It contains a unique
    column config id, a list of column definition information, and the operation type used to finalize the columns.
    
    :var columnConfigId: The unique identifier of the column configuration.
    :var operationType: The operation that was used to finalize the columns to be returned back. Supported values are:
    "Intersection", "Union" and "Configured".
    :var typesForArrange: The valid Teamcenter types used for fetching the columns.
    :var columns: A list of column details.
    """
    columnConfigId: str = ''
    operationType: str = ''
    typesForArrange: List[str] = ()
    columns: List[ColumnDefInfo] = ()


@dataclass
class ColumnDefInfo(TcBaseObj):
    """
    Contains details about a specific column. This includes the type of object for which the column is applicable, the
    name of the property displayed in the column, a flag indicating if the column should be used to order information
    displayed in the client, pixel width of the column, a flag indicating if the column should be text wrapped, a flag
    indicating if the column should be hidden and the column sort order, filters applied on a column, filter definition
    for the type of custom column filter to display in the client and the datatype of the property.
    
    :var hiddenFlag: If true, the column should be hidden on the client user interface.
    :var isFilteringEnabled: If true, column filtering is enabled on this column; otherwise, column filtering is not
    supported on this column.
    :var displayName: The display name for the value displayed in the column header.
    :var sortDirection: How the columns are sorted. Supported values are: "Ascending" and "Descending". This value will
    be empty if the column is not marked for sorting.
    :var filterDefinitionKey: The string that represents a custom filter definition which the clients can define in the
    client view model.
    :var filters: A list of filter criteria that is applied on the column.
    :var isFrozen: If true, the table has columns frozen until this column; otherwise, this column is not frozen.
    :var isTextWrapped: If true, the text of the column will be wrapped; otherwise, the text of the column will not be
    wrapped.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between 1 and 500.
    :var sortPriority: Sort priority set on column helps identify the order in which the columns should be used during
    sort. Sort priority value will be zero for columns not marked for sorting.
    :var columnOrder: The column order value is used to arrange the columns in order.
    :var propertyName: The property name for the value displayed in the column.
    :var associatedTypeName: The business object type for the value displayed in the column. This can be any valid
    Teamcenter business object type.
    :var dataType: The data type of the property for the given column.
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
    sortPriority: int = 0
    columnOrder: int = 0
    propertyName: str = ''
    associatedTypeName: str = ''
    dataType: str = ''
