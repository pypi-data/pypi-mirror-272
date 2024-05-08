from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExportFilesOfflineInput(TcBaseObj):
    """
    Input structure for exportFilesOffline operation.
    
    :var datasetUid: UID of Dataset
    :var itemRevisionUid: UID of ItemRevision
    """
    datasetUid: str = ''
    itemRevisionUid: str = ''
