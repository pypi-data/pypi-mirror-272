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

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class DataforseoLabsGoogleSerpCompetitorsLiveRequestInfo(BaseModel):
    """
    DataforseoLabsGoogleSerpCompetitorsLiveRequestInfo
    """ # noqa: E501
    keywords: Optional[List[StrictStr]] = Field(default=None, description="keywords array required field the results will be based on the keywords you specify in this array UTF-8 encoding; the keywords will be converted to lowercase format; a keyword should be at least 3 characters long; you can specify the maximum of 200 keywords")
    location_name: Optional[StrictStr] = Field(default=None, description="full name of the location required field if you don’t specify location_code Note: it is required to specify either location_name or location_code you can receive the list of available locations with location_name parameters by making a separate request to the https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages example: United Kingdom")
    location_code: Optional[StrictInt] = Field(default=None, description="unique location identifier required field if you don’t specify location_name Note: it is required to specify either location_name or location_code you can receive the list of available locations with their location_code parameters by making a separate request to the https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages example: 2840")
    language_name: Optional[StrictStr] = Field(default=None, description="full name of the language required field if you don’t specify language_code Note: it is required to specify either language_name or language_code you can receive the list of available languages with their language_name parameters by making a separate request to the https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages example: English")
    language_code: Optional[StrictStr] = Field(default=None, description="unique language identifier required field if you don’t specify language_name Note: it is required to specify either language_name or language_code you can receive the list of available languages with their language_code parameters by making a separate request to the https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages example: en")
    include_subdomains: Optional[StrictBool] = Field(default=None, description="indicates if the subdomains will be included in the search optional field if set to false, the subdomains will be ignored default value: true")
    item_types: Optional[List[StrictStr]] = Field(default=None, description="search results type indicates type of search results included in the response optional field possible values: [\"organic\", \"paid\", \"featured_snippet\", \"local_pack\"] default value: [\"organic\", \"paid\", \"featured_snippet\", \"local_pack\"]")
    limit: Optional[StrictInt] = Field(default=None, description="the maximum number of returned domains optional field default value: 100 maximum value: 1000")
    offset: Optional[StrictInt] = Field(default=None, description="offset in the results array of returned domains optional field default value: 0 if you specify the 10 value, the first ten domains in the results array will be omitted and the data will be provided for the successive domains")
    filters: Optional[List[Optional[Dict[str, Any]]]] = Field(default=None, description="array of results filtering parameters optional field you can add several filters at once (8 filters maximum) you should set a logical operator and, or between the conditions the following operators are supported: regex, <, <=, >, >=, =, <>, in, not_in, like, not_like you can use the % operator with like and not_like to match any string of zero or more characters example: [\"median_position\",\"in\",[1,10]] [[\"median_position\",\"in\",[1,10]],\"and\",[\"domain\",\"not_like\",\"%wikipedia.org%\"]] [[\"domain\",\"not_like\",\"%wikipedia.org%\"], \"and\", [[\"relevant_serp_items\",\">\",0],\"or\",[\"median_position\",\"in\",[1,10]]]] for more information about filters, please refer to Dataforseo Labs – Filters or this help center guide")
    order_by: Optional[List[StrictStr]] = Field(default=None, description="results sorting rules optional field you can use the same values as in the filters array to sort the results possible sorting types: asc – results will be sorted in the ascending order desc – results will be sorted in the descending order the comma is used as a separator example: [\"avg_position,asc\"] default rule: [\"rating,desc\"] note that you can set no more than three sorting rules in a single request you should use a comma to separate several sorting rules example: [\"avg_position,asc\",\"etv,desc\"]")
    tag: Optional[StrictStr] = Field(default=None, description="user-defined task identifier optional field the character limit is 255 you can use this parameter to identify the task and match it with the result you will find the specified tag value in the data object of the response")
    __properties: ClassVar[List[str]] = ["keywords", "location_name", "location_code", "language_name", "language_code", "include_subdomains", "item_types", "limit", "offset", "filters", "order_by", "tag"]

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
        """Create an instance of DataforseoLabsGoogleSerpCompetitorsLiveRequestInfo from a JSON string"""
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
        # set to None if location_name (nullable) is None
        # and model_fields_set contains the field
        if self.location_name is None and "location_name" in self.model_fields_set:
            _dict['location_name'] = None

        # set to None if location_code (nullable) is None
        # and model_fields_set contains the field
        if self.location_code is None and "location_code" in self.model_fields_set:
            _dict['location_code'] = None

        # set to None if language_name (nullable) is None
        # and model_fields_set contains the field
        if self.language_name is None and "language_name" in self.model_fields_set:
            _dict['language_name'] = None

        # set to None if language_code (nullable) is None
        # and model_fields_set contains the field
        if self.language_code is None and "language_code" in self.model_fields_set:
            _dict['language_code'] = None

        # set to None if include_subdomains (nullable) is None
        # and model_fields_set contains the field
        if self.include_subdomains is None and "include_subdomains" in self.model_fields_set:
            _dict['include_subdomains'] = None

        # set to None if item_types (nullable) is None
        # and model_fields_set contains the field
        if self.item_types is None and "item_types" in self.model_fields_set:
            _dict['item_types'] = None

        # set to None if limit (nullable) is None
        # and model_fields_set contains the field
        if self.limit is None and "limit" in self.model_fields_set:
            _dict['limit'] = None

        # set to None if offset (nullable) is None
        # and model_fields_set contains the field
        if self.offset is None and "offset" in self.model_fields_set:
            _dict['offset'] = None

        # set to None if filters (nullable) is None
        # and model_fields_set contains the field
        if self.filters is None and "filters" in self.model_fields_set:
            _dict['filters'] = None

        # set to None if order_by (nullable) is None
        # and model_fields_set contains the field
        if self.order_by is None and "order_by" in self.model_fields_set:
            _dict['order_by'] = None

        # set to None if tag (nullable) is None
        # and model_fields_set contains the field
        if self.tag is None and "tag" in self.model_fields_set:
            _dict['tag'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DataforseoLabsGoogleSerpCompetitorsLiveRequestInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "keywords": obj.get("keywords"),
            "location_name": obj.get("location_name"),
            "location_code": obj.get("location_code"),
            "language_name": obj.get("language_name"),
            "language_code": obj.get("language_code"),
            "include_subdomains": obj.get("include_subdomains"),
            "item_types": obj.get("item_types"),
            "limit": obj.get("limit"),
            "offset": obj.get("offset"),
            "filters": obj.get("filters"),
            "order_by": obj.get("order_by"),
            "tag": obj.get("tag")
        })
        return _obj


