from asyncio import Event


class CalendarRepository:
    def __init__(self, session):
        self.session = session

    async def create(self, data: dict):
        async with self.session as db:
            event = Event(**data)
            db.add(event)

            await db.commit() 

            return event.id