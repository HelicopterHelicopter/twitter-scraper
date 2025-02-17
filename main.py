import os
import requests
import urllib.parse
import json
import time
from datetime import datetime, timedelta
import math
from config import *

# Target brand to scrape
TARGET_BRAND = "Swiggy"

# Twitter API Headers
headers = {
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "cookie": "guest_id=v1%3A172820709170303809; night_mode=2; guest_id_marketing=v1%3A172820709170303809; guest_id_ads=v1%3A172820709170303809; gt=1891496364590109054; external_referer=padhuUp37zjgzgv1mFWxJ12Ozwit7owX|0|8e8t2xd8A2w%3D; kdt=0HFL69oXBT4smAFZmoOBQR5DSnxzTDmicE9rMxEb; auth_token=0e0815db530dd94a6d0bab4a9dfc9455dd86bc0c; ct0=50f3f4bd260b8fc0747edd08d6b09412daa10d62c98f2e10d21be14f05ad0c508bca822b936d7763cb7a03db11e63a7e9490a375ab4f3a453bc243381813410b424611dc2b34005d2ce2dd677db320c9; lang=en; twid=u%3D1472799072306089987; att=1-RWb89Y7fjSqKzz2yI1HVXiuvjeEIiBbGtTEgtzSk; personalization_id=\"v1_Guf8V7+WfltcBpWeIn0b0g==\"",
    "x-csrf-token": "50f3f4bd260b8fc0747edd08d6b09412daa10d62c98f2e10d21be14f05ad0c508bca822b936d7763cb7a03db11e63a7e9490a375ab4f3a453bc243381813410b424611dc2b34005d2ce2dd677db320c9",
    "x-twitter-auth-type": "OAuth2Session",
    "x-twitter-client-language": "en",
    "x-twitter-active-user": "yes",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "referer": "https://x.com/home?lang=en"
}

# Constants for retry mechanism
BASE_DELAY = 5  # Base delay between tweets
MAX_WAIT_TIME = 600  # 10 minutes in seconds
INITIAL_RETRY_DELAY = 30  # Initial retry delay when tweet format is invalid
MAX_RETRY_DELAY = 300  # Maximum retry delay (5 minutes)

# File to store tweets
TWEETS_FILE = "tweets.json"

