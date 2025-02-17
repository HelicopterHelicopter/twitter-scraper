import requests
import json
import urllib.parse

def test_twitter_auth():
    # Updated headers from active Twitter session
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

    # Variables and features for the request
    variables = {
        "screen_name": "Swiggy",
        "withSafetyModeUserFields": True
    }

    features = {
        "hidden_profile_subscriptions_enabled": True,
        "subscriptions_verification_info_is_identity_verified_enabled": True,
        "subscriptions_verification_info_verified_since_enabled": True,
        "highlights_tweets_tab_ui_enabled": True,
        "responsive_web_twitter_article_notes_tab_enabled": True,
        "creator_subscriptions_tweet_preview_api_enabled": True,
        "responsive_web_graphql_exclude_directive_enabled": True,
        "verified_phone_label_enabled": True,
        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
        "responsive_web_graphql_timeline_navigation_enabled": True,
        "profile_label_improvements_pcf_label_in_post_enabled": True,
        "rweb_tipjar_consumption_enabled": True,
        "subscriptions_feature_can_gift_premium": True
    }

    # Encode parameters
    variables_encoded = urllib.parse.quote(json.dumps(variables, separators=(',', ':')))
    features_encoded = urllib.parse.quote(json.dumps(features, separators=(',', ':')))

    # Construct URL with all parameters
    test_url = f'https://x.com/i/api/graphql/32pL5BWe9WKeSK1MoPvFQQ/UserByScreenName?variables={variables_encoded}&features={features_encoded}'
    
    print("Making test request to Twitter API...")
    response = requests.get(test_url, headers=headers)
    
    print(f"\nResponse Status Code: {response.status_code}")
    print("\nResponse Headers:")
    for key, value in response.headers.items():
        print(f"{key}: {value}")
    
    print("\nResponse Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

    if response.status_code == 401:
        print("\nDiagnosis:")
        print("- Status 401 indicates unauthorized access")
        print("- This confirms the current credentials are invalid or expired")
        print("- New credentials will be needed from an active Twitter/X session")
    elif response.status_code == 200:
        print("\nSuccess!")
        print("- Authentication is working")
        print("- These credentials can be used in main.py")

if __name__ == "__main__":
    test_twitter_auth() 