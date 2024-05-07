# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.google_shopping_sponsored_carousel_merchant_serp_element_item import GoogleShoppingSponsoredCarouselMerchantSerpElementItem

class TestGoogleShoppingSponsoredCarouselMerchantSerpElementItem(unittest.TestCase):
    """GoogleShoppingSponsoredCarouselMerchantSerpElementItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GoogleShoppingSponsoredCarouselMerchantSerpElementItem:
        """Test GoogleShoppingSponsoredCarouselMerchantSerpElementItem
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GoogleShoppingSponsoredCarouselMerchantSerpElementItem`
        """
        model = GoogleShoppingSponsoredCarouselMerchantSerpElementItem()
        if include_optional:
            return GoogleShoppingSponsoredCarouselMerchantSerpElementItem(
                rank_group = 56,
                rank_absolute = 56,
                position = '',
                xpath = '',
                title = '',
                items = [
                    dataforseo_client.models.google_shopping_sponsored_carousel_element.GoogleShoppingSponsoredCarouselElement(
                        type = '', 
                        xpath = '', 
                        title = '', 
                        tags = [
                            ''
                            ], 
                        seller = '', 
                        price = 1.337, 
                        currency = '', 
                        product_rating = dataforseo_client.models.rating_element.RatingElement(
                            type = '', 
                            position = '', 
                            rating_type = '', 
                            value = '', 
                            votes_count = 56, 
                            rating_max = 56, ), 
                        product_images = [
                            ''
                            ], 
                        shop_ad_aclk = '', 
                        delivery_info = dataforseo_client.models.delivery_info.DeliveryInfo(
                            delivery_message = '', 
                            delivery_price = dataforseo_client.models.price_info.PriceInfo(
                                current = 1.337, 
                                regular = 1.337, 
                                max_value = 1.337, 
                                currency = '', 
                                is_price_range = True, 
                                displayed_price = '', ), 
                            stores_count_info = dataforseo_client.models.stores_count_info.StoresCountInfo(
                                count = '', 
                                displayed_text = '', 
                                count_from_text = True, ), ), )
                    ]
            )
        else:
            return GoogleShoppingSponsoredCarouselMerchantSerpElementItem(
        )
        """

    def testGoogleShoppingSponsoredCarouselMerchantSerpElementItem(self):
        """Test GoogleShoppingSponsoredCarouselMerchantSerpElementItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
