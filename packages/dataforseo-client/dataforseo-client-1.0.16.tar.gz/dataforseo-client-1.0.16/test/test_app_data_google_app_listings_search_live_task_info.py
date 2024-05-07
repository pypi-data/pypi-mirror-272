# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.app_data_google_app_listings_search_live_task_info import AppDataGoogleAppListingsSearchLiveTaskInfo

class TestAppDataGoogleAppListingsSearchLiveTaskInfo(unittest.TestCase):
    """AppDataGoogleAppListingsSearchLiveTaskInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AppDataGoogleAppListingsSearchLiveTaskInfo:
        """Test AppDataGoogleAppListingsSearchLiveTaskInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AppDataGoogleAppListingsSearchLiveTaskInfo`
        """
        model = AppDataGoogleAppListingsSearchLiveTaskInfo()
        if include_optional:
            return AppDataGoogleAppListingsSearchLiveTaskInfo(
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
                    dataforseo_client.models.app_data_google_app_listings_search_live_result_info.AppDataGoogleAppListingsSearchLiveResultInfo(
                        total_count = 56, 
                        count = 56, 
                        offset = 56, 
                        offset_token = '', 
                        items = [
                            dataforseo_client.models.app_datale_app_listings_search_live_item.AppDataleAppListingsSearchLiveItem(
                                app_id = '', 
                                se_domain = '', 
                                location_code = 56, 
                                language_code = '', 
                                check_url = '', 
                                time_update = '', 
                                item = dataforseo_client.models.base_app_data_serp_element_item.BaseAppDataSerpElementItem(), )
                            ], )
                    ]
            )
        else:
            return AppDataGoogleAppListingsSearchLiveTaskInfo(
        )
        """

    def testAppDataGoogleAppListingsSearchLiveTaskInfo(self):
        """Test AppDataGoogleAppListingsSearchLiveTaskInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
