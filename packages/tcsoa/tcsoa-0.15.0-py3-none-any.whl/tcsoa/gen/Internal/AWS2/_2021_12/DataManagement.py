from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Dataset, WorkspaceObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.Internal.AWS2._2017_06.DataManagement import ViewData
from dataclasses import dataclass


@dataclass
class GetViewerDataIn(TcBaseObj):
    """
    The input structure for GetViewerData2.
    
    :var obj: The BusinessObject with an associated Dataset for which relevant viewer needs to be fetched.
    :var dataset: The Dataset object which is currently displayed in the viewer. If  NULL, the default viewer
    associated with the input object is retrieved.
    :var namedReference: The named reference object currently displayed in the viewer. If NULL, the first viewable
    named reference of the Dataset is returned.
    :var direction: The direction for Dataset retrieval from input object based on Dataset currently displayed in the
    viewer. If direction is  empty, then the Dataset input argument is ignored, and input object is processed to get
    the associated Dataset and relevant viewer. 
    If direction is "next" or "previous" and namedReference is NULL, then the input object is processed to find the
    next or previous in line Dataset and its first viewable named reference with its relevant viewer. 
    If direction is "next" or "previous" and namedReference is specified, then the input object is processed to find
    the next or previous in line viewable named reference with its relevant viewer. 
    Valid values for direction are "next", "previous" and "".
    """
    obj: BusinessObject = None
    dataset: BusinessObject = None
    namedReference: BusinessObject = None
    direction: str = ''


@dataclass
class GetViewerDataOutput(TcBaseObj):
    """
    Output structure for viewer data.
    
    :var dataset: The Dataset whose associated file needs to be displayed in the viewer.
    :var views: The list of ViewData objects.
    :var hasMoreDatasets: If true, more than one Dataset is related to input object; otherwise, false.
    :var hasMoreNamedReferences: If true, more than one named reference is related to attached Dataset; otherwise,
    false.
    """
    dataset: BusinessObject = None
    views: List[ViewData] = ()
    hasMoreDatasets: bool = False
    hasMoreNamedReferences: bool = False


@dataclass
class GetViewerDataResponse(TcBaseObj):
    """
    Response structure for getViewerData2 operation.
    
    :var output: The list of GetViewerDataOutput objects.
    :var serviceData: The service data.
    """
    output: GetViewerDataOutput = None
    serviceData: ServiceData = None


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
