import os
import requests
from requests.auth import HTTPBasicAuth
from typing import Dict, Any


class MemoryEngineConnector:
    def __init__(self):
        """
        Initializes the MemoryEngineConnector with
        environment variables for URL, user, and password.
        """
        self.memory_engine_url = os.getenv("MEMORY_ENGINE_URL")
        self.user = os.getenv("MEMORY_ENGINE_USER")
        self.password = os.getenv("MEMORY_ENGINE_PASSWORD")

        if not self.memory_engine_url or not self.user or not self.password:
            raise EnvironmentError(
                "Environment variables for MEMORY_ENGINE_URL, user, or password are missing."
            )

        self.auth = HTTPBasicAuth(self.user, self.password)

    def request_encode_memory(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a request to encode memory information.

        Parameters
        ----------
        payload : dict
            The payload to be sent to the encode memory endpoint.

        Returns
        -------
        dict
            The response JSON from the memory encoding request.
        """
        url = f"{self.memory_engine_url}/encode/chat"
        return self._send_post_request(url, payload)

    def request_recall_memory(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a request to recall memory information.

        Parameters
        ----------
        payload : dict
            The payload to be sent to the recall memory endpoint.

        Returns
        -------
        dict
            The response JSON from the memory recall request.
        """
        url = f"{self.memory_engine_url}/recall/chat"
        return self._send_post_request(url, payload)
    
    def reset_memory(self) -> Dict[str, Any]:
        """
        Sends a DELETE request to reset memory.

        Returns
        -------
        dict
            The response JSON from the reset memory request.
        """
        url = f"{self.memory_engine_url}/reset"
        response = requests.delete(url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    def _send_post_request(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a POST request to the specified URL with the given payload and authentication.

        Parameters
        ----------
        url : str
            The URL to send the POST request to.
        payload : dict
            The JSON payload to send with the request.

        Returns
        -------
        dict
            The response JSON from the request.

        Raises
        ------
        HTTPError
            If the HTTP request returned an unsuccessful status code.
        """
        response = requests.post(url, json=payload, auth=self.auth)
        response.raise_for_status()
        return response.json()