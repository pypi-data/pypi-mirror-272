# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.appendix_business_data_limits_rates_data_info import AppendixBusinessDataLimitsRatesDataInfo

class TestAppendixBusinessDataLimitsRatesDataInfo(unittest.TestCase):
    """AppendixBusinessDataLimitsRatesDataInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AppendixBusinessDataLimitsRatesDataInfo:
        """Test AppendixBusinessDataLimitsRatesDataInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AppendixBusinessDataLimitsRatesDataInfo`
        """
        model = AppendixBusinessDataLimitsRatesDataInfo()
        if include_optional:
            return AppendixBusinessDataLimitsRatesDataInfo(
                google = dataforseo_client.models.appendix_business_data_google_info.AppendixBusinessDataGoogleInfo(
                    my_business_info = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), 
                    my_business_updates = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), 
                    hotel_info = dataforseo_client.models.appendix_serp_limits_rates_data_info.AppendixSerpLimitsRatesDataInfo(
                        task_post = 1.337, 
                        task_get = dataforseo_client.models.appendix_function_type_info.AppendixFunctionTypeInfo(
                            regular = 1.337, 
                            advanced = 1.337, 
                            html = 1.337, ), 
                        tasks_ready = 1.337, 
                        locations = 1.337, 
                        languages = 1.337, 
                        live = dataforseo_client.models.appendix_function_type_info.AppendixFunctionTypeInfo(
                            regular = 1.337, 
                            advanced = 1.337, 
                            html = 1.337, ), 
                        errors = 1.337, 
                        tasks_fixed = 1.337, 
                        jobs = dataforseo_client.models.appendix_jobs_serp_limits_rates_data_info.AppendixJobsSerpLimitsRatesDataInfo(
                            task_post = 1.337, ), 
                        screenshot = 1.337, ), 
                    hotel_searches = , 
                    reviews = , 
                    questions_and_answers = , ),
                locations = 1.337,
                languages = 1.337,
                errors = 1.337,
                yelp = dataforseo_client.models.appendix_business_data_day_limits_rates_data_info.AppendixBusinessDataDayLimitsRatesDataInfo(
                    reviews = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), 
                    search = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), ),
                social_media = dataforseo_client.models.appendix_social_media_business_data_limits_rates_data_info.AppendixSocialMediaBusinessDataLimitsRatesDataInfo(
                    facebook = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), 
                    pinterest = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), 
                    reddit = , ),
                tripadvisor = dataforseo_client.models.appendix_business_data_day_limits_rates_data_info.AppendixBusinessDataDayLimitsRatesDataInfo(
                    reviews = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), 
                    search = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), ),
                trustpilot = dataforseo_client.models.appendix_business_data_day_limits_rates_data_info.AppendixBusinessDataDayLimitsRatesDataInfo(
                    reviews = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), 
                    search = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), ),
                business_listings = dataforseo_client.models.appendix_business_listings_business_data_limits_rates_data_info.AppendixBusinessListingsBusinessDataLimitsRatesDataInfo(
                    search = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), 
                    categories_aggregation = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                        task_post = 1.337, 
                        task_get = 1.337, 
                        tasks_ready = 1.337, 
                        live = 1.337, ), 
                    categories = 1.337, 
                    locations = 1.337, )
            )
        else:
            return AppendixBusinessDataLimitsRatesDataInfo(
        )
        """

    def testAppendixBusinessDataLimitsRatesDataInfo(self):
        """Test AppendixBusinessDataLimitsRatesDataInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
