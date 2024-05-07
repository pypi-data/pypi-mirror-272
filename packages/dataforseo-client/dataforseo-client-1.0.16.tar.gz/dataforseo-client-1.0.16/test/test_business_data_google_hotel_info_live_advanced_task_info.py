# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.business_data_google_hotel_info_live_advanced_task_info import BusinessDataGoogleHotelInfoLiveAdvancedTaskInfo

class TestBusinessDataGoogleHotelInfoLiveAdvancedTaskInfo(unittest.TestCase):
    """BusinessDataGoogleHotelInfoLiveAdvancedTaskInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> BusinessDataGoogleHotelInfoLiveAdvancedTaskInfo:
        """Test BusinessDataGoogleHotelInfoLiveAdvancedTaskInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `BusinessDataGoogleHotelInfoLiveAdvancedTaskInfo`
        """
        model = BusinessDataGoogleHotelInfoLiveAdvancedTaskInfo()
        if include_optional:
            return BusinessDataGoogleHotelInfoLiveAdvancedTaskInfo(
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
                    dataforseo_client.models.business_data_google_hotel_info_live_advanced_result_info.BusinessDataGoogleHotelInfoLiveAdvancedResultInfo(
                        hotel_identifier = '', 
                        location_code = 56, 
                        language_code = '', 
                        check_url = '', 
                        datetime = '', 
                        title = '', 
                        stars = 56, 
                        stars_description = '', 
                        address = '', 
                        phone = '', 
                        about = dataforseo_client.models.hotel_about_info.HotelAboutInfo(
                            description = '', 
                            sub_descriptions = [
                                ''
                                ], 
                            check_in_time = dataforseo_client.models.work_time_info.WorkTimeInfo(
                                hour = 56, 
                                minute = 56, ), 
                            check_out_time = dataforseo_client.models.work_time_info.WorkTimeInfo(
                                hour = 56, 
                                minute = 56, ), 
                            full_address = '', 
                            domain = '', 
                            url = '', 
                            amenities = [
                                dataforseo_client.models.hotel_amenity_info.HotelAmenityInfo(
                                    category = '', 
                                    category_label = '', 
                                    items = [
                                        dataforseo_client.models.hotel_amenity_item_info.HotelAmenityItemInfo(
                                            amenity = '', 
                                            amenity_label = '', 
                                            hint = '', 
                                            hint_label = '', )
                                        ], )
                                ], 
                            popular_amenities = [
                                dataforseo_client.models.hotel_amenity_item_info.HotelAmenityItemInfo(
                                    amenity = '', 
                                    amenity_label = '', 
                                    hint = '', 
                                    hint_label = '', )
                                ], ), 
                        location = dataforseo_client.models.location.Location(
                            neighborhood = '', 
                            neighborhood_description = '', 
                            maps_url = '', 
                            overall_score = 1.337, 
                            score_by_categories = dataforseo_client.models.score_by_categories.ScoreByCategories(
                                overall = 1.337, 
                                things_to_do = 1.337, 
                                restaurants = 1.337, 
                                transit = 1.337, 
                                airport_access = 1.337, ), 
                            latitude = 1.337, 
                            longitude = 1.337, 
                            location_chain = [
                                dataforseo_client.models.location_chain.LocationChain(
                                    card_id = '', 
                                    feature_id = '', 
                                    cid = '', 
                                    title = '', )
                                ], ), 
                        reviews = dataforseo_client.models.hotel_review_info.HotelReviewInfo(
                            value = 1.337, 
                            votes_count = 56, 
                            mentions = [
                                dataforseo_client.models.review_mention_info.ReviewMentionInfo(
                                    title = '', 
                                    positive_score = 1.337, 
                                    positive_count = 56, 
                                    negative_count = 56, 
                                    total_count = 56, 
                                    visible_by_default = True, )
                                ], 
                            rating_distribution = {
                                'key' : 56
                                }, 
                            other_sites_reviews = [
                                dataforseo_client.models.other_sites_reviews_info.OtherSitesReviewsInfo(
                                    title = '', 
                                    url = '', 
                                    review_text = '', 
                                    rating = dataforseo_client.models.rating_info.RatingInfo(
                                        rating_type = '', 
                                        value = 1.337, 
                                        votes_count = 56, 
                                        rating_max = 56, ), )
                                ], ), 
                        overview_images = [
                            ''
                            ], 
                        prices = dataforseo_client.models.hotel_price_info.HotelPriceInfo(
                            price = 56, 
                            price_without_discount = 56, 
                            currency = '', 
                            discount_text = '', 
                            check_in = '', 
                            check_out = '', 
                            visitors = 56, ), )
                    ]
            )
        else:
            return BusinessDataGoogleHotelInfoLiveAdvancedTaskInfo(
        )
        """

    def testBusinessDataGoogleHotelInfoLiveAdvancedTaskInfo(self):
        """Test BusinessDataGoogleHotelInfoLiveAdvancedTaskInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
