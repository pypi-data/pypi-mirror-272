from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2020_01.DataManagement import AdditionalInfo
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReferencedAssemblyFileInfo(TcBaseObj):
    """
    A structure representing the data relevant to the referenced assembly directmodel dataset.
    
    :var inputIndex: A number that corresponds to the index of the "lines" argument in input, for which the information
    was successfully obtained.
    :var transform: A list of 16 doubles representing the transform of the referenced line. The format is same as the
    "Absolute Occurrence Transform" BOMLine property.
    :var data: For future use.
    :var ticket: The FMS Fileticket for the DirectModel JTPART named reference.
    :var referenceSet: The name of the reference set.
    :var fileObject: The JTPART file object.
    :var originalFileName: The original file name of the JTPART named reference file object.
    """
    inputIndex: int = 0
    transform: List[float] = ()
    data: AdditionalInfo = None
    ticket: str = ''
    referenceSet: str = ''
    fileObject: BusinessObject = None
    originalFileName: str = ''


@dataclass
class ReferencedAssemblyFileInputInfo(TcBaseObj):
    """
    The list of objects for which the assembly Dataset objects and their tranforms in the referenced structure are
    needed.
    
    :var lines: The list of input BOMLine objects in the referencing structure for which the 
    assembly Dataset objects need to be derived from the referenced structure. 
    For example, a list of Manufacturing BOMLine objects. Currently, 
    only BOMLine objects from MBOM or BOP structures are supported.
    :var additionalInfo: For future use.
    """
    lines: List[BusinessObject] = ()
    additionalInfo: AdditionalInfo = None


@dataclass
class ReferencedAssemblyFileResponse(TcBaseObj):
    """
    The response representing the assembly datasets for the supplied objects from referencing structure.
    
    :var result: A list of ReferencedAssemblyFileInfo entities which contain Dataset objects and their transforms.
    :var additionalInfo: For future use.
    :var serviceData: The partial errors are captured.
    """
    result: List[ReferencedAssemblyFileInfo] = ()
    additionalInfo: AdditionalInfo = None
    serviceData: ServiceData = None
