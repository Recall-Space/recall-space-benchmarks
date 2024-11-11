from pydantic import BaseModel, Field
from agent_builder.builders.tool_builder import ToolBuilder
from recall_space_benchmarks.utils.recall_space.memory_engine_connector import MemoryEngineConnector
import requests
from textwrap import dedent


# Schema for the information that will be encoded in memory
class CognitiveEncoderSchema(BaseModel):
    information: str = Field(description="Information to be encoded in memory. ")


# Function to encode memory by making a POST request to the MEMORY_ENGINE_URL
def encode_memory(information: str):
    try:
        memory_engine_connector = MemoryEngineConnector()
        # Prepare the payload
        payload = {"messages": [{"role": "user", "content": information}]}
        response = memory_engine_connector.request_encode_memory(payload=payload)
        return response["output"]

    except requests.RequestException as e:
        return f"Error while encoding memroy {str(e)}"


class CognitiveRecallerSchema(BaseModel):
    instructions: str = Field(description="Detailed instructions to recall the memory")


def recall_memory(instructions: str):
    try:
        memory_engine_connector = MemoryEngineConnector()
        # Prepare the payload
        payload = {"messages": [{"role": "user", "content": f"{instructions}"}]}
        response = memory_engine_connector.request_recall_memory(payload=payload)
        return response["output"]

    except requests.RequestException as e:
        return f"Error while recalling memory {str(e)}"

def recall_memory(instructions: str):
    try:
        memory_engine_connector = MemoryEngineConnector()
        # Prepare the payload
        payload = {"messages": [{"role": "user", "content": f"{instructions}"}]}
        response = memory_engine_connector.request_recall_memory(payload=payload)
        return response["output"]

    except requests.RequestException as e:
        return f"Error while recalling memroy {str(e)}"



######
# Instantiate the tool builder.
tool_builder = ToolBuilder()
# Define name of tool.
tool_builder.set_name(name="CognitiveEncoder")
# Set the function for the tool.
tool_builder.set_function(function=encode_memory)
# Provide the description for tool
tool_builder.set_description(
    description=dedent(
        """
    The Cognitive Encoder Tool is responsible for encoding information into memory, 
    simulating the human learning process. This tool captures and organizes new data,
    experiences, and knowledge, storing them effectively for future use. It mimics the 
    cognitive process of encoding, where information from the environment is transformed 
    into a format that can be stored in long-term memory. This tool ensures that the agent 
    can learn from interactions, adapt to new information, and build a comprehensive 
    knowledge base over time.
                """
    )
)
# Add the tool schema
tool_builder.set_schema(schema=CognitiveEncoderSchema)
# Build and get the tool
cognitive_encoder_tool = tool_builder.build()

#########
# Instantiate the tool builder.
tool_builder = ToolBuilder()
# Define name of tool.
tool_builder.set_name(name="CognitiveRecaller")
# Set the function for the tool.
tool_builder.set_function(function=recall_memory)
# Provide the description for tool
tool_builder.set_description(
    description=dedent(
        """
                The Cognitive Recall Tool is designed to retrieve stored information from memory,
                emulating the cognitive process of recalling. This tool accesses encoded knowledge,
                experiences, and data, bringing relevant information back into active use when needed.
                It supports decision-making, problem-solving, and reasoning by providing timely access
                to previously learned information. The Cognitive Recall Tool ensures that the agent can
                efficiently utilize its memory to respond to queries, perform tasks, and adapt to new
                situations by referencing past knowledge.
                """
    )
)
# Add the tool schema
tool_builder.set_schema(schema=CognitiveRecallerSchema)
# Build and get the tool
cognitive_recaller_tool = tool_builder.build()
