# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.shopping_dataforseo_labs_serp_element_item import ShoppingDataforseoLabsSerpElementItem

class TestShoppingDataforseoLabsSerpElementItem(unittest.TestCase):
    """ShoppingDataforseoLabsSerpElementItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ShoppingDataforseoLabsSerpElementItem:
        """Test ShoppingDataforseoLabsSerpElementItem
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ShoppingDataforseoLabsSerpElementItem`
        """
        model = ShoppingDataforseoLabsSerpElementItem()
        if include_optional:
            return ShoppingDataforseoLabsSerpElementItem(
                rank_group = 56,
                rank_absolute = 56,
                position = '',
                xpath = '',
                title = '',
                items = [
                    dataforseo_client.models.shopping_element.ShoppingElement(
                        type = '', 
                        title = '', 
                        price = dataforseo_client.models.price_info.PriceInfo(
                            current = 1.337, 
                            regular = 1.337, 
                            max_value = 1.337, 
                            currency = '', 
                            is_price_range = True, 
                            displayed_price = '', ), 
                        source = '', 
                        description = '', 
                        marketplace = '', 
                        marketplace_url = '', 
                        url = '', )
                    ]
            )
        else:
            return ShoppingDataforseoLabsSerpElementItem(
        )
        """

    def testShoppingDataforseoLabsSerpElementItem(self):
        """Test ShoppingDataforseoLabsSerpElementItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
