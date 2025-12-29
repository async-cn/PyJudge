from .config import load_json, load_text, read_global_config
from .logger import Logger
from prettytable import PrettyTable, SINGLE_BORDER
from tqdm import tqdm
import subprocess
import threading
import sys

STATE_NAMES = [
    "AC",
    "ERR",
    "WA",
    "TLE"
]
STATE_BGCOLORS = [
    "\033[102m",
    "\033[43m",
    "\033[101m",
    "\033[44m"
]
NONE_COLOR:str = "\033[0;0m"

global_config:dict = read_global_config()
logger = Logger("Judger")

def judge_single(program_path:str, judge_in:str, judge_ans:str, time_limit:int, anstype) -> (int, str):
    """
    执行并评测Python程序

    参数:
        program_path: Python程序文件路径
        judge_in: 输入字符串
        judge_ans: 期望的输出字符串

    返回:
        0: 输出完全正确
        1: stderr不为空
        2: 输出与期望不符
        3: 程序超时
    """
    try:
        # 启动子进程执行Python程序
        proc = subprocess.Popen(
            [sys.executable, program_path],  # 使用当前Python解释器
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # 使用文本模式
            bufsize=1,  # 行缓冲
            universal_newlines=True
        )

        # 设置超时标志
        timeout_flag = False

        def kill_process():
            nonlocal timeout_flag
            if proc.poll() is None:  # 如果进程还在运行
                timeout_flag = True
                proc.terminate()  # 尝试正常终止
                proc.wait(timeout=0.1)  # 等待一小段时间
                if proc.poll() is None:  # 如果还未终止
                    proc.kill()  # 强制杀死

        # 设置超时计时器
        timer = threading.Timer(time_limit / 1000, kill_process)
        timer.start()

        try:
            # 向程序输入数据
            stdout_data, stderr_data = proc.communicate(
                input=judge_in,
                timeout=time_limit / 1000 + 0.1  # 比计时器稍长，确保能触发超时处理
            )
        except subprocess.TimeoutExpired:
            # 如果communicate超时，说明计时器已经触发
            timer.cancel()  # 确保计时器取消
            return 3, f"Time limit exceeded: {time_limit} ms"

        # 取消计时器（如果还在运行）
        timer.cancel()

        # 检查是否超时
        if timeout_flag:
            return 3, f"Time limit exceeded: {time_limit} ms"

        # 检查stderr是否为空
        if stderr_data and stderr_data.strip():
            return 1, f"An error occured: \"{stderr_data.strip()}\""

        # 处理输出
        # 1. 去掉首尾的空行
        output_lines = stdout_data.splitlines(keepends=False)

        # 去掉开头的空行
        start_idx = 0
        for i, line in enumerate(output_lines):
            if line.strip():  # 找到第一个非空行
                start_idx = i
                break

        # 去掉结尾的空行
        end_idx = len(output_lines)
        for i in range(len(output_lines) - 1, -1, -1):
            if output_lines[i].strip():  # 找到最后一个非空行
                end_idx = i + 1
                break

        if start_idx >= end_idx:
            output_lines = []
        else:
            output_lines = output_lines[start_idx:end_idx]

        # 2. 去掉每一行末尾的第一个空格（如果存在）
        processed_lines = []
        for line in output_lines:
            if line.endswith(' '):
                # 只去掉行尾的第一个空格
                line = line[:-1]
            processed_lines.append(line)

        # 3. 重新组合为输出字符串
        output = '\n'.join(processed_lines)

        # 与期望答案比较
        try:
            output = anstype(output)
        except:
            return 2, "Wrong Answer (Unexpected output datatype)"
        try:
            judge_ans = anstype(judge_ans)
        except:
            return 1, "Failed to format answer"
        if isinstance(output, str):
            if output == judge_ans:
                return 0, "OK"
            min_len = min(len(output), len(judge_ans))
            for i in range(min_len):
                if output[i] != judge_ans[i]:
                    return 2, f"Wrong Answer: At char #{i+1}, expected \"{judge_ans[i]}\", got \"{output[i]}\""
            if len(output) > len(judge_ans):
                return 2, "Wrong Answer: Output too long"
            else:  # len(output) < len(judge_ans)
                return 2, "Wrong Answer: Output too short"
        else:
            if output == judge_ans:
                return 0, "OK"
            else:
                return 2, "Wrong Answer"

    except FileNotFoundError:
        # 如果程序文件不存在
        # raise FileNotFoundError(f"Program file not found: {program_path}")
        return 1, "Program not found: {program_path}"
    except Exception as e:
        # 其他异常情况
        # raise RuntimeError(f"Error while judging program: {str(e)}")
        return 1, f"Error while judging program: \"{str(e)}\""

