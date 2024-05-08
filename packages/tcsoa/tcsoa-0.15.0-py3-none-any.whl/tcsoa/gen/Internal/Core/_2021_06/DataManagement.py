from __future__ import annotations

from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class FileNameRelation(TcBaseObj):
    """
    The structure contains information for naming Datasets related to the WorkspaceObject object.
    
    :var fileName: The file name. The file name can be either the name, "test.docx" or the full qualify local path,
    such as: "C:\temp\test.docx"
    :var relationName: The relation name. This relation is used to relate the WorkspaceObject to the Dataset and can be
    used when generating the Dataset name. If relationName is empty or not a valid Teamcenter relation type name,
    fileName will be used to create the Dataset name.
    """
    fileName: str = ''
    relationName: str = ''


@dataclass
class GenerateDatasetNameOutput(TcBaseObj):
    """
    The structure that contains the WorkspaceObject object and a map of file name to Dataset name.
    
    :var workspaceObject: The WorkspaceObject business object.
    :var fileNameDatasetNameMap: A map (string, string) of file name to the Dataset name.
    """
    workspaceObject: WorkspaceObject = None
    fileNameDatasetNameMap: FileNameDatasetNameMap = None


@dataclass
class GenerateDatasetNameResponse(TcBaseObj):
    """
    The GenerateDatasetNameResponse structure contains a list of GenerateDatasetNameOutput structure and the
    ServiceData object.
    
    :var output: A list of GenerateDatasetNameOutput structure.
    :var serviceData: The service data contains any partial errors which may have been encountered during processing.
    """
    output: List[GenerateDatasetNameOutput] = ()
    serviceData: ServiceData = None


@dataclass
class GenerateDsNameInput(TcBaseObj):
    """
    The structure contains information for naming Datasets related to the WorkspaceObject object.
    
    :var workspaceObject: The WorkspaceObject object.
    :var fileNameRelations: A list of FileNameRelation.
    :var additionalInfo: A map (string, string) of attribute name to value pairs. This is additional information
    (name/value pair) used for naming the Dataset. This is a placeholder for future use and it is not used.
    """
    workspaceObject: WorkspaceObject = None
    fileNameRelations: List[FileNameRelation] = ()
    additionalInfo: NamingOptionsMap = None


"""
A map of file name to Dataset name pairs.
"""
FileNameDatasetNameMap = Dict[str, str]


"""
This map has information about the name/value pair of the naming options.
"""
NamingOptionsMap = Dict[str, str]
