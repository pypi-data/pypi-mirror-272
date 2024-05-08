from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2021_06.ResourceManagement import GuidedComponentSearchForOccResponse
from tcsoa.base import TcService


class ResourceManagementService(TcService):

    @classmethod
    def guidedComponentSearchForOccurrence(cls, occUID: str) -> GuidedComponentSearchForOccResponse:
        """
        This operation obtains information about matching classification objects (ICO objects) for a given Connection
        Point (CP). A Guided Component Search (GCS) is used to get this information. The matching data is returned in
        the form of list of UIDs (Unique Identifier) for classification objects, list of classes in which these ICO
        objects are classified, number of ICO objects associated with each class and list of CP UIDs. 
        The ID (Identifier) of the common main class of matching ICO objects is also returned.
        """
        return cls.execute_soa_method(
            method_name='guidedComponentSearchForOccurrence',
            library='Internal-Manufacturing',
            service_date='2021_06',
            service_name='ResourceManagement',
            params={'occUID': occUID},
            response_cls=GuidedComponentSearchForOccResponse,
        )
