from __future__ import annotations

from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDatasetIndexableFilesInfoResp(TcBaseObj):
    """
    The response structure with information on indexable files for the given Dataset(s) and service data to hold any
    errors that may have encountered during the operation.
    
    :var datasetInfoMap: A map (string, DatasetInfo) of Dataset UID and object containing information on the Dataset
    and its associated indexable files.
    :var serviceData: Service Data.
    """
    datasetInfoMap: DatasetInfoMap = None
    serviceData: ServiceData = None


@dataclass
class DatasetFileInfo(TcBaseObj):
    """
    Structure containing information on ImanFile associated with a Dataset.
    
    :var referenceName: The reference name used to associate this file with the Dataset.
    :var fileName: The original name of the file.
    :var fileUID: The unique identifier of the ImanFile.
    :var fmsFileTicket: The FMS read file ticket for the file to be downloaded.
    :var isText: If true, the file is of type text, otherwise it is a binary file.
    """
    referenceName: str = ''
    fileName: str = ''
    fileUID: str = ''
    fmsFileTicket: str = ''
    isText: bool = False


@dataclass
class DatasetInfo(TcBaseObj):
    """
    Structure containing information on a Dataset and its associated files.
    
    :var datasetType: The type of the Dataset. e.g. PDF, MSWord, UGMASTER
    :var filesInfo: A list of objects containing information on files associated with the Dataset.
    """
    datasetType: str = ''
    filesInfo: List[DatasetFileInfo] = ()


"""
A map (string, DatasetInfo) of Dataset UID and object containing information on Dataset and its indexable files.
"""
DatasetInfoMap = Dict[str, DatasetInfo]
