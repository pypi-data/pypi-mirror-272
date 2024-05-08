from __future__ import annotations

from enum import Enum
from tcsoa.gen.BusinessObjects import Role, GroupMember, Group, TC_Project
from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ProjectInformation(TcBaseObj):
    """
    The structure defines a property to be set on new TC_Project business object.
    
    :var projectId: Unique identifier for the project.The valid value can be string without '%','*','@' character.
    :var projectName: Unique name for the project. The valid value can be string without '.','%','*','@' character.
    :var projectDescription: Describes the project.
    :var useProgramSecurity: True if the project uses program level security.
    :var projectCategory: Specifies a project category.
    :var deepCopy: If False, copy the following information from existing project or program:
       -    Project team.
       -    Properties which include active, visible, use program security, project category, collaboration category
    and other custom properties.
    If True, copy the following information from existing project or program: 
       -    Project team.
       -    Properties which include active, visible, use program security, project category, collaboration category
    and other custom properties.
       -    Project libraries (Defines an association between primary object and secondary objects via
    Fnd0LibraryForProject relation where project is the primary object).
       -    Project Data (The objects which are assigned to the source project. Assign the new project to these
    objects.)
    :var propertyMap: A map (string, list of strings) of property names and desired values. The calling client is
    responsible for converting the different property types (int, float, date .etc) to a string using the appropriate
    functions in the SOA client framework's Property Class.
    """
    projectId: str = ''
    projectName: str = ''
    projectDescription: str = ''
    useProgramSecurity: bool = False
    projectCategory: str = ''
    deepCopy: bool = False
    propertyMap: ProjectPropertyMap = None


@dataclass
class ProjectTeamInput(TcBaseObj):
    """
    The input necessary to retrieve the ProjectTeam for the given TC_Project.
    
    :var project: The TC_Project of the ProjectTeam.
    :var parentNode: Parent node in the ProjectTeam for which child nodes are to be fetched.   If it is NULL, all first
    level nodes of the ProjectTeam will be fetched.
    :var filterCriteria: A list of FilterCriteriaInput to apply to the ProjectTeam.
    :var sortCriteria: List of sort criteria to apply to the filtered ProjectTeam.
    :var startIndex: The first element in the ProjectTeam to return.
    :var maxToReturn: The number of ProjectTeam nodes to return.
    """
    project: TC_Project = None
    parentNode: GroupOrRoleNode = None
    filterCriteria: List[FilterCriteriaInput] = ()
    sortCriteria: List[SearchSortCriteria] = ()
    startIndex: int = 0
    maxToReturn: int = 0


@dataclass
class ProjectTeamResponse(TcBaseObj):
    """
    The structure to hold the ProjectTeam member nodes and their children.
    
    :var totalCount: The total ProjectTeam members nodes represented by the ouput.
    :var endIndex: The index of the last ProjectTeam node.
    :var groupsAndRoles: A hiearchical  list of Group and Role nodes in the ProjectTeam.
    :var serviceData: The SOA framework object containing objects that were created, deleted or updated by the Service,
    plain objects and error information. For this service, the service data contains partial error information.  The
    plain objects contains the Group, Role and GroupMember objects.
    """
    totalCount: int = 0
    endIndex: int = 0
    groupsAndRoles: List[GroupOrRoleNodeWithChildren] = ()
    serviceData: ServiceData = None


@dataclass
class SearchSortCriteria(TcBaseObj):
    """
    Defines the sort criteria to be applied to the output ProjectTeam nodes.
    
    :var fieldName: The name of the field on which to perform the sorting.
    :var direction: The direction in which the sorting needs to be performed - 'ASC' or 'DESC'.
    """
    fieldName: str = ''
    direction: SortDirection = None


@dataclass
class FilterCriteriaInput(TcBaseObj):
    """
    Defines filter criteria to be applied to the response.
    
    :var columnName: The internal name of the property on which column filtering is applied.
    :var values: A list of filter values.
    :var operation: Specifies the type of column filter operation applied. The supported values are: "CONTAINS",
    "EQUAL", "GREATER THAN", "LESS THAN" and "BETWEEN".
    """
    columnName: str = ''
    values: List[str] = ()
    operation: str = ''


@dataclass
class GroupMemberWithPrivilege(TcBaseObj):
    """
    Identifies GroupMember and their status within the ProjectTeam.
    
    :var member: The group member.
    :var status: The privilege status of the GroupMember within the ProjectTeam of the input TC_Project.
    0 = Regular member.
    1 = Privileged member.
    2 = Project Team Administrator.
    3 = Project Administrator.
    :var isRemovable: True if the member can be removed from the ProjectTeam.  Otherwise, false.
    :var type: Indicates the group member type.
    """
    member: GroupMember = None
    status: int = 0
    isRemovable: bool = False
    type: str = ''


@dataclass
class GroupOrRoleNode(TcBaseObj):
    """
    The Teamcenter Group or Role represented by the node.
    
    :var grp: The Teamcenter Group of the ProjectTeam member represented by this node.
    :var role: The Teamcenter Role of the ProjectTeam member represented by this node, if applicable.  When the node
    represents a Group member, role must be NULL. When the node represents a specific Role within a Teamcenter Group
    both group and role are required.
    """
    grp: Group = None
    role: Role = None


@dataclass
class GroupOrRoleNodeWithChildren(TcBaseObj):
    """
    Represents a node in the ProjectTeam and its corresponding children.
    
    :var groupOrRole: The Group or Role corresponding to the ProjectTeam node.
    :var isRemovable: True if the Group or Role can be removed from the ProjectTeam.
    :var type: Indicates the displayable type name for the node.  Typically Group or Role.
    :var childGroupsOrRoles: A list of child GroupOrRoleNode representing Group or Role nodes in the ProjectTeam.
    :var childMembers: A list of child GroupMember, the member&rsquo;s status within the team and whether that member
    can be removed
    """
    groupOrRole: GroupOrRoleNode = None
    isRemovable: bool = False
    type: str = ''
    childGroupsOrRoles: List[GroupOrRoleNodeWithChildren] = ()
    childMembers: List[GroupMemberWithPrivilege] = ()


class SortDirection(Enum):
    """
    - ASC     Sort values in ascending order.
    - DESC    Sort values in descending order.
    
    """
    ASC = 'ASC'
    DESC = 'DESC'


"""
A map (string, list of strings) of property names and desired values. The calling client is responsible for converting the different property types (int, float, date .etc) to a string using the appropriate functions in the SOA client framework's Property class.
"""
ProjectPropertyMap = Dict[str, List[str]]
