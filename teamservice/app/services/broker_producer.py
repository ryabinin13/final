import aio_pika


class BrokerProducerService:

    def __init__(self, channel):
        self.channel = channel


    async def publish_message_to_user(self, message):
        message = aio_pika.Message(body=message.encode())
        await self.channel.default_exchange.publish(message, routing_key="user_email_from_team")


    async def publish_message_to_org(self, message):
        message = aio_pika.Message(body=message.encode())
        await self.channel.default_exchange.publish(message, routing_key="team_to_organization")

    async def publish_message_to_calendar(self, message):
        message = aio_pika.Message(body=message.encode())
        await self.channel.default_exchange.publish(message, routing_key="team_to_calendar")