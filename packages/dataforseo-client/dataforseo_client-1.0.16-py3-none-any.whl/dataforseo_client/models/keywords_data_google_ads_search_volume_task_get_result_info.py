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
from dataforseo_client.models.spell_info import SpellInfo
from typing import Optional, Set
from typing_extensions import Self

class KeywordsDataGoogleAdsSearchVolumeTaskGetResultInfo(BaseModel):
    """
    KeywordsDataGoogleAdsSearchVolumeTaskGetResultInfo
    """ # noqa: E501
    keyword: Optional[StrictStr] = Field(default=None, description="keyword keyword is returned with decoded %## (plus symbol ‘+’ will be decoded to a space character)")
    spell: Optional[SpellInfo] = None
    location_code: Optional[StrictInt] = Field(default=None, description="location code in a POST array if there is no data, then the value is null")
    language_code: Optional[StrictStr] = Field(default=None, description="language code in a POST array if there is no data, then the value is null")
    search_partners: Optional[StrictBool] = Field(default=None, description="indicates whether data from partner networks included in the response")
    competition: Optional[StrictStr] = Field(default=None, description="competition represents the relative amount of competition associated with the given keyword in paid SERP only; this value is based on Google Ads data and can take the following values: HIGH, MEDIUM, LOW; if there is no data the value is null; learn more about the metric in this help center article")
    competition_index: Optional[StrictInt] = Field(default=None, description="competition represents the relative amount of competition associated with the given keyword in paid SERP only; this value is based on Google Ads data and can be between 0 and 100 (inclusive); if there is no data the value is null; learn more about the metric in this help center article")
    search_volume: Optional[StrictInt] = Field(default=None, description="monthly average search volume rate; represents either the (approximate) number of searches for the given keyword idea on google.com or google.com and partners, depending on the user’s targeting; if there is no data then the value is null")
    low_top_of_page_bid: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="minimum bid for the ad to be displayed at the top of the first page indicates the value greater than about 20% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers); the value may differ depending on the location specified in a POST request")
    high_top_of_page_bid: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="maximum bid for the ad to be displayed at the top of the first page indicates the value greater than about 80% of the lowest bids for which ads were displayed (based on Google Ads statistics for advertisers); the value may differ depending on the location specified in a POST request")
    cpc: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="cost per click indicates the amount paid for each click on the ad displayed for a given keyword")
    monthly_searches: Optional[List[MonthlySearches]] = Field(default=None, description="monthly searches represents the (approximate) number of searches on this keyword idea (as available for the past twelve months by default), targeted to the specified geographic locations; if there is no data then the value is null")
    __properties: ClassVar[List[str]] = ["keyword", "spell", "location_code", "language_code", "search_partners", "competition", "competition_index", "search_volume", "low_top_of_page_bid", "high_top_of_page_bid", "cpc", "monthly_searches"]

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
        """Create an instance of KeywordsDataGoogleAdsSearchVolumeTaskGetResultInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of spell
        if self.spell:
            _dict['spell'] = self.spell.to_dict()
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

        # set to None if competition (nullable) is None
        # and model_fields_set contains the field
        if self.competition is None and "competition" in self.model_fields_set:
            _dict['competition'] = None

        # set to None if competition_index (nullable) is None
        # and model_fields_set contains the field
        if self.competition_index is None and "competition_index" in self.model_fields_set:
            _dict['competition_index'] = None

        # set to None if search_volume (nullable) is None
        # and model_fields_set contains the field
        if self.search_volume is None and "search_volume" in self.model_fields_set:
            _dict['search_volume'] = None

        # set to None if low_top_of_page_bid (nullable) is None
        # and model_fields_set contains the field
        if self.low_top_of_page_bid is None and "low_top_of_page_bid" in self.model_fields_set:
            _dict['low_top_of_page_bid'] = None

        # set to None if high_top_of_page_bid (nullable) is None
        # and model_fields_set contains the field
        if self.high_top_of_page_bid is None and "high_top_of_page_bid" in self.model_fields_set:
            _dict['high_top_of_page_bid'] = None

        # set to None if cpc (nullable) is None
        # and model_fields_set contains the field
        if self.cpc is None and "cpc" in self.model_fields_set:
            _dict['cpc'] = None

        # set to None if monthly_searches (nullable) is None
        # and model_fields_set contains the field
        if self.monthly_searches is None and "monthly_searches" in self.model_fields_set:
            _dict['monthly_searches'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of KeywordsDataGoogleAdsSearchVolumeTaskGetResultInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "keyword": obj.get("keyword"),
            "spell": SpellInfo.from_dict(obj["spell"]) if obj.get("spell") is not None else None,
            "location_code": obj.get("location_code"),
            "language_code": obj.get("language_code"),
            "search_partners": obj.get("search_partners"),
            "competition": obj.get("competition"),
            "competition_index": obj.get("competition_index"),
            "search_volume": obj.get("search_volume"),
            "low_top_of_page_bid": obj.get("low_top_of_page_bid"),
            "high_top_of_page_bid": obj.get("high_top_of_page_bid"),
            "cpc": obj.get("cpc"),
            "monthly_searches": [MonthlySearches.from_dict(_item) for _item in obj["monthly_searches"]] if obj.get("monthly_searches") is not None else None
        })
        return _obj


