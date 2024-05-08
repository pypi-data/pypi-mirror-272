from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GroupName(TcBaseObj):
    """
    This structure contains the real and display name of the group.
    
    :var dispName: Display name of the group.
    :var realName: Real name of the group.
    :var isModifiable: True if the mapping group can be modified by logged in user
    """
    dispName: str = ''
    realName: str = ''
    isModifiable: bool = False


@dataclass
class ImportExcelData(TcBaseObj):
    """
    This structure contains all the data required to import a file to Teamcenter.
    
    :var selectedObject: Selected Object under which the Specification will be created.
    :var transientFileWriteTicket: The write ticket of the Excel file to be imported to Teamcenter.
    :var mappingGroupData: List of mapping groups to be consumed during the import Specification.
    :var importOptions: A list of options to be used during the import. Supported options are: "ParseHeader" and
    "RunInBackground". If "ParseHeader" option is chosen, the header row in the Excel sheet is parsed. If
    "RunInBackground" option is chosen, the excel file import runs in background mode and user will get a notification
    when complete, else after completion of import, the top line Revision of the created structure will be opened.
    :var typePropInfos: List of object types and property related information to be retrieved for the types found in
    input Excel sheet.
    """
    selectedObject: BusinessObject = None
    transientFileWriteTicket: str = ''
    mappingGroupData: MappingGroupData = None
    importOptions: List[str] = ()
    typePropInfos: List[TypePropInfo] = ()


@dataclass
class ImportExcelResponse(TcBaseObj):
    """
    This structure contains the list of objects of type SpecElementRevision or RequirementSpecRevision.
    
    :var revObjects: List of business objects of type SpecElementRevision or RequirementSpecRevision.
    :var serviceData: Service data.
    """
    revObjects: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class MappingGroupData(TcBaseObj):
    """
    This structure contains the real and display name of the mapping group along with the mapping information.
    
    :var groupName: It contains the real and display name of the group.
    :var actionName: Supported action: "CREATE", " UPDATE" or "DELETE"
    :var mappingInfo: List of property related information.
    """
    groupName: GroupName = None
    actionName: str = ''
    mappingInfo: List[PropInfo] = ()


@dataclass
class MappingGroupInput(TcBaseObj):
    """
    This structure contains all the data required to import a file to Teamcenter.
    
    :var transientFileWriteTicket: The write ticket of the Excel file to be imported to Teamcenter.
    :var mappingGroupData: It contains the action name, group name and mapping information.
    :var importOptions: List of options to be used during the import. Supported option: "ParseHeader" - The header row
    in the Excel sheet is parsed.
    """
    transientFileWriteTicket: str = ''
    mappingGroupData: MappingGroupData = None
    importOptions: List[str] = ()


@dataclass
class MappingGroupOutput(TcBaseObj):
    """
    This structure contains the type and property related data which is parsed from the input Excel sheet.
    
    :var mappingGroups: List of mapping group related information
    :var propInfos: List of property related information
    :var typePropInfos: List of object types and property related information to be retrieved for the types found in
    input Excel sheet. This list will be used only when importOption is set to "ParseHeader".
    """
    mappingGroups: List[GroupName] = ()
    propInfos: List[PropInfo] = ()
    typePropInfos: List[TypePropInfo] = ()


@dataclass
class MappingGroupResponse(TcBaseObj):
    """
    This structure contains the list of MappingGroupOutput
    
    :var mappingOutputs: List of mapping outputs.
    :var serviceData: Service data.
    """
    mappingOutputs: List[MappingGroupOutput] = ()
    serviceData: ServiceData = None


@dataclass
class PropInfo(TcBaseObj):
    """
    'PropInfo' structure contains the property related information to be set.
    
    :var propHeader: The name of the property used as column header in Excel sheet.
    :var realPropName: BMIDE real name of the property.
    :var dispPropName: Display name of the property.
    :var isRequired: True if it is a required property.
    """
    propHeader: str = ''
    realPropName: str = ''
    dispPropName: str = ''
    isRequired: bool = False


@dataclass
class TypePropInfo(TcBaseObj):
    """
    'TypePropInfo' structure is a container to hold the types and property related information.
    
    :var objectType: Valid subclass of "SpecElement" or "RequirementSpec" to be created in Teamcenter.
    :var dispTypeName: Display name of the object type.
    :var propInfos: List of property related information.
    """
    objectType: str = ''
    dispTypeName: str = ''
    propInfos: List[PropInfo] = ()
