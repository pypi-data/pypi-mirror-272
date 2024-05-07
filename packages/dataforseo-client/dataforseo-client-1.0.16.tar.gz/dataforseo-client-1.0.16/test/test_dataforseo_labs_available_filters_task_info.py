# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.dataforseo_labs_available_filters_task_info import DataforseoLabsAvailableFiltersTaskInfo

class TestDataforseoLabsAvailableFiltersTaskInfo(unittest.TestCase):
    """DataforseoLabsAvailableFiltersTaskInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DataforseoLabsAvailableFiltersTaskInfo:
        """Test DataforseoLabsAvailableFiltersTaskInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DataforseoLabsAvailableFiltersTaskInfo`
        """
        model = DataforseoLabsAvailableFiltersTaskInfo()
        if include_optional:
            return DataforseoLabsAvailableFiltersTaskInfo(
                id = '',
                status_code = 56,
                status_message = '',
                time = '',
                cost = 1.337,
                result_count = 56,
                path = [
                    ''
                    ],
                data = dataforseo_client.models.data.data(),
                result = [
                    dataforseo_client.models.dataforseo_labs_available_filters_result_info.DataforseoLabsAvailableFiltersResultInfo(
                        related_keywords = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        keyword_suggestions = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        ranked_keywords = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        keyword_ideas = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        serp_competitors = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        relevant_pages = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        subdomains = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        competitors_domain = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        categories_for_domain = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        keywords_for_categories = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        domain_intersection = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        page_intersection = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        domain_whois_overview = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        top_searches = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        domain_metrics_by_categories = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        keywords_for_site = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        product_competitors = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        product_keyword_intersections = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        app_intersection = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        app_competitors = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        keywords_for_app = {
                            'key' : {
                                'key' : ''
                                }
                            }, 
                        database_rows_count = {
                            'key' : ''
                            }, )
                    ]
            )
        else:
            return DataforseoLabsAvailableFiltersTaskInfo(
        )
        """

    def testDataforseoLabsAvailableFiltersTaskInfo(self):
        """Test DataforseoLabsAvailableFiltersTaskInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
