import pandas as pd

def start():
    print("liangfei_first_module")
    print("liangfei_wangjunyue")
    # 读取Excel文件
    df = pd.read_excel('e://count/pycharmexam20240428.xlsx')
    # 显示数据框架的内容
    print(df)