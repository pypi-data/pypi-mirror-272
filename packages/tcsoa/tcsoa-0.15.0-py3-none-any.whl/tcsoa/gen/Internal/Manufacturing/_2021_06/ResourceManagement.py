from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GuidedComponentSearchForOccResponse(TcBaseObj):
    """
    This contains list of structures which internally contains ID of the class and number of matching ICO objects
    associated with it. It also contains list of UIDs for matching ICO objects, list of Connection Point UIDs and the
    ID of the common main class of the matching ICO objects.
    
    :var serviceData: The service data containing partial errors if any.
    :var matchingClasses: List of MatchingClass structure.
    :var icoUids: A list of UIDs for matching ICO objects.
    :var cpUids: A list of UIDs for matching Connection Point objects.
    :var defaultClassId: The ID of the common main class of the matching ICO objects.
    """
    serviceData: ServiceData = None
    matchingClasses: List[MatchingClass] = ()
    icoUids: List[str] = ()
    cpUids: List[str] = ()
    defaultClassId: str = ''


@dataclass
class MatchingClass(TcBaseObj):
    """
    This structure contains ID of the class in which matching ICO objects occur and associated number of ICO objects.
    
    :var classID: ID of class in which matching ICO objects occur.
    :var matchingIcoCount: Number of matching ICO objects associated with this class.
    """
    classID: str = ''
    matchingIcoCount: int = 0
