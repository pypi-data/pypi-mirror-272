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
from dataforseo_client.models.amazon_delivery_info import AmazonDeliveryInfo
from dataforseo_client.models.base_amazon_serp_element_item import BaseAmazonSerpElementItem
from dataforseo_client.models.price_info import PriceInfo
from dataforseo_client.models.rating_element import RatingElement
from typing import Optional, Set
from typing_extensions import Self

class DataAmazonAmazonSellerMainItemSerpElementItem(BaseAmazonSerpElementItem):
    """
    DataAmazonAmazonSellerMainItemSerpElementItem
    """ # noqa: E501
    rank_group: Optional[StrictInt] = Field(default=None, description="position within a group of elements with identical type values positions of elements with different type values are omitted from rank_group")
    rank_absolute: Optional[StrictInt] = Field(default=None, description="absolute rank in SERP absolute position among all the elements found in Amazon Sellers SERP")
    position: Optional[StrictStr] = Field(default=None, description="alignment of the element in SERP possible values: left, right")
    xpath: Optional[StrictStr] = Field(default=None, description="XPath of the element")
    seller_name: Optional[StrictStr] = Field(default=None, description="business name of the seller")
    seller_url: Optional[StrictStr] = Field(default=None, description="url forwarding to the seller’s page on Amazon")
    ships_from: Optional[StrictStr] = Field(default=None, description="sender company name")
    price: Optional[PriceInfo] = None
    rating: Optional[RatingElement] = None
    condition: Optional[StrictStr] = Field(default=None, description="product condition condition of the product offered by the seller")
    condition_description: Optional[StrictStr] = Field(default=None, description="product condition details expanded details on the condition of the product offered by the seller")
    delivery_info: Optional[AmazonDeliveryInfo] = None
    __properties: ClassVar[List[str]] = ["type", "rank_group", "rank_absolute", "position", "xpath", "seller_name", "seller_url", "ships_from", "price", "rating", "condition", "condition_description", "delivery_info"]

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
        """Create an instance of DataAmazonAmazonSellerMainItemSerpElementItem from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of price
        if self.price:
            _dict['price'] = self.price.to_dict()
        # override the default output from pydantic by calling `to_dict()` of rating
        if self.rating:
            _dict['rating'] = self.rating.to_dict()
        # override the default output from pydantic by calling `to_dict()` of delivery_info
        if self.delivery_info:
            _dict['delivery_info'] = self.delivery_info.to_dict()
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

        # set to None if seller_name (nullable) is None
        # and model_fields_set contains the field
        if self.seller_name is None and "seller_name" in self.model_fields_set:
            _dict['seller_name'] = None

        # set to None if seller_url (nullable) is None
        # and model_fields_set contains the field
        if self.seller_url is None and "seller_url" in self.model_fields_set:
            _dict['seller_url'] = None

        # set to None if ships_from (nullable) is None
        # and model_fields_set contains the field
        if self.ships_from is None and "ships_from" in self.model_fields_set:
            _dict['ships_from'] = None

        # set to None if condition (nullable) is None
        # and model_fields_set contains the field
        if self.condition is None and "condition" in self.model_fields_set:
            _dict['condition'] = None

        # set to None if condition_description (nullable) is None
        # and model_fields_set contains the field
        if self.condition_description is None and "condition_description" in self.model_fields_set:
            _dict['condition_description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DataAmazonAmazonSellerMainItemSerpElementItem from a dict"""
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
            "seller_name": obj.get("seller_name"),
            "seller_url": obj.get("seller_url"),
            "ships_from": obj.get("ships_from"),
            "price": PriceInfo.from_dict(obj["price"]) if obj.get("price") is not None else None,
            "rating": RatingElement.from_dict(obj["rating"]) if obj.get("rating") is not None else None,
            "condition": obj.get("condition"),
            "condition_description": obj.get("condition_description"),
            "delivery_info": AmazonDeliveryInfo.from_dict(obj["delivery_info"]) if obj.get("delivery_info") is not None else None
        })
        return _obj


