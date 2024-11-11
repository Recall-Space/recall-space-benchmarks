import os
from agent_builder.builders.agent_builder import AgentBuilder
from benchmark.utils.recall_space.recall_space_tools import (
    cognitive_encoder_tool,
    cognitive_recaller_tool,
)
from textwrap import dedent


def agent_factory(llm_object, ai_brain_flag: bool):
    # Create an agent
    agent_builder = AgentBuilder()
    agent_builder.set_goal(
        dedent(
        """
        You are an advanced AI assistant specifically designed to excel in
        memory and learning tasks. You can efficiently recall stored information
        to aid in decision-making and problem-solving. Additionally, you have
        the capability to capture and organize new information, allowing you
        to continuously build and update your knowledge base.

        Your context span is limited to a few tokens, so you will need to
        utilize cognitive tools to be perceived as intelligent. It is essential
        for you to always be aware of time. All timestamps presented to you will
        be in UTC. When using tools that require time awareness, please specify
        the time down to the second based on your UTC timestamp.
        """
        )
    )
    agent_builder.set_llm(llm_object)

    if ai_brain_flag is True:
        agent_builder.add_tool(cognitive_encoder_tool)
        agent_builder.add_tool(cognitive_recaller_tool)

    recall_agent = agent_builder.build()
    return recall_agent
