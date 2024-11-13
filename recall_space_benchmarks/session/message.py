"""
A message is follows the Open AI format for messages. Namely:
    - role
    - content
We also added timestamp.
"""

from textwrap import dedent


class Message:
    """
    Represents a session message.

    Attributes:
        sender (str): The sender of the message.
        content (str): The content of the message.
    """

    def __init__(self, sender: str, content: str):
        """
        Initializes a message with sender, content, and timestamp.

        Args:
            sender (str): The sender of the message, either assistant or user.
            content (str): The content of the message.
        """
        self.sender = sender
        self.content = content

    def to_str(self):
        return dedent(f"""
        # user name: {self.sender}
        ### content:
            {self.content}
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
            "content": self.content
        }
