from typing import Dict, Generator

import mwapi
from loguru import logger

log_message = "who={request}, what={object}, why={reason}, how={action}"


class WikiAPI:
    def __init__(self, url: str, api_path: str):
        self.url = url
        self.api_path = api_path
        self.session = mwapi.Session(self.url, api_path=self.api_path)
        self.api_url = self.session.api_url
        self.user_info = self.session.get(action="query", meta='userinfo')

    def get_next_json_batch_for_action_list_continuation(self, parameters: Dict) -> Generator:
        json_batches = self.get_action_list_continuation_batch(parameters)
        for json_batch in json_batches:
            logger.info(log_message, request=self.__str__(),
                        object="First json: {}".format(json_batch[parameters["action"]][parameters["list"]][0]),
                        reason="Tracking status",
                        action="Get batch")
            for json in json_batch[parameters["action"]][parameters["list"]]:
                yield json

    def get_action_list_continuation_batch(self, parameters: Dict[str, any]) -> Generator:
        return self.session.get(**parameters)

    def is_title_exists(self, title: str):
        return True if self.session.get(action="query", titles=title)["query"]["pages"].get("-1") is None else False

    def __str__(self) -> str:
        return '{}({})'.format(type(self).__name__, ', '.join('%s:%s' % item for item in vars(self).items()))

    def __repr__(self) -> str:
        return self.__str__()
