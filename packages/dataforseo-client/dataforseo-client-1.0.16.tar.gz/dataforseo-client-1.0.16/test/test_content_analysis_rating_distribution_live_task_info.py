# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.content_analysis_rating_distribution_live_task_info import ContentAnalysisRatingDistributionLiveTaskInfo

class TestContentAnalysisRatingDistributionLiveTaskInfo(unittest.TestCase):
    """ContentAnalysisRatingDistributionLiveTaskInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ContentAnalysisRatingDistributionLiveTaskInfo:
        """Test ContentAnalysisRatingDistributionLiveTaskInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ContentAnalysisRatingDistributionLiveTaskInfo`
        """
        model = ContentAnalysisRatingDistributionLiveTaskInfo()
        if include_optional:
            return ContentAnalysisRatingDistributionLiveTaskInfo(
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
                    dataforseo_client.models.content_analysis_rating_distribution_live_result_info.ContentAnalysisRatingDistributionLiveResultInfo(
                        type = '', 
                        min = 1.337, 
                        max = 1.337, 
                        metrics = dataforseo_client.models.content_analysis_summary_info.ContentAnalysisSummaryInfo(
                            type = '', 
                            total_count = 56, 
                            rank = 56, 
                            top_domains = [
                                dataforseo_client.models.top_domain_info.TopDomainInfo(
                                    domain = '', 
                                    count = 56, )
                                ], 
                            sentiment_connotations = {
                                'key' : 56
                                }, 
                            connotation_types = {
                                'key' : 56
                                }, 
                            text_categories = [
                                dataforseo_client.models.content_analysis_categories_info.ContentAnalysisCategoriesInfo(
                                    category = [
                                        56
                                        ], 
                                    count = 56, )
                                ], 
                            page_categories = [
                                dataforseo_client.models.content_analysis_categories_info.ContentAnalysisCategoriesInfo(
                                    count = 56, )
                                ], 
                            page_types = {
                                'key' : 56
                                }, 
                            countries = {
                                'key' : 56
                                }, 
                            languages = {
                                'key' : 56
                                }, ), )
                    ]
            )
        else:
            return ContentAnalysisRatingDistributionLiveTaskInfo(
        )
        """

    def testContentAnalysisRatingDistributionLiveTaskInfo(self):
        """Test ContentAnalysisRatingDistributionLiveTaskInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
