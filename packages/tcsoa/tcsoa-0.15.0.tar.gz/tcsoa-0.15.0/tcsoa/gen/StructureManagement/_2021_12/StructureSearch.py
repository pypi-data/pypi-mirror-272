from __future__ import annotations

from tcsoa.gen.StructureManagement._2014_12.StructureSearch import AdditionalInfo
from tcsoa.gen.BusinessObjects import BusinessObject, RuntimeBusinessObject
from tcsoa.gen.StructureManagement._2021_06.StructureSearch import ExtraObjects
from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpandResponse2(TcBaseObj):
    """
    The found objects and the expand cursor that can be used in next Expand.
    
    :var objectsDone: Number of objects returned so far.
    :var estimatedObjectsLeft: Estimated number of objects 0f the structure.
    :var foundObjects: The next list of objects returned by the startExpandBOMLines or nextExpandBOMLines operation.
    :var expandCursor: SearchCursor object that tracks the expand results. This object is used to get the next set of
    results for this startExpandBOMLines operation.
    :var extraObjs: A list of Dataset objects for the lines returned.
    :var additionalInfo: Currently not used.
    :var serviceData: Service Data for any error information. Typically, this will contain errors about any malformed
    search recipes.
    """
    objectsDone: int = 0
    estimatedObjectsLeft: int = 0
    foundObjects: List[RuntimeBusinessObject] = ()
    expandCursor: BusinessObject = None
    extraObjs: List[ExtraObjects] = ()
    additionalInfo: AdditionalInfo = None
    serviceData: ServiceData = None


"""
Map containing Expand flags and values.
"""
SettingsMap2 = Dict[str, List[str]]
