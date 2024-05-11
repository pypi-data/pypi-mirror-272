from typing import Union, Optional
from dataclasses import dataclass, field, asdict
from logging import Logger
from requests import Response

import json
import requests

logger = Logger('easywebhooker')


@dataclass
class HookConfig:
    # This field serves as a subscription, and only notifies the corresponding hook when a specified event occurs
    # Subscribe to all events by default
    # Some variables (see below) can only be available under certain conditions, and the caller should specify under what conditions a variable is available
    when: list[str] = None

    method: str = 'GET'

    # A python f-string
    # Variables are available
    url: str = ""

    # A python expression, automatically calculated when on webhooks
    # Variables are available
    # A dict object will be treated as json, using requests.request(json=body)
    # else using requests.request(body=body)
    body: str = 'None'

    headers: dict[str, str] = field(default_factory=dict[str, str])
    timeout: int = 5
    request_kwargs: dict[str, object] = field(default_factory=dict[str, object])

    def __hash__(self) -> int:
        return hash(json.dumps(asdict(self)))


ConfigType = list[Union[dict, HookConfig]]
config: ConfigType = None


def configure(_config: ConfigType):
    global config
    config = _config


def webhook(now = '', _config: ConfigType = [], **kwargs) -> dict[HookConfig, Response]:
    global config
    current_config = config if config else _config

    result = {}
    for hookconfig in current_config:
        if type(hookconfig) == dict:
            hookconfig = HookConfig(**hookconfig)
        hookconfig: HookConfig

        if not now == '':
            _when = hookconfig.when
            if _when == None:
                _when = [now]
            elif type(_when) == str:
                _when = [_when]
            if not now in _when:
                continue

        url = hookconfig.url.format(kwargs)
        body = eval(hookconfig.body, {}, kwargs)
        method = hookconfig.method.upper()

        if type(body) == dict:
            body = json.dumps(body, ensure_ascii=True)

        _logger = logger.getChild(f'{method} {url}')
        _logger.debug('Start')
        response = requests.request(method,
                                    url,
                                    data=body,
                                    headers=hookconfig.headers,
                                    timeout=hookconfig.timeout,
                                    **hookconfig.request_kwargs)
        _logger.debug(f'Finished with code {response.status_code}, size {len(response.content)}')

        result[hookconfig] = response

    return result
