from __future__ import annotations

from typing import List
from tcsoa.gen.Server import PartialErrors
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AddPoliciesResponse(TcBaseObj):
    """
    The policies added to the session.
    
    :var policyIDs: A list of policy IDs. The initial size and order of this list will match the input list of
    'clientPolicies', with an unique ID generated for each policy defined in the  'clientPolicies' list. Successfully
    added policies from the 'namedPolicies'  list are appended to th end of this list.
    :var partialErrors: Partial errors or warnings.
    """
    policyIDs: List[str] = ()
    partialErrors: PartialErrors = None
