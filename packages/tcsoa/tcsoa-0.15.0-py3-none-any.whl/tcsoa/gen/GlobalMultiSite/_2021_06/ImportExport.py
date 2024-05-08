from __future__ import annotations

from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportFilesOfflineFileInfo(TcBaseObj):
    """
    File information structure contain file property map.
    
    :var properties: A map (string, string) of file property name and value pairs. In case of ImanFile, the following
    set of key/values are provided: 
    "datasetUid", "<UID to the Dataset>"
    "fileName", "<the name of the file>"
    "fileTicket", "<ticket string>"
    "reference", "<file reference>"
    In case of TCXML file, the following set of key/values are provided:
    "TCXML", "true"
    "fileTicket", "ticket string".
    In case of TCXML file, the key "TCXML" with value "true" will be present.
    In case of ImanFile, TCXML key itself will not be present.
    """
    properties: NameValueMap = None


@dataclass
class ExportFilesOfflineResponse(TcBaseObj):
    """
    Response structure for exportFilesOffline operation.
    
    :var files: A list of exported ImanFile objects information.
    :var serviceData: Service data contains the partial errors.
    """
    files: List[ExportFilesOfflineFileInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ImportNXFileInfo(TcBaseObj):
    """
    Structure to hold UID of Dataset and file ticket for importing one NX native file into a corresponding NX Dataset.
    
    :var datasetUid: UID for a NX Dataset:
    &#61607;    UGMASTER
    &#61607;    UGPART
    :var ticket: The FMS write ticket used to transfer the NX file to the transient volume.
    """
    datasetUid: str = ''
    ticket: str = ''


"""
Map for storing generic string name-value pair.
"""
NameValueMap = Dict[str, str]
