from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0CommandCollection
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ClientInput(TcBaseObj):
    """
    Specifies client input information including client name and hosting client name.
    
    :var clientName: The name of a client application, as represented by an instance of Fnd0Client in the Teamcenter
    database. This value must match the value of fnd0ClientName property.
    :var hostingClientName: Specifies the name of a hosting Client application, as represented by an instance of
    Fnd0Client, in the Teamcenter databases. This value must match a value of the fnd0ClientName property. For example,
    if Client A is integrated with Client B and the user can invoke Client B commands from within Client A, the input
    to getUiConfigs would specify Client A as hosting Client and Client B as the Client. If the caller wanted native
    commands for Client A, Client A would be specified as Client and hosting Client would be empty.
    """
    clientName: str = ''
    hostingClientName: str = ''


@dataclass
class ScopeInput(TcBaseObj):
    """
    Contains scope input information including scope name and scope query parameter.
    
    :var scopeName: The name of a scope. For Site and current login user, this value should be empty.
    :var scopeQueryParam: The query scope that is used to retrieve the UI configurations. Valid values are Site, Group,
    Role, User, LoginUser, and AvailableForLoginUser. Site returns the configuration defined for the site. Group
    returns the configuration defined for a specific Teamcenter Group. Role returns the configuration defined for a
    specific Teamcenter Role. User returns the configurations defined for a specific Teamcenter User. LoginUser returns
    the current configuration defined for the current login user. AvailableForLoginUser returns all the configurations
    available for the current login user. The value for scopeName should be empty when scopeQueryParam is set to:
    "Site", "LoginUser" or "AvailableForLoginUser".
    """
    scopeName: str = ''
    scopeQueryParam: str = ''


@dataclass
class CommandCollectionInfo(TcBaseObj):
    """
    Contains a command collection and indexes to its children commands or command collections.
    
    :var childIsCollection: If true ,the child is a command collection; otherwise, the child is a command.
    :var childIsVisible: If true, command or collection is visible; otherwise, the command or collection is not visible.
    :var childConfigIndex: Index of the child in either the CommandConfigData:commands list or the
    CommandConfigData:cmdsCollections list. It is used by client to build the command hierarchy.
    :var commandCollection: Fnd0CommandCollection object.
    """
    childIsCollection: List[bool] = ()
    childIsVisible: List[bool] = ()
    childConfigIndex: List[int] = ()
    commandCollection: Fnd0CommandCollection = None
