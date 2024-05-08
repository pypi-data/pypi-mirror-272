from __future__ import annotations

from tcsoa.gen.BusinessObjects import ItemRevision, BOMLine
from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetAlignDesignsInput(TcBaseObj):
    """
    A list of selected part BOMLine objects and request preference.
    
    :var partLines: A list of selected part BOMLine objects.
    :var requestPref: Map (string, string) of preference names and value pairs. Supported key is: "includeBomLines".
    Supported values are: True/False. Keys and values are case sensitive. If "includeBomLines" with value True is
    specified then only the list of aligned design lines (BOMLine) will be returned in response.
    """
    partLines: List[BOMLine] = ()
    requestPref: RequestPreference = None


@dataclass
class GetAlignedDesignsResp(TcBaseObj):
    """
    The clone stable ID chains of the aligned design lines, the aligned design lines (BOMLine) objects and design
    product (ItemRevision).
    
    :var alignedOccCsidPaths: A list of clone stable ID chains of the aligned design lines.
    :var alignedBomLines: A list of aligned design lines (BOMLine). This will only be returned if  includeBomLines
    preference value is set as True in requestPref.
    :var designProduct: Design product (ItemRevision) in whose scope the aligned design lines are identified.
    :var serviceData: The service data containing partial error if any.
    """
    alignedOccCsidPaths: List[str] = ()
    alignedBomLines: List[BOMLine] = ()
    designProduct: ItemRevision = None
    serviceData: ServiceData = None


@dataclass
class GetAlignedPartsCsidChainResp(TcBaseObj):
    """
    The clone stable ID chains of the aligned part lines and aligned part line (BOMLine) objects.
    
    :var alignedOccCsidPaths: A list of clone stable ID chains of the aligned part lines.
    :var alignedBomLines: A list of aligned part lines (BOMLine). This will only be returned if  includeBomLines
    preference value is set as True in requestPref.
    :var serviceData: The service data containing partial error if any.
    """
    alignedOccCsidPaths: List[str] = ()
    alignedBomLines: List[BOMLine] = ()
    serviceData: ServiceData = None


@dataclass
class GetAlignedPartsInput(TcBaseObj):
    """
    A list of clone stable ID chains for selected design lines, the part line (BOMLine) and the request preference.
    
    :var inputPartLine: A Part Line (BOMLine) that is the Top Line in the eBOM structure.
    :var occurrenceChains: A list of clone stable ID chains of the Design Lines within the dBOM structure. A chain is a
    string of BOMLine.bl_clone_stable_occurrence_id property values starting from the first child of Top Line in the
    dBOM structure descending each BOMLine till the BOMLine for the correlated Part Line in the eBOM structure that
    needs to be identified. Use delimiter, '/' (forward slash) between each bl_clone_stable_occurrence_id property
    value.
    :var requestPref: Map (string, string) of preference names and value pairs. Allowed key is: "includeBomLines" and
    allowed values are: True/False. Keys and values are case sensitive. If "includeBomLines" with value True is
    specified then only the list of aligned part lines (BOMLine) will be returned in response.
    """
    inputPartLine: BOMLine = None
    occurrenceChains: List[str] = ()
    requestPref: RequestPreference = None


"""
Map (string, string) of preference names and value pairs. Allowed preference name is: includeBomLines and allowed values are: True/False. Keys and values are case sensitive.
"""
RequestPreference = Dict[str, str]
