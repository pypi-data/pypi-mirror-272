from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, RuntimeBusinessObject
from tcsoa.gen.StructureManagement._2021_06.StructureSearch import ExpandOptions
from tcsoa.gen.StructureManagement._2021_12.StructureSearch import ExpandResponse2, SettingsMap2
from typing import List
from tcsoa.base import TcService


class StructureSearchService(TcService):

    @classmethod
    def nextExpandBOMLines2(cls, pageSize: int, expandOptions: ExpandOptions, expandCursor: BusinessObject) -> ExpandResponse2:
        """
        This operation gets the next set of objects from a previously executed expansion result. The results returned
        are based on the pageSize specified in the input. This API returns the same response structure as that of
        startExpandBOMLines.
        
        Use cases:
        This API is used in conjunction with startExpandBOMLines2 operation. startExpandBOMLines2 operation is a
        prerequisite for invoking nextExpandBOMLines2. The expand cursor returned by the startExpandBOMLines2 is used
        to call nextExpandBOMLines2 operation. This operation could be called repeatedly by the caller, until all the
        expansion results are returned.
        """
        return cls.execute_soa_method(
            method_name='nextExpandBOMLines2',
            library='StructureManagement',
            service_date='2021_12',
            service_name='StructureSearch',
            params={'pageSize': pageSize, 'expandOptions': expandOptions, 'expandCursor': expandCursor},
            response_cls=ExpandResponse2,
        )

    @classmethod
    def startExpandBOMLines2(cls, bomLines: List[RuntimeBusinessObject], expandSettings: SettingsMap2, pageSize: int, expandOptions: ExpandOptions) -> ExpandResponse2:
        """
        This operation initiates a sequence of operations to expand BOMLine objects based on  filter information on
        BOMWindow and returns a list of BOMLine objects. Filter information could be a complex expression set that
        combines multiple simpler Expand terms in a logical sequence. 
        Expansion is always executed within the scope of a BOMWindow under one or more BOMLine objects. 
        The results of an expansion are returned one set at a time based on the pageSize. The ExpandResponse also
        contains a Cursor object that the caller uses to expand the next set of results by invoking the
        StructureManagement::StructureSearch::nextExpandBOMLines call.
        
        Use cases:
        1.    Expand all lines of a structure page by page by setting levels to 0 (expand all levels) and pageSize is
        100. The operation will return the result breadth first.
        2.    Expand all lines of a structure by setting levels to 0 (expand all levels) and pageSize is 0.
        3.    Expand all child lines of a list of lines by setting level to 1 and pageSize is 100.
        4.    Expand all child lines from the structure based on the given pageSize.
        The returned childlines may or may not contain specific datasets. For example, if dataset information is
        specified - dataset relation is IMAN_reference and dataset type is Text then the response will contain the
        specified datasets (if there are any). 
        5.    Expand the child lines from the structure given the page size. The dataset information contains the
        minimum number of dataset objects to be returned. For example, dataset relation is given as IMAN_reference,
        dataset type is Text, expandRelatedObjects is 1 and min datasets to be returned is set to 10. In this case, the
        response will contain only 10 specified datasets.
        6.     Expand the child lines from the structure given the page size. When dataset information specify the
        dataset relation and dataset type. In this case, the response will contain 0 datasets.
        7.    Expand the child lines defined by the Expand criteria (Expand criteria given in the BOM window) given the
        page size.
        """
        return cls.execute_soa_method(
            method_name='startExpandBOMLines2',
            library='StructureManagement',
            service_date='2021_12',
            service_name='StructureSearch',
            params={'bomLines': bomLines, 'expandSettings': expandSettings, 'pageSize': pageSize, 'expandOptions': expandOptions},
            response_cls=ExpandResponse2,
        )
