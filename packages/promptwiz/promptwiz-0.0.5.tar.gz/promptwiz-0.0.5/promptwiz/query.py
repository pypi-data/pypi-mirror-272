from dataclasses import dataclass
from typing import Dict, Optional, Union


@dataclass
class Query:
    """
    A PromptWiz Query
        
    Parameters
    ----------
        prompt_id : :class:`int`\n
            The Prompt Wiz prompt ID\n
        variables : Optional[Dict[:class:`str`, :class:`str`]]\n
            The variables for the prompt parameters, or `None` if the prompt does\n
            not have any parameters\n
        link_id : Optional[:class:`int`]\n
            A unique ID for the query. This ID will be echoed back by Prompt Wiz in results\n
            to allow linking queries in a query set to results in a result set\n
        model_api_key : Optional[:class:`str`]\n
            An API key for the model service (e.g. OpenAI) to be queried. This allows for\n
            an override to the organisation’s API key saved under the API Keys page in the PromptWiz app.\n
            Please keep in mind if this parameter is used, the value may have to be updated if the model\n
            service is changed in a newer prompt version\n
        results_size : Optional[:class:`str`]\n
            The number of results to generate
    """
    prompt_id: int
    variables: Optional[Dict[str, str]] = None
    link_id: Optional[Union[int, str]] = None
    model_api_key: Optional[str] = None
    results_size: Optional[int] = None

    def as_dict(self):
        query = dict(promptId=self.prompt_id)
        if self.variables is not None:
            query["variables"] = self.variables
        if self.link_id is not None:
            query["linkId"] = self.link_id
        if self.model_api_key is not None:
            query["modelApiKey"] = self.model_api_key
        if self.results_size is not None:
            query["resultsSize"] = self.results_size
        return query