import pandas as pd
from tqdm import tqdm
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

tqdm.pandas()  # 进度条
ANALYZER = SentimentIntensityAnalyzer()  # 情感分析器


def get_sentiment_score(text):
    # 计算情感得分
    vs = ANALYZER.polarity_scores(str(text))  # 计算情感得分
    return vs["compound"]


def get_sentiment_category(sentiment_score):
    # 计算情感得分类别
    if sentiment_score >= 0.05:
        return "positive"  # positive
    elif sentiment_score <= -0.05:
        return "negative"  # negative
    else:
        return "neutral"  # neutral


if __name__ == "__main__":
    ############# Youtube-final_data #############
    data = pd.read_csv("Youtube-final_data.csv", low_memory=False)  # 读取数据
    data = data[["Order", "User Name", "Date", "Time", "Like Count", "Comment", "User Link"]]
    data["Sentiment Score"] = data["Comment"].progress_apply(get_sentiment_score)  # 计算情感得分
    data["Sentiment Category"] = data["Sentiment Score"].progress_apply(get_sentiment_category)  # 计算情感分类
    data.to_csv("Youtube-final_data-Sentiment.csv", index=False)  # 保存数据
    print("Done!")

    ############# IMDB_reviews_cleaned #############
    data = pd.read_csv("IMDB_reviews_cleaned.csv", low_memory=False)  # 读取数据
    data["Sentiment Score"] = data["Review"].progress_apply(get_sentiment_score)  # 计算情感得分
    data["Sentiment Category"] = data["Sentiment Score"].progress_apply(get_sentiment_category)  # 计算情感分类
    data.to_csv("IMDB_reviews_cleaned-Sentiment.csv", index=False)  # 保存数据
    print("Done!")
