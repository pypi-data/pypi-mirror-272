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

from pydantic import BaseModel, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from dataforseo_client.models.reddit_reviews import RedditReviews
from typing import Optional, Set
from typing_extensions import Self

class BusinessDataSocialMediaRedditLiveResultInfo(BaseModel):
    """
    BusinessDataSocialMediaRedditLiveResultInfo
    """ # noqa: E501
    type: Optional[StrictStr] = Field(default=None, description="type of element")
    page_url: Optional[StrictStr] = Field(default=None, description="URL of the page the data is provided for corresponding URL you specified in the targets array when setting a task")
    reddit_reviews: Optional[List[RedditReviews]] = Field(default=None, description="reddit reviews for the page_url")
    __properties: ClassVar[List[str]] = ["type", "page_url", "reddit_reviews"]

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
        """Create an instance of BusinessDataSocialMediaRedditLiveResultInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in reddit_reviews (list)
        _items = []
        if self.reddit_reviews:
            for _item in self.reddit_reviews:
                if _item:
                    _items.append(_item.to_dict())
            _dict['reddit_reviews'] = _items
        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        # set to None if page_url (nullable) is None
        # and model_fields_set contains the field
        if self.page_url is None and "page_url" in self.model_fields_set:
            _dict['page_url'] = None

        # set to None if reddit_reviews (nullable) is None
        # and model_fields_set contains the field
        if self.reddit_reviews is None and "reddit_reviews" in self.model_fields_set:
            _dict['reddit_reviews'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BusinessDataSocialMediaRedditLiveResultInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "page_url": obj.get("page_url"),
            "reddit_reviews": [RedditReviews.from_dict(_item) for _item in obj["reddit_reviews"]] if obj.get("reddit_reviews") is not None else None
        })
        return _obj


