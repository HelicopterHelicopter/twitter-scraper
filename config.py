# Twitter API Headers
TWITTER_HEADERS = {
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "cookie": "guest_id=v1%3A172820709170303809; night_mode=2; guest_id_marketing=v1%3A172820709170303809; guest_id_ads=v1%3A172820709170303809; gt=1891496364590109054; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; kdt=0HFL69oXBT4smAFZmoOBQR5DSnxzTDmicE9rMxEb; auth_token=0e0815db530dd94a6d0bab4a9dfc9455dd86bc0c; ct0=50f3f4bd260b8fc0747edd08d6b09412daa10d62c98f2e10d21be14f05ad0c508bca822b936d7763cb7a03db11e63a7e9490a375ab4f3a453bc243381813410b424611dc2b34005d2ce2dd677db320c9; lang=en; twid=u%3D1472799072306089987; att=1-RWb89Y7fjSqKzz2yI1HVXiuvjeEIiBbGtTEgtzSk; personalization_id=\"v1_Guf8V7+WfltcBpWeIn0b0g==\"",
    "x-csrf-token": "50f3f4bd260b8fc0747edd08d6b09412daa10d62c98f2e10d21be14f05ad0c508bca822b936d7763cb7a03db11e63a7e9490a375ab4f3a453bc243381813410b424611dc2b34005d2ce2dd677db320c9",
    "x-twitter-auth-type": "OAuth2Session",
    "x-twitter-client-language": "en",
    "x-twitter-active-user": "yes",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "referer": "https://x.com/home?lang=en"
}

# File paths
TWEETS_FILE = "tweets.json"
BRANDS_FILE = "brands.json"  # Combined brands file

# Scraping limits
MAX_TWEETS_PER_ACCOUNT = 100  # Maximum tweets to scrape per account

# Retry mechanism constants
BASE_DELAY = 5  # Base delay between tweets
MAX_WAIT_TIME = 600  # 10 minutes in seconds
INITIAL_RETRY_DELAY = 30  # Initial retry delay when tweet format is invalid
MAX_RETRY_DELAY = 300  # Maximum retry delay (5 minutes)
MAX_RETRIES = 5  # Maximum number of retries
NO_TWEETS_TIMEOUT = 15 * 60  # 15 minutes

# API endpoints
USER_BY_SCREEN_NAME_URL = 'https://x.com/i/api/graphql/32pL5BWe9WKeSK1MoPvFQQ/UserByScreenName?'
TWEET_DETAIL_URL = 'https://x.com/i/api/graphql/Ez6kRPyXbqNlhBwcNMpU-Q/TweetDetail?'
USER_TWEETS_URL = 'https://x.com/i/api/graphql/eB8E8M_tVXS-5wuFivd48Q/UserTweets?'

# Default API parameters
DEFAULT_TWEET_FEATURES = {
    "responsive_web_graphql_exclude_directive_enabled": True,
    "verified_phone_label_enabled": False,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "tweetypie_unmention_optimization_enabled": True,
    "responsive_web_edit_tweet_api_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "view_counts_everywhere_api_enabled": True,
    "longform_notetweets_consumption_enabled": True,
    "responsive_web_twitter_article_tweet_consumption_enabled": False,
    "tweet_awards_web_tipping_enabled": False,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "standardized_nudges_misinfo": True,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "rweb_video_timestamps_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "longform_notetweets_inline_media_enabled": True,
    "responsive_web_media_download_video_enabled": False,
    "responsive_web_enhance_cards_enabled": False
}