from __future__ import annotations

from tcsoa.gen.Internal.Security._2021_12.AwProjectLevelSecurity import FilterCriteriaInput, SearchSortCriteria, GroupMemberWithPrivilege
from tcsoa.gen.BusinessObjects import Role, Group, TC_Project
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ProjectTeamInput2(TcBaseObj):
    """
    The input necessary to retrieve the ProjectTeam for the given TC_Project.
    
    :var project: The TC_Project of the ProjectTeam.
    :var parent: Parent node in the ProjectTeam for which child nodes are to be fetched. If it is NULL, all first level
    nodes of the ProjectTeam will be fetched.
    :var filterCriteria: test
    :var sortCriteria: test
    :var startIndex: The first element in the ProjectTeam to return.
    :var maxToReturn: The number of ProjectTeam nodes to return.
    """
    project: TC_Project = None
    parent: GroupOrRoleNode2 = None
    filterCriteria: List[FilterCriteriaInput] = ()
    sortCriteria: List[SearchSortCriteria] = ()
    startIndex: int = 0
    maxToReturn: int = 0


@dataclass
class ProjectTeamResponse2(TcBaseObj):
    """
    test
    
    :var totalCount: test
    :var endIndex: test
    :var groupsAndRoles: test
    :var sd: test
    """
    totalCount: int = 0
    endIndex: int = 0
    groupsAndRoles: List[GroupOrRoleNodeWithChildren2] = ()
    sd: ServiceData = None


@dataclass
class GroupOrRoleNode2(TcBaseObj):
    """
    Specifies a Group or Role member of a ProjectTeam.
    
    :var tcGroup: The Teamcenter Group of the ProjectTeam member represented by this node.
    :var tcRole:  The Teamcenter Role of the ProjectTeam member represented by this node, if applicable. When the node
    represents a Group member, role must be NULL. When the node represents a specific Role within a Teamcenter Group
    both tcGroup and tcRole are required.
    :var isRemovable: Indicates if this node can be removed from the project team.
    """
    tcGroup: Group = None
    tcRole: Role = None
    isRemovable: bool = False


@dataclass
class GroupOrRoleNodeWithChildren2(TcBaseObj):
    """
    test
    
    :var groupOrRole: test
    :var type: test
    :var childGroupsOrRoles: A list of child GroupOrRoleNode representing Group or Role nodes in the ProjectTeam.
    :var childMembers: test
    """
    groupOrRole: GroupOrRoleNode2 = None
    type: str = ''
    childGroupsOrRoles: List[GroupOrRoleNodeWithChildren2] = ()
    childMembers: List[GroupMemberWithPrivilege] = ()
