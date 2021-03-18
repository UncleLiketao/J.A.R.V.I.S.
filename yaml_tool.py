import os
import yaml

current_path = os.path.abspath(".")
yaml_path = os.path.join(current_path, "answer.yaml")


def get_yaml_data(yaml_file):
    print("****获取yaml文件数据****")
    file = open(yaml_file, 'r', encoding='utf-8')
    file_data = file.read()
    file.close()

    # 将字符串转化为字典或列表
    print("***转化yaml数据为字典或列表***")
    data = yaml.safe_load(file_data)
    print(data)
    return data


get_yaml_data(yaml_path)
