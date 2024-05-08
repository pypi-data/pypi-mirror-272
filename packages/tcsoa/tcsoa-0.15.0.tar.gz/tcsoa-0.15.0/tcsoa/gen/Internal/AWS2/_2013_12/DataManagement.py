from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetStyleSheetClassificationData(TcBaseObj):
    """
    The associated classification trace and classification object associated with the specified Business Object.
    
    :var classificationObject: The Classification object to which this object has been associated.
    :var classificationTrace: The classification trace for this classification assignment.
    """
    classificationObject: BusinessObject = None
    classificationTrace: List[str] = ()


@dataclass
class GetStyleSheetDatasetInfo(TcBaseObj):
    """
    Contains the style sheet dataset info.
    
    :var datasetLastSaveDate: Contains the last save date(lsd) of the dataset
    :var datasetContent: The content of the dataset.
    """
    datasetLastSaveDate: datetime = None
    datasetContent: str = ''
