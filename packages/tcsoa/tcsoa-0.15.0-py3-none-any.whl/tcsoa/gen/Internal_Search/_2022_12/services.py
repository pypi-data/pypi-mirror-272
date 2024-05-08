from __future__ import annotations

from tcsoa.gen.Internal.Search._2022_12.FullTextSearch import Awp0FullTextSavedSearchResponse, Awp0CreateFTSSavedSearchInput
from typing import List
from tcsoa.base import TcService


class FullTextSearchService(TcService):

    @classmethod
    def createFullTextSavedSearch2(cls, inputs: List[Awp0CreateFTSSavedSearchInput]) -> Awp0FullTextSavedSearchResponse:
        """
        This operation creates Awp0FullTextSavedSearch objects. Awp0FullTextSavedSearch objects are used to store
        information about a saved search such as search name, search string, search filters, chart input parameters etc.
        """
        return cls.execute_soa_method(
            method_name='createFullTextSavedSearch2',
            library='Internal-Search',
            service_date='2022_12',
            service_name='FullTextSearch',
            params={'inputs': inputs},
            response_cls=Awp0FullTextSavedSearchResponse,
        )
