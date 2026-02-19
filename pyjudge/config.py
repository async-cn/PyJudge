"""
配置相关
    load: 加载yaml配置文件
    load_json: 加载json配置文件
    load_text: 读取文本文件
    read_global_config: 获取全局配置
"""
import os
import json

import yaml

def load(path:str) -> dict:
    """
    加载yaml配置文件
    :param path: yaml文件路径
    :return: 配置内容
    """
    with open(path, "r", encoding='utf-8') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

def load_json(path:str) -> dict:
    """
    加载json配置文件
    :param path: json文件路径
    :return: 配置内容
    """
    with open(path, "r", encoding='utf-8') as f:
        return json.load(f)

def load_text(path:str) -> str:
    """
    从文件读取文本
    :param path: 文件路径
    :return: 文本内容
    """
    with open(path, "r", encoding='utf-8') as f:
        return f.read()

def read_global_config() -> dict:
    """
    读取全局配置
    :return: 全局配置
    """
    script_dir = os.path.dirname(__file__)
    return load(os.path.join(script_dir, 'configs/global.yml'))

if __name__ == "__main__":
    print(read_global_config())
