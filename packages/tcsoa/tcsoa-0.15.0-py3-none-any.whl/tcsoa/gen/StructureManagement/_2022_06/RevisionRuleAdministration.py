from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import RevisionRule
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetAPSValidRevisionRulesResponse(TcBaseObj):
    """
    Get Valid Revision Rule Response structure.
    
    :var validRevisionRules: A list of RevisionRule instances.
    :var serviceData: Teamcenter service data.
    """
    validRevisionRules: List[RevisionRule] = ()
    serviceData: ServiceData = None