def judge_multi(program_path:str, config:dict, show_process:bool) -> dict:
    result = {
        'states': [],
        'messages': []
    }
    if show_process:
        pbar = tqdm(total=len(config['nodes']), unit='node')
        pbar.set_description('Processing')
    for node in config['nodes']:
        time_limit = global_config['default-time-limit'] if 'time-limit' not in node else node['time-limit']
        if 'file' in node:
            try:
                node['input'] = load_text(node['file']['input'])
            except Exception as e:
                error_msg = f"Failed to load input file: {node['file']['input']}"
                logger.error(error_msg)
                logger.error(e)
                result['states'].append(1)
                result['messages'].append(error_msg)
                continue
            try:
                node['ans'] = load_text(node['file']['ans'])
            except Exception as e:
                error_msg = f"Failed to load answer file: {node['file']['ans']}"
                logger.error(error_msg)
                logger.error(e)
                result['states'].append(1)
                result['messages'].append(error_msg)
                continue
        state, msg = judge_single(program_path, node['input'], node['ans'], time_limit, str if not 'anstype' in node else eval(node['anstype']))
        result['states'].append(state)
        result['messages'].append(msg)
        if show_process: pbar.update(1)
    if show_process: pbar.close()
    return result

def quick_judge(program_path:str, config_path:str) -> dict:
    config = load_json(config_path)
    return judge_multi(program_path, config , True)

def display_judge_result(result:dict, node_nums:int, config:dict) -> None:
    states = result['states']
    messages = result['messages']
    maxw = global_config['display']['nodes-max-cols']
    result_display:list = []
    table = PrettyTable()
    table.title = f"测试结果 - {config['name']}"
    table.set_style(SINGLE_BORDER)
    field_names = []
    for i in range(min(node_nums, maxw)):
        field_names.append("列 %d" % (i+1))
    table.field_names = field_names

    for r in range(int(node_nums / maxw)+1 if node_nums % maxw else int(node_nums / maxw)):
        result_display.append([])
        for i in range(maxw):
            if r*maxw+i >= node_nums:
                break
            result_display[-1].append(f'#{r*maxw+i+1}')
        result_display.append([])
        for i in range(maxw):
            curi = r*maxw+i
            if curi >= node_nums:
                break
            result_display[-1].append(
                STATE_BGCOLORS[states[curi]] + STATE_NAMES[states[curi]] + NONE_COLOR
            )
    table.add_rows(result_display)
    print(table)

    msgtable = PrettyTable()
    msgtable.set_style(SINGLE_BORDER)
    msgtable.title = "异常测试点信息"
    msgtable.field_names = ["测试点", "状态", "信息"]
    acs = node_nums
    for i in range(node_nums):
        if states[i]:
            acs -= 1
            msgtable.add_row([f'#{i+1}', STATE_BGCOLORS[states[i]] + STATE_NAMES[states[i]] + NONE_COLOR, messages[i]])
    if acs == node_nums:
        print("\033[92m恭喜你，通过了此题！\033[0m")
        print(f"Score: \033[92m100\033[0m")
    else:
        print(msgtable)
        if acs/node_nums >= 0.5:
            print(f"Score: \033[93m{round(100 * (acs / node_nums))}\033[0m")
        else:
            print(f"Score: \033[91m{round(100 * (acs / node_nums))}\033[0m")
