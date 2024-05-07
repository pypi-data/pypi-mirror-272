# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.keywords_data_dataforseo_trends_demography_live_result_info import KeywordsDataDataforseoTrendsDemographyLiveResultInfo

class TestKeywordsDataDataforseoTrendsDemographyLiveResultInfo(unittest.TestCase):
    """KeywordsDataDataforseoTrendsDemographyLiveResultInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> KeywordsDataDataforseoTrendsDemographyLiveResultInfo:
        """Test KeywordsDataDataforseoTrendsDemographyLiveResultInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `KeywordsDataDataforseoTrendsDemographyLiveResultInfo`
        """
        model = KeywordsDataDataforseoTrendsDemographyLiveResultInfo()
        if include_optional:
            return KeywordsDataDataforseoTrendsDemographyLiveResultInfo(
                keywords = [
                    ''
                    ],
                type = '',
                location_code = 56,
                language_code = '',
                datetime = '',
                items_count = 56,
                items = [
                    dataforseo_client.models.dataforseo_trends_demography_info.DataforseoTrendsDemographyInfo(
                        position = 56, 
                        type = '', 
                        keywords = [
                            ''
                            ], 
                        demography = dataforseo_client.models.demography.Demography(
                            age = [
                                dataforseo_client.models.dataforseo_trends_data_info.DataforseoTrendsDataInfo(
                                    keyword = '', 
                                    values = [
                                        dataforseo_client.models.demography_item_value_info.DemographyItemValueInfo(
                                            type = '', 
                                            value = 56, )
                                        ], )
                                ], 
                            gender = [
                                dataforseo_client.models.dataforseo_trends_data_info.DataforseoTrendsDataInfo(
                                    keyword = '', )
                                ], ), 
                        demography_comparison = dataforseo_client.models.demography_comparison.DemographyComparison(), )
                    ]
            )
        else:
            return KeywordsDataDataforseoTrendsDemographyLiveResultInfo(
        )
        """

    def testKeywordsDataDataforseoTrendsDemographyLiveResultInfo(self):
        """Test KeywordsDataDataforseoTrendsDemographyLiveResultInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
