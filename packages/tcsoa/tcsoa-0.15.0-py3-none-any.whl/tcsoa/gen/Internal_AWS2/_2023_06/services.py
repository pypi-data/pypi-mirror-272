from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2016_03.Finder import ColumnConfigInput
from tcsoa.gen.Internal.AWS2._2023_06.UiConfig import GetOrResetUIColumnConfigResponse, StringMap2, ColumnDefInfo, SaveColumnConfigData
from tcsoa.gen.Internal.AWS2._2016_03.UiConfig import GetOrResetUIColumnConfigInput
from tcsoa.gen.Internal.AWS2._2017_12.DataManagement import GetTableViewModelPropertiesIn
from tcsoa.gen.Internal.AWS2._2023_06.DataManagement import GetTableViewModelPropsResp
from typing import List
from tcsoa.gen.Internal.AWS2._2020_05.UiConfig import NamedColumnConfigInput
from tcsoa.gen.Internal.AWS2._2023_06.Finder import SearchResponse, SaveColumnConfigData
from tcsoa.gen.Internal.AWS2._2019_06.Finder import SearchInput3
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class UiConfigService(TcService):

    @classmethod
    def getOrResetUIColumnConfigs4(cls, getOrResetUiConfigsIn: List[GetOrResetUIColumnConfigInput]) -> GetOrResetUIColumnConfigResponse:
        """
        This operation returns information used by the client to render the table view in Active Workspace. The
        information returned includes column configuration information of the table view. 
        If the resetColumnConfig flag is "True", this operation deletes the column configuration of the input scope and
        then queries the new effective UI column configuration for the login user. This operation clears the login user
        column configurations.
        
        Use cases:
        Request UI Configuration(s) based on the current login user
        Client requests the column information for one or more client scopes using this operation and scope as login
        user.
        
        Request UI Configuration(s) based on a specific Teamcenter scope
        Client requests the column information for one or more client scopes using this operation and scope as Role,
        Site or Group.
        
        Request to reset UI Column Configuration(s) based on the current login user
        If a client needs to reset the column information for login user scope, they can use this operation. The new
        effective UI column configuration will be retrieved for the login user.
        """
        return cls.execute_soa_method(
            method_name='getOrResetUIColumnConfigs4',
            library='Internal-AWS2',
            service_date='2023_06',
            service_name='UiConfig',
            params={'getOrResetUiConfigsIn': getOrResetUiConfigsIn},
            response_cls=GetOrResetUIColumnConfigResponse,
        )

    @classmethod
    def saveNamedColumnConfig2(cls, uid: str, columns: List[ColumnDefInfo], namedColumnConfigCriteria: StringMap2) -> ServiceData:
        """
        This service operation saves the named column configuration information to the Teamcenter database. Active
        Workspace client may use this information to populate columns of tables in various sublocations as the user
        navigates.
        
        Use cases:
        Save Named Column Configuration:
        A user wants to modify an existing named column configuration for a given table by adding or removing columns.
        The modified named column configuration will become the active column configuration for that user.
        """
        return cls.execute_soa_method(
            method_name='saveNamedColumnConfig2',
            library='Internal-AWS2',
            service_date='2023_06',
            service_name='UiConfig',
            params={'uid': uid, 'columns': columns, 'namedColumnConfigCriteria': namedColumnConfigCriteria},
            response_cls=ServiceData,
        )

    @classmethod
    def saveUIColumnConfigs2(cls, columnConfigurations: List[SaveColumnConfigData]) -> ServiceData:
        """
        This service operation saves column configuration information to the Teamcenter database. A Teamcenter client
        may use this information to render the user interface as the user navigates the Teamcenter client. Default
        column configurations are initially created by a utility during install. This operation will modify the default
        column configuration for the site, group, role or a specific user.
        
        Use cases:
        User level column configuration:
        A User wants to change the default column configuration for a Client Scope when he is logged into the client.
        The saved configuration will override the default configuration for the user's applicable role, group or site.
        """
        return cls.execute_soa_method(
            method_name='saveUIColumnConfigs2',
            library='Internal-AWS2',
            service_date='2023_06',
            service_name='UiConfig',
            params={'columnConfigurations': columnConfigurations},
            response_cls=ServiceData,
        )

    @classmethod
    def createNamedColumnConfig2(cls, namedColumnConfigInput: NamedColumnConfigInput, columns: List[ColumnDefInfo], namedColumnConfigCriteria: StringMap2) -> ServiceData:
        """
        This service operation creates the named column configuration information in the Teamcenter database. Active
        Workspace client may use this information to populate columns of tables in various sublocations as the user
        navigates. Default named column configurations can be initially created by a utility during install.
        
        Use cases:
        Create Named Column Configuration:
        A user wants to create a named column configuration for a given table when he/she is logged into the client.
        The named column configuration will become the active column configuration for that user on the given table.
        """
        return cls.execute_soa_method(
            method_name='createNamedColumnConfig2',
            library='Internal-AWS2',
            service_date='2023_06',
            service_name='UiConfig',
            params={'namedColumnConfigInput': namedColumnConfigInput, 'columns': columns, 'namedColumnConfigCriteria': namedColumnConfigCriteria},
            response_cls=ServiceData,
        )


