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

keywords = ["Tsinghua University","清华大学"]

def sns_scrape(keyword):
    os.system(f'snscrape --jsonl --progress --since {since_date} twitter-search "{keyword}" > temp.json')
    with open("temp.json", "r", encoding="utf8") as file:
        data = [json.loads(line) for line in file]
    os.remove("temp.json")
    return data

if __name__ == "__main__":
    all_data = []
    for keyword in keywords:
        all_data.extend(sns_scrape(keyword))
    json_file = path/(str(datetime.datetime.today().date()) + "_" + timestamp)
    with open(str(json_file) + ".json", "w", encoding="utf8") as file:
        for entry in all_data:
            json.dump(entry, file)
            file.write("\n")
    df = pd.json_normalize(all_data)
    useful_columns = ["url", "date", "content", "replyCount", "retweetCount", "likeCount", 
                      "user.username", "user.displayname", "user.verified", "user.followersCount", 
                      "user.friendsCount", "user.statusesCount"]
    df = df[useful_columns]
    df.to_excel(str(json_file) + ".xlsx", index=False)
