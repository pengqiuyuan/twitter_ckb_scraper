import datetime
import os
import pathlib
import json
import pandas as pd

path = pathlib.Path("./data/")
path.mkdir(parents=True, exist_ok=True)

since_date = str(datetime.datetime.today().date() - datetime.timedelta(days=1))
json_file = path/str(datetime.datetime.today().date())

def sns_scrape():
    os.system(f'snscrape --jsonl --progress --since {since_date} twitter-search "新疆" > {json_file}.json')

    # 从 JSON 文件中读取数据
    with open(str(json_file) + ".json", "r", encoding="utf8") as file:
        data = [json.loads(line) for line in file]

    # 将数据转换为 DataFrame
    df = pd.json_normalize(data)

    # 将 DataFrame 保存为 Excel 文件
    df.to_excel(str(json_file) + ".xlsx", index=False)

if __name__ == "__main__":
    sns_scrape()

