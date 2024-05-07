# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.appendix_explore_keywords_data_price_data import AppendixExploreKeywordsDataPriceData

class TestAppendixExploreKeywordsDataPriceData(unittest.TestCase):
    """AppendixExploreKeywordsDataPriceData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AppendixExploreKeywordsDataPriceData:
        """Test AppendixExploreKeywordsDataPriceData
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AppendixExploreKeywordsDataPriceData`
        """
        model = AppendixExploreKeywordsDataPriceData()
        if include_optional:
            return AppendixExploreKeywordsDataPriceData(
                live = dataforseo_client.models.appendix_task_keywords_data_price_data_info.AppendixTaskKeywordsDataPriceDataInfo(
                    priority_low = [
                        dataforseo_client.models.appendix_priority_tasks_ready_keywords_data_price_data_info.AppendixPriorityTasksReadyKeywordsDataPriceDataInfo(
                            cost_type = '', 
                            cost = 1.337, )
                        ], 
                    priority_normal = [
                        dataforseo_client.models.appendix_priority_tasks_ready_keywords_data_price_data_info.AppendixPriorityTasksReadyKeywordsDataPriceDataInfo(
                            cost_type = '', 
                            cost = 1.337, )
                        ], 
                    priority_high = [
                        
                        ], ),
                task_get = dataforseo_client.models.appendix_task_keywords_data_price_data_info.AppendixTaskKeywordsDataPriceDataInfo(
                    priority_low = [
                        dataforseo_client.models.appendix_priority_tasks_ready_keywords_data_price_data_info.AppendixPriorityTasksReadyKeywordsDataPriceDataInfo(
                            cost_type = '', 
                            cost = 1.337, )
                        ], 
                    priority_normal = [
                        dataforseo_client.models.appendix_priority_tasks_ready_keywords_data_price_data_info.AppendixPriorityTasksReadyKeywordsDataPriceDataInfo(
                            cost_type = '', 
                            cost = 1.337, )
                        ], 
                    priority_high = [
                        
                        ], ),
                task_post = dataforseo_client.models.appendix_task_keywords_data_price_data_info.AppendixTaskKeywordsDataPriceDataInfo(
                    priority_low = [
                        dataforseo_client.models.appendix_priority_tasks_ready_keywords_data_price_data_info.AppendixPriorityTasksReadyKeywordsDataPriceDataInfo(
                            cost_type = '', 
                            cost = 1.337, )
                        ], 
                    priority_normal = [
                        dataforseo_client.models.appendix_priority_tasks_ready_keywords_data_price_data_info.AppendixPriorityTasksReadyKeywordsDataPriceDataInfo(
                            cost_type = '', 
                            cost = 1.337, )
                        ], 
                    priority_high = [
                        
                        ], )
            )
        else:
            return AppendixExploreKeywordsDataPriceData(
        )
        """

    def testAppendixExploreKeywordsDataPriceData(self):
        """Test AppendixExploreKeywordsDataPriceData"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
