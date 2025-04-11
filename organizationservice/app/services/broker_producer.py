import aio_pika


class BrokerProducerService:

    def __init__(self, channel):
        self.channel = channel


    async def publish_team_id(self, message):
        message = aio_pika.Message(body=message.encode())
        await self.channel.default_exchange.publish(message, routing_key="team_from_organization")