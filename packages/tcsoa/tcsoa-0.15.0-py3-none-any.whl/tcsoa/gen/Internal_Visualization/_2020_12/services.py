from __future__ import annotations

from tcsoa.gen.Internal.Visualization._2020_12.StructureManagement import ExpandPSFromOccurrenceListResponse, AdditionalInfo
from tcsoa.gen.Internal.Visualization._2011_12.StructureManagement import ExpandPSFromOccurrenceListPref, ExpandPSFromOccurrenceListInfo
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def expandPSFromOccurrenceList2(cls, info: List[ExpandPSFromOccurrenceListInfo], pref: ExpandPSFromOccurrenceListPref, additionalInfo: AdditionalInfo) -> ExpandPSFromOccurrenceListResponse:
        """
        This operation returns BOMLine objects for the occurrences recorded in the occurrence list of the input
        occurrence object. Optionally, it can also return the objects of given type and relation that are attached to
        the objects that the BOMLine objects represent (object of BOMLine). 
        
        The operation can expand datasets and other objects related to parent and child BOMLine objects. Expansion of
        the related objects can be controlled by specifying a filter. The filter criteria supported are: relation name,
        related object type, and named references. 
        
        This operation allows for expansion to reference object associated to a named reference. Typically this is a
        file and in that case a FMS ticket will be returned to provide access to this file. Where a named reference
        points to a file, this operation allows caller to specify from a defined set of handler options, which specific
        handler should be used in choosing files to return. This is specified through the input parameter
        'NamedRefHandler' (included in the info object). The service would also return the side car jt referenced via
        the pmi0blpmi_bl_jt_tags property on the BOMLine. This information is returned only if the input to the
        'NamedRefHandler' is mentioned as PreferredJt and if the pmi template is deployed in the database.
        
        Use cases:
        When the user wants to expand a specific list of occurrences into an existing BOMWindow that contains the
        parent BOMLine of the occurrences.
        This service is used to support the following primary use cases.
        
        Pruned launch of selected lines to visualization
        - User opens structure in Structure Manager/Multi Structure Manager/Manufacturing Process Planner, configures
        it, selects some lines, and sends those lines to Lifecycle Viewer or integrated standalone visualization.
        - The launching client (system) calls createVisSCsFromBOMs to record the selected lines and BOM configuration
        information.
        - The visualization client receives the request to open the selected lines as an object reference to a
        VisStructureContext object.
        - The visualization client calls the createBOMsFromRecipes operation and passes the VisStructureContext object
        reference.
        - The system creates a BOMWindow and configures it properly (to match launching configuration).
        - The client pulls the occurrence_list from the VisStructureContext object.
        - The client issues an expandPSFromOccurrenceList call to load the occurrences.
        - The client(system) loads the selected occurrences in the visualization client, the structure is pruned to
        contain only those occurrences sent.
        
        
        
        Product View launch to visualization
        - User selects a Product View in the Product View Gallery of embedded visualization inside Structure
        Manager/Multi Structure Manager/Manufacturing Process Planner, or in My Teamcenter and sends it to integrated
        standalone TcVis or Lifecycle Viewer.
        - The visualization client receives the request to open the selected product View.
        - The visualization client interrogates the Product View data model, fetches the files from the dataset, and
        gets a list of visible lines for the Product View.
        - The client issues an expandPSFromOccurrenceList call for all visible lines referenced by the Product View.
        - The client loads the visible lines then applies the product view.
        
        
        
        Use Case Dependencies: 
        The expandPSFormOccurrenceList operation is called for existing parent BOMLine objects within a BOMWindow (i.e.
        the parent BOMLine objects must already exist within a created BOMWindow) and also requires a previously
        captured/defined list of occurrences represented as a list of UID strings.
        
        The following services are used in conjunction with expandPSFromOccurrenceList to complete the use cases above.
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. createVisSCsFromBOMs
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. createBOMsFromRecipes
        Teamcenter::Soa::Internal::Visualization::_2008_06::StructureManagement. areRecipesMergible
        Teamcenter::Soa::Internal::Visualization::_2010_09::DataManagement. getSnapshot3DInfo
        """
        return cls.execute_soa_method(
            method_name='expandPSFromOccurrenceList2',
            library='Internal-Visualization',
            service_date='2020_12',
            service_name='StructureManagement',
            params={'info': info, 'pref': pref, 'additionalInfo': additionalInfo},
            response_cls=ExpandPSFromOccurrenceListResponse,
        )
