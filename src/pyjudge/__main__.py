from .config import load_json
from .judge import quick_judge, display_judge_result
from .logger import Logger
from sys import argv, exit
import os

logger = Logger("Main")

if argv[1].lower() != "-f":
    if not os.path.exists(argv[1]):
        logger.error(f"路径不存在: {argv[1]}")
        exit(0)

    config_path = os.path.join(argv[1], "judge.json")
    if not os.path.exists(config_path):
        logger.error(f"测试配置文件不存在: {config_path}")
    config = load_json(config_path)
    program_path_relative = config["program"]+".py" if "program" in config else config["name"]+".py"
    program_path = os.path.join(argv[1], program_path_relative)
    if not os.path.exists(program_path):
        logger.error(f"被试程序不存在: {program_path}")

    result = quick_judge(program_path, config_path, argv[1])
    display_judge_result(result, len(config['nodes']), config)
