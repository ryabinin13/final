from app.repositories.team import TeamRepository
from app.repositories.team_memebership import TeamMembershipRepository
from app.schemas.team import TeamCreateSchema
from app.models.team_memberships import Status
from app.schemas.user import UserChangeStatusSchema
from exceptions import UserAlreadyHasTeamException


class TeamService:

    def __init__(self, team_repository: TeamRepository, team_memberships_repository: TeamMembershipRepository, app_state):
        self.team_repository = team_repository
        self.team_memberships_repository = team_memberships_repository
        self.app_state = app_state


    async def team_create(self, team_create_schema: TeamCreateSchema, user_id):
        team_membership = await self.team_memberships_repository.get_user_id(user_id=user_id)
        if team_membership:
            raise UserAlreadyHasTeamException
        
        team_dict = team_create_schema.model_dump()
        team_id = await self.team_repository.create(team_dict)
        team_membership_dict = {"team_id": team_id, "user_id": user_id, "status": Status.ADMIN}
        await self.team_memberships_repository.create(team_membership_dict)

    async def add_user(self, team_id, email, current_user_id):
        team_member_current = await self.team_memberships_repository.get_user_id(current_user_id)
        if team_member_current.status == Status.ADMIN:
            await self.app_state.broker_producer_service.publish_message_to_user(str(team_id) +  " " + str(email))


    async def change_status(self, team_id, user_id, user_change_status_schema: UserChangeStatusSchema):
        team_membership = await self.team_memberships_repository.get_user_id(user_id=user_id)
        if team_membership.team_id != team_id:
            raise Exception
        
        return await self.team_memberships_repository.update(team_membership=team_membership, data=user_change_status_schema.model_dump())


    async def delete_user(self, team_id, user_id):
        team_membership = await self.team_memberships_repository.get_user_id(user_id=user_id)
        if team_membership.team_id != team_id:
            raise Exception

        return await self.team_memberships_repository.delete(team_membership.id)

        
        
