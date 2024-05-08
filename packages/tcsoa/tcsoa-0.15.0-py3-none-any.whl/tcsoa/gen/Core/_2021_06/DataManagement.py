from __future__ import annotations

from tcsoa.gen.BusinessObjects import Dataset
from typing import List
from tcsoa.gen.Core._2007_09.DataManagement import NamedReferenceInfo
from tcsoa.gen.Core._2010_04.DataManagement import NamedReferenceObjectInfo
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class RemoveNamedReferenceFromDataset(TcBaseObj):
    """
    Input structure for the removeNamedReferenceFromDataset2 operation. This contains information of Dataset, a list of
    named referenced which are going to be removed.
    
    :var clientID: A unique string supplied by the caller.
    :var dataset: The Dataset object from which to remove the specified named references.
    :var nrInfo: A list of named reference information to be removed which contains information of named reference type
    value, object reference.
    :var createNewDatasetVersion: If true, a new Dataset version is created after the removal of named reference;
    otherwise, no new version is created for a Dataset.
    """
    clientID: str = ''
    dataset: Dataset = None
    nrInfo: List[NamedReferenceInfo] = ()
    createNewDatasetVersion: bool = False


@dataclass
class AddNamedReferenceToDatasetInfo(TcBaseObj):
    """
    Input structure for the addNamedReferenceToDatasets operation. This contains information of Dataset, 
    list of named referenced which are going to be added with a specific reference type.
    
    :var clientID: A unique string supplied by the caller.
    :var dataset: The Dataset object to which the specified named references will be added.
    :var nrInfo: A list of named reference information to be added which contains information about named reference
    type value, object reference and object type name.
    :var createNewDatasetVersion: If true, a new Dataset version is created after the addition of a named reference;
    otherwise, no new version is created for a Dataset.
    """
    clientID: str = ''
    dataset: Dataset = None
    nrInfo: List[NamedReferenceObjectInfo] = ()
    createNewDatasetVersion: bool = False