class DataManagementService(TcService):

    @classmethod
    def getTableViewModelProperties2(cls, input: GetTableViewModelPropertiesIn) -> GetTableViewModelPropsResp:
        """
        The operation returns the column configuration and Table View Model properties for the input object UIDs.
        
        Use cases:
        Use Case 1: When the user opens a structure in the content tab and switch to table mode. The column
        configuration and related properties that need to be returned.
        
        Use Case 2: When a structure is opened in the tree mode. The column configuration and related properties that
        need to be returned.
        """
        return cls.execute_soa_method(
            method_name='getTableViewModelProperties2',
            library='Internal-AWS2',
            service_date='2023_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GetTableViewModelPropsResp,
        )


class FinderService(TcService):

    @classmethod
    def performSearchViewModel5(cls, searchInput: SearchInput3, columnConfigInput: ColumnConfigInput, saveColumnConfigData: SaveColumnConfigData, inflateProperties: bool, noServiceData: bool) -> SearchResponse:
        """
        This operation routes a search request to a specific provider specified as providerName in the searchInput
        structures.
        
        The framework allows a custom solution to be able to provide a new specific provider to collect data, perform
        sorting and filtering. The provider can be a User Inbox retriever or Full Text searcher, for example. The new
        data provider can be encapsulated via a new runtime business object from Fnd0BaseProvider class. The
        implementation is done using its fnd0performSearch operation.
        
        RuntimeBusinessObject 
        ---- Fnd0BaseProvider (foundation template) 
        -------- Fnd0GetChildrenProvider(foundation template) 
        -------- Awp0FullTextSearchProvider (aws template)
        -------- Awp0TaskSearchProvider (aws template)
        -------- etc.
        
        This operation provides a common interface to send the request to and receive the response from a new data
        provider. Ultimately it allows common framework in UI to support filter, pagination, and sorting. 
        
        This operation allows the caller to send the search input, filter values, and sorting data. These input values
        are then to be passed to the fnd0performSearch operation on the server to collect, sort, and filter its
        results. 
        
        The first two input parameters are important. The first input is the provider name. This is a string to
        represent the type name of RuntimeBusinessObject which this request should be routed to. If the template that
        contains the class is not installed, a partial error 217016 is returned. The second input is the search input
        map. The key is different per each provider. For example, for Full Text searcher, the input key would be a
        searchString. For User Inbox retriever, the input key would be an Inbox Type. The fnd0performSearch
        implementation for each provider takes into account the key name as it is used to store the values in
        OperationInput object. 
        
        The internal property name is passed as part of search input to allow grouping of business objects. The
        grouping allows for added functionality such as color coding, etc. If no internal property name is passed,
        default value is assumed as "object_type" to group the business objects. 
        
        If a new list of column config data is passed in to be saved, it will get saved in the database for the login
        user scope. This will be done prior to performing the search.
        
        The column configuration input has the criteria needed to query for the columns configured for the provided
        client and client scope URI. The final list of columns are identified based on the types returned back in the
        search results and the operation type (Union / Intersection / Configured ) configured for the client scope URI.
        Finally the determined column attributes and the attributes to be inflated passed in as part of search input
        criteria are combined. This combined list of attributes along with the business objects found during search are
        added to the Service data.
        
        Use cases:
        Use Case 1: User clicks on Inbox tile
        A search request will be made by passing in the needed criteria. In this case the provider name is
        "Awp0InboxProvider". It queries for the data and finds the effective columns for the client scope URI passed in
        through column config input. The results are finally shown in the view type selected in client. If table view
        is selected the returned effective columns will be shown.
        
        Use Case 2: User performs search by entering a keyword in global search input box. 
        A search request will be made by passing in the needed criteria that includes the keyword user has typed in. In
        this case the provider name is "Awp0FullTextSearchProvider". It queries for the data and finds the effective
        columns for the client scope URI passed in through column config input. The results are finally shown in the
        view type selected in client. If table view is selected the returned effective columns will be shown. 
        
        Use Case 3: User tries to save new column configurations after performing search. 
        The new list of column configurations will be saved for the login user scope. Later the search request will be
        made by passing in the needed criteria that includes the keyword user had typed in. In this case the provider
        name is "Awp0FullTextSearchProvider". It queries for the data and finds the effective columns for the client
        scope URI passed in through column config input. The results are finally shown in the view type selected in
        client. If table view is selected the returned effective columns will be shown.
        """
        return cls.execute_soa_method(
            method_name='performSearchViewModel5',
            library='Internal-AWS2',
            service_date='2023_06',
            service_name='Finder',
            params={'searchInput': searchInput, 'columnConfigInput': columnConfigInput, 'saveColumnConfigData': saveColumnConfigData, 'inflateProperties': inflateProperties, 'noServiceData': noServiceData},
            response_cls=SearchResponse,
        )
