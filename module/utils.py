from typing import Tuple,List

# 文件写入
def log(msg:Tuple[str,str,List[str]]):
    with open("msg.csv","a",encoding="utf-8") as f:
        f.write(f"{msg[0]},{msg[1]},{msg[2]}\n")
