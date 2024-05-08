from __future__ import annotations

import httpx
import json
import requests

from typing import Any, Dict, Generator, List, Optional, Tuple

from promptwiz.query import Query


_SUPPORTED_API_VERSIONS = ["0.1"]

DEFAULT_API_VERSION = "0.1"
DEFAULT_PROMPT_WIZ_URL = "https://app.promptwiz.co.uk"
DEFAULT_STREAM_TIMEOUT_SECONDS = 10.0


class _Api:
    def __init__(self):
        self._api_key = None
        self._api_version = DEFAULT_API_VERSION
        self._prompt_wiz_url = DEFAULT_PROMPT_WIZ_URL
        self._stream_timeout_seconds = DEFAULT_STREAM_TIMEOUT_SECONDS
    
    @property
    def api_key(self) -> str:
        """The PromptWiz API key used in requests"""
        return self._api_key
    
    @api_key.setter
    def api_key(self, api_key: str) -> None:
        self._api_key = api_key
    
    @property
    def api_version(self) -> str:
        """The PromptWiz API version used in requests"""
        return self._api_version
    
    @api_version.setter
    def api_version(self, api_version: str | float) -> None:
        if isinstance(api_version, float):
            api_version = str(api_version)
        if api_version not in _SUPPORTED_API_VERSIONS:
            raise ValueError(f"Unsupported PromptWiz API version: {api_version}")
        self._api_version = api_version
    
    @property
    def prompt_wiz_url(self) -> str:
        """The PromptWiz URL targeted in requests"""
        return self._prompt_wiz_url
    
    @prompt_wiz_url.setter
    def prompt_wiz_url(self, prompt_wiz_url: str) -> None:
        self._prompt_wiz_url = prompt_wiz_url
    
    @property
    def stream_timeout_seconds(self) -> float:
        """The response timeout for streaming requests"""
        return self._stream_timeout_seconds
    
    @stream_timeout_seconds.setter
    def stream_timeout_seconds(self, stream_timeout_seconds: float) -> None:
        self._stream_timeout_seconds = stream_timeout_seconds
    
    @property
    def _prompt_wiz_api_url(self) -> str:
        return f"{self._prompt_wiz_url}/api/v{self.api_version}"
    
    @property
    def _prompt_wiz_evaluate_api_url(self) -> str:
        return f"{self._prompt_wiz_api_url}/evaluate/"
    
    @property
    def _prompt_wiz_prompt_api_url(self) -> str:
        return f"{self._prompt_wiz_api_url}/prompt/"
    
    @property
    def _headers(self) -> Dict[str, str]:
        return dict(apiKey=self._api_key or "")
    
    def _build_evaluate_payload(
        self, 
        query_set: List[Query], 
        accept_partial: Optional[bool] = None,
        stream: Optional[bool] = None,
    ) -> Dict[str, Any]:
        request_payload = dict(querySet=[query.as_dict() for query in query_set])
        if accept_partial is not None:
            request_payload["acceptPartial"] = accept_partial
        if stream is not None:
            request_payload["stream"] = stream
        return request_payload

    def evaluate(
        self, 
        query_set: List[Query], 
        accept_partial: Optional[bool] = None, 
    ) -> Tuple[List[Dict[str, Any]], Optional[List[Dict[str, str]]], int]:
        """
        Evaluates a given request
        
        Parameters
        ----------
            query_set : List[:class:`promptwiz.Query`]\n
                A list of Prompt Wiz queries to be evaluated, see :class:`promptwiz.Query`\n
            accept_partial : Optional[:class:`bool`]\n
                A boolean indicating whether partial result sets are accepted.\n
                A partial result set is one that does not contain a result for\n
                for every query in the query set
        
        Returns
        -------
            results_set : List[Dict[:class:`str`, Any]]\n
                The result set\n
            erros : List[Dict[:class:`str`, :class:`str`]]\n
                A list of Prompt Wiz errors, or `None` if there are no errors\n
            status_code : :class:`int`\n
                A HTTP status code
        """
        request_payload = self._build_evaluate_payload(query_set=query_set, accept_partial=accept_partial)
        response = requests.post(self._prompt_wiz_evaluate_api_url, json=request_payload, headers=self._headers)
        try:
            response_payload = json.loads(response.text)
            return response_payload.get("resultSet", []), response_payload.get("errors"), response.status_code
        except Exception as err:
            return (
                [], 
                [
                    dict(
                        code="UNKOWN_RESPONSE", 
                        description=f"Could not parse the PromptWiz response: {err}\n{response.text}"
                    ),
                ], 
                response.status_code,
            )
    
    def async_evaluate(
        self, 
        query_set: List[Query], 
    ) -> Generator[List[Dict[str, Any]]]:
        """
        Evaluates a given request and returns the response as a stream
        
        Parameters
        ----------
            query_set : List[:class:`promptwiz.Query`]\n
                A list of Prompt Wiz queries to be evaluated, see :class:`promptwiz.Query`\n
        
        Yields
        -------
            results_set : List[Dict[:class:`str`, Any]]\n
                The result set\n
            erros : List[Dict[:class:`str`, :class:`str`]]\n
                A list of Prompt Wiz errors, or `None` if there are no errors\n
            status_code : :class:`int`\n
                A HTTP status code
        """
        request_payload = self._build_evaluate_payload(query_set=query_set, stream=True)
        with httpx.stream(
            'POST', 
            self._prompt_wiz_evaluate_api_url, 
            json=request_payload, 
            headers=self._headers, 
            timeout=self.stream_timeout_seconds,
        ) as response:
            for chunk in response.iter_text():
                if len(chunk) > 0:
                    chunk_json = json.loads(chunk)
                    yield chunk_json.get("resultSet", [])

    def prompt(
        self,
        prompt_id: int, 
    ) -> Tuple[List[Dict[str, Any]], Optional[List[Dict[str, str]]], int]:
        """
        Evaluates a given request
        
        Parameters
        ----------
            prompt_id : :class:`int`\n
                The Prompt Wiz prompt ID
        
        Returns
        -------
            prompt : Dict[:class:`str`, Any]\n
                The prompt data\n
            erros : List[Dict[:class:`str`, :class:`str`]]\n
                A list of Prompt Wiz errors, or `None` if there are no errors\n
            status_code : :class:`int`\n
                A HTTP status code
        """
        request_payload = dict(promptId=prompt_id)
        response = requests.post(self._prompt_wiz_prompt_api_url, json=request_payload, headers=self._headers)
        try:
            response_payload = json.loads(response.text)
            return response_payload.get("prompt", {}), response_payload.get("errors"), response.status_code
        except Exception as err:
            return (
                [], 
                [
                    dict(
                        code="UNKOWN_RESPONSE", 
                        description=f"Could not parse the PromptWiz response: {err}\n{response.text}"
                    ),
                ], 
                response.status_code,
            )


Api = _Api()