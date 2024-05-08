from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from datetime import datetime


@dataclass
class AdditionalInfo(TcBaseObj):
    """
    Structure for additional information.
    
    :var strToBooleanVectorMap: A map (string, list of bool) to capture additional information. The key
    isConsiderSubHierarchy to cancel checkout with or without hierarchy. If false, cancels checkout without hierarchy.
    :var strToDateVectorMap: A map (string, list of date) to capture additional information for future use.
    :var strToDoubleVectorMap: A map (string, list of double) to capture additional information for future use.
    :var strToIntegerVectorMap: A map (string, list of int) to capture additional information for future use.
    :var strToObjVectorMap: A map (string, list of BusinessObject) to capture additional information for future use.
    :var strToStringVectorMap: A map (string, list of string) to capture additional information for future use.
    """
    strToBooleanVectorMap: StringToBooleanVectorMap = None
    strToDateVectorMap: StringToDateVectorMap = None
    strToDoubleVectorMap: StringToDoubleVectorMap = None
    strToIntegerVectorMap: StringToIntegerVectorMap = None
    strToObjVectorMap: StringToObjectVectorMap = None
    strToStringVectorMap: StringToStringVectorMap = None


"""
A map (string, list of bool) to capture additional information.
"""
StringToBooleanVectorMap = Dict[str, List[bool]]


"""
A map (string, list of DateTime) to capture additional information.
"""
StringToDateVectorMap = Dict[str, List[datetime]]


"""
A map (string, list of double) to capture additional information.
"""
StringToDoubleVectorMap = Dict[str, List[float]]


"""
A map (string, list of int) to capture additional information.
"""
StringToIntegerVectorMap = Dict[str, List[int]]


"""
A map (string, list of BusinessObject) to capture additional information.
"""
StringToObjectVectorMap = Dict[str, List[BusinessObject]]


"""
A map (string, list of string) to capture additional information.
"""
StringToStringVectorMap = Dict[str, List[str]]
