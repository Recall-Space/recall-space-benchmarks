"""
Main location of recall space llms deployments.
Instances operated via langchain chat classes.
"""

import os
from langchain_openai import AzureChatOpenAI
from langchain_cohere import ChatCohere
from langchain_mistralai import ChatMistralAI


base_url_cohere = os.getenv("AZURE_COHERE_COMMAND_R_API")
base_url_mistral = os.getenv("AZURE_MISTRAL_API")

try:
    url = base_url_cohere.split("=")[1]
    deployment_name_cohere = url.split("https://")[1].split(".")[0]
except:
    deployment_name_cohere = "cohere"

try:
    url = base_url_mistral.split("=")[1]
    deployment_name_mistral = url.split("https://")[1].split(".")[0]
except:
    deployment_name_mistral = "mistral"


models_map = {
    "gpt-4o": AzureChatOpenAI(
        base_url=os.getenv("AZURE_GPT4O_BASE_URL"),
        api_key=os.getenv("AZURE_GPT4O_KEY"),
        api_version=os.getenv("AZURE_GPT4O_API_VERSION"),
        streaming=False,
    ),
    "gpt-4o-mini": AzureChatOpenAI(
        base_url=os.getenv("AZURE_GPT4O_MINI_BASE_URL"),
        api_key=os.getenv("AZURE_GPT4O_MINI_KEY"),
        api_version=os.getenv("AZURE_GPT4O_MINI_API_VERSION"),
        streaming=False,
    ),
    "cohere-command-r-08-2024": ChatCohere(
        base_url=base_url_cohere,
        cohere_api_key=os.getenv("AZURE_COHERE_COMMAND_R_KEY"),
        model=deployment_name_cohere,
    ),
    "mistral-large-2407": ChatMistralAI(
        base_url=base_url_mistral,
        api_key=os.getenv("AZURE_MISTRAL_KEY"),
        safe_mode=True,
    ),
}
