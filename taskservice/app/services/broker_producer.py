import aio_pika


class BrokerProducerService:

    def __init__(self, channel):
        self.channel = channel



    async def publish_add_user_in_task(self, task_id, email):
        message_body = str(task_id) + " " + email
        message = aio_pika.Message(body=message_body.encode())
        await self.channel.default_exchange.publish(message, routing_key="user_email_from_task")


    async def publish_mark_to_mark(self, message):
        message_body = message
        message = aio_pika.Message(body=message_body.encode())
        await self.channel.default_exchange.publish(message, routing_key="mark_from_task")