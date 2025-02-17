import json
from datetime import datetime
import pandas as pd
from typing import List, Dict, Any
import matplotlib.pyplot as plt
from collections import Counter

def load_tweets_data(file_path: str = "tweets.json") -> List[Dict[Any, Any]]:
    """Load tweets from the JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def convert_to_dataframe(tweets: List[Dict]) -> pd.DataFrame:
    """Convert tweets list to a pandas DataFrame with proper date parsing"""
    df = pd.DataFrame(tweets)
    df['tweet_created_at'] = pd.to_datetime(df['tweet_created_at'])
    return df

def get_basic_stats(df: pd.DataFrame) -> Dict:
    """Get basic statistics about the tweets"""
    stats = {
        'total_tweets': len(df),
        'total_views': df['views'].sum(),
        'total_likes': df['favorite_count'].sum(),
        'total_retweets': df['retweet_count'].sum(),
        'total_replies': df['reply_count'].sum(),
        'total_quotes': df['quote_count'].sum(),
        'avg_engagement_rate': (df['favorite_count'] + df['retweet_count'] + df['reply_count']).mean(),
        'most_liked_tweet': df.loc[df['favorite_count'].idxmax()]['tweet_text'],
        'most_retweeted_tweet': df.loc[df['retweet_count'].idxmax()]['tweet_text'],
        'most_viewed_tweet': df.loc[df['views'].idxmax()]['tweet_text'],
    }
    return stats

def get_hashtag_analysis(df: pd.DataFrame) -> Dict:
    """Analyze hashtag usage"""
    all_hashtags = []
    for hashtags in df['hashtags']:
        if hashtags:  # Check if hashtags list is not empty
            all_hashtags.extend([h['text'] for h in hashtags])
    
    hashtag_counts = Counter(all_hashtags)
    return {
        'total_hashtags_used': len(all_hashtags),
        'unique_hashtags': len(hashtag_counts),
        'top_hashtags': dict(hashtag_counts.most_common(10))
    }

def get_temporal_analysis(df: pd.DataFrame) -> Dict:
    """Analyze temporal patterns in tweets"""
    df['hour'] = df['tweet_created_at'].dt.hour
    df['day_of_week'] = df['tweet_created_at'].dt.day_name()
    
    hourly_activity = df['hour'].value_counts().sort_index().to_dict()
    daily_activity = df['day_of_week'].value_counts().to_dict()
    
    return {
        'hourly_activity': hourly_activity,
        'daily_activity': daily_activity,
        'most_active_hour': df['hour'].mode().iloc[0],
        'most_active_day': df['day_of_week'].mode().iloc[0]
    }

def plot_engagement_over_time(df: pd.DataFrame, save_path: str = None):
    """Plot engagement metrics over time"""
    plt.figure(figsize=(15, 8))
    plt.plot(df['tweet_created_at'], df['favorite_count'], label='Likes')
    plt.plot(df['tweet_created_at'], df['retweet_count'], label='Retweets')
    plt.plot(df['tweet_created_at'], df['reply_count'], label='Replies')
    
    plt.title('Engagement Over Time')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

def analyze_tweets(json_file: str = "tweets.json"):
    """Main function to analyze tweets and print insights"""
    # Load and prepare data
    tweets = load_tweets_data(json_file)
    df = convert_to_dataframe(tweets)
    
    # Get various analyses
    basic_stats = get_basic_stats(df)
    hashtag_stats = get_hashtag_analysis(df)
    temporal_stats = get_temporal_analysis(df)
    
    # Print insights
    print("\n=== Tweet Analysis Report ===\n")
    
    print("Basic Statistics:")
    print(f"Total Tweets: {basic_stats['total_tweets']}")
    print(f"Total Views: {basic_stats['total_views']:,}")
    print(f"Total Likes: {basic_stats['total_likes']:,}")
    print(f"Total Retweets: {basic_stats['total_retweets']:,}")
    print(f"Average Engagement Rate: {basic_stats['avg_engagement_rate']:.2f}")
    
    print("\nMost Popular Tweet (by likes):")
    print(f"'{basic_stats['most_liked_tweet'][:100]}...'")
    
    print("\nHashtag Analysis:")
    print(f"Total Hashtags Used: {hashtag_stats['total_hashtags_used']}")
    print("Top 5 Hashtags:")
    for hashtag, count in list(hashtag_stats['top_hashtags'].items())[:5]:
        print(f"#{hashtag}: {count} times")
    
    print("\nTemporal Analysis:")
    print(f"Most Active Day: {temporal_stats['most_active_day']}")
    print(f"Most Active Hour: {temporal_stats['most_active_hour']:02d}:00")
    
    # Generate engagement plot
    plot_engagement_over_time(df, 'engagement_over_time.png')
    print("\nEngagement plot has been saved as 'engagement_over_time.png'")

if __name__ == "__main__":
    analyze_tweets() 