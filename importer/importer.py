"""
题单导入器
根据JSON导入题单
"""
import os
import sys
import json
import shutil
import subprocess

from tqdm import tqdm
from colorama import Fore


# noinspection DuplicatedCode
def generate(program_path, data):
    '''
    运行指定Python程序并获取处理后的输出

    Args:
        program_path: 要运行的.py文件路径
        data: 要传入程序输入流的数据

    Returns:
        处理后的输出字符串
    '''
    try:
        # 将数据编码为字节，以便通过stdin传递
        if isinstance(data, str):
            input_data = data.encode('utf-8')
        else:
            input_data = str(data).encode('utf-8')

        # 使用当前Python解释器运行目标程序
        result = subprocess.run(
            [sys.executable, program_path],
            input=input_data,
            capture_output=True,
            text=False,  # 不使用文本模式，以便手动处理编码
            timeout=30  # 设置超时时间，避免程序无限运行
        )

        # 解码输出字节为字符串
        output = result.stdout.decode('utf-8')

        # 处理输出文本
        lines = output.splitlines()

        # 去除每行末尾的空格
        cleaned_lines = [line.rstrip() for line in lines]

        # 去除末尾的空行
        while cleaned_lines and cleaned_lines[-1] == '':
            cleaned_lines.pop()

        # 重新组合为字符串
        final_output = '\n'.join(cleaned_lines)

        return final_output

    except subprocess.TimeoutExpired:
        return '程序执行超时'
    except FileNotFoundError:
        return f'找不到文件: {program_path}'
    except Exception as e:
        return f'执行出错: {str(e)}'

def main():
    """
    主函数
    :return: 无
    """
    debug_mode = False
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

    print('请输入题单JSON（若未自动生成，换行输入END并回车）:')
    lines = []
    while True:
        line = input().strip()
        if line == 'END' or line == 'DEBUG':
            if line == 'DEBUG':
                debug_mode = True
            break
        lines.append(line)
    data = json.loads('\n'.join(lines))

    root = data['name'].strip()
    if os.path.exists(root):
        op = input(f'题单 {data["name"]} 已存在，请选择处理方式（O=覆盖，R=重命名新题单，C=取消并退出）: {Fore.BLUE}').strip().upper()
        match op:
            case 'O':
                shutil.rmtree(root)
            case 'R':
                data['name'] = input("请输入新名称（不含空格、*、/、\\、|、:）: ").strip()
                root = data['name']
            case 'C':
                print("已取消生成")
                sys.stdout.write(Fore.RESET)
                return
            case _:
                print("未知操作")
        sys.stdout.write(Fore.RESET)
    os.mkdir(root)
    os.chdir(root)

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(data['description'])

    pbar = tqdm(total=data['problems_num'], desc='生成题目', position=0, bar_format='%s{l_bar}{bar}{r_bar}%s' % (Fore.RESET, Fore.RESET))

    for p in range(data['problems_num']):
        problem = data['problems'][p]
        pbar.set_postfix_str(problem['name'])
        capital = chr(65+p)
        cpdir = capital + '-' + problem['name']
        os.mkdir(cpdir)
        os.chdir(cpdir)

        with open(f'{capital}.md', 'w', encoding='utf-8') as f:
            f.write(problem['desc'])

        with open(f'{capital}-solution.md', 'w', encoding='utf-8') as f:
            f.write(problem['solution'])

        with open(f'{capital}.py', 'w', encoding='utf-8') as f:
            f.write('')

        testerdata = problem['data']
        input_generator = f'{capital}-input.py'
        ans_generator = f'{capital}-ans.py'
        with open(input_generator, 'w', encoding='utf-8') as f:
            f.write(testerdata['input_generator'])
        with open(ans_generator, 'w', encoding='utf-8') as f:
            f.write(testerdata['ans_generator'])

        judge = {
            'name': capital + '-' + problem['name'],
            'program': capital,
            'nodes': []
        }
        os.mkdir('data')

        with tqdm(total=testerdata['tester_nodes_num'], desc='生成测试数据', leave=False, position=1) as pbar_tester:
            for i in range(testerdata['tester_nodes_num']):
                pbar_tester.set_postfix_str(f'Data #{i+1}')
                judge['nodes'].append({
                    'file': {
                        'input': f'data/{i+1}.in',
                        'ans': f'data/{i+1}.ans'
                    }
                })
                judge_input = generate(input_generator, str(i))
                judge_ans = generate(ans_generator, judge_input)
                with open(f'data/{i+1}.in', 'w', encoding='utf-8') as f:
                    f.write(judge_input)
                with open(f'data/{i+1}.ans', 'w', encoding='utf-8') as f:
                    f.write(judge_ans)
                pbar_tester.update(1)

        with open('judge.json', 'w', encoding='utf-8') as f:
            json.dump(judge, f, ensure_ascii=False, indent=4)

        if not debug_mode:
            os.remove(input_generator)
            os.remove(ans_generator)
        os.chdir('..')
        pbar.update(1)

    pbar.close()
    del pbar

    os.mkdir('.answers')
    os.chdir('.answers')


    with tqdm(total=data['problems_num'], leave=False, desc='生成答案') as pbar:
        for i in range(data['problems_num']):
            pbar.set_postfix_str(f'{chr(65+i)} {data["problems"][i]["name"]}')
            with open(f'{chr(65+i)}.py', 'w', encoding='utf-8') as f:
                f.write(data['problems'][i]['data']['ans_generator'])
            pbar.update(1)

    os.chdir('..')

    with tqdm(total=data['problems_num'], leave=False, desc='生成评测指令') as pbar:
        with open('judge.txt', 'w', encoding='utf-8') as f:
            for i in range(data['problems_num']):
                f.write(f'python -m PyJudge ./{data['name']}/{chr(65+i)}-{data['problems'][i]['name']}\n')

    print(f"{Fore.GREEN}题单生成完毕: {os.path.abspath(os.path.join(root, '..'))}", end=Fore.RESET)

if __name__ == '__main__':
    main()
