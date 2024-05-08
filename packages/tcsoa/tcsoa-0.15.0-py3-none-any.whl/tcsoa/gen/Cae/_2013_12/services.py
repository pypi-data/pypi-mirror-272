from __future__ import annotations

from tcsoa.gen.Cae._2013_12.SimulationProcessManagement import InputObjectsStructure2
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SimulationProcessManagementService(TcService):

    @classmethod
    def launchSimulationTool2(cls, inputObjects: List[InputObjectsStructure2], toolName: str, launchType: str, itemCreationOption: str, datasetCreationOption: str, plmxmlExportFileName: str, workingDirectory: str, runtimeArguments: List[str]) -> ServiceData:
        """
        This operation launches the simulation tool as per the pre-defined configuration. The configuration contains
        details about the tool launch type, export and import rules for the files, notification, and cleanup. The
        inputs to the operation is an array of InputObjectStructure2, each containing one or more business objects,
        name of the tool to be launched and the launch type. The launch type could be LOCAL or REMOTE. Based on the
        input values of parameters itemCreationOption and datasetCreationOption, ItemRevision and Dataset objects are
        created or modified.
        
        It is a pre-requisite that the Simulation Administrator or user with DBA privileges must configure the
        simulation tool and store it in XML format as a named reference with the Dataset name specified in the
        preference CAE_simulation_tool_config_dsname.
        
        To use this operation, the user should have either a simulation_author or rtt_author license. 
        
        
        Use cases:
        Use Case 1: Launch Simulation Tool with As Needed Item Creation Option
        When this operation is executed with itemCreationOption "As Needed", no new Teamcenter Item will be created if
        there exists one as per the process output configuration. If found none, new Item will be created as per the
        process output configuration.
        
        Use Case 2: Launch Simulation Tool with Always Item Creation Option
        When this operation is executed with itemCreationOption "Always", new Teamcenter Item objects will be created
        as per the process output configuration.
        
        Use Case 3: Launch Simulation Tool with Never Item Creation Option
        When this operation is executed with itemCreationOption "Never" and if no existing Item is found as per the
        process output configuration, no new Teamcenter Item objects will be created.
        
        Use Case 4: Launch Simulation Tool with As Needed Dataset Creation Option
        When this operation is executed with datasetCreationOption "As Needed", no new Teamcenter Dataset will be
        created if there exists one as per the process output configuration. If found none, new Dataset will be created
        as per the process output configuration.
        
        Use Case 5: Launch Simulation Tool with Always Dataset Creation Option
        When this operation is executed with datasetCreationOption "Always", new Teamcenter Dataset objects will be
        created as per the process output configuration.
        
        Use Case 6: Launch Simulation Tool with Never Dataset Creation Option
        When this operation is executed with datasetCreationOption "Never" and if no existing Dataset is found as per
        the process output configuration, no new Teamcenter Dataset objects will be created.
        """
        return cls.execute_soa_method(
            method_name='launchSimulationTool2',
            library='Cae',
            service_date='2013_12',
            service_name='SimulationProcessManagement',
            params={'inputObjects': inputObjects, 'toolName': toolName, 'launchType': launchType, 'itemCreationOption': itemCreationOption, 'datasetCreationOption': datasetCreationOption, 'plmxmlExportFileName': plmxmlExportFileName, 'workingDirectory': workingDirectory, 'runtimeArguments': runtimeArguments},
            response_cls=ServiceData,
        )
