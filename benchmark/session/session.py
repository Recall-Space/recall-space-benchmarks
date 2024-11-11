"""
Abstract class to create sessions between user and agent.
"""

from typing import Any, Dict, List, Optional

class Session:
    """
    Manages a chat session between two participants.
    """

    def __init__(self,
                user_name: str, agent_name: str, agent: Any,
                session_name: str, db_handler: Any=None):
        """
        Initializes the session with two participants and a db_handler. 
        Generates a unique session_name under the user name.

        Args:
            user_name (str): The name of the user participant.
            agent_name (str): The name of the agent participant.
            agent (Any): The agent object that implements method to reply.
            db_handler (Any): Database operations.
            session_name (str): The name of the session.
        """
        self.user_name = user_name
        self.agent_name = agent_name
        self.agent = agent
        self.db_handler = db_handler
        self.session_name = session_name

    def send_message(self, sender: str, content: str, include_chat_history: bool, **keywords) -> Optional[Dict[str, Any]]:
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
        raise NotImplementedError

    def save_session(self) -> str:
        """
        Saves the current session to the database.

        Returns:
            str: A success message.
        """
        raise NotImplementedError

    def delete_session(self) -> str:
        """
        Deletes the current session from the database.

        Returns:
            str: A success message.
        """
        raise NotImplementedError

    def get_session_messages(self, total_messages: int = -1) -> List[Dict[str, Any]]:
        """
        Retrieves session messages from the database.

        Args:
            total_messages (int): The total number of messages to retrieve. 
            Default is -1 (all).

        Returns:
            List[Dict[str, Any]]: A list of message dictionaries.
        """
        raise NotImplementedError
    
    def reset(self):
        raise NotImplementedError