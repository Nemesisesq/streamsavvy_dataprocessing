# from behave import *
#
# from data_processor.sorter import get_package_channels
#
# use_step_matcher("re")
# x = {
#     "url": "http://0.0.0.0:8000/api/package/2346/",
#     "data": {
#         "services": [],
#         "hardware": [],
#         "content": [
#             {
#                 "channel": [
#                     {
#                         "display_name": "Amazon",
#                         "name": "Amazon",
#                         "modified": "2016-02-26T02:36:39.458106Z",
#                         "url": "http://localhost:8000/api/services/80/",
#                         "source": "amazon",
#                         "guidebox_data": {
#                             "artwork_608x342": "http://static-api.guidebox.com/041014/thumbnails_xlarge/140-5569024100-608x342-channel.jpg",
#                             "id": 140,
#                             "channel_type": "online",
#                             "name": "Amazon",
#                             "external_ids": {
#                                 "imdb": 'null',
#                                 "wikipedia_id": 'null'
#                             },
#                             "artwork_304x171": "http://static-api.guidebox.com/041014/thumbnails_medium/140-2284897161-304x171-channel.jpg",
#                             "artwork_448x252": "http://static-api.guidebox.com/041014/thumbnails_large/140-6702848975-448x252-channel.jpg",
#                             "live_stream": {
#                                 "web": [],
#                                 "android": [],
#                                 "ios": []
#                             },
#                             "social": {
#                                 "facebook": {
#                                     "facebook_id": 'null',
#                                     "link": 'null'
#                                 },
#                                 "twitter": {
#                                     "twitter_id": 'null',
#                                     "link": 'null'
#                                 }
#                             },
#                             "artwork_208x117": "http://static-api.guidebox.com/041014/thumbnails_small/140-8624025415-208x117-channel.jpg",
#                             "short_name": "amazon"
#                         },
#                         "is_on_sling": 'false'
#                     }
#                 ],
#                 "modified": "2016-06-22T13:18:05.544923Z",
#                 "channels_last_checked": "2016-05-24T23:44:13.497163Z",
#                 "on_netflix": 'false',
#                 "guidebox_data": {
#                     "tvdb": 277928,
#                     "id": 19367,
#                     "detail": {
#                         "runtime": 60,
#                         "air_day_of_week": "Friday",
#                         "id": 19367,
#                         "fanart": "http://static-api.guidebox.com/041014/fanart/19367-0-0-0-20060042029-469885550-31802556275-tv.jpg",
#                         "tv_com": "http://www.tv.com/shows/bosch/",
#                         "imdb_id": "tt3502248",
#                         "type": "online",
#                         "overview": "For LAPD homicide cop Harry Bosch — hero, maverick, nighthawk. From a dangerous maze of blind alleys to a daring criminal heist beneath the city to the tortuous link that must be uncovered, his survival instincts will be tested to their limit. Joining with an enigmatic and seductive female FBI agent, pitted against enemies inside his own department, Bosch must make the agonizing choice between justice and vengeance, as he tracks down a killer whose ''true'' face will shock him.",
#                         "title": "Bosch",
#                         "tags": [
#                             {
#                                 "tag": "police",
#                                 "id": 125
#                             },
#                             {
#                                 "tag": "lapd",
#                                 "id": 154
#                             },
#                             {
#                                 "tag": "murder suspect",
#                                 "id": 196
#                             },
#                             {
#                                 "tag": "homicide detective",
#                                 "id": 197
#                             },
#                             {
#                                 "tag": "child murder",
#                                 "id": 198
#                             },
#                             {
#                                 "tag": "los angeles",
#                                 "id": 153
#                             },
#                             {
#                                 "tag": "murder trial",
#                                 "id": 199
#                             },
#                             {
#                                 "tag": "los angeles california",
#                                 "id": 1628
#                             },
#                             {
#                                 "tag": "police procedural",
#                                 "id": 6056
#                             }
#                         ],
#                         "status": "Continuing",
#                         "cast": [
#                             {
#                                 "id": 314424,
#                                 "character_name": "Harry Bosch",
#                                 "name": "Titus Welliver"
#                             }
#                         ],
#                         "channels": [
#                             {
#                                 "is_primary": 1,
#                                 "id": 140,
#                                 "artwork_448x252": "http://static-api.guidebox.com/041014/thumbnails_large/140-6702848975-448x252-channel.jpg",
#                                 "live_stream": {
#                                     "web": [],
#                                     "android": [],
#                                     "ios": []
#                                 },
#                                 "social": {
#                                     "facebook": {
#                                         "facebook_id": 'null',
#                                         "link": 'null'
#                                     },
#                                     "twitter": {
#                                         "twitter_id": 'null',
#                                         "link": 'null'
#                                     }
#                                 },
#                                 "short_name": "amazon",
#                                 "name": "Amazon",
#                                 "external_ids": {
#                                     "imdb": 'null',
#                                     "wikipedia_id": 'null'
#                                 },
#                                 "artwork_608x342": "http://static-api.guidebox.com/041014/thumbnails_xlarge/140-5569024100-608x342-channel.jpg",
#                                 "artwork_304x171": "http://static-api.guidebox.com/041014/thumbnails_medium/140-2284897161-304x171-channel.jpg",
#                                 "artwork_208x117": "http://static-api.guidebox.com/041014/thumbnails_small/140-8624025415-208x117-channel.jpg",
#                                 "channel_type": "online"
#                             }
#                         ],
#                         "air_time": "22:00",
#                         "common_sense_media": "https://www.commonsensemedia.org/tv-reviews/bosch",
#                         "artwork_304x171": "http://static-api.guidebox.com/022615/thumbnails_medium/19367-8667029398-304x171-show-thumbnail.jpg",
#                         "tvrage": {
#                             "link": "http://www.tvrage.com/shows/id-36430",
#                             "tvrage_id": 36430
#                         },
#                         "wikipedia_id": 41974768,
#                         "artwork_448x252": "http://static-api.guidebox.com/022615/thumbnails_large/19367-7142098904-448x252-show-thumbnail.jpg",
#                         "network": "Amazon",
#                         "tvdb": 277928,
#                         "banner": "http://static-api.guidebox.com/041014/banner/19367-0-0-0-69111000706-134276400955-17748567280-tv.jpg",
#                         "alternate_titles": [],
#                         "container_show": 0,
#                         "poster": "http://static-api.guidebox.com/012915/shows/posters/19367-4311514050-2932933876-2762629208-600x855.jpg",
#                         "genres": [
#                             {
#                                 "id": 7,
#                                 "title": "Crime"
#                             },
#                             {
#                                 "id": 9,
#                                 "title": "Drama"
#                             },
#                             {
#                                 "id": 17,
#                                 "title": "Mystery"
#                             }
#                         ],
#                         "url": "http://www.guidebox.com/#!AMAZON/19367-Bosch/full-episodes",
#                         "first_aired": "2015-02-13",
#                         "social": {
#                             "facebook": {
#                                 "facebook_id": 0,
#                                 "link": "https://www.facebook.com/BoschAmazon"
#                             },
#                             "twitter": {
#                                 "twitter_id": 2149613827,
#                                 "link": "https://twitter.com/BoschAmazon"
#                             }
#                         },
#                         "artwork_608x342": "http://static-api.guidebox.com/022615/thumbnails_xlarge/19367-862685997-608x342-show-thumbnail.jpg",
#                         "metacritic": "http://www.metacritic.com/tv/bosch",
#                         "artwork_208x117": "http://static-api.guidebox.com/022615/thumbnails_small/19367-6216263687-208x117-show-thumbnail.jpg",
#                         "freebase": "/m/0_s4fhj",
#                         "rating": "TV-MA",
#                         "themoviedb": 60585
#                     },
#                     "artwork_448x252": "http://static-api.guidebox.com/022615/thumbnails_large/19367-7142098904-448x252-show-thumbnail.jpg",
#                     "sources": {
#                         "web": {
#                             "clips": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "episodes": {
#                                 "total": 20,
#                                 "free": 0,
#                                 "subscription": 20,
#                                 "all_sources": [
#                                     {
#                                         "type": "subscription",
#                                         "id": 13,
#                                         "display_name": "Amazon Prime",
#                                         "source": "amazon_prime"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 146,
#                                         "display_name": "Amazon",
#                                         "source": "amazon_buy"
#                                     }
#                                 ],
#                                 "tv_everywhere": 0,
#                                 "paid": 10
#                             },
#                             "segments": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             }
#                         },
#                         "android": {
#                             "clips": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "episodes": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "segments": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             }
#                         },
#                         "ios": {
#                             "clips": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "episodes": {
#                                 "total": 20,
#                                 "free": 0,
#                                 "subscription": 20,
#                                 "all_sources": [
#                                     {
#                                         "type": "subscription",
#                                         "id": 13,
#                                         "display_name": "Amazon Prime",
#                                         "source": "amazon_prime"
#                                     }
#                                 ],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "segments": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             }
#                         }
#                     },
#                     "imdb_id": "tt3502248",
#                     "container_show": 0,
#                     "freebase": "/m/0_s4fhj",
#                     "title": "Bosch",
#                     "tvrage": {
#                         "link": "http://www.tvrage.com/shows/id-36430",
#                         "tvrage_id": 36430
#                     },
#                     "first_aired": "2015-02-13",
#                     "alternate_titles": [],
#                     "artwork_608x342": "http://static-api.guidebox.com/022615/thumbnails_xlarge/19367-862685997-608x342-show-thumbnail.jpg",
#                     "artwork_304x171": "http://static-api.guidebox.com/022615/thumbnails_medium/19367-8667029398-304x171-show-thumbnail.jpg",
#                     "artwork_208x117": "http://static-api.guidebox.com/022615/thumbnails_small/19367-6216263687-208x117-show-thumbnail.jpg",
#                     "wikipedia_id": 41974768,
#                     "themoviedb": 60585
#                 },
#                 "title": "Bosch",
#                 "justAdded": 'true',
#                 "url": "http://localhost:8000/api/content/352/"
#             },
#             {
#                 "channel": [
#                     {
#                         "display_name": "FOX",
#                         "name": "FOX",
#                         "modified": "2016-05-23T04:29:33.405360Z",
#                         "url": "http://localhost:8000/api/services/9/",
#                         "source": "fox",
#                         "guidebox_data": {
#                             "id": 4,
#                             "external_ids": {
#                                 "imdb": "co0070925",
#                                 "wikipedia_id": 46252
#                             },
#                             "live_stream": {
#                                 "web": [],
#                                 "android": [],
#                                 "ios": []
#                             },
#                             "social": {
#                                 "facebook": {
#                                     "facebook_id": 45002877992,
#                                     "link": "https://www.facebook.com/FOXTV"
#                                 },
#                                 "twitter": {
#                                     "twitter_id": 16537989,
#                                     "link": "https://twitter.com/FOXTV"
#                                 }
#                             },
#                             "is_over_the_air": "'true'",
#                             "short_name": "fox",
#                             "name": "FOX",
#                             "artwork_608x342": "http://static-api.guidebox.com/060515/thumbnails_xlarge/4-6226862594-608x342-channel.jpg",
#                             "artwork_448x252": "http://static-api.guidebox.com/060515/thumbnails_large/4-8287207526-448x252-channel.jpg",
#                             "artwork_304x171": "http://static-api.guidebox.com/060515/thumbnails_medium/4-938629993-304x171-channel.jpg",
#                             "artwork_208x117": "http://static-api.guidebox.com/060515/thumbnails_small/4-9622087343-208x117-channel.jpg",
#                             "channel_type": "television"
#                         },
#                         "is_over_the_air": "'true'",
#                         "is_on_sling": 'false'
#                     }
#                 ],
#                 "modified": "2016-06-22T13:21:35.973748Z",
#                 "channels_last_checked": 'null',
#                 "on_netflix": 'false',
#                 "guidebox_data": {
#                     "tvdb": 259007,
#                     "id": 12990,
#                     "detail": {
#                         "runtime": 30,
#                         "air_day_of_week": "Tuesday",
#                         "id": 12990,
#                         "fanart": "http://static-api.guidebox.com/041014/fanart/12990-0-0-0-50571728133-130563014389-5994291702-tv.jpg",
#                         "tv_com": "http://www.tv.com/shows/the-mindy-project/",
#                         "imdb_id": "tt2211129",
#                         "type": "television",
#                         "overview": "Mindy Lahiri can quote every romantic comedy starring Meg Ryan that exists. She loves the good ones and the bad ones, because the girl always gets the guy. Mindy is determined to be more punctual, spend less money, lose weight and read more books – all in pursuit of becoming a well-rounded perfect woman…who can meet and date the perfect guy. Mindy is a skilled OB/GYN and shares a practice with a few other doctors, none of whom make life any easier for her. Jeremy Reed is the walking definition of total bad news. He not only shares a practice with Mindy, but sometimes her bed as well – despite her best efforts to resist. He is funny, self-absorbed and super sexy. In contrast, Danny Castellano is a hothead and guys’ guy who has a habit of stealing Mindy’s patients. As Mindy attempts to get her career off the ground and meet a guy who passes her red flag test, only time will tell if she gets her romantic comedy ending.",
#                         "title": "The Mindy Project",
#                         "tags": [
#                             {
#                                 "tag": "indian",
#                                 "id": 1932
#                             },
#                             {
#                                 "tag": "gynecologist",
#                                 "id": 1380
#                             },
#                             {
#                                 "tag": "new york",
#                                 "id": 21
#                             },
#                             {
#                                 "tag": "workplace humor",
#                                 "id": 242
#                             },
#                             {
#                                 "tag": "workplace romance",
#                                 "id": 239
#                             },
#                             {
#                                 "tag": "sitcom",
#                                 "id": 54
#                             },
#                             {
#                                 "tag": "co worker",
#                                 "id": 4461
#                             },
#                             {
#                                 "tag": "doctor",
#                                 "id": 8
#                             },
#                             {
#                                 "tag": "female lead",
#                                 "id": 781
#                             },
#                             {
#                                 "tag": "female protagonist",
#                                 "id": 396
#                             },
#                             {
#                                 "tag": "new york city",
#                                 "id": 2297
#                             }
#                         ],
#                         "status": "Continuing",
#                         "cast": [
#                             {
#                                 "id": 459952,
#                                 "character_name": "Mindy Lahiri",
#                                 "name": "Mindy Kaling"
#                             },
#                             {
#                                 "id": 466262,
#                                 "character_name": "Danny Castellano",
#                                 "name": "Chris Messina"
#                             },
#                             {
#                                 "id": 55540,
#                                 "character_name": "Jeremy Reed",
#                                 "name": "Ed Weeks"
#                             },
#                             {
#                                 "id": 467571,
#                                 "character_name": "Morgan Tookers",
#                                 "name": "Ike Barinholtz"
#                             },
#                             {
#                                 "id": 212781,
#                                 "character_name": "Beverly",
#                                 "name": "Beth Grant"
#                             }
#                         ],
#                         "channels": [
#                             {
#                                 "is_primary": 1,
#                                 "id": 4,
#                                 "artwork_448x252": "http://static-api.guidebox.com/060515/thumbnails_large/4-8287207526-448x252-channel.jpg",
#                                 "live_stream": {
#                                     "web": [],
#                                     "android": [],
#                                     "ios": []
#                                 },
#                                 "social": {
#                                     "facebook": {
#                                         "facebook_id": 45002877992,
#                                         "link": "https://www.facebook.com/FOXTV"
#                                     },
#                                     "twitter": {
#                                         "twitter_id": 16537989,
#                                         "link": "https://twitter.com/FOXTV"
#                                     }
#                                 },
#                                 "short_name": "fox",
#                                 "name": "FOX",
#                                 "external_ids": {
#                                     "imdb": "co0070925",
#                                     "wikipedia_id": 46252
#                                 },
#                                 "artwork_608x342": "http://static-api.guidebox.com/060515/thumbnails_xlarge/4-6226862594-608x342-channel.jpg",
#                                 "artwork_304x171": "http://static-api.guidebox.com/060515/thumbnails_medium/4-938629993-304x171-channel.jpg",
#                                 "artwork_208x117": "http://static-api.guidebox.com/060515/thumbnails_small/4-9622087343-208x117-channel.jpg",
#                                 "channel_type": "television"
#                             }
#                         ],
#                         "air_time": "9:30 PM",
#                         "common_sense_media": "https://www.commonsensemedia.org/tv-reviews/the-mindy-project",
#                         "artwork_304x171": "http://static-api.guidebox.com/120214/thumbnails_medium/12990-1997713819-304x171-show-thumbnail.jpg",
#                         "tvrage": {
#                             "link": "http://www.tvrage.com/shows/id-31682",
#                             "tvrage_id": 31682
#                         },
#                         "wikipedia_id": 35801977,
#                         "artwork_448x252": "http://static-api.guidebox.com/120214/thumbnails_large/12990-6980853104-448x252-show-thumbnail.jpg",
#                         "network": "Hulu",
#                         "tvdb": 259007,
#                         "banner": "http://static-api.guidebox.com/041014/banner/12990-0-0-0-106018247846-102450384370-3448266065-tv.jpg",
#                         "alternate_titles": [],
#                         "container_show": 0,
#                         "poster": "http://static-api.guidebox.com/012915/shows/posters/12990-1177758887-5685946448-3521592147-600x855.jpg",
#                         "genres": [
#                             {
#                                 "id": 6,
#                                 "title": "Comedy"
#                             }
#                         ],
#                         "url": "http://www.guidebox.com/#!FOX/12990-The-Mindy-Project/full-episodes",
#                         "first_aired": "2012-09-25",
#                         "social": {
#                             "facebook": {
#                                 "facebook_id": 407288339301542,
#                                 "link": "https://www.facebook.com/TheMindyProject"
#                             },
#                             "twitter": {
#                                 "twitter_id": 577403888,
#                                 "link": "https://twitter.com/TheMindyProject"
#                             }
#                         },
#                         "artwork_608x342": "http://static-api.guidebox.com/120214/thumbnails_xlarge/12990-4716415531-608x342-show-thumbnail.jpg",
#                         "metacritic": "http://www.metacritic.com/tv/the-mindy-project",
#                         "artwork_208x117": "http://static-api.guidebox.com/120214/thumbnails_small/12990-9636425478-208x117-show-thumbnail.jpg",
#                         "freebase": "/m/0jt1q7m",
#                         "rating": "TV-14",
#                         "themoviedb": 44857
#                     },
#                     "artwork_448x252": "http://static-api.guidebox.com/120214/thumbnails_large/12990-6980853104-448x252-show-thumbnail.jpg",
#                     "sources": {
#                         "web": {
#                             "clips": {
#                                 "total": 11,
#                                 "free": 11,
#                                 "subscription": 0,
#                                 "all_sources": [
#                                     {
#                                         "type": "free",
#                                         "id": 1,
#                                         "display_name": "Hulu",
#                                         "source": "hulu_free"
#                                     }
#                                 ],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "episodes": {
#                                 "total": 91,
#                                 "free": 1,
#                                 "subscription": 90,
#                                 "all_sources": [
#                                     {
#                                         "type": "subscription",
#                                         "id": 10,
#                                         "display_name": "Hulu",
#                                         "source": "hulu_plus"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 145,
#                                         "display_name": "iTunes",
#                                         "source": "itunes"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 147,
#                                         "display_name": "VUDU",
#                                         "source": "vudu"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 146,
#                                         "display_name": "Amazon",
#                                         "source": "amazon_buy"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 148,
#                                         "display_name": "Google Play",
#                                         "source": "google_play"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 157,
#                                         "display_name": "YouTube",
#                                         "source": "youtube_purchase"
#                                     },
#                                     {
#                                         "type": "free",
#                                         "id": 1,
#                                         "display_name": "Hulu",
#                                         "source": "hulu_free"
#                                     }
#                                 ],
#                                 "tv_everywhere": 0,
#                                 "paid": 67
#                             },
#                             "segments": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             }
#                         },
#                         "android": {
#                             "clips": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "episodes": {
#                                 "total": 91,
#                                 "free": 0,
#                                 "subscription": 91,
#                                 "all_sources": [
#                                     {
#                                         "type": "subscription",
#                                         "id": 10,
#                                         "display_name": "Hulu",
#                                         "source": "hulu_plus"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 147,
#                                         "display_name": "VUDU",
#                                         "source": "vudu"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 148,
#                                         "display_name": "Google Play",
#                                         "source": "google_play"
#                                     }
#                                 ],
#                                 "tv_everywhere": 0,
#                                 "paid": 67
#                             },
#                             "segments": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             }
#                         },
#                         "ios": {
#                             "clips": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "episodes": {
#                                 "total": 91,
#                                 "free": 0,
#                                 "subscription": 91,
#                                 "all_sources": [
#                                     {
#                                         "type": "subscription",
#                                         "id": 10,
#                                         "display_name": "Hulu",
#                                         "source": "hulu_plus"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 145,
#                                         "display_name": "iTunes",
#                                         "source": "itunes"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 147,
#                                         "display_name": "VUDU",
#                                         "source": "vudu"
#                                     }
#                                 ],
#                                 "tv_everywhere": 0,
#                                 "paid": 67
#                             },
#                             "segments": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             }
#                         }
#                     },
#                     "imdb_id": "tt2211129",
#                     "container_show": 0,
#                     "freebase": "/m/0jt1q7m",
#                     "title": "The Mindy Project",
#                     "tvrage": {
#                         "link": "http://www.tvrage.com/shows/id-31682",
#                         "tvrage_id": 31682
#                     },
#                     "first_aired": "2012-09-25",
#                     "alternate_titles": [],
#                     "artwork_608x342": "http://static-api.guidebox.com/120214/thumbnails_xlarge/12990-4716415531-608x342-show-thumbnail.jpg",
#                     "artwork_304x171": "http://static-api.guidebox.com/120214/thumbnails_medium/12990-1997713819-304x171-show-thumbnail.jpg",
#                     "artwork_208x117": "http://static-api.guidebox.com/120214/thumbnails_small/12990-9636425478-208x117-show-thumbnail.jpg",
#                     "wikipedia_id": 35801977,
#                     "themoviedb": 44857
#                 },
#                 "title": "The Mindy Project",
#                 "justAdded": 'true',
#                 "url": "http://localhost:8000/api/content/285/"
#             },
#             {
#                 "channel": [
#                     {
#                         "display_name": "Misc",
#                         "name": "Misc",
#                         "modified": "2016-02-26T02:36:32.228539Z",
#                         "url": "http://localhost:8000/api/services/16/",
#                         "source": "misc_shows",
#                         "guidebox_data": {
#                             "artwork_608x342": "http://static-api.guidebox.com/041014/thumbnails_xlarge/97-3512137644-608x342-channel.jpg",
#                             "id": 97,
#                             "channel_type": "online",
#                             "name": "Misc",
#                             "external_ids": {
#                                 "imdb": 'null',
#                                 "wikipedia_id": 'null'
#                             },
#                             "artwork_304x171": "http://static-api.guidebox.com/041014/thumbnails_medium/97-9804287133-304x171-channel.jpg",
#                             "artwork_448x252": "http://static-api.guidebox.com/041014/thumbnails_large/97-7645400767-448x252-channel.jpg",
#                             "live_stream": {
#                                 "web": [],
#                                 "android": [],
#                                 "ios": []
#                             },
#                             "social": {
#                                 "facebook": {
#                                     "facebook_id": 'null',
#                                     "link": 'null'
#                                 },
#                                 "twitter": {
#                                     "twitter_id": 'null',
#                                     "link": 'null'
#                                 }
#                             },
#                             "artwork_208x117": "http://static-api.guidebox.com/041014/thumbnails_small/97-3607915244-208x117-channel.jpg",
#                             "short_name": "misc_shows"
#                         },
#                         "is_on_sling": 'false'
#                     }
#                 ],
#                 "modified": "2016-06-17T13:51:08.853943Z",
#                 "channels_last_checked": 'null',
#                 "on_netflix": 'false',
#                 "guidebox_data": {
#                     "tvdb": 279392,
#                     "id": 17779,
#                     "detail": {
#                         "runtime": 25,
#                         "air_day_of_week": "Wednesday",
#                         "id": 17779,
#                         "fanart": "http://static-api.guidebox.com/041014/fanart/17779-0-0-0-203721011140-135386436610-8282211220-tv.jpg",
#                         "tv_com": 'null',
#                         "imdb_id": "tt3147316",
#                         "type": "online",
#                         "overview": "Kevin Pacalioglu may have no money and no clue, but he can see dead people, so that’s pretty cool. Faced with a constant stream of stubborn spirits, Pac goes to whatever lengths require the least amount of effort to help New York City’s most frivolous ghosts finish their unfinished business.",
#                         "title": "Deadbeat",
#                         "tags": [
#                             {
#                                 "tag": "ghost",
#                                 "id": 812
#                             }
#                         ],
#                         "status": "Continuing",
#                         "cast": [
#                             {
#                                 "id": 410786,
#                                 "character_name": "Kevin Pacalioglu",
#                                 "name": "Tyler Labine"
#                             },
#                             {
#                                 "id": 554599,
#                                 "character_name": "Clyde",
#                                 "name": "Kal Penn"
#                             },
#                             {
#                                 "id": 82541,
#                                 "character_name": "Camomile White",
#                                 "name": "Cat Deeley"
#                             },
#                             {
#                                 "id": 40271,
#                                 "character_name": "Roofie",
#                                 "name": "Brandon T. Jackson"
#                             },
#                             {
#                                 "id": 98909,
#                                 "character_name": "Sue",
#                                 "name": "Lucy DeVito"
#                             }
#                         ],
#                         "channels": [
#                             {
#                                 "is_primary": 1,
#                                 "id": 97,
#                                 "artwork_448x252": "http://static-api.guidebox.com/041014/thumbnails_large/97-7645400767-448x252-channel.jpg",
#                                 "live_stream": {
#                                     "web": [],
#                                     "android": [],
#                                     "ios": []
#                                 },
#                                 "social": {
#                                     "facebook": {
#                                         "facebook_id": 'null',
#                                         "link": 'null'
#                                     },
#                                     "twitter": {
#                                         "twitter_id": 'null',
#                                         "link": 'null'
#                                     }
#                                 },
#                                 "short_name": "misc_shows",
#                                 "name": "Misc",
#                                 "external_ids": {
#                                     "imdb": 'null',
#                                     "wikipedia_id": 'null'
#                                 },
#                                 "artwork_608x342": "http://static-api.guidebox.com/041014/thumbnails_xlarge/97-3512137644-608x342-channel.jpg",
#                                 "artwork_304x171": "http://static-api.guidebox.com/041014/thumbnails_medium/97-9804287133-304x171-channel.jpg",
#                                 "artwork_208x117": "http://static-api.guidebox.com/041014/thumbnails_small/97-3607915244-208x117-channel.jpg",
#                                 "channel_type": "online"
#                             }
#                         ],
#                         "air_time": "",
#                         "common_sense_media": 'null',
#                         "artwork_304x171": "http://static-api.guidebox.com/thumbs03_14/thumbnails_medium/17779-4971915255-304x171.jpg",
#                         "tvrage": {
#                             "link": "http://www.tvrage.com/shows/id-37477",
#                             "tvrage_id": 37477
#                         },
#                         "wikipedia_id": 42444704,
#                         "artwork_448x252": "http://static-api.guidebox.com/thumbs03_14/thumbnails_large/17779-3331402964-448x252.jpg",
#                         "network": "Hulu",
#                         "tvdb": 279392,
#                         "banner": "http://static-api.guidebox.com/041014/banner/17779-0-0-0-12333602267-28627317945-39326661097-tv.jpg",
#                         "alternate_titles": [],
#                         "container_show": 0,
#                         "poster": "http://static-api.guidebox.com/012915/shows/posters/17779-8437148370-5769506944-8946089400-600x855.jpg",
#                         "genres": [
#                             {
#                                 "id": 6,
#                                 "title": "Comedy"
#                             }
#                         ],
#                         "url": "http://www.guidebox.com/#!MISC/17779-Deadbeat/full-episodes",
#                         "first_aired": "2014-04-09",
#                         "social": {
#                             "facebook": {
#                                 "facebook_id": 675848615827775,
#                                 "link": "https://www.facebook.com/pages/Deadbeat/675848615827775"
#                             },
#                             "twitter": {
#                                 "twitter_id": 'null',
#                                 "link": 'null'
#                             }
#                         },
#                         "artwork_608x342": "http://static-api.guidebox.com/thumbs03_14/thumbnails_xlarge/17779-6773993899-608x342.jpg",
#                         "metacritic": 'null',
#                         "artwork_208x117": "http://static-api.guidebox.com/thumbs03_14/thumbnails_small/17779-338286772-208x117.jpg",
#                         "freebase": "/m/0106bhw5",
#                         "rating": "TV-14",
#                         "themoviedb": 62234
#                     },
#                     "artwork_448x252": "http://static-api.guidebox.com/thumbs03_14/thumbnails_large/17779-3331402964-448x252.jpg",
#                     "sources": {
#                         "web": {
#                             "clips": {
#                                 "total": 32,
#                                 "free": 32,
#                                 "subscription": 0,
#                                 "all_sources": [
#                                     {
#                                         "type": "free",
#                                         "id": 1,
#                                         "display_name": "Hulu",
#                                         "source": "hulu_free"
#                                     }
#                                 ],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "episodes": {
#                                 "total": 23,
#                                 "free": 10,
#                                 "subscription": 13,
#                                 "all_sources": [
#                                     {
#                                         "type": "free",
#                                         "id": 1,
#                                         "display_name": "Hulu",
#                                         "source": "hulu_free"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 147,
#                                         "display_name": "VUDU",
#                                         "source": "vudu"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 146,
#                                         "display_name": "Amazon",
#                                         "source": "amazon_buy"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 148,
#                                         "display_name": "Google Play",
#                                         "source": "google_play"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 157,
#                                         "display_name": "YouTube",
#                                         "source": "youtube_purchase"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 145,
#                                         "display_name": "iTunes",
#                                         "source": "itunes"
#                                     },
#                                     {
#                                         "type": "subscription",
#                                         "id": 10,
#                                         "display_name": "Hulu",
#                                         "source": "hulu_plus"
#                                     }
#                                 ],
#                                 "tv_everywhere": 0,
#                                 "paid": 23
#                             },
#                             "segments": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             }
#                         },
#                         "android": {
#                             "clips": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "episodes": {
#                                 "total": 23,
#                                 "free": 0,
#                                 "subscription": 23,
#                                 "all_sources": [
#                                     {
#                                         "type": "purchase",
#                                         "id": 147,
#                                         "display_name": "VUDU",
#                                         "source": "vudu"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 148,
#                                         "display_name": "Google Play",
#                                         "source": "google_play"
#                                     },
#                                     {
#                                         "type": "subscription",
#                                         "id": 10,
#                                         "display_name": "Hulu",
#                                         "source": "hulu_plus"
#                                     }
#                                 ],
#                                 "tv_everywhere": 0,
#                                 "paid": 23
#                             },
#                             "segments": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             }
#                         },
#                         "ios": {
#                             "clips": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             },
#                             "episodes": {
#                                 "total": 23,
#                                 "free": 0,
#                                 "subscription": 23,
#                                 "all_sources": [
#                                     {
#                                         "type": "purchase",
#                                         "id": 147,
#                                         "display_name": "VUDU",
#                                         "source": "vudu"
#                                     },
#                                     {
#                                         "type": "purchase",
#                                         "id": 145,
#                                         "display_name": "iTunes",
#                                         "source": "itunes"
#                                     },
#                                     {
#                                         "type": "subscription",
#                                         "id": 10,
#                                         "display_name": "Hulu",
#                                         "source": "hulu_plus"
#                                     }
#                                 ],
#                                 "tv_everywhere": 0,
#                                 "paid": 23
#                             },
#                             "segments": {
#                                 "total": 0,
#                                 "free": 0,
#                                 "subscription": 0,
#                                 "all_sources": [],
#                                 "tv_everywhere": 0,
#                                 "paid": 0
#                             }
#                         }
#                     },
#                     "imdb_id": "tt3147316",
#                     "container_show": 0,
#                     "freebase": "/m/0106bhw5",
#                     "title": "Deadbeat",
#                     "tvrage": {
#                         "link": "http://www.tvrage.com/shows/id-37477",
#                         "tvrage_id": 37477
#                     },
#                     "first_aired": "2014-04-09",
#                     "alternate_titles": [],
#                     "artwork_608x342": "http://static-api.guidebox.com/thumbs03_14/thumbnails_xlarge/17779-6773993899-608x342.jpg",
#                     "artwork_304x171": "http://static-api.guidebox.com/thumbs03_14/thumbnails_medium/17779-4971915255-304x171.jpg",
#                     "artwork_208x117": "http://static-api.guidebox.com/thumbs03_14/thumbnails_small/17779-338286772-208x117.jpg",
#                     "wikipedia_id": 42444704,
#                     "themoviedb": 62234
#                 },
#                 "title": "Deadbeat",
#                 "justAdded": 'false',
#                 "url": "http://localhost:8000/api/content/957/"
#             }
#         ]
#     }
# }
#
#
# @given("a package")
# def step_impl(context):
#     # context.rest_client.BASE_URL = 'http://0.0.0.0:8000'
#     # context.package = context.rest_client.get('http://0.0.0.0:8000/api/package/2346/')
#     """
#     :type context: behave.runner.Context
#     """
#
#
# @when("we pull out the channels")
# def step_impl(context):
#     context.channels = get_package_channels(x)
#     """
#     :type context: behave.runner.Context
#     """
#     pass
#
#
# @then("we have a list of channels")
# def step_impl(context):
#     assert len(context.channels) > 0
#     """
#     :type context: behave.runner.Context
#     """
#     pass
