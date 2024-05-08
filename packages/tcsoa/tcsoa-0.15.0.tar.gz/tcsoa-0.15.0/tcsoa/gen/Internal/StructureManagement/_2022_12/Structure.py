from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import POM_object, WorkspaceObject, PSOccurrenceThread
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetOccAttrsObjectsIn(TcBaseObj):
    """
    This contains information of the PSOccurrence and list of the types of occurrence attribute objects which need to
    be returned.
    
    :var clientId: Identifier that helps the client track the object(s) created or updated.
    :var bvrOrOccRev: A PSBOMViewRevision object or any subtype of Fnd0AbstractOccRevision whose struct last mod date
    needs to be updated and which manages the occurrence.
    :var occurrence: A PSOccurrenceThread object for which the attribute group object needs to be created. This input
    is ignored when bvrOrOccRev is subtype of Fnd0AbstractOccRevision.
    :var occAttrObjectTypes: The type of occurrence attribute objects which need to be returned. Any subtype of
    Fnd0AbstractOccAttrs is supported.
    """
    clientId: str = ''
    bvrOrOccRev: WorkspaceObject = None
    occurrence: PSOccurrenceThread = None
    occAttrObjectTypes: List[str] = ()


@dataclass
class GetOccAttrsObjectsResponse(TcBaseObj):
    """
    Contains information of the Occurrence Attribute objects alonf with its owning PSOccurrence and its type.
    
    :var occAttrObjects: Occurrence attribute objects. It is mapped to its owning PSOccurrence and has information of
    its type. Any subtype of Fnd0AbstractOccAttrs is supported.
    :var serviceData: The Service Data. This contains information of any failures during the operation.
    """
    occAttrObjects: List[OccWithAttrObjectsInfo] = ()
    serviceData: ServiceData = None


@dataclass
class AttributeInfo(TcBaseObj):
    """
    Contains information of the property with its name and values.
    
    :var propName: Name os the property
    :var propValues: List of Values for the given property.
    """
    propName: str = ''
    propValues: List[str] = ()


@dataclass
class OccAttrInfo(TcBaseObj):
    """
    Contains information of the Occurrence Attribute object and its type.
    
    :var occAttrType: The type of occurrence attribute object.
    :var occAttrObject: Occurrence attribute object. Any subtype of Fnd0AbstractOccAttrs is supported.
    """
    occAttrType: str = ''
    occAttrObject: POM_object = None


@dataclass
class OccWithAttrObjectsInfo(TcBaseObj):
    """
    Contains information of the owning PSOccurrence and all associated Occurrence Attribute objects information.
    
    :var clientId: Input client Id to track the created or updated occurrence attribute objects..
    :var bvrOrOccRev: A PSBOMViewRevision object or any subtype of Fnd0AbstractOccRevision whose struct last mod date
    has been updated if the property is present in preference.
    :var occurrence: Owning PSOccurrence object thread.
    :var occAttrInfo: List of Attribute objects information which include its type and object
    """
    clientId: str = ''
    bvrOrOccRev: WorkspaceObject = None
    occurrence: PSOccurrenceThread = None
    occAttrInfo: List[OccAttrInfo] = ()


@dataclass
class CreateOrUpdateOccAttrObjectsIn(TcBaseObj):
    """
    This contains information to create or update the occurrence attribute objects for the PSOccurrence.
    For creating the occurrence attribute objects, PSOccurrence and occurrence attribute object type must be added to
    input. For updating, the occurrence attribute object must be added to the input.
    The input also contains information of the property to be set along with the new value that has to be updated on
    property.
    
    :var clientId: Identifier that helps the client track the object(s) created or updated.
    :var bvrOrOccRev: A PSBOMViewRevision object or any subtype of Fnd0AbstractOccRevision whose struct last mod date
    needs to be updated and which manages the occurrence.
    :var occurrence: A PSOccurrenceThread object for which the attribute group object needs to be created. This input
    is ignored when bvrOrOccRev is subtype of Fnd0AbstractOccRevision.
    :var occAttrObjectType: The type of occurrence attribute group which needs to be created. Any subtype of
    Fnd0AbstractOccAttrs is supported.
    :var propInfo: The property name and its value that must be updated.
    """
    clientId: str = ''
    bvrOrOccRev: WorkspaceObject = None
    occurrence: PSOccurrenceThread = None
    occAttrObjectType: str = ''
    propInfo: List[AttributeInfo] = ()


@dataclass
class CreateOrUpdateOccAttrObjectsResp(TcBaseObj):
    """
    Contains information of the created or updated Occurrence attribute objects along with its PSOccurrence and the
    occurrence attribute type.
    
    :var createdOrUpdatedOccAttrObjects: A list containing information of created or updated occurrence attribute
    objects with its owning PSOccurrence and its type. Any subtype of Fnd0AbstractOccAttrs is supported.
    :var serviceData: Contains information of any failures during the operation.
    """
    createdOrUpdatedOccAttrObjects: List[OccWithAttrObjectsInfo] = ()
    serviceData: ServiceData = None
