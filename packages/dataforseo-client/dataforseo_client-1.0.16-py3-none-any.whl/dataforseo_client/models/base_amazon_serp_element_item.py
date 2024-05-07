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
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class BaseAmazonSerpElementItem(BaseModel):
    """
    BaseAmazonSerpElementItem
    """ # noqa: E501
    type: Optional[StrictStr] = Field(default=None, description="type of element")
    __properties: ClassVar[List[str]] = ["type"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    # JSON field name that stores the object type
    __discriminator_property_name: ClassVar[str] = 'type'

    # discriminator mappings
    __discriminator_value_class_map: ClassVar[Dict[str, str]] = {
        'amazon_paid': 'DataAmazonAmazonPaidSerpElementItem','amazon_product_info': 'DataAmazonAmazonProductInfoSerpElementItem','amazon_review_item': 'DataAmazonAmazonReviewItemSerpElementItem','amazon_seller_item': 'DataAmazonAmazonSellerItemSerpElementItem','amazon_seller_main_item': 'DataAmazonAmazonSellerMainItemSerpElementItem','amazon_serp': 'DataAmazonAmazonSerpSerpElementItem','editorial_recommendations': 'DataAmazonEditorialRecommendationsSerpElementItem','related_searches': 'DataAmazonRelatedSearchesSerpElementItem','top_rated_from_our_brands': 'DataAmazonTopRatedFromOurBrandsSerpElementItem'
    }

    @classmethod
    def get_discriminator_value(cls, obj: Dict[str, Any]) -> Optional[str]:
        """Returns the discriminator value (object type) of the data"""
        discriminator_value = obj[cls.__discriminator_property_name]
        if discriminator_value:
            return cls.__discriminator_value_class_map.get(discriminator_value)
        else:
            return None

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Union[Self, Self, Self, Self, Self, Self, Self, Self, Self]]:
        """Create an instance of BaseAmazonSerpElementItem from a JSON string"""
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
        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Optional[Union[Self, Self, Self, Self, Self, Self, Self, Self, Self]]:
        """Create an instance of BaseAmazonSerpElementItem from a dict"""
        # look up the object type based on discriminator mapping
        object_type = cls.get_discriminator_value(obj)
        if object_type:
            klass = globals()[object_type]
            return klass.from_dict(obj)
        else:
            raise ValueError("BaseAmazonSerpElementItem failed to lookup discriminator value from " +
                             json.dumps(obj) + ". Discriminator property name: " + cls.__discriminator_property_name +
                             ", mapping: " + json.dumps(cls.__discriminator_value_class_map))

from dataforseo_client.models.data_amazon_amazon_paid_serp_element_item import DataAmazonAmazonPaidSerpElementItem
from dataforseo_client.models.data_amazon_amazon_product_info_serp_element_item import DataAmazonAmazonProductInfoSerpElementItem
from dataforseo_client.models.data_amazon_amazon_review_item_serp_element_item import DataAmazonAmazonReviewItemSerpElementItem
from dataforseo_client.models.data_amazon_amazon_seller_item_serp_element_item import DataAmazonAmazonSellerItemSerpElementItem
from dataforseo_client.models.data_amazon_amazon_seller_main_item_serp_element_item import DataAmazonAmazonSellerMainItemSerpElementItem
from dataforseo_client.models.data_amazon_amazon_serp_serp_element_item import DataAmazonAmazonSerpSerpElementItem
from dataforseo_client.models.data_amazon_editorial_recommendations_serp_element_item import DataAmazonEditorialRecommendationsSerpElementItem
from dataforseo_client.models.data_amazon_related_searches_serp_element_item import DataAmazonRelatedSearchesSerpElementItem
from dataforseo_client.models.data_amazon_top_rated_from_our_brands_serp_element_item import DataAmazonTopRatedFromOurBrandsSerpElementItem
# TODO: Rewrite to not use raise_errors
BaseAmazonSerpElementItem.model_rebuild(raise_errors=False)

