import os
import requests
import pymongo
from dotenv import load_dotenv
import urllib.parse
import json
import certifi

load_dotenv()

mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"),tlsCAFile=certifi.where())

db = mongo_client["remus"]

collection = db["tweets"]

screen_name = "letsblinkit"

def get_user_id_from_screen_name(screen_name, headers):
    get_userid_url = 'https://x.com/i/api/graphql/32pL5BWe9WKeSK1MoPvFQQ/UserByScreenName?'

    get_user_id_variables = {
        "screen_name": screen_name
    }

    get_user_id_features = '%7B%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22profile_label_improvements_pcf_label_in_post_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Atrue%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C%22subscriptions_feature_can_gift_premium%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D'

    field_toggles = '%7B%22withAuxiliaryUserLabels%22%3Afalse%7D'

    variables_encoded = urllib.parse.quote(str(json.dumps(get_user_id_variables, separators=(',', ':'))))

    get_userid_url = f"{get_userid_url}variables={variables_encoded}&features={get_user_id_features}&field_toggles={field_toggles}"

    print(get_userid_url)
    response = requests.get(get_userid_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data["data"]["user"]["result"]["rest_id"]
    else:
        return None

headers = {
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "cookie": 'night_mode=2; kdt=HEbCyPxa6nekqpXh9Qhwdb3dWpx40XMBJWRuVpaQ; lang=en; _ga=GA1.1.1547864365.1739287225; _ga_RJGMY4G45L=GS1.1.1739287225.1.1.1739287258.27.0.0; ph_phc_TXdpocbGVeZVm5VJmAsHTMrCofBQu3e0kN8HGMNGTVW_posthog=%7B%22distinct_id%22%3A%220194f599-69fb-7f54-86ca-c4fc03b588ad%22%2C%22%24sesid%22%3A%5B1739287270897%2C%220194f599-69fa-7e74-9d7b-a05689ddc5f8%22%2C1739287259642%5D%7D; dnt=1; guest_id=v1%3A173942711626061845; guest_id_marketing=v1%3A173942711626061845; guest_id_ads=v1%3A173942711626061845; auth_token=d5a259b01518ca773791ceac6708f1ed26028d52; ct0=7c43ced97ab676d885d67df4e2de2b54054dd1d73bbe1602558f565595039ac78e3ac1a6b9e4c05729af1f267a76b9a3a2b47d53545561458c394300c6d5e500459d92c2b25e2052e226c3e1ccf13a8f; twid=u%3D1889920480758370304; personalization_id="v1_aiC/jbBd2ya6iAXfAdaJtQ=="',
    "x-csrf-token": "7c43ced97ab676d885d67df4e2de2b54054dd1d73bbe1602558f565595039ac78e3ac1a6b9e4c05729af1f267a76b9a3a2b47d53545561458c394300c6d5e500459d92c2b25e2052e226c3e1ccf13a8f"
}

user_id = get_user_id_from_screen_name(screen_name, headers)

print(user_id)

variables = {
    "userId": user_id,
    "count":20,
    "includePromotedContent":True,
    "withQuickPromoteEligibilityTweetFields":True,
    "withVoice":True,
    "withV2Timeline":True
}

features = {
    "responsive_web_graphql_exclude_directive_enabled": "true",
    "verified_phone_label_enabled": "false",
    "creator_subscriptions_tweet_preview_api_enabled": "true",
    "responsive_web_graphql_timeline_navigation_enabled": "true",
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": "false",
    "c9s_tweet_anatomy_moderator_badge_enabled": "true",
    "tweetypie_unmention_optimization_enabled": "true",
    "responsive_web_edit_tweet_api_enabled": 'true',
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": "true",
    "view_counts_everywhere_api_enabled": "true",
    "longform_notetweets_consumption_enabled": "true",
    "responsive_web_twitter_article_tweet_consumption_enabled": "false",
    "tweet_awards_web_tipping_enabled": "false",
    "freedom_of_speech_not_reach_fetch_enabled": "true",
    "standardized_nudges_misinfo": "true",
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": "true",
    "rweb_video_timestamps_enabled": "true",
    "longform_notetweets_rich_text_read_enabled": "true",
    "longform_notetweets_inline_media_enabled": "true",
    "responsive_web_media_download_video_enabled": "false",
    "responsive_web_enhance_cards_enabled": "false"
}

features_json = json.dumps(features)

encoded_features = urllib.parse.quote(str(features_json), safe='/')

api_base_url = 'https://x.com/i/api/graphql/eB8E8M_tVXS-5wuFivd48Q/UserTweets?'

run = True

while run:
    encoded_variables = urllib.parse.quote(str(json.dumps(variables, separators=(',', ':'))))
    api_url = f"{api_base_url}variables={encoded_variables}&features={encoded_features}"

    response = requests.get(api_url, headers=headers)

    print(response.status_code)

    if response.status_code == 200:
        data = response.json()

        instructions = data["data"]["user"]["result"]["timeline_v2"]["timeline"]["instructions"]

        for intruction in instructions:
            if intruction["type"] == "TimelineAddEntries":
                entries = intruction["entries"]

                for entry in entries:
                    if entry["entryId"].startswith("tweet-"):
                        try:
                            print("tweet found")
                            tweetId = entry["entryId"]
                            tweet_text = entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["full_text"]
                            views = entry["content"]["itemContent"]["tweet_results"]["result"]["views"]["count"]
                            tweet_created_at = entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["created_at"]
                            hashtags = entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["entities"]["hashtags"]
                            favorite_count = entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["favorite_count"]
                            quote_count = entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["quote_count"]
                            reply_count = entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["reply_count"]
                            retweet_count = entry["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["retweet_count"]

                            existing = collection.find_one({
                                "tweetId": tweetId
                            })
                            print(existing)
                            if existing:
                                print("tweet already exists. updating...")
                                existing["views"] = views
                                existing["favorite_count"] = favorite_count
                                existing["quote_count"] = quote_count
                                existing["reply_count"] = reply_count
                                existing["retweet_count"] = retweet_count

                                collection.replace_one({
                                    "_id": existing["_id"]
                                },
                                existing)

                                continue

                            collection.insert_one({
                                "account": screen_name,
                                "tweetId": tweetId,
                                "tweet_text": tweet_text,
                                "views": views,
                                "tweet_created_at": tweet_created_at,
                                "hashtags": hashtags,
                                "favorite_count": favorite_count,
                                "quote_count": quote_count,
                                "reply_count": reply_count,
                                "retweet_count": retweet_count
                            })
                            print("new tweet added")

                        except Exception as e:
                            print(e)

                        
                    elif entry["entryId"].startswith("cursor-bottom"):
                        variables["cursor"] = entry["content"]["value"]
                
                break



    else:
        run = False


