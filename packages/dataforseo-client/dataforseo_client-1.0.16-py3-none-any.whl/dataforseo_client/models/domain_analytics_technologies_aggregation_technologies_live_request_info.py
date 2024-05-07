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

from pydantic import BaseModel, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class DomainAnalyticsTechnologiesAggregationTechnologiesLiveRequestInfo(BaseModel):
    """
    DomainAnalyticsTechnologiesAggregationTechnologiesLiveRequestInfo
    """ # noqa: E501
    group: Optional[StrictStr] = Field(default=None, description="id of the target technology group required field if you don’t specify technology or category you can find the full list of technology group ids on this page example: \"marketing\"")
    category: Optional[StrictStr] = Field(default=None, description="id of the target technology category required field if you don’t specify group or technology you can find the full list of technology category ids on this page example: \"crm\"")
    technology: Optional[StrictStr] = Field(default=None, description="target technology required field if you don’t specify group or category you can find the full list of technologies on this page example: \"Salesforce\"")
    keyword: Optional[StrictStr] = Field(default=None, description="target keyword in the domain’s meta keywords optional field UTF-8 encoding each keyword should be at least 3 characters long example: \"seo\"")
    mode: Optional[StrictStr] = Field(default=None, description="search mode optional field possible search mode types: as_is – search for results exactly matching the specified group ids, category ids, or technology names entry – search for results matching a part of the specified group ids, category ids, or technology names default value: as_is")
    filters: Optional[List[Optional[Dict[str, Any]]]] = Field(default=None, description="array of results filtering parameters optional field you can add several filters at once (8 filters maximum) you should set a logical operator and, or between the conditions the following operators are supported: <, <=, >, >=, =, <>, in, not_in, like,not_like you can use the % operator with like and not_like to match any string of zero or more characters you can use the following parameters to filter the results: domain_rank, last_visited, country_iso_code, language_code, content_language_code example: [[\"country_iso_code\",\"=\",\"US\"], \"and\", [\"domain_rank\",\">\",800]]for more information about filters, please refer to Domain Analytics Technologies API – Filters")
    order_by: Optional[List[StrictStr]] = Field(default=None, description="results sorting rules optional field you can use the following values to sort the results: groups_count, categories_count, technologies_count possible sorting types: asc – results will be sorted in the ascending order desc – results will be sorted in the descending order you should use a comma to set up a sorting type example: [\"groups_count,desc\"] note that you can set no more than three sorting rules in a single request you should use a comma to separate several sorting rules example: [\"groups_count,desc\",\"technologies_count,desc\"] default value: [\"groups_count,desc\",\"categories_count,desc\",\"technologies_count,desc\"]")
    internal_groups_list_limit: Optional[StrictInt] = Field(default=None, description="maximum number of returned technology groups optional field you can use this field to limit the number of items with identical \"group\" in the results default value: 5 maximum value: 10000")
    internal_categories_list_limit: Optional[StrictInt] = Field(default=None, description="maximum number of returned technology categories within the same group optional field you can use this field to limit the number of items with identical \"category\" in the results default value: 5 maximum value: 10000")
    internal_technologies_list_limit: Optional[StrictInt] = Field(default=None, description="maximum number of returned technologies within the same category optional field you can use this field to limit the number of items with identical \"technology\" in the results default value: 10 maximum value: 10000")
    internal_list_limit: Optional[StrictInt] = Field(default=None, description="maximum number of items with identical \"category\", \"group\", and \"technology\" optional field if you use this field, the values specified in internal_groups_list_limit, internal_categories_list_limit and internal_technologies_list_limit will be ignored; you can use this field to limit the number of items with identical \"category\", \"group\", or \"technology\" default value: 10 maximum value: 10000")
    limit: Optional[StrictInt] = Field(default=None, description="the maximum number of returned technologies optional field default value: 100 maximum value: 10000")
    offset: Optional[StrictInt] = Field(default=None, description="offset in the results array of returned domains optional field default value: 0 maximum value: 9999 if you specify the 10 value, the first ten technologies in the results array will be omitted and the data will be provided for the successive technologies")
    tag: Optional[StrictStr] = Field(default=None, description="user-defined task identifier optional field the character limit is 255 you can use this parameter to identify the task and match it with the result you will find the specified tag value in the data object of the response")
    __properties: ClassVar[List[str]] = ["group", "category", "technology", "keyword", "mode", "filters", "order_by", "internal_groups_list_limit", "internal_categories_list_limit", "internal_technologies_list_limit", "internal_list_limit", "limit", "offset", "tag"]

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
        """Create an instance of DomainAnalyticsTechnologiesAggregationTechnologiesLiveRequestInfo from a JSON string"""
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
        # set to None if group (nullable) is None
        # and model_fields_set contains the field
        if self.group is None and "group" in self.model_fields_set:
            _dict['group'] = None

        # set to None if category (nullable) is None
        # and model_fields_set contains the field
        if self.category is None and "category" in self.model_fields_set:
            _dict['category'] = None

        # set to None if technology (nullable) is None
        # and model_fields_set contains the field
        if self.technology is None and "technology" in self.model_fields_set:
            _dict['technology'] = None

        # set to None if keyword (nullable) is None
        # and model_fields_set contains the field
        if self.keyword is None and "keyword" in self.model_fields_set:
            _dict['keyword'] = None

        # set to None if mode (nullable) is None
        # and model_fields_set contains the field
        if self.mode is None and "mode" in self.model_fields_set:
            _dict['mode'] = None

        # set to None if filters (nullable) is None
        # and model_fields_set contains the field
        if self.filters is None and "filters" in self.model_fields_set:
            _dict['filters'] = None

        # set to None if order_by (nullable) is None
        # and model_fields_set contains the field
        if self.order_by is None and "order_by" in self.model_fields_set:
            _dict['order_by'] = None

        # set to None if internal_groups_list_limit (nullable) is None
        # and model_fields_set contains the field
        if self.internal_groups_list_limit is None and "internal_groups_list_limit" in self.model_fields_set:
            _dict['internal_groups_list_limit'] = None

        # set to None if internal_categories_list_limit (nullable) is None
        # and model_fields_set contains the field
        if self.internal_categories_list_limit is None and "internal_categories_list_limit" in self.model_fields_set:
            _dict['internal_categories_list_limit'] = None

        # set to None if internal_technologies_list_limit (nullable) is None
        # and model_fields_set contains the field
        if self.internal_technologies_list_limit is None and "internal_technologies_list_limit" in self.model_fields_set:
            _dict['internal_technologies_list_limit'] = None

        # set to None if internal_list_limit (nullable) is None
        # and model_fields_set contains the field
        if self.internal_list_limit is None and "internal_list_limit" in self.model_fields_set:
            _dict['internal_list_limit'] = None

        # set to None if limit (nullable) is None
        # and model_fields_set contains the field
        if self.limit is None and "limit" in self.model_fields_set:
            _dict['limit'] = None

        # set to None if offset (nullable) is None
        # and model_fields_set contains the field
        if self.offset is None and "offset" in self.model_fields_set:
            _dict['offset'] = None

        # set to None if tag (nullable) is None
        # and model_fields_set contains the field
        if self.tag is None and "tag" in self.model_fields_set:
            _dict['tag'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DomainAnalyticsTechnologiesAggregationTechnologiesLiveRequestInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "group": obj.get("group"),
            "category": obj.get("category"),
            "technology": obj.get("technology"),
            "keyword": obj.get("keyword"),
            "mode": obj.get("mode"),
            "filters": obj.get("filters"),
            "order_by": obj.get("order_by"),
            "internal_groups_list_limit": obj.get("internal_groups_list_limit"),
            "internal_categories_list_limit": obj.get("internal_categories_list_limit"),
            "internal_technologies_list_limit": obj.get("internal_technologies_list_limit"),
            "internal_list_limit": obj.get("internal_list_limit"),
            "limit": obj.get("limit"),
            "offset": obj.get("offset"),
            "tag": obj.get("tag")
        })
        return _obj