def load_tweets():
    """Load existing tweets from file, create file if doesn't exist"""
    try:
        if not os.path.exists(TWEETS_FILE):
            with open(TWEETS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []
        with open(TWEETS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading tweets: {e}")
        return []

def save_tweets(tweets):
    """Save tweets to JSON file with proper Unicode handling"""
    with open(TWEETS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, indent=2, ensure_ascii=False)

def get_user_id_from_screen_name(screen_name, headers):
    """Get Twitter user ID from screen name"""
    get_userid_url = USER_BY_SCREEN_NAME_URL

    get_user_id_variables = {
        "screen_name": screen_name.lstrip('@')
    }

    get_user_id_features = '%7B%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22profile_label_improvements_pcf_label_in_post_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C%22subscriptions_feature_can_gift_premium%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D'

    field_toggles = '%7B%22withAuxiliaryUserLabels%22%3Afalse%7D'

    variables_encoded = urllib.parse.quote(str(json.dumps(get_user_id_variables, separators=(',', ':'))))

    get_userid_url = f"{get_userid_url}variables={variables_encoded}&features={get_user_id_features}&field_toggles={field_toggles}"

    print(f"Getting user ID for {screen_name}")
    response = requests.get(get_userid_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        user_id = data["data"]["user"]["result"]["rest_id"]
        print(f"Found user ID: {user_id}")
        return user_id
    else:
        print(f"Failed to get user ID. Status code: {response.status_code}")
        return None

def is_valid_tweet_format(tweet_data):
    """Validate if tweet data has all required fields in correct format"""
    required_fields = {
        "account": str,
        "tweetId": str,
        "tweet_text": str,
        "views": int,
        "tweet_created_at": str,
        "hashtags": list,
        "favorite_count": int,
        "quote_count": int,
        "reply_count": int,
        "retweet_count": int
    }
    
    try:
        for field, field_type in required_fields.items():
            if field not in tweet_data:
                print(f"Missing field: {field}")
                return False
            if not isinstance(tweet_data[field], field_type):
                print(f"Invalid type for {field}: expected {field_type}, got {type(tweet_data[field])}")
                return False
        return True
    except Exception as e:
        print(f"Error validating tweet format: {e}")
        return False

def get_tweet_with_retry(entry, screen_name, headers, start_time):
    """Get tweet data with retry mechanism for invalid format"""
    retry_delay = INITIAL_RETRY_DELAY
    retry_count = 0
    max_retries = 5  # Maximum number of retries per tweet
    
    while retry_count < max_retries:
        try:
            tweet_result = entry["content"]["itemContent"]["tweet_results"]["result"]
            tweet_id = tweet_result["rest_id"]
            
            # Try to get view count, default to 0 if not available
            try:
                views_count = tweet_result.get("views", {}).get("count", 0)
                views_count = int(views_count) if isinstance(views_count, str) else views_count
            except (KeyError, TypeError):
                views_count = 0
            
            legacy = tweet_result["legacy"]
            
            tweet_data = {
                "account": screen_name,
                "tweetId": tweet_id,
                "tweet_text": legacy["full_text"],
                "views": views_count,
                "tweet_created_at": legacy["created_at"],
                "hashtags": legacy["entities"]["hashtags"],
                "favorite_count": legacy["favorite_count"],
                "quote_count": legacy["quote_count"],
                "reply_count": legacy["reply_count"],
                "retweet_count": legacy["retweet_count"],
                "engagement_score": legacy["favorite_count"] + legacy["retweet_count"] * 2 + legacy["reply_count"] * 3  # Custom engagement score
            }
            
            if is_valid_tweet_format(tweet_data):
                # Get replies for valid tweet
                print(f"Fetching replies for tweet {tweet_id}")
                replies = get_tweet_replies(tweet_id, headers)
                # Initialize empty list if replies is None
                replies = replies if replies is not None else []
                tweet_data["replies"] = replies
                print(f"Found {len(replies)} replies")
                return tweet_data
            else:
                print(f"Invalid tweet format, attempt {retry_count + 1}/{max_retries}")
                
                # Check if we've exceeded maximum wait time
                if (datetime.now() - start_time).total_seconds() > MAX_WAIT_TIME:
                    print("Exceeded maximum wait time (10 minutes). Terminating program.")
                    return None
                
                # Wait with exponential backoff
                print(f"Waiting {retry_delay} seconds before retry...")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)
                retry_count += 1
        
        except Exception as e:
            print(f"Error processing tweet: {e}")
            if (datetime.now() - start_time).total_seconds() > MAX_WAIT_TIME:
                print("Exceeded maximum wait time (10 minutes). Terminating program.")
                return None
            print(f"Waiting {retry_delay} seconds before retry...")
            time.sleep(retry_delay)
            retry_delay = min(retry_delay * 2, MAX_RETRY_DELAY)
            retry_count += 1
    
    print("Maximum retry attempts reached for tweet")
    return None

def get_tweet_replies(tweet_id, headers):
    """Fetch replies for a specific tweet"""
    replies_url = 'https://x.com/i/api/graphql/Ez6kRPyXbqNlhBwcNMpU-Q/TweetDetail?'
    
    variables = {
        "focalTweetId": tweet_id,
        "referrer": "tweet",
        "with_rux_injections": False,
        "includePromotedContent": False,
        "withCommunity": True,
        "withQuickPromoteEligibilityTweetFields": True,
        "withBirdwatchNotes": True,
        "withVoice": True,
        "withV2Timeline": True,
        "withDownvotePerspective": True,
        "withReactionsMetadata": True,
        "withReactionsPerspective": True,
        "withSuperFollowsTweetFields": True,
        "withSuperFollowsUserFields": True,
        "withVoice": True,
        "withUserResults": True,
        "rankingMode": "Relevance"
    }

    features = {
        "profile_label_improvements_pcf_label_in_post_enabled": True,
        "rweb_tipjar_consumption_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": True,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "premium_content_api_read_enabled": False,
        "communities_web_enable_tweet_community_results_fetch": True,
        "c9s_tweet_anatomy_moderator_badge_enabled": True,
        "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
        "responsive_web_grok_analyze_post_followups_enabled": True,
        "responsive_web_jetfuel_frame": False,
        "responsive_web_grok_share_attachment_enabled": True,
        "articles_preview_enabled": True,
        "responsive_web_edit_tweet_api_enabled": True,
        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
        "view_counts_everywhere_api_enabled": True,
        "longform_notetweets_consumption_enabled": True,
        "responsive_web_twitter_article_tweet_consumption_enabled": True,
        "tweet_awards_web_tipping_enabled": False,
        "responsive_web_grok_analysis_button_from_backend": True,
        "creator_subscriptions_quote_tweet_preview_enabled": False,
        "freedom_of_speech_not_reach_fetch_enabled": True,
        "standardized_nudges_misinfo": True,
        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
        "rweb_video_timestamps_enabled": True,
        "longform_notetweets_rich_text_read_enabled": True,
        "longform_notetweets_inline_media_enabled": True,
        "responsive_web_grok_image_annotation_enabled": False,
        "responsive_web_enhance_cards_enabled": False
    }

    field_toggles = {
        "withArticleRichContentState": False,
        "withArticlePlainText": False,
        "withGrokAnalyze": False,
        "withDisallowedReplyControls": False
    }

    variables_encoded = urllib.parse.quote(json.dumps(variables, separators=(',', ':')))
    features_encoded = urllib.parse.quote(json.dumps(features, separators=(',', ':')))
    field_toggles_encoded = urllib.parse.quote(json.dumps(field_toggles, separators=(',', ':')))
    full_url = f"{replies_url}variables={variables_encoded}&features={features_encoded}&fieldToggles={field_toggles_encoded}"

    try:
        response = requests.get(full_url, headers=headers)
        print(f"Replies fetch status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            replies = []
            
            try:
                conversation_data = data.get("data", {}).get("threaded_conversation_with_injections_v2", {})
                if not conversation_data:
                    print("No conversation data found")
                    return []

                instructions = conversation_data.get("instructions", [])
                
                def process_tweet_data(tweet_data):
                    if not tweet_data:
                        return None
                        
                    result = tweet_data.get("result", {})
                    if not result:
                        return None
                    
                    legacy = result.get("legacy", {})
                    core = result.get("core", {})
                    
                    if legacy.get("in_reply_to_status_id_str") == tweet_id:
                        user_results = core.get("user_results", {}).get("result", {})
                        user_legacy = user_results.get("legacy", {})
                        
                        favorite_count = legacy.get("favorite_count", 0)
                        retweet_count = legacy.get("retweet_count", 0)
                        reply_count = legacy.get("reply_count", 0)
                        quote_count = legacy.get("quote_count", 0)
                        
                        engagement_score = (
                            favorite_count * 1.0 +
                            retweet_count * 2.0 +
                            reply_count * 1.5 +
                            quote_count * 2.0
                        )
                        
                        if user_legacy.get("verified", False):
                            engagement_score *= 1.1
                            
                        follower_count = user_legacy.get("followers_count", 0)
                        if follower_count > 0:
                            engagement_score *= (1 + (math.log10(follower_count) / 10))
                        
                        reply_data = {
                            "reply_id": result.get("rest_id", ""),
                            "reply_text": legacy.get("full_text", ""),
                            "reply_author": user_legacy.get("screen_name", ""),
                            "reply_author_name": user_legacy.get("name", ""),
                            "reply_created_at": legacy.get("created_at", ""),
                            "reply_likes": favorite_count,
                            "reply_retweets": retweet_count,
                            "reply_replies": reply_count,
                            "reply_quotes": quote_count,
                            "engagement_score": engagement_score,
                            "author_followers": follower_count,
                            "author_verified": user_legacy.get("verified", False)
                        }
                        
                        views = result.get("views", {})
                        if views:
                            reply_data["reply_views"] = views.get("count", 0)
                            
                        return reply_data
                    return None

                for instruction in instructions:
                    if instruction.get("type") == "TimelineAddEntries":
                        entries = instruction.get("entries", [])
                        for entry in entries:
                            entry_type = entry.get("content", {}).get("entryType", "unknown")
                            
                            if entry.get("entryId", "").startswith(f"tweet-{tweet_id}"):
                                continue

                            content = entry.get("content", {})
                            
                            if entry_type == "TimelineTimelineItem":
                                item_content = content.get("itemContent", {})
                                tweet_results = item_content.get("tweet_results", {})
                                reply_data = process_tweet_data(tweet_results)
                                if reply_data:
                                    replies.append(reply_data)
                            
                            elif entry_type == "TimelineTimelineModule":
                                items = content.get("items", [])
                                for item in items:
                                    item_content = item.get("item", {}).get("itemContent", {})
                                    tweet_results = item_content.get("tweet_results", {})
                                    reply_data = process_tweet_data(tweet_results)
                                    if reply_data:
                                        replies.append(reply_data)
                
                replies.sort(key=lambda x: x["engagement_score"], reverse=True)
                top_replies = replies[:5]
                
                print(f"Found {len(replies)} total replies, returning top 5 most relevant")
                return top_replies
                
            except Exception as e:
                print(f"Error parsing reply data: {e}")
                return []
        else:
            print(f"Failed to fetch replies. Status code: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Error fetching replies for tweet {tweet_id}: {e}")
        return []

def save_tweet(tweet_data):
    """Save a single tweet by appending it to the tweets file"""
    try:
        # Load existing tweets
        tweets = load_tweets()
        
        # Check if tweet already exists
        tweet_exists = False
        for i, t in enumerate(tweets):
            if t["tweetId"] == tweet_data["tweetId"]:
                # Update existing tweet
                tweets[i] = tweet_data
                tweet_exists = True
                print(f"Updated tweet {tweet_data['tweetId']} in file")
                break

        if not tweet_exists:
            # Add new tweet
            tweets.append(tweet_data)
            print(f"Added new tweet {tweet_data['tweetId']} to file")
        
        # Sort tweets by engagement score
        tweets.sort(key=lambda x: x["engagement_score"], reverse=True)
        
        # Save back to file
        with open(TWEETS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        print(f"Error saving tweet to file: {e}")

def update_brand_status(brand_name, tweets_count=0):
    """Update brand's scraping status in the brands.json file"""
    try:
        with open(BRANDS_FILE, 'r', encoding='utf-8') as f:
            brands = json.load(f)
        
        if brand_name in brands:
            brands[brand_name].update({
                "is_scraped": True,
                "last_scraped": datetime.now().isoformat(),
                "tweets_scraped": tweets_count
            })
            
            with open(BRANDS_FILE, 'w', encoding='utf-8') as f:
                json.dump(brands, f, indent=2, ensure_ascii=False)
            print(f"Updated status for {brand_name} in {BRANDS_FILE}")
    except Exception as e:
        print(f"Error updating brand status: {e}")

def get_next_brand_to_scrape():
    """Get the next brand that hasn't been scraped yet"""
    try:
        with open(BRANDS_FILE, 'r', encoding='utf-8') as f:
            brands = json.load(f)
        
        for brand_name, brand_data in brands.items():
            if not brand_data["is_scraped"]:
                return brand_name, brand_data["handle"]
        return None, None
    except Exception as e:
        print(f"Error getting next brand: {e}")
        return None, None

def main():
    while True:
        brand_name, handle = get_next_brand_to_scrape()
        if not brand_name:
            print("No more brands to scrape")
            break
            
        print(f"Starting to scrape {handle}")
        user_id = get_user_id_from_screen_name(handle, TWITTER_HEADERS)
        if not user_id:
            continue

        tweets_processed = 0
        variables = {
            "userId": user_id,
            "count": 40,
            "includePromotedContent": False,
            "withHighlightedLabel": True,
            "withQuickPromoteEligibilityTweetFields": True,
            "withVoice": True,
            "withV2Timeline": True
        }

        features_json = json.dumps(DEFAULT_TWEET_FEATURES)
        encoded_features = urllib.parse.quote(str(features_json), safe='/')
        
        run = True
        start_time = datetime.now()

        while run and tweets_processed < MAX_TWEETS_PER_ACCOUNT:
            try:
                if (datetime.now() - start_time).total_seconds() > NO_TWEETS_TIMEOUT:
                    print("No tweets received for 15 minutes. Moving to next brand...")
                    break

                encoded_variables = urllib.parse.quote(str(json.dumps(variables, separators=(',', ':'))))
                api_url = f"{USER_TWEETS_URL}variables={encoded_variables}&features={encoded_features}"

                response = requests.get(api_url, headers=TWITTER_HEADERS)
                print(f"Response status: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    new_tweets_found = False

                    instructions = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]
                    for instruction in instructions:
                        if instruction["type"] == "TimelineAddEntries":
                            entries = instruction["entries"]
                            for entry in entries:
                                if entry["entryId"].startswith("tweet-"):
                                    if tweets_processed >= MAX_TWEETS_PER_ACCOUNT:
                                        run = False
                                        break
                                        
                                    time.sleep(BASE_DELAY)
                                    tweet_data = get_tweet_with_retry(entry, handle.lstrip('@'), TWITTER_HEADERS, start_time)
                                    if tweet_data:
                                        save_tweet(tweet_data)
                                        tweets_processed += 1
                                        new_tweets_found = True
                                        print(f"Processed {tweets_processed}/{MAX_TWEETS_PER_ACCOUNT} tweets for {handle}")
                                
                                elif entry["entryId"].startswith("cursor-bottom"):
                                    variables["cursor"] = entry["content"]["value"]
                            
                            if not new_tweets_found:
                                print("No new tweets found in this batch")
                                run = False
                            break
                else:
                    print(f"Request failed with status code: {response.status_code}")
                    if (datetime.now() - start_time).total_seconds() > MAX_WAIT_TIME:
                        break
                    time.sleep(INITIAL_RETRY_DELAY)

            except Exception as e:
                print(f"Error occurred: {e}")
                if (datetime.now() - start_time).total_seconds() > MAX_WAIT_TIME:
                    break
                time.sleep(INITIAL_RETRY_DELAY)

        # Update brand status after processing
        update_brand_status(brand_name, tweets_processed)
        print(f"Completed scraping {handle} with {tweets_processed} tweets")

if __name__ == "__main__":
    main()


