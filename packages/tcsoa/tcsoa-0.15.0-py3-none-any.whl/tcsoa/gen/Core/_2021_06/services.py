from __future__ import annotations

from tcsoa.gen.Core._2021_06.DataManagement import RemoveNamedReferenceFromDataset, AddNamedReferenceToDatasetInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def removeNamedReferenceFromDataset2(cls, removeNamedReferenceIn: List[RemoveNamedReferenceFromDataset]) -> ServiceData:
        """
        This operation removes the specified named references from a Dataset.If the NamedReferenceInfo.targetObject
        input is specified and matched then only that named reference is removed from the Dataset. The
        NamedReferenceInfo.targetObject input is not matched with any named references in the Dataset instance then no
        named reference is removed. If the NamedReferenceInfo.deleteTarget input is true then the
        NamedReferenceInfo.targetObject will be deleted if it is no longer referenced. This operation can optionally
        create a new version of an input Dataset.
        
        Use cases:
        &bull;    The user shall use this operation to remove named reference from the Dataset.
        &bull;    In Teamcenter Rich Client named reference dialog, the user Checkout Dataset, and upload the file as
        named reference. The user performs a Cancel Checkout operation to remove the named reference which is added
        after Checkout operation.
        """
        return cls.execute_soa_method(
            method_name='removeNamedReferenceFromDataset2',
            library='Core',
            service_date='2021_06',
            service_name='DataManagement',
            params={'removeNamedReferenceIn': removeNamedReferenceIn},
            response_cls=ServiceData,
        )

    @classmethod
    def addNamedReferenceToDatasets(cls, addNamedReferenceIn: List[AddNamedReferenceToDatasetInfo]) -> ServiceData:
        """
        This operation adds a list of named references to the input Dataset. Operation adds only existing named
        reference objects and does not create new named reference. This operation can optionally create a new version
        of an input Dataset.
        
        Use cases:
        &bull;    The user shall use this operation to add named reference to the exiting Dataset.
        &bull;    In Teamcenter Rich Client named reference dialog, the user Checkout Dataset and remove named
        reference from Dataset. The user performs a Cancel Checkout operation to retain the named reference which is
        removed after the Checkout operation.
        """
        return cls.execute_soa_method(
            method_name='addNamedReferenceToDatasets',
            library='Core',
            service_date='2021_06',
            service_name='DataManagement',
            params={'addNamedReferenceIn': addNamedReferenceIn},
            response_cls=ServiceData,
        )
