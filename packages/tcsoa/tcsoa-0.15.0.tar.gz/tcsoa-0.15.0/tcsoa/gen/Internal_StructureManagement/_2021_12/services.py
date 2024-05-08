from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2021_12.EffectivitiesManagement import EffectivitiesInputInfo2
from tcsoa.gen.BusinessObjects import ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class EffectivitiesManagementService(TcService):

    @classmethod
    def createOrUpdateDateEffectivities(cls, effectivitiesInfo: List[EffectivitiesInputInfo2], effectivityGroupRevision: ItemRevision) -> ServiceData:
        """
        Creates or updates effectivity information for the given Fnd0EffectvtyGrpRevision represented by the input
        parameter 'effectivityGroupRevision'.
        
        Use cases:
        - Create Effectivity objects with provided date ranges and endItem for a given Fnd0EffectvtyGrpRevision object.
        - Update Effectivity information like date ranges and endItem for a list of Effectivity objects belonging to an
        Fnd0EffectvtyGrpRevision.
        - Remove an Effectivity object from an Fnd0EffectvtyGrpRevision object.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateDateEffectivities',
            library='Internal-StructureManagement',
            service_date='2021_12',
            service_name='EffectivitiesManagement',
            params={'effectivitiesInfo': effectivitiesInfo, 'effectivityGroupRevision': effectivityGroupRevision},
            response_cls=ServiceData,
        )
