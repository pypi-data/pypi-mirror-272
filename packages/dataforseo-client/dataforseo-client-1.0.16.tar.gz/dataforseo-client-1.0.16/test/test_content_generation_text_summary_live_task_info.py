# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.content_generation_text_summary_live_task_info import ContentGenerationTextSummaryLiveTaskInfo

class TestContentGenerationTextSummaryLiveTaskInfo(unittest.TestCase):
    """ContentGenerationTextSummaryLiveTaskInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ContentGenerationTextSummaryLiveTaskInfo:
        """Test ContentGenerationTextSummaryLiveTaskInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ContentGenerationTextSummaryLiveTaskInfo`
        """
        model = ContentGenerationTextSummaryLiveTaskInfo()
        if include_optional:
            return ContentGenerationTextSummaryLiveTaskInfo(
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
                    dataforseo_client.models.content_generation_text_summary_live_result_info.ContentGenerationTextSummaryLiveResultInfo(
                        sentences = 56, 
                        paragraphs = 56, 
                        words = 56, 
                        characters_without_spaces = 56, 
                        characters_with_spaces = 56, 
                        words_per_sentence = 1.337, 
                        characters_per_word = 1.337, 
                        vocabulary_density = 1.337, 
                        keyword_density = {
                            'key' : 56
                            }, 
                        automated_readability_index = 1.337, 
                        coleman_liau_index = 1.337, 
                        flesch_kincaid_grade_level = 1.337, 
                        smog_readability_index = 1.337, 
                        spelling_errors = 56, 
                        grammar_errors = 56, )
                    ]
            )
        else:
            return ContentGenerationTextSummaryLiveTaskInfo(
        )
        """

    def testContentGenerationTextSummaryLiveTaskInfo(self):
        """Test ContentGenerationTextSummaryLiveTaskInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
