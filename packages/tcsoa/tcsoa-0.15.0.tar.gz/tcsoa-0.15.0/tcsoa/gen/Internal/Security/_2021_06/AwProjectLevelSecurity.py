from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateProjectInfo(TcBaseObj):
    """
    Structure that holds the information required to create  a Teamcenter Authorization project.
    
    :var projectId: Unique identifier for the project.
    :var projectName: Unique name for the project.
    :var projectDescription: Describes the project.
    :var useProgramSecurity: True if the project uses program level security.
    :var projectCategory: Empty or specifies a valid project category. Valid project categories are defined in the
    Fnd0ProjectCategories list of values.
    :var clientId: Unique client identifier. If there is an error during create, the client id in the ServiceData
    partial error list can be used to associate to the clientId in the input to detect which object creation failed.
    """
    projectId: str = ''
    projectName: str = ''
    projectDescription: str = ''
    useProgramSecurity: bool = False
    projectCategory: str = ''
    clientId: str = ''
