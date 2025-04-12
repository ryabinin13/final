import aio_pika


class BrokerProducerService:

    def __init__(self, channel):
        self.channel = channel
        
    async def publish_user_data_to_team(self, message):
        message = aio_pika.Message(body=message.encode())
        await self.channel.default_exchange.publish(message, routing_key="user_to_team")

    async def publish_user_data_to_task(self, message):
        message = aio_pika.Message(body=message.encode())
        await self.channel.default_exchange.publish(message, routing_key="user_to_task")

    async def publish_user_data_to_meeting(self, message):
        message = aio_pika.Message(body=message.encode())
        await self.channel.default_exchange.publish(message, routing_key="user_to_meeting")

    async def publish_user_data_to_org(self, message):
        message = aio_pika.Message(body=message.encode())
        await self.channel.default_exchange.publish(message, routing_key="user_to_organization")