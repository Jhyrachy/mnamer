from collections.abc import Mapping
from copy import deepcopy
from json import dumps

from mnamer.constants import (
    CONFIGURATION_KEYS,
    DIRECTIVE_KEYS,
    PREFERENCE_DEFAULTS,
    PREFERENCE_KEYS,
)
from mnamer.exceptions import MnamerConfigException
from mnamer.utils import config_find, config_load, merge_dicts


def _to_json(d):
    return dumps(d, sort_keys=True, skipkeys=True, allow_nan=False)


class Configuration(Mapping):
    def __init__(self, **overrides):
        self._dict = deepcopy(PREFERENCE_DEFAULTS)
        for key, value in overrides.items():
            if key not in CONFIGURATION_KEYS:
                raise MnamerConfigException("%s is not a valid field" % key)
            else:
                self._dict[key] = value

    def __getitem__(self, key):
        return self._dict.__getitem__(key)

    def __iter__(self):
        return self._dict.__iter__()

    def __len__(self):
        return self._dict.__len__()

    def load_file(self):
        json_file = config_find()
        json_data = config_load(json_file)
        for key, value in json_data.items():
            value = json_data.get(key)
            if key not in PREFERENCE_KEYS:
                raise MnamerConfigException("%s is not a valid field" % key)
            elif value is not None:
                setattr(self, key, value)
        return json_file

    @property
    def preference_dict(self):
        return {k: v for k, v in self._dict.items() if k in PREFERENCE_KEYS}

    @property
    def preference_json(self):
        return _to_json(self.preference_dict)

    @property
    def directive_dict(self):
        return {k: v for k, v in self._dict.items() if k in DIRECTIVE_KEYS}

    @property
    def directive_json(self):
        return _to_json(self.directive_dict)

    @property
    def config_json(self):
        return _to_json(self._dict)
