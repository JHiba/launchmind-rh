import uuid
from datetime import datetime

message_bus = {
    "ceo": [],
    "product": [],
    "engineer": [] 
}

def create_message(from_agent, to_agent, message_type, payload, parent_id=None):
    return {
        "message_id": str(uuid.uuid4()),
        "from_agent": from_agent,
        "to_agent": to_agent,
        "message_type": message_type,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat(),
        "parent_message_id": parent_id
    }

def send_message(message):
    message_bus[message["to_agent"]].append(message)

def get_messages(agent_name):
    msgs = message_bus[agent_name][:]
    message_bus[agent_name] = []
    return msgs