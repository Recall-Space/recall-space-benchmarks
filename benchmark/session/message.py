"""
A message is follows the Open AI format for messages. Namely:
    - role
    - content
We also added timestamp.
"""

from textwrap import dedent
import datetime


class Message:
    """
    Represents a session message.

    Attributes:
        sender (str): The sender of the message.
        content (str): The content of the message.
        timestamp (datetime): The timestamp of the message.
    """

    def __init__(self, sender: str, content: str, timestamp=None):
        """
        Initializes a message with sender, content, and timestamp.

        Args:
            sender (str): The sender of the message, either assistant or user.
            content (str): The content of the message.
            timestamp (datetime, optional): The timestamp of the message. Defaults to current time.
        """
        self.sender = sender
        self.content = content
        self.timestamp = timestamp or datetime.datetime.now(datetime.timezone.utc)

    def to_str(self):
        return dedent(f"""
        # user name: {self.sender}
        ### content:
            {self.content}
        ### timestamp: 
            {self.timestamp}
        """)


    def to_dict(self, is_agent: bool = False) -> dict:
        """
        Converts the message to a dictionary format suitable for MongoDB insertion.

        Returns:
            dict: The message as a dictionary.
        """
        if is_agent is True:
            role = "assistant"
        else:
            role = "user"

        return {
            "sender": self.sender,
            "role": role,
            "content": self.content,
            "timestamp": self.timestamp,
        }
