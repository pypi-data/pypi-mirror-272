from __future__ import annotations

from tcsoa.gen.BusinessObjects import Item, Effectivity
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EffectivitiesInputInfo2(TcBaseObj):
    """
    Input structure containing details like dateRange and endItem to create, update or delete a Effectivity object for
    the input Fnd0EffectvtyGrpRevision object.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var effectivityComponent: An Effectivity object to be updated or deleted from the Fnd0EffectvtyGrpRevision object.
    If the 'effectivityComponent' is NULL, a new Effectivity object is created using the given 'dateRange' with or
    without 'endItemComponent'.
    :var endItemComponent: A Item object representing a product, system or module with respect to which user can
    configure the structure by Effectivity.
    :var dateRange: A list of effectivity date range, a valid range of dates:
    - Open range, for example, from 05 January onward.
    - Closed range, for example, from 01 January to 30 April.
    :var openEndedStatus: Effectivity open ended status, 0 for EFFECTIVITY_closed, 1 for EFFECTIVITY_open_ended, 2 for
    FFECTIVITY_stock_out.
    :var decision: Flag to decide if Effectivity object is to be updated or deleted. 
    decision = 0 (Create Effectivity component).
    decision = 1 ( Update Effectivity component ).
    decision = 2 ( Delete Effectivity component ).
    There is no flag required for create. This argument is ignored if 'effectivityComponent' is given as NULL, a new
    Effectivity object is created. Hence, the default value of decision will be zero which means create operation.
    """
    clientId: str = ''
    effectivityComponent: Effectivity = None
    endItemComponent: Item = None
    dateRange: List[datetime] = ()
    openEndedStatus: int = 0
    decision: int = 0
