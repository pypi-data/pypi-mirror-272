from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, GroupMember
from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FilterCategory(TcBaseObj):
    """
    A list of search filter categories ordered by filter priority.
    
    :var internalName: The internal name for the search filter field.
    :var displayName: The display name for the search filter field.
    :var defaultFilterValueDisplayCount: The default number of search filter values to display within the search filter
    field.
    """
    internalName: str = ''
    displayName: str = ''
    defaultFilterValueDisplayCount: int = 0


@dataclass
class GetFilteredOrgTreeInput(TcBaseObj):
    """
    The structure contains search criteria and pagination parameter required for the getFilteredOrganizationTree
    service operation.
    
    :var startIndex: The start index of OrganizationTree node to return. Valid value starts at 0. If input is negative,
    all found Organization Tree nodes will be returned.
    :var maxToReturn: The maximum number of OrganizationTree nodes to return. If input is 0 or negative all found
    OrganizationTree nodes will be returned.
    :var cursor: A structure containing cursor for pagination and focus node selection.
    :var focusObjUid: The uid of the Object to focus to.
    :var searchFilterMap: A map (string, list of SearchFilter) containing the list of search filters for each search
    filter field.The key in the map is the property name that represents the filter category. It is in the format
    "TypeName.PropertyName". For example: Group.group_name, the value in the map is the value of the search filter.
    :var pagingType: The type of paging operation. Valid values are GetCurrentPage, GetNextPage, GetPreviousPage.
    :var searchCriteria: A map (string, string) used to perform the search. For full text search in organization tree
    the key is &lsquo;searchString&rsquo;.  To honor the preference &lsquo;TC_supress_inactive_group_members&rsquo;
    configuration or not the key is &lsquo;useInactiveGMPref&rsquo;.
    :var sortCriteria: The criterion to use to sort the results.
    """
    startIndex: int = 0
    maxToReturn: int = 0
    cursor: Cursor = None
    focusObjUid: str = ''
    searchFilterMap: SearchFilterMap = None
    pagingType: str = ''
    searchCriteria: SearchCriteria = None
    sortCriteria: SortCriteria = None


@dataclass
class GetFilteredOrgTreeResponse(TcBaseObj):
    """
    A structure containing filtered organization tree in hierarchical manner and search filter map and search filter
    categories information.
    
    :var totalFound: The total number of organization tree nodes found.
    :var endIndex: The index of the last node.
    :var orgTree: A structure contains the information of organization tree and its children.
    :var searchFilterCategories: A list of search filter categories ordered by filter priority.
    :var searchFilterMap: A map (string, list of SearchFilter) containing the list of search filters for each search
    filter field based on the search results.
    :var cursor: The cursor for the results returned so far.
    :var additionalSearchInfoMap: A map (string/list of strings) that can be used to send additional search information
    related to filter categories.
    :var serviceData: The service data object.
    """
    totalFound: int = 0
    endIndex: int = 0
    orgTree: OrganizationTree = None
    searchFilterCategories: List[FilterCategory] = ()
    searchFilterMap: SearchFilterMap = None
    cursor: Cursor = None
    additionalSearchInfoMap: StringVectorMap = None
    serviceData: ServiceData = None


@dataclass
class OrganizationTree(TcBaseObj):
    """
    A structure containing the information for the organization tree and its children.
    
    :var orgTreeNodes: A list of OrganizationTreeNode structure.
    """
    orgTreeNodes: List[OrganizationTreeNode] = ()


@dataclass
class OrganizationTreeNode(TcBaseObj):
    """
    A structure containing the information for the organization object in the tree and its children.
    
    :var orgObject: The organization object can be Group,Role,User.
    :var isLeaf: False if the node has the childrens otherwise True.
    :var displayName: The display name of the orgObject.
    :var groupMember: The GroupMember object for the orgObject if it is of type User.
    :var cursor: The cursor information for each orgObject. Applied to only non leaf node.
    :var children: A OrganizationTree strcuture to return child nodes in hierarchical manner.
    """
    orgObject: BusinessObject = None
    isLeaf: bool = False
    displayName: str = ''
    groupMember: GroupMember = None
    cursor: Cursor = None
    children: OrganizationTree = None


@dataclass
class SearchFilter(TcBaseObj):
    """
    A structure representing a string type of search filter.
    
    :var count: The number of values in the filter. This field is populated on the service response and is ignored on
    the service input.
    :var selected: True, if the Search Filter is selected; otherwise, False.
    :var stringDisplayValue: The display value for a string filter.
    :var stringValue: The internal value for a string filter.
    """
    count: int = 0
    selected: bool = False
    stringDisplayValue: str = ''
    stringValue: str = ''


@dataclass
class SortCriteria(TcBaseObj):
    """
    The criteria to use to sort the results.
    
    :var fieldName: The name of the field on which to perform the sorting.
    :var sortDirection: The direction in which the sorting needs to be performed - 'ASC' or 'DESC'.
    """
    fieldName: str = ''
    sortDirection: str = ''


@dataclass
class Cursor(TcBaseObj):
    """
    A structure containing cursor for pagination and focus node selection.
    
    :var startIndex: The Cursor start position for the search result returned so far.
    :var startReached: If true, the first page of the results has been reached.
    :var endIndex: The Cursor end position for the search result returned so far.
    :var endReached: If true the last page of the results has been reached.
    """
    startIndex: int = 0
    startReached: bool = False
    endIndex: int = 0
    endReached: bool = False


"""
A generic map to pass the search criteria.
"""
SearchCriteria = Dict[str, str]


"""
A map containing a list of search filters for each search filter field.
"""
SearchFilterMap = Dict[str, List[SearchFilter]]


"""
A map of string to list of strings.
"""
StringVectorMap = Dict[str, List[str]]
