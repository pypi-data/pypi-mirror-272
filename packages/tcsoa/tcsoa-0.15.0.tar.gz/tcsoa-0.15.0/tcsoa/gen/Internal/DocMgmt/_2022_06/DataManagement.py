from __future__ import annotations

from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class FileNameRelation(TcBaseObj):
    """
    The structure contains information for naming Datasets based on the WorkspaceObject object.
    
    :var fileName: The file name. The file name can be either the name, "test.docx" or the full qualify local path,
    such as: "C:\temp\test.docx". If it is the full qualify local path, only the file name will be used. The file name
    is used to generate the Dataset name. If the "Fnd0GenerateDSNameWithoutExt" business constant for type
    WorkpaceObject object is false or not existed, then the Dataset name returned will have the file name extension
    including the period (for example, "test.docx"); otherwise, the Dataset names returned will not have the file name
    extensions (for example, "test").
    :var relationName: The relation name. This is a placeholder for future use and it is not used.
    """
    fileName: str = ''
    relationName: str = ''


@dataclass
class GenerateDatasetNameOutput(TcBaseObj):
    """
    The structure that contains the WorkspaceObject object and a map of file name to Dataset name.
    
    :var workspaceObject: The WorkspaceObject business object.
    :var fileNameDatasetNameMap: A map (string, string) of file name to the Dataset name.  The keys of this map are the
    input file names.  The values of this map are the generated Dataset names.  Unique Dataset names are not required,
    so duplicate names may exist in the map. When duplicate file names are passed as input to this operation, one
    key/value pair will be returned for each unique file name.
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
    This input data structure includes the WorkspaceObject and a list of FileNameRelation structures.
    
    :var workspaceObject: The WorkspaceObject object of interest.
    :var fileNameRelations: A list of FileNameRelation objects.
    """
    workspaceObject: WorkspaceObject = None
    fileNameRelations: List[FileNameRelation] = ()


"""
A map of file name to Dataset name pairs.
"""
FileNameDatasetNameMap = Dict[str, str]
