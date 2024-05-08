from __future__ import annotations

from tcsoa.gen.StructureManagement._2014_12.StructureSearch import AdditionalInfo
from tcsoa.gen.BusinessObjects import BusinessObject, RuntimeBusinessObject
from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpandBOMLinesNamedReferenceInfo(TcBaseObj):
    """
    This structure is used to identify the reference object corresponding to the named reference.
    
    :var namedReferenceType: Type of reference object.
    :var namedReferenceName: Name of reference object.
    :var referenceObject: Object reference corresponding to the named reference.
    :var fileTicket: FMS ticket used to retrieve the file in cases where referenceObject is a file.
    """
    namedReferenceType: str = ''
    namedReferenceName: str = ''
    referenceObject: BusinessObject = None
    fileTicket: str = ''


@dataclass
class ExpandBOMLinesObjects(TcBaseObj):
    """
    Through this structure, the bom line, the objects attached to the bom line object are returned.
    
    :var bomLine: BOMLine object reference where related objects are related.
    :var relatedObjects: List of object references attached to line with given relation.
    """
    bomLine: BusinessObject = None
    relatedObjects: List[ExpandBOMLinesRelatedObjectInfo] = ()


@dataclass
class ExpandBOMLinesRelatedObjectInfo(TcBaseObj):
    """
    This structure is used to identify the reference object corresponding to the named reference.
    
    :var relatedObject: The resulting related object by following a relation specified in the DataSetExpression.
    :var namedRefList: List of named reference and reference object of relatedObject.
    """
    relatedObject: BusinessObject = None
    namedRefList: List[ExpandBOMLinesNamedReferenceInfo] = ()


@dataclass
class ExpandOptions(TcBaseObj):
    """
    Expansion Options for a given expansion
    
    :var dataSetInfoToLoad: A list of Information to load related DataSet objects.
    :var additionalInfo: Currently not used, possible future usage.
    """
    dataSetInfoToLoad: List[DataSetExpression] = ()
    additionalInfo: AdditionalInfo = None


@dataclass
class ExpandResponse(TcBaseObj):
    """
    Response SOA Structure for expansion results. It contains found objects and the expansion cursor that can be used
    in next expansion.
    
    :var objectsDone: Number of objects returned so far.
    :var estimatedObjectsLeft: Estimated number of objects left for one level expansion.
    :var foundObjects: The next list of objects returned by the startExpandBOMLines or nextExpandBOMLines operation.
    :var expandCursor: SearchCursor object that tracks the expand results. This object is used to get the next set of
    results for this startExpandBOMLines operation.
    :var extraObjects: A list of Dataset objects for the lines returned.
    :var serviceData: Service Data for any error information.
    """
    objectsDone: int = 0
    estimatedObjectsLeft: int = 0
    foundObjects: List[RuntimeBusinessObject] = ()
    expandCursor: BusinessObject = None
    extraObjects: List[ExtraObjects] = ()
    serviceData: ServiceData = None


@dataclass
class ExtraObjects(TcBaseObj):
    """
    It contains the datasets to be returned.
    
    :var parentInfo: The parent information.
    :var childrenInfo: A list of infomation of the children that contain DataSet objects.
    """
    parentInfo: ExpandBOMLinesObjects = None
    childrenInfo: List[ExpandBOMLinesObjects] = ()


@dataclass
class RelatedObjectTypeAndNamedRefs(TcBaseObj):
    """
    This structure contains a related object type and the list of its named references to be processed.
    
    :var objectTypeName: Object type name.
    Valid values are:
    - DirectModel
    - JtSimplification
    - Aws0JtSpatialHierarchy
    
    
    :var namedReferenceNames: A list of Named reference names.
    Valid values are:
    - JTPART
    - ALSG
    - Aws0SpatialJt
    
    """
    objectTypeName: str = ''
    namedReferenceNames: List[str] = ()


@dataclass
class DataSetExpression(TcBaseObj):
    """
    Dataset criteria for the expansion
    
    :var relationName: The relation name.
    Valid values are:
    - IMAN_Rendering
    - SimplifiedRendering
    - Aws0SpatialRendering
    
    
    :var relatedObjAndNamedRefs: List of related object types and named references.
    :var namedRefHandler: Used to identify how named references will be processed. 
    Valid values are: 
    0: UseNamedRefsList -- Only the named references listed in the input RelatedObjectTypeAndNamedRefs struct are
    processed. 
    1: NoNamedRefs -- No named references are to be processed. The input RelatedObjectTypeAndNamedRefs will be ignored. 
    2: AllNamedRefs -- All named references are to be processed. The input RelatedObjectTypeAndNamedRefs will be
    ignored. 
    3. PreferredJT -- Specialized code for selecting which named references to process is executed. This is intended
    for selecting the most appropriate JT files for visualization purposes. If related object is a DirectModel,
    RelatedObjectTypeAndNamedReferences contents will be ignored and only the preferred JT is returned. If related
    object is not Direct Model, named reference expansion will proceed as though namedRefHandler is UseNamedRefsList.
    """
    relationName: str = ''
    relatedObjAndNamedRefs: List[RelatedObjectTypeAndNamedRefs] = ()
    namedRefHandler: int = 0


"""
Map containing expansion flags and values.
"""
SettingsMap = Dict[str, List[str]]
