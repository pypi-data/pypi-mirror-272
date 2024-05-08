from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Requirementsmanagement._2022_12.RequirementsManagement import SetContentInput2
from tcsoa.base import TcService


class RequirementsManagementService(TcService):

    @classmethod
    def setRichContent2(cls, inputs: List[SetContentInput2]) -> ServiceData:
        """
        This operation sets text, images, and embedded contents such as Microsoft Word files, Microsoft Excel Files or
        Microsoft PowerPoint Files on a FullText object. The to-be-updated FullText object or any BusinessObject with a
        FullText, attached via an IMAN_Specification relation is supported. If FullText object is not attached to the
        input object with IMAN_Specification relation, a new FullText object will be created.
        
        Use cases:
        The user sets contents of a requirement by using setRichContent2 SOA. The requirement contents can be in plain
        text, HTML or MSWord format containing images and embedded contents such as Microsoft Word files, Microsoft
        Excel Files or Microsoft PowerPoint Files.
        """
        return cls.execute_soa_method(
            method_name='setRichContent2',
            library='Requirementsmanagement',
            service_date='2022_12',
            service_name='RequirementsManagement',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )
