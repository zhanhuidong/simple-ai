from components.memory.memory import BaseMemory, MessageInfo, MessageListParameter
from utils import datetime_util, identifier_util

if __name__ == "__main__":
    message_1 = MessageInfo(user_id="user_1", system_message="system", user_message="user", assistant_message="assistant")
    message_2 = MessageInfo(user_id="user_1", system_message="system", user_message="user", assistant_message="assistant")
    message_3 = MessageInfo(user_id="user_1", system_message="system", user_message="user", assistant_message="assistant")
    message_4 = MessageInfo(user_id="user_2", system_message="system", user_message="user", assistant_message="assistant")

    client = BaseMemory()

    client.save_message(message_1)
    client.save_message(message_2)
    created = datetime_util.get_current_timestamp()
    client.save_message(message_3)
    client.save_message(message_4)

    messages = client.list_message(MessageListParameter(api_key="user_1", created=created, limit=2))

    for message in messages:
        print(message.model_dump())