# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from dataforseo_client.models.base_serp_element_item import BaseSerpElementItem
from dataforseo_client.models.event_dates import EventDates
from dataforseo_client.models.information_and_tickets_element import InformationAndTicketsElement
from dataforseo_client.models.location_info import LocationInfo
from typing import Optional, Set
from typing_extensions import Self

class EventItemSerpElementItem(BaseSerpElementItem):
    """
    EventItemSerpElementItem
    """ # noqa: E501
    rank_group: Optional[StrictInt] = Field(default=None, description="group rank in SERP position within a group of elements with identical type values positions of elements with different type values are omitted from rank_group")
    rank_absolute: Optional[StrictInt] = Field(default=None, description="absolute rank in SERP absolute position among all the elements in SERP")
    position: Optional[StrictStr] = Field(default=None, description="the alignment of the element in SERP can take the following values: left, right")
    xpath: Optional[StrictStr] = Field(default=None, description="the XPath of the element")
    title: Optional[StrictStr] = Field(default=None, description="title of the result in SERP")
    description: Optional[StrictStr] = Field(default=None, description="description of the results element in SERP")
    url: Optional[StrictStr] = Field(default=None, description="relevant URL")
    image_url: Optional[StrictStr] = Field(default=None, description="URL of the image featured in the element")
    event_dates: Optional[EventDates] = None
    location_info: Optional[LocationInfo] = None
    information_and_tickets: Optional[List[InformationAndTicketsElement]] = Field(default=None, description="additional information and ticket purchase options if there is none, equals null")
    __properties: ClassVar[List[str]] = ["type", "rank_group", "rank_absolute", "position", "xpath", "title", "description", "url", "image_url", "event_dates", "location_info", "information_and_tickets"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of EventItemSerpElementItem from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of event_dates
        if self.event_dates:
            _dict['event_dates'] = self.event_dates.to_dict()
        # override the default output from pydantic by calling `to_dict()` of location_info
        if self.location_info:
            _dict['location_info'] = self.location_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in information_and_tickets (list)
        _items = []
        if self.information_and_tickets:
            for _item in self.information_and_tickets:
                if _item:
                    _items.append(_item.to_dict())
            _dict['information_and_tickets'] = _items
        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        # set to None if rank_group (nullable) is None
        # and model_fields_set contains the field
        if self.rank_group is None and "rank_group" in self.model_fields_set:
            _dict['rank_group'] = None

        # set to None if rank_absolute (nullable) is None
        # and model_fields_set contains the field
        if self.rank_absolute is None and "rank_absolute" in self.model_fields_set:
            _dict['rank_absolute'] = None

        # set to None if position (nullable) is None
        # and model_fields_set contains the field
        if self.position is None and "position" in self.model_fields_set:
            _dict['position'] = None

        # set to None if xpath (nullable) is None
        # and model_fields_set contains the field
        if self.xpath is None and "xpath" in self.model_fields_set:
            _dict['xpath'] = None

        # set to None if title (nullable) is None
        # and model_fields_set contains the field
        if self.title is None and "title" in self.model_fields_set:
            _dict['title'] = None

        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if url (nullable) is None
        # and model_fields_set contains the field
        if self.url is None and "url" in self.model_fields_set:
            _dict['url'] = None

        # set to None if image_url (nullable) is None
        # and model_fields_set contains the field
        if self.image_url is None and "image_url" in self.model_fields_set:
            _dict['image_url'] = None

        # set to None if information_and_tickets (nullable) is None
        # and model_fields_set contains the field
        if self.information_and_tickets is None and "information_and_tickets" in self.model_fields_set:
            _dict['information_and_tickets'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of EventItemSerpElementItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "rank_group": obj.get("rank_group"),
            "rank_absolute": obj.get("rank_absolute"),
            "position": obj.get("position"),
            "xpath": obj.get("xpath"),
            "title": obj.get("title"),
            "description": obj.get("description"),
            "url": obj.get("url"),
            "image_url": obj.get("image_url"),
            "event_dates": EventDates.from_dict(obj["event_dates"]) if obj.get("event_dates") is not None else None,
            "location_info": LocationInfo.from_dict(obj["location_info"]) if obj.get("location_info") is not None else None,
            "information_and_tickets": [InformationAndTicketsElement.from_dict(_item) for _item in obj["information_and_tickets"]] if obj.get("information_and_tickets") is not None else None
        })
        return _obj


