from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, BOMLine
from tcsoa.gen.Internal.Visualization._2008_06.StructureManagement import ExpandPSRelatedObjectInfo
from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExpandPSData1(TcBaseObj):
    """
     Through this structure, the child BOMLine , the object of the BOMLine and the object attached to the bom line
    object are returned.
    
    :var bomLine: BOMLine object reference of the children.
    :var objectOfBOMLine: Object that the child represents.
    :var indexOfrelatedObjectsInfo: The index into 'ExpandPSFromOccurrenceListOutput::relatedObjects' array that has the
     information about the related object and relation type.
    :var resolutionStatus: Resolution status of 'bomLine'.
    - 0 - Unknown
    - 1 - Full Resolved
    - 2 - Partially Resolved
    
    
    :var isAlternate: BOMLine resolution is to an alternate representation of input. If true, 'bomLine' has resolved to
    an alternate representation of input; if false 'bomLine' is the actual representation of input.
    """
    bomLine: BOMLine = None
    objectOfBOMLine: BusinessObject = None
    indexOfrelatedObjectsInfo: List[int] = ()
    resolutionStatus: int = 0
    isAlternate: bool = False


@dataclass
class ExpandPSFromOccurrenceListOutput(TcBaseObj):
    """
    This structure contains the client identifier and the list of 'OccurrenceListResults'.
    
    :var clientId: Identifier that helps the client track the objects created. This is the clientId specified  in the
    'ExpandPSFromOccurrenceListInfo'.
    :var occurrenceList: List of 'OccurrenceListResults' structs describing the occurrences that were expanded.
    """
    clientId: str = ''
    occurrenceList: List[OccurrenceListResults] = ()


@dataclass
class ExpandPSFromOccurrenceListResponse(TcBaseObj):
    """
    Response structure for the 'expandPSFromOccurrenceList'() operation.
    
    :var output: List of 'ExpandPSFromOccurrenceListOutput' structures containing the objects corresponding to the
    parent and the child BOMLine objects, their siblings and their related objects as well.
    :var serviceData: The service data contains the plain objects and the error stack, if any.
    :var relatedObjects: List of objects attached to BOMLine with given relation.
    :var childrenOfParent: A map(Key = BOMLine, Value = Array of 'ExpandPSData1') that contains the expanded parent
    BOMLine as the key and 'ExpandPSData1' of its children as value. This is populated only when the wantSiblings is
    true.
    :var additionalInfo: Currently unused. Future example usage: additionalInfo.strToIntegerVectorMap
    ["containsInProcessAssembly"] = (1);
    """
    output: List[ExpandPSFromOccurrenceListOutput] = ()
    serviceData: ServiceData = None
    relatedObjects: List[ExpandPSRelatedObjectInfo] = ()
    childrenOfParent: ParentLineToChildrenDataMap1 = None
    additionalInfo: AdditionalInfo = None


@dataclass
class OccurrenceChainResult(TcBaseObj):
    """
    This structure contains the client identifier and the list of 'ExpandPSData1' structures for each occurrence in a
    given chain.
    
    :var clientId: Identifier that helps the client track the object(s) created. The client ID that was specified in
    the 
    'OccurrenceChain'.
    :var occurrenceChain: List of 'ExpandPSData1' structs describing the occurrences that were expanded in the given
    'OccurrenceChain'.
    """
    clientId: str = ''
    occurrenceChain: List[ExpandPSData1] = ()


@dataclass
class OccurrenceListResults(TcBaseObj):
    """
    This structure records the parent context and the occurrences expanded in that context.
    
    :var clientId: Identifier that helps the client track the objects created. The client ID that was specified in the 
    'OccurrenceChainList'.
    :var parent: 'ExpandPSData1' describing the parent BOMLine.
    :var occurrenceList: List of 'OccurrenceChainResult' structs describing the occurrences that were expanded in the
    context of the given parent.
    """
    clientId: str = ''
    parent: ExpandPSData1 = None
    occurrenceList: List[OccurrenceChainResult] = ()


@dataclass
class AdditionalInfo(TcBaseObj):
    """
    AdditionalInfo has a list of key value pairs to capture the result.
    
    :var strToDateVectorMap: String to list of Date map.
    :var strToDoubleVectorMap: String to list of Double map.
    :var strToStringVectorMap: String to list of String map.
    :var strToObjectVectorMap: String to list of Teamcenter BusinessObject map.
    :var strToIntegerVectorMap: String to list of Integer map.
    """
    strToDateVectorMap: StringToDateVectorMap = None
    strToDoubleVectorMap: StringToDoubleVectorMap = None
    strToStringVectorMap: StringToStringVectorMap = None
    strToObjectVectorMap: StringToObjectVectorMap = None
    strToIntegerVectorMap: StringToIntegerVectorMap = None


"""
List of children for a given parent. This is returned when the wantSiblings is true.If the line is a leaf node then it would be found in the map.
"""
ParentLineToChildrenDataMap1 = Dict[BOMLine, List[ExpandPSData1]]


"""
A map of string to list of dates.
"""
StringToDateVectorMap = Dict[str, List[datetime]]


"""
A map of string to list of doubles.
"""
StringToDoubleVectorMap = Dict[str, List[float]]


"""
A map of string to list of integers.
"""
StringToIntegerVectorMap = Dict[str, List[int]]


"""
A map of string to list of Teamcenter BusinessObjects.
"""
StringToObjectVectorMap = Dict[str, List[BusinessObject]]


"""
A map of string to list of strings.
"""
StringToStringVectorMap = Dict[str, List[str]]
