import json

from odmantic import Model, Field


class ShowsModel(Model):
    id: int = Field(primary_field=True, default=1)
    data: dict = Field(...)

    class Config:
        collection = "Shows"
        json_loads = json.loads
        parse_doc_with_default_factories = True