# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.yelp_search_organic_business_data_serp_element_item import YelpSearchOrganicBusinessDataSerpElementItem

class TestYelpSearchOrganicBusinessDataSerpElementItem(unittest.TestCase):
    """YelpSearchOrganicBusinessDataSerpElementItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> YelpSearchOrganicBusinessDataSerpElementItem:
        """Test YelpSearchOrganicBusinessDataSerpElementItem
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `YelpSearchOrganicBusinessDataSerpElementItem`
        """
        model = YelpSearchOrganicBusinessDataSerpElementItem()
        if include_optional:
            return YelpSearchOrganicBusinessDataSerpElementItem(
                rank_group = 56,
                rank_absolute = 56,
                yelp_business_id = '',
                business_url = '',
                alias = '',
                name = '',
                description = '',
                location = dataforseo_client.models.business_address_location_info.BusinessAddressLocationInfo(
                    address_lines = [
                        ''
                        ], 
                    latitude = '', 
                    longitude = '', ),
                price_range = 56,
                phone = '',
                is_guaranteed = True,
                rating = dataforseo_client.models.rating_info.RatingInfo(
                    rating_type = '', 
                    value = 1.337, 
                    votes_count = 56, 
                    rating_max = 56, ),
                categories = [
                    ''
                    ],
                photos = [
                    ''
                    ],
                tags = [
                    ''
                    ],
                business_highlights = [
                    ''
                    ],
                service_offerings = [
                    dataforseo_client.models.service_offerings_element.ServiceOfferingsElement(
                        type = '', 
                        name = '', 
                        is_available = True, )
                    ]
            )
        else:
            return YelpSearchOrganicBusinessDataSerpElementItem(
        )
        """

    def testYelpSearchOrganicBusinessDataSerpElementItem(self):
        """Test YelpSearchOrganicBusinessDataSerpElementItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
