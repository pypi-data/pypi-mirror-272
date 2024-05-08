from __future__ import annotations

from tcsoa.gen.Internal.Security._2022_06.AwProjectLevelSecurity import ProjectTeamResponse2, ProjectTeamInput2
from tcsoa.base import TcService


class AwProjectLevelSecurityService(TcService):

    @classmethod
    def getProjectTeam2(cls, input: ProjectTeamInput2) -> ProjectTeamResponse2:
        """
        This operation returns the paginated output representing ProjectTeam for the given TC_Project object based on
        the input filter, sort and node information.
        
        Use cases:
        The use cases below are examples of how the TC_Project and filter information can be used to return specific
        ProjectTeam information. For any of the use cases, sort and pagenination can be added to input to determine the
        order and quantity of information returned from the service.
        
        Return first level ProjectTeam: 
        Provide only the TC_Project object with no filter info to return the first level project team information.
        These are the project nodes that have explicitly been added to the ProjectTeam, for example Engineering group,
        or a specific Role within a Group such as Designer role.
        
        Return specific user, group and members within the ProjectTeam: 
        Provide the TC_Project and filter information specifying a search string, if applicable, and the type(s) of
        member. The returned members may have been added explicitly to the Project Team or they may be included due to
        their Group or Role membership.
        
        Return User members with one or more statuses within the TC_Project: 
        Provide the TC_Project and filter information including the status(es) of interest. The returned user members
        may have been added explicitly to the ProjectTeam or they may be included due to their Group or Role membership.
        
        Return the members associated with a specific ProjectTeam node: 
        Provide the TC_Project, Group or Role , and filter . The returned User members may have been added explicitly
        to the ProjectTeam or they may be included due to their Group or Role membership.
        """
        return cls.execute_soa_method(
            method_name='getProjectTeam2',
            library='Internal-Security',
            service_date='2022_06',
            service_name='AwProjectLevelSecurity',
            params={'input': input},
            response_cls=ProjectTeamResponse2,
        )
