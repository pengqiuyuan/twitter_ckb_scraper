import datetime
import os
import pathlib
import json
import pandas as pd
import time

path = pathlib.Path("./data/")
path.mkdir(parents=True, exist_ok=True)

since_date = str(datetime.datetime.today().date() - datetime.timedelta(days=1))
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

keywords = ["Tsinghua University"]

def sns_scrape(keyword):
    json_file = path/(str(datetime.datetime.today().date()) + "_" + timestamp)
    os.system(f'snscrape --jsonl --progress --since {since_date} twitter-search "{keyword}" > {json_file}.json')

    # 从 JSON 文件中读取数据
    with open(str(json_file) + ".json", "r", encoding="utf8") as file:
        data = [json.loads(line) for line in file]

    # 将数据转换为 DataFrame
    df = pd.json_normalize(data)

    # 选择部分有用的列
    useful_columns = ["url", "date", "content", "replyCount", "retweetCount", "likeCount", 
                      "user.username", "user.displayname", "user.verified", "user.followersCount", 
                      "user.friendsCount", "user.statusesCount"]
    df = df[useful_columns]

    # 将 DataFrame 保存为 Excel 文件
    df.to_excel(str(json_file) + ".xlsx", index=False)

if __name__ == "__main__":
    for keyword in keywords:
        sns_scrape(keyword)
        time.sleep(5)  # 增加5秒延迟
