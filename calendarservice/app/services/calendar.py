from app.repositories.calendar import CalendarRepository


class CalendarService:
    def __init__(self, calendar_repository: CalendarRepository, app_state):
        self.calendar_repository = calendar_repository
        self.app_state = app_state


    async def create_event(self, create_event_schema):
        await self.app_state.broker_producer_service.publish_message_to_team(str(create_event_schema.team_id) + " " + str(create_event_schema.title) + " " + create_event_schema.discription)

