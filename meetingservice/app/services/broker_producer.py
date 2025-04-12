import aio_pika


class BrokerProducerService:
    def __init__(self, channel):
        self.channel = channel


    async def publish_message_to_user(self, message):
        message_body = str(message)
        message = aio_pika.Message(body=message_body.encode())
        await self.channel.default_exchange.publish(message, routing_key="user_email_from_meeting")