# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.keywords_data_bing_keyword_performance_live_result_info import KeywordsDataBingKeywordPerformanceLiveResultInfo

class TestKeywordsDataBingKeywordPerformanceLiveResultInfo(unittest.TestCase):
    """KeywordsDataBingKeywordPerformanceLiveResultInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> KeywordsDataBingKeywordPerformanceLiveResultInfo:
        """Test KeywordsDataBingKeywordPerformanceLiveResultInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `KeywordsDataBingKeywordPerformanceLiveResultInfo`
        """
        model = KeywordsDataBingKeywordPerformanceLiveResultInfo()
        if include_optional:
            return KeywordsDataBingKeywordPerformanceLiveResultInfo(
                keyword = '',
                location_code = 56,
                language_code = '',
                year = 56,
                month = 56,
                keyword_kpi = dataforseo_client.models.keyword_kpi.KeywordKpi(
                    desktop = [
                        dataforseo_client.models.keyword_kpi_info.KeywordKpiInfo(
                            ad_position = '', 
                            clicks = 56, 
                            impressions = 56, 
                            average_cpc = 1.337, 
                            ctr = 1.337, 
                            total_cost = 56, 
                            average_bid = 1.337, )
                        ], 
                    mobile = [
                        dataforseo_client.models.keyword_kpi_info.KeywordKpiInfo(
                            ad_position = '', 
                            clicks = 56, 
                            impressions = 56, 
                            average_cpc = 1.337, 
                            ctr = 1.337, 
                            total_cost = 56, 
                            average_bid = 1.337, )
                        ], 
                    tablet = [
                        
                        ], )
            )
        else:
            return KeywordsDataBingKeywordPerformanceLiveResultInfo(
        )
        """

    def testKeywordsDataBingKeywordPerformanceLiveResultInfo(self):
        """Test KeywordsDataBingKeywordPerformanceLiveResultInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
