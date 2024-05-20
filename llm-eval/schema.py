import json
from typing import List, Literal
from pydantic import BaseModel
import streamlit as st


class ModelConfig(BaseModel):
    model: str = "snowflake/snowflake-arctic-instruct"
    temperature: float = 0.7
    top_p: float = 1.0
    max_new_tokens: int = 1024


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class Conversation:
    messages: List[Message] = []
    model_config: ModelConfig = None

    def __init__(self):
        self.reset_messages()
        self.model_config = ModelConfig()

    def add_message(self, message: Message, container=None, render=True):
        self.messages.append(message)
        if render:
            self.render_message(message, container)

    def reset_messages(self):
        self.messages = []

    def render_all(self, container=None):
        for message in self.messages:
            self.render_message(message, container)

    def render_message(self, message: Message, container=None):
        if container is not None:
            container.chat_message(message.role).write(message.content)
        else:
            st.chat_message(message.role).write(message.content)

    def to_json(self):
        d = {
            "messages": [dict(m) for m in self.messages],
            "model_config": dict(self.model_config),
        }
        return json.dumps(d)

    @classmethod
    def from_json(cls, raw_json: str):
        d = json.loads(raw_json, strict=False)
        c = Conversation()
        c.model_config = ModelConfig.parse_obj(d["model_config"])
        c.messages = [Message.parse_obj(m) for m in d["messages"]]
        return c