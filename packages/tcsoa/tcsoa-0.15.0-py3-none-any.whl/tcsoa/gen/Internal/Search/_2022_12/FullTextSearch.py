from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awp0FullTextSavedSearch
from enum import Enum
from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Awp0CreateFTSSavedSearchInput(TcBaseObj):
    """
    Input structure for createFullTextSavedSearch service operation.
    
    :var applicationName: Name of the application that the given saved search object belongs to.
    The application name is optional and can be an empty string. In that case the saved search is global and
    application independent.
    Application owners have to make sure to use unique names. Owners can use for example the AW template ID as string.
    (e.g., mrm0mfgresourcemgraw for Resource Manager)
    :var applicationPinnedSavedSearchTileTemplateId: The tile template ID used to pinned saved search tiles at home.
    :var pinSearch: If the Awp0FullTextSavedSearch object is to be pinned.
    Supported values are:
    -1 = Do no pin or unpin the saved search.
    0 = Unpin the saved search.
    1 = Pin the saved search.
    :var receiveNotification: If the client will receive a notification when the saved-search result changes.
    Supported values are:
    -1 = Do no set or remove notification for the saved search.
    0 = Remove notification.
    1 = Set notification.
    :var shareSavedSearch: If the saved search will be available to all users. 
    The awp0is_global_shared property on Awp0FullTextSavedSearch object indicates if the search is shared or not. 
    Supported values are:
    -1 = Do not change the value of set awp0is_global_shared property on Awp0FullTextSavedSearch object. 
    0 = set awp0is_global_shared property on Awp0FullTextSavedSearch object to "false".
    1 = set awp0is_global_shared property on Awp0FullTextSavedSearch object to "true".
    :var savedSearchName: The saved search name. Alphanumeric and special characters are allowed. If a saved search
    with the same name already exists, a partial error is returned in the ServiceData object.
    :var searchString: The search string. Alphanumeric and special characters are allowed.
    :var searchFilterMap: A map (string, list of searchFilter) of filter category internal names and a list of filters
    for each category. A category is defined in the typeName.propertyName format. For example:
    WorkspaceObject.object_type. A category can be a Teamcenter core type/property name or a Classification
    type/property name. In some cases, a category can also be a non-Teamcenter type/property name constructed just for
    the purpose of grouping other categories.
    :var overwriteExistingSearch: If true and Awp0FullTextSavedsearch object with the same name already exists for the
    current user, then this operation replaces the existing object.
    If false and Awp0FullTextSavedSearch object with the same name already exists for the current user, then this
    operation will return a partial error.
    If Awp0FullTextSavedSearch object with the same name does not exist, then the parameter is ignored.
    :var chartInputParameters: A map (string, string) containing chart input parameters. This includes category name
    for which chart is generated as well as additional parameters to support various types of charts. Currently the
    only supported key is: "chartOn": The category internal name for which chart is generated (format of the value:
    typeName.propertyName). A category is defined in the typeName.propertyName format. For example:
    WorkspaceObject.object_type. A category can be a Teamcenter core type/property name or Classification type/property
    name. In some cases, a category can also represent a non-Teamcenter type/property name constructed just  for the
    purpose of grouping other categories.
    """
    applicationName: str = ''
    applicationPinnedSavedSearchTileTemplateId: str = ''
    pinSearch: int = 0
    receiveNotification: int = 0
    shareSavedSearch: int = 0
    savedSearchName: str = ''
    searchString: str = ''
    searchFilterMap: SearchFilterMap = None
    overwriteExistingSearch: bool = False
    chartInputParameters: ChartInputParameters = None


@dataclass
class Awp0FullTextSavedSearchResponse(TcBaseObj):
    """
    List of newly created saved searches and the service data containing partial errors if any.
    
    :var savedSearchList: List of Awp0FullTextSavedSearch objects created or modified by this service operation.
    :var serviceData: Service data.
    """
    savedSearchList: List[Awp0FullTextSavedSearch] = ()
    serviceData: ServiceData = None


@dataclass
class SearchFilter(TcBaseObj):
    """
    A structure representing a string, date or numeric type of search filter.
    
    :var searchFilterType: The type of search filter. Valid values are "StringFilter", "DateFilter", "NumericFilter".
    :var stringValue: The value for a string filter. This field is applicable only if the "searchFilterType" field is
    set to "StringFilter".
    :var startDateValue: The starting value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter".
    :var endDateValue: The ending value for a date filter. This field is applicable only if the "searchFilterType"
    field is set to "DateFilter".
    :var startNumericValue: The starting value for a numeric filter. This field is applicable only if the
    "searchFilterType" field is set to "NumericFilter".
    :var endNumericValue: The ending value for a numeric filter. This field is applicable only if the
    "searchFilterType" field is set to "NumericFilter".
    :var count: The number of values in the filter. This field is populated on the service response and is ignored on
    the service input.
    :var selected: A flag that indicates if the filter was previously selected and used to filter the search results.
    This field is populated on the service response and is ignored on the service input.
    :var startEndRange: The 'gap' used to generate the start and end values.
    """
    searchFilterType: SearchFilterType = None
    stringValue: str = ''
    startDateValue: datetime = None
    endDateValue: datetime = None
    startNumericValue: float = 0.0
    endNumericValue: float = 0.0
    count: int = 0
    selected: bool = False
    startEndRange: str = ''


class SearchFilterType(Enum):
    """
    An enumeration for different types of search filters like string, date, numeric.
    """
    SearchStringFilter = 'SearchStringFilter'
    SearchDateFilter = 'SearchDateFilter'
    SearchNumericFilter = 'SearchNumericFilter'


"""
A map <string, string> containing chart input parameters. 
NOTE: Supported keys are:

chartOn: The current charted on category internal name (format of the value: TypeName.propertyName)
"""
ChartInputParameters = Dict[str, str]


"""
A map of category internal names and list of filters in each category. (string/list of SearchFilter)
"""
SearchFilterMap = Dict[str, List[SearchFilter]]
