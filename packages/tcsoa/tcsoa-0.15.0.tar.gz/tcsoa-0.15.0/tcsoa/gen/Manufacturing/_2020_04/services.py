from __future__ import annotations

from tcsoa.gen.Manufacturing._2020_04.Core import AdditionalInfo
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class CoreService(TcService):

    @classmethod
    def cancelManufacturingCheckout(cls, rootObjects: List[BusinessObject], additionalInfo: AdditionalInfo) -> ServiceData:
        """
        Cancels checkout of all given objects which were checked out by user. Supported types are Mfg0BvrProcess,
        Mfg0BvrProcessArea, Mfg0BvrOperation, Mfg0BvrStudy and Mfg0BvrWorkarea, and its subtypes. The structure is
        traversed, and the following checkouts are canceled: 
        &bull;    All the selected objects and its children.
        &bull;    ItemRevision.
        &bull;    BOMView Revision.
        &bull;    Assigned plant, which is of type Mfg0BvrWorkarea and assigned resource, which is of type
        Mfg0BvrResource.
        &bull;    Attached Dataset and Form objects (to all the above).
        If given rootObjects are not checked out, the operation moves on to the sub objects canceling sub object
        checkout.
        
        Use cases:
        &bull; Use Case 1: Default Cancel Checkout
        User has performed "Manufacturing Checkout" operation on some Mfg0BvrProcess objects in Process Simulate or
        Teamcenter MPP. User selects any of the Mfg0BvrProcess objects, and performs "Cancel Manufacturing Checkout"
        operation. User gives input rootObjects only, manufactuing checkout of selected objects are cancelled with
        hierarchy.
        
        &bull;    Use Case 2:  Cancel Checkout without hierarchy 
        User has performed "Manufacturing Checkout" operation on some Mfg0MESimStudy objects with hierarchy in "Study
        Manager" application in Process Simulate or Teamcenter Active Workspace . User wants to cancel checkout on root
        object only. User provides argument value false in  isConsiderSubHierarchy and performs "Cancel Manufacturing
        Checkout" operation. Manufactuing checkout of selected objects are cancelled only on Mfg0MESimStudy object.
        """
        return cls.execute_soa_method(
            method_name='cancelManufacturingCheckout',
            library='Manufacturing',
            service_date='2020_04',
            service_name='Core',
            params={'rootObjects': rootObjects, 'additionalInfo': additionalInfo},
            response_cls=ServiceData,
        )
