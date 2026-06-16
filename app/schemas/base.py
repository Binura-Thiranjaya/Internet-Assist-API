from __future__ import annotations
from marshmallow import Schema, pre_load, RAISE
class BaseSchema(Schema):
    class Meta:
        unknown = RAISE
    @pre_load
    def trim_strings(self, data, **kwargs):
        if isinstance(data, dict):
            return {
                key: value.strip() if isinstance(value, str) else value
                for key, value in data.items()
            }
        return data
