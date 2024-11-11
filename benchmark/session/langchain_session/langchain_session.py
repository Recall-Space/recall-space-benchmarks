"""
This class manages a session involving two participants, who may be agents. 
An agent must implement the invoke method and utilize the Langchain schema 
for message handling.

The db_handler is responsible for data persistence. In the context of Recall Space, 
the db_handler is implemented using MongoDB. It should support the following methods:
    - get_session
    - insert_session
    - delete_session
"""

import datetime
import inspect
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from benchmark.session import Message
from benchmark.session import Session
logger = logging.getLogger()


class LangChainSession(Session):
    """
    Manages a chat session between two participants, one of whom is a 
    Langchain object that implements the 'invoke' method.
    """

    def __init__(self,
                user_name: str, agent_name: str, agent: Any,
                session_name: str, db_handler: Any=None):
        """
        Initializes the session with two participants and a MongoDB handler. 
        Generates a unique session_name ID.

        Args:
            user_name (str): The name of the user participant.
            agent_name (str): The name of the agent participant.
            agent (Any): The agent object that implements the invoke method.
                The response of the agent should either be AIMessage or
                a dictionary with key "output".
            db_handler (Any): The MongoDB handler for database operations.
            session_name (str): The name of the session.
        """
        self.user_name = user_name
        self.agent_name = agent_name
        self.agent = agent
        self.db_handler = db_handler
        self.session_name = session_name
        self.list_messages = []
        self.list_messages_with_schema = []
        if self.db_handler is not None:
            # To resume existing session.
            self.list_messages = self.get_session_messages()
            self.list_messages_with_schema = [
                self.to_langchain_schema(each) for each in self.list_messages
            ]
        super().__init__(user_name=self.user_name,
                         agent_name=self.agent_name,
                         agent=self.agent,
                         session_name=self.session_name,
                         db_handler=self.db_handler)
        

    def send_message(self, sender: str, content: str, include_chat_history= True, **keywords) -> Optional[Dict[str, Any]]:
        """
        Sends a message from the specified sender and gets a response from 
        the agent.

        Args:
            sender (str): The name of the sender (user or agent).
            content (str): The content of the message.

        Returns:
            Optional[Dict[str, Any]]: The agent's response message if 
            available; otherwise, None.
        """
        agent_message = None
        sender_message = Message(sender, content)
        sender_message_dict = sender_message.to_dict()
        self.list_messages.append(sender_message_dict)
        if ("chat_history" in inspect.signature(self.agent.invoke).parameters):
            keywords["chat_history"] = []
            if include_chat_history is True:
                keywords["chat_history"]= self.list_messages_with_schema

        if sender == self.user_name:
            logger.info(sender_message.to_str())
            agent_raw_response = self.agent.invoke(
                input=sender_message.to_str(), **keywords
            )
            if isinstance(agent_raw_response, AIMessage):
                agent_response = agent_raw_response.content
            else:
                agent_response = agent_raw_response["output"]
                
            agent_message = Message(self.agent_name, agent_response)

        # Append the original message with schema
        self.list_messages_with_schema.append(
            self.to_langchain_schema(sender_message_dict)
        )

        if agent_message is not None:
            # Append the agent message with schema
            agent_message_dict = agent_message.to_dict(is_agent=True)
            self.list_messages.append(agent_message_dict)
            self.list_messages_with_schema.append(
                self.to_langchain_schema(agent_message_dict)
            )
        return agent_message.__dict__ if agent_message else None

    def save_session(self) -> str:
        """
        Saves the current session to the database.

        Returns:
            str: A success message.
        """
        response = "success"
        if self.db_handler is not None:
            session_data = {
                "user": self.user_name,
                "session": self.session_name,
                "participant_2": self.agent_name,
                "timestamp": datetime.now(timezone.utc),
                "list_messages": self.list_messages,
            }
            self.db_handler.insert_session(session_data)
        else:
            response = "Failed. db_handler is not configured."
        return response

    def delete_session(self) -> str:
        """
        Deletes the current session from the database.

        Returns:
            str: A success message.
        """
        response = "success"
        if self.db_handler is not None:
            self.db_handler.delete_session(self.session_name)
        else:
            response = "Failed. db_handler is not configured."
        return response

    def get_session_messages(self, total_messages: int = -1) -> List[Dict[str, Any]]:
        """
        Retrieves session messages from the database.

        Args:
            total_messages (int): The total number of messages to retrieve. 
            Default is -1 (all).

        Returns:
            List[Dict[str, Any]]: A list of message dictionaries.
        """
        if self.db_handler is not None:
            list_messages = self.db_handler.get_session(
                user=self.user_name, session=self.session_name
            )
            if total_messages != -1:
                return list_messages[-total_messages:]
        else:
            list_messages = self.list_messages
        return list_messages or []

    def to_langchain_schema(self, message_dict: Dict[str, Any]) -> Optional[Any]:
        """
        Converts a message dictionary to a Langchain schema message.

        Args:
            message_dict (Dict[str, Any]): The message dictionary to convert.

        Returns:
            Optional[Any]: A Langchain message object (AIMessage, HumanMessage, 
            or SystemMessage) or None.
        """
        message_with_schema = None
        if message_dict.get("role") == "assistant":
            message_with_schema = AIMessage(content=message_dict["content"])

        if message_dict.get("role") == "user":
            message_with_schema = HumanMessage(content=message_dict["content"])

        if message_dict.get("role") == "system":
            message_with_schema = SystemMessage(content=message_dict["content"])
        return message_with_schema

    def reset(self):
        self.list_messages = []
        self.list_messages_with_schema = []
        self.delete_session()
            