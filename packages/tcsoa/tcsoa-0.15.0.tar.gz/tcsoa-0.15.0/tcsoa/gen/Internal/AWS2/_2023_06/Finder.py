from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2019_06.Finder import FilterCriteriaResponse
from typing import List, Dict
from tcsoa.gen.Internal.AWS2._2016_03.Finder import SearchFilterField, ObjectsGroupedByProperty
from tcsoa.gen.Internal.AWS2._2018_05.Finder import SearchCursor
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.Internal.AWS2._2017_12.Finder import SearchFilter4


@dataclass
class ColumnConfig(TcBaseObj):
    """
    This structure contains information for a column configuration within a client scope URI. It contains a unique
    column config id, a list of column definition information, and the operation type used to finalize the columns.
    
    :var columnConfigId: The unique identifier of the column configuration.
    :var operationType: The operation that was used to finalize the columns to be returned back. Supported values are:
    "Intersection", "Union" and "Configured".
    :var columns: A list of column details.
    """
    columnConfigId: str = ''
    operationType: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class SaveColumnConfigData(TcBaseObj):
    """
    This structure contains column configuration details and a list of column definitions information.
    
    :var scope: The scope value is used to apply the UI configurations for that scope. Supported values are :
    "LoginUser" - Returns the current configuration defined for the current login user. 
    Note: Other scope values "Site", "Group" and "Role" are not supported.
    :var scopeName: The name of a valid Teamcenter scope.
    For example "Group" scope, scopeName can be "dba","Engineering". 
    For "LoginUser" scope, this value should be empty.
    :var clientScopeURI: The unique name of the client scope containing configurations.
    Supported values are: 
    "Awp0SearchResults" for global search.
    "fnd0Inbox" for inbox.
    "fnd0alltasks" for all inbox tasks.
    "fnd0mytasks" for my inbox tasks.
    "fnd0surrogatescope" for surrogate inbox tasks.
    "Fnd0Report" for report..
    "Awp0ObjectNavigation" for object navigation.
    "Awp0AdvancedSearch" for advanced search.
    :var columnConfigId: The unique identifier for the column configuration.
    Example: "searchResultsColConfig" for search location.
    :var columns:  Ordered list of column information.
    """
    scope: str = ''
    scopeName: str = ''
    clientScopeURI: str = ''
    columnConfigId: str = ''
    columns: List[ColumnDefInfo] = ()


@dataclass
class SearchResponse(TcBaseObj):
    """
    A service response structure containing search results and column configurations.
    
    :var totalFound: Total number of view model business objects found.
    :var totalLoaded: Total number of view model business objects loaded.
    :var objectsGroupedByProperty: The structure containing an internal property name and a map of objects to the
    property group id. It also contains a list of unmatched objects which do not match any group.
    :var columnConfig: Effective column configuration for the client scope URI.
    :var serviceData: The service data object.
    :var defaultFilterFieldDisplayCount: The default number of search filter categories to display.
    :var endIndex: Cursor end position for the results returned so far. This value, 'endIndex', correlates with
    'startindex' in SearchInput.
    :var searchResultsJSON: Search results in JSON Format. With this, Client can directly bind the view model
    properties JSON to the view.
    :var cursor: Cursor for the results returned so far.
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var searchFilterCategoriesUnpopulated: A list of empty search filter categories.
    :var searchFilterMap: A map (string, list of SearchFilter4) containing the list of search filters for each search
    filter field based on the search results.
    :var additionalSearchInfoMap: A generic map (string/list of strings) that can be used to send additional search
    information to the consumer. 
    
    Supported key values are:
    searchTermsToHighlight - used to indicate which Search Terms need to be highlighted.
    """
    totalFound: int = 0
    totalLoaded: int = 0
    objectsGroupedByProperty: ObjectsGroupedByProperty = None
    columnConfig: ColumnConfig = None
    serviceData: ServiceData = None
    defaultFilterFieldDisplayCount: int = 0
    endIndex: int = 0
    searchResultsJSON: str = ''
    cursor: SearchCursor = None
    searchFilterCategories: List[SearchFilterField] = ()
    searchFilterCategoriesUnpopulated: List[SearchFilterField] = ()
    searchFilterMap: SearchFilterMap8 = None
    additionalSearchInfoMap: StringVectorMap3 = None


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
    :var sortDirection: How the columns are sorted. Supported values are: "Ascending" and "Descending". This value will
    be empty if the column is not marked for sorting.
    :var filterDefinitionKey: The string that represents a custom filter definition which the clients can define in the
    client view model.
    :var dataType: The data type of the property for the given column.
    :var filters: A list of filter criteria that is applied on the column.
    :var isFrozen: If true, the table has columns frozen until this column; otherwise, this column is not frozen.
    :var isTextWrapped: If true, the text of the column will be wrapped; otherwise, the text of the column will not be
    wrapped.
    :var columnOrder: The column order value is used to arrange the columns in order.
    :var pixelWidth: The pixel width for the column. Valid pixel widths are integer values between 1 and 500.
    :var sortPriority: Sort priority set on column helps identify the order in which the columns should be used during
    sort. Sort priority value will be zero for columns not marked for sorting.
    :var propertyName: The property name for the value displayed in the column.
    :var associatedTypeName: The business object type for the value displayed in the column. This can be any valid
    Teamcenter business object type.
    :var displayName: The display name for the value displayed in the column header.
    """
    hiddenFlag: bool = False
    isFilteringEnabled: bool = False
    sortDirection: str = ''
    filterDefinitionKey: str = ''
    dataType: str = ''
    filters: List[FilterCriteriaResponse] = ()
    isFrozen: bool = False
    isTextWrapped: bool = False
    columnOrder: int = 0
    pixelWidth: int = 0
    sortPriority: int = 0
    propertyName: str = ''
    associatedTypeName: str = ''
    displayName: str = ''


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap8 = Dict[str, List[SearchFilter4]]


"""
A map of string to list of strings.
"""
StringVectorMap3 = Dict[str, List[str]]
