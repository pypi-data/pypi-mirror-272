# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.dataforseo_labs_google_top_searches_live_result_info import DataforseoLabsGoogleTopSearchesLiveResultInfo

class TestDataforseoLabsGoogleTopSearchesLiveResultInfo(unittest.TestCase):
    """DataforseoLabsGoogleTopSearchesLiveResultInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DataforseoLabsGoogleTopSearchesLiveResultInfo:
        """Test DataforseoLabsGoogleTopSearchesLiveResultInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DataforseoLabsGoogleTopSearchesLiveResultInfo`
        """
        model = DataforseoLabsGoogleTopSearchesLiveResultInfo()
        if include_optional:
            return DataforseoLabsGoogleTopSearchesLiveResultInfo(
                se_type = '',
                location_code = 56,
                language_code = '',
                total_count = 56,
                items_count = 56,
                offset = 56,
                offset_token = '',
                items = [
                    dataforseo_client.models.keyword_data_info.KeywordDataInfo(
                        se_type = '', 
                        keyword = '', 
                        location_code = 56, 
                        language_code = '', 
                        keyword_info = dataforseo_client.models.keyword_info.KeywordInfo(
                            se_type = '', 
                            last_updated_time = '', 
                            competition = 1.337, 
                            competition_level = '', 
                            cpc = 1.337, 
                            search_volume = 56, 
                            low_top_of_page_bid = 1.337, 
                            high_top_of_page_bid = 1.337, 
                            categories = [
                                56
                                ], 
                            monthly_searches = [
                                dataforseo_client.models.monthly_searches.MonthlySearches(
                                    year = 56, 
                                    month = 56, 
                                    search_volume = 56, )
                                ], ), 
                        keyword_properties = dataforseo_client.models.keyword_properties.KeywordProperties(
                            se_type = '', 
                            core_keyword = '', 
                            synonym_clustering_algorithm = '', 
                            keyword_difficulty = 56, 
                            detected_language = '', 
                            is_another_language = True, ), 
                        impressions_info = dataforseo_client.models.impressions_info.ImpressionsInfo(
                            se_type = '', 
                            last_updated_time = '', 
                            bid = 56, 
                            match_type = '', 
                            ad_position_min = 1.337, 
                            ad_position_max = 1.337, 
                            ad_position_average = 1.337, 
                            cpc_min = 1.337, 
                            cpc_max = 1.337, 
                            cpc_average = 1.337, 
                            daily_impressions_min = 1.337, 
                            daily_impressions_max = 1.337, 
                            daily_impressions_average = 1.337, 
                            daily_clicks_min = 1.337, 
                            daily_clicks_max = 1.337, 
                            daily_clicks_average = 1.337, 
                            daily_cost_min = 1.337, 
                            daily_cost_max = 1.337, 
                            daily_cost_average = 1.337, ), 
                        serp_info = dataforseo_client.models.serp_info.SerpInfo(
                            se_type = '', 
                            check_url = '', 
                            serp_item_types = [
                                ''
                                ], 
                            se_results_count = '', 
                            last_updated_time = '', 
                            previous_updated_time = '', ), 
                        avg_backlinks_info = dataforseo_client.models.avg_backlinks_info.AvgBacklinksInfo(
                            se_type = '', 
                            backlinks = 1.337, 
                            dofollow = 1.337, 
                            referring_pages = 1.337, 
                            referring_domains = 1.337, 
                            referring_main_domains = 1.337, 
                            rank = 1.337, 
                            main_domain_rank = 1.337, 
                            last_updated_time = '', ), 
                        search_intent_info = dataforseo_client.models.search_intent_info.SearchIntentInfo(
                            se_type = '', 
                            main_intent = '', 
                            foreign_intent = [
                                ''
                                ], 
                            last_updated_time = '', ), )
                    ]
            )
        else:
            return DataforseoLabsGoogleTopSearchesLiveResultInfo(
        )
        """

    def testDataforseoLabsGoogleTopSearchesLiveResultInfo(self):
        """Test DataforseoLabsGoogleTopSearchesLiveResultInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
