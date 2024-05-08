from __future__ import annotations

from tcsoa.gen.Internal.OrgMgmt._2023_06.OrganizationManagement import GetFilteredOrgTreeResponse, GetFilteredOrgTreeInput
from tcsoa.base import TcService


class OrganizationManagementService(TcService):

    @classmethod
    def getFilteredOrganizationTree(cls, input: GetFilteredOrgTreeInput) -> GetFilteredOrgTreeResponse:
        """
        This operation gets the filtered list of organization objects Group, Role, User, GroupMember in hierachical
        manner and updated filter category values for a given filter criteria.
        
        Use cases:
        Use Case 1: User performs search by entering a keyword in content search input box - 'dba'
        
        A search request will be made by passing the searchCriteria  with 'searchString':'value'. Value would be the
        keyword user has typed in.The results will return all the Group,Role,User node which contains the string 'dba'
        in it and it is displayed in tree mode.
        The result also contains the filter category values based on the search results.
        
        Use Case 2: User performs search by selecting filter value from filter panel : Group = dba
        
        A search request will be made by passing filter criteria in searchFilterMap. The results will return
        &lsquo;dba&rsquo; Group node and it is displayed in tree mode.
        The result also contains the filter category values based on the search results.
        """
        return cls.execute_soa_method(
            method_name='getFilteredOrganizationTree',
            library='Internal-OrgMgmt',
            service_date='2023_06',
            service_name='OrganizationManagement',
            params={'input': input},
            response_cls=GetFilteredOrgTreeResponse,
        )
