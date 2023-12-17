import pandas as pd
from cnsenti import Sentiment
from tqdm import tqdm

tqdm.pandas()  # 进度条
SENTI = Sentiment()  # 情感分析器 https://www.heywhale.com/mw/dataset/6113895baca2460017a475be/file


def get_sentiment_score(text):
    # 计算情感得分
    result = SENTI.sentiment_calculate(str(text))  # 计算情感得分
    pos_score = result["pos"]  # 正面得分
    neg_score = result["neg"]  # 负面得分
    if pos_score < 0:  # 有些情感词语的得分为负数，这里将其置为0
        pos_score = 0
    if neg_score < 0:  # 有些情感词语的得分为负数，这里将其置为0
        neg_score = 0
    score = pos_score / (pos_score + neg_score) if pos_score + neg_score != 0 else 0.5  # 映射为0-1之间
    score = (score - 0.5) * 2 if score >= 0.5 else (0.5 - score) * -2  # 映射为-1-1之间
    return round(score, 4)


def get_sentiment_category(sentiment_score):
    # 计算情感得分类别
    if sentiment_score >= 0.3:
        return "positive"  # positive
    elif sentiment_score <= -0.3:
        return "negative"  # negative
    else:
        return "neutral"  # neutral


if __name__ == "__main__":
    ############# 芭比 电影 #############
    data = pd.read_csv("芭比 电影.csv", low_memory=False)  # 读取数据
    data["Sentiment Score"] = data["content"].progress_apply(get_sentiment_score)  # 计算情感得分
    data["Sentiment Category"] = data["Sentiment Score"].progress_apply(get_sentiment_category)  # 计算情感分类
    data.to_csv("芭比 电影-Sentiment.csv", index=False)  # 保存数据
    print("Done!")

    ############# doubandata #############
    data = pd.read_excel("doubandata.xlsx")  # 读取数据
    data["Sentiment Score"] = data["Review"].progress_apply(get_sentiment_score)  # 计算情感得分
    data["Sentiment Category"] = data["Sentiment Score"].progress_apply(get_sentiment_category)  # 计算情感分类
    data.to_excel("doubandata-Sentiment.xlsx", index=False)  # 保存数据
    print("Done!")
