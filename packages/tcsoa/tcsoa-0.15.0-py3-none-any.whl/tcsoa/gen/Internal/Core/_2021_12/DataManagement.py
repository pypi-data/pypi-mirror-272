from __future__ import annotations

from tcsoa.gen.BusinessObjects import Dataset, WorkspaceObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class DatasetsForFile(TcBaseObj):
    """
    Dataset objects for the given file name.
    
    :var fileName: The input file name.
    :var dataset: The first found Dataset instance with the given file name.
    """
    fileName: str = ''
    dataset: Dataset = None


@dataclass
class DatasetsForFileInput(TcBaseObj):
    """
    DatasetsForFileInput object containing references to the input data.
    
    :var clientID: A unique string used to identify return data elements with this input structure.
    :var fileNames: File names to fetch the Dataset instances.
    :var parentObject: WorkspaceObject business object related to the Dataset.
    """
    clientID: str = ''
    fileNames: List[str] = ()
    parentObject: WorkspaceObject = None


@dataclass
class DatasetsForFileOutput(TcBaseObj):
    """
    An object containing the clientID and list of DatasetsForFile.
    
    :var clientID: The unmodified value from the input clientId.This can be used by the caller to indentify this data
    structure with the source input.
    :var datasetsForFile: A list containing Dataset objects for the given file name.
    """
    clientID: str = ''
    datasetsForFile: List[DatasetsForFile] = ()


@dataclass
class DatasetsForFileResponse(TcBaseObj):
    """
    An object containing the list of DatasetsForFileOutput and serviceData.
    
    :var output: A list of DatasetsForFileOutput.
    :var serviceData: Service data object associated with the operation.
    """
    output: List[DatasetsForFileOutput] = ()
    serviceData: ServiceData = None
