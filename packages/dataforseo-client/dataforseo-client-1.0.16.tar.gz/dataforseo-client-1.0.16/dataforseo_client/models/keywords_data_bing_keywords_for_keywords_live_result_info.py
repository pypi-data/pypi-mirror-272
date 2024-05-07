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

from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from dataforseo_client.models.monthly_searches import MonthlySearches
from typing import Optional, Set
from typing_extensions import Self

class KeywordsDataBingKeywordsForKeywordsLiveResultInfo(BaseModel):
    """
    KeywordsDataBingKeywordsForKeywordsLiveResultInfo
    """ # noqa: E501
    keyword: Optional[StrictStr] = Field(default=None, description="keyword in a POST array")
    location_code: Optional[StrictInt] = Field(default=None, description="location code in a POST array if there is no data, then the value is null")
    language_code: Optional[StrictStr] = Field(default=None, description="language code in a POST array if there is no data, then the value is null")
    search_partners: Optional[StrictBool] = Field(default=None, description="indicates whether data from partner networks is included in the response")
    device: Optional[StrictStr] = Field(default=None, description="device type indicates for what device type the data is provided; possible values: all, mobile, desktop, tablet")
    competition: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="competition represents the relative amount of competition associated with the given keyword in paid SERP only. This value is based on Bing Ads data. Possible values: 0.1, 0.5,0.90.1 – low competition, 0.5 – medium competition, 0.9 – high competition; if there is no data the value is null")
    cpc: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="cost-per-click represents the average cost per click (USD) historically paid for the keyword. if there is no data, then the value is null")
    search_volume: Optional[StrictInt] = Field(default=None, description="monthly average search volume rate represents the (approximate) number of searches for the keyword on the Bing search engine, depending on the user’s targetingsearch volume is rounded to the closest decimal values if there is no data, then the value is null")
    categories: Optional[List[Optional[StrictStr]]] = Field(default=None, description="product and service categories legacy field, the value will always be null")
    monthly_searches: Optional[List[MonthlySearches]] = Field(default=None, description="monthly searches represents the (approximate) number of searches on this keyword (as available for the past twelve months), targeted to the specified geographic locations. if there is no data, then the value is null")
    __properties: ClassVar[List[str]] = ["keyword", "location_code", "language_code", "search_partners", "device", "competition", "cpc", "search_volume", "categories", "monthly_searches"]

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
        """Create an instance of KeywordsDataBingKeywordsForKeywordsLiveResultInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in monthly_searches (list)
        _items = []
        if self.monthly_searches:
            for _item in self.monthly_searches:
                if _item:
                    _items.append(_item.to_dict())
            _dict['monthly_searches'] = _items
        # set to None if keyword (nullable) is None
        # and model_fields_set contains the field
        if self.keyword is None and "keyword" in self.model_fields_set:
            _dict['keyword'] = None

        # set to None if location_code (nullable) is None
        # and model_fields_set contains the field
        if self.location_code is None and "location_code" in self.model_fields_set:
            _dict['location_code'] = None

        # set to None if language_code (nullable) is None
        # and model_fields_set contains the field
        if self.language_code is None and "language_code" in self.model_fields_set:
            _dict['language_code'] = None

        # set to None if search_partners (nullable) is None
        # and model_fields_set contains the field
        if self.search_partners is None and "search_partners" in self.model_fields_set:
            _dict['search_partners'] = None

        # set to None if device (nullable) is None
        # and model_fields_set contains the field
        if self.device is None and "device" in self.model_fields_set:
            _dict['device'] = None

        # set to None if competition (nullable) is None
        # and model_fields_set contains the field
        if self.competition is None and "competition" in self.model_fields_set:
            _dict['competition'] = None

        # set to None if cpc (nullable) is None
        # and model_fields_set contains the field
        if self.cpc is None and "cpc" in self.model_fields_set:
            _dict['cpc'] = None

        # set to None if search_volume (nullable) is None
        # and model_fields_set contains the field
        if self.search_volume is None and "search_volume" in self.model_fields_set:
            _dict['search_volume'] = None

        # set to None if categories (nullable) is None
        # and model_fields_set contains the field
        if self.categories is None and "categories" in self.model_fields_set:
            _dict['categories'] = None

        # set to None if monthly_searches (nullable) is None
        # and model_fields_set contains the field
        if self.monthly_searches is None and "monthly_searches" in self.model_fields_set:
            _dict['monthly_searches'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of KeywordsDataBingKeywordsForKeywordsLiveResultInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "keyword": obj.get("keyword"),
            "location_code": obj.get("location_code"),
            "language_code": obj.get("language_code"),
            "search_partners": obj.get("search_partners"),
            "device": obj.get("device"),
            "competition": obj.get("competition"),
            "cpc": obj.get("cpc"),
            "search_volume": obj.get("search_volume"),
            "categories": obj.get("categories"),
            "monthly_searches": [MonthlySearches.from_dict(_item) for _item in obj["monthly_searches"]] if obj.get("monthly_searches") is not None else None
        })
        return _obj


