# PyJudge
![](https://img.shields.io/badge/License-MIT-blue)
![](https://img.shields.io/badge/Edition-Beta-green)
![](https://img.shields.io/badge/Python%20version-Python%203.x-blue)

一款有点好用的 Python 判题机。

支持自定义测试点输入输出和时间限制、详细调试信息显示，并根据程序的表现统计得分。

## Getting Started / 开始使用
### Environment / 环境需求：
 - Python 3 或更高版本
 - ```pip``` (Python包安装器)
### Installation / 安装
Clone this repository (克隆此仓库):
```shell
git clone https://github.com/async-cn/PyJudge.git
cd PyJudge
```
Install the requirements (安装所需依赖):
```shell
pip install -r requirements.txt
```
## Usage / 使用方法
### Terminal / 终端运行（推荐）
1. 进入PyJudge目录。
```shell
cd .../PyJudge。
```
2. 进入父目录
```shell
cd .. 
```
3. 执行以下命令，将```<path>```替换为题目**目录**（即```judge.json```与提交的程序共同所在的目录）。
```shell
python -m PyJudge "<path>"
```
### Script / 脚本运行
1. 在图形化界面中打开PyJudge目录。
2. 将题目**目录**拖动至```judge.sh```( Linux/MacOS/... )或```judge.cmd```( Windows ) 文件上。

## Problem Structure / 题目结构
具体示例见```example```目录

题目的文件结构如下（其中```.in```和```.ans```文件可选择不创建）
```text
my_problem/
├─judge.json
├─2.in
├─2.ans
└─my_program.py
```

```judge.json```的内容

其中```nodes```为测试点列表，可以直接输入数据或从文件读取。
```json
{
    "name": "雷霆题目",
    "program": "my_program",
    "nodes": [
    {
      "input": "7\n16\n5\n5",
      "ans": "48804"
    },
    {
      "file": {
          "input": "2.in",
          "ans": "2.ans"
      }
    }
  ]
}
```
## Gallery / 实际使用例图
![gallery/img_3.png](gallery/img_3.png)
![gallery/img_1.png](gallery/img_1.png)
![gallery/img_2.png](gallery/img_2.png)