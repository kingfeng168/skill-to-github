# 脱敏脚本模板（复制干净副本 + 路径通用化）
# 用法：改 SRC / DST / rules 后运行，生成开源发布目录
import shutil, os

SRC = r"C:\Users\<you>\.workbuddy\skills\<skill-name>"
DST = r"<release-dir>/<skill-name>"

def ignore(d, names):
    return {n for n in names if n in (".eia_key", "__pycache__", ".git") or n.endswith(".zip")}

shutil.copytree(SRC, DST, ignore=ignore, dirs_exist_ok=True)

# 路径替换规则（长路径优先；按需把左侧改为你的真实个人路径 → 右侧通用路径）
rules = [
    ("C:/Users/<you>/Desktop/report/daily_data.json", "./daily_data.json"),
    ("C:/Users/<you>/Desktop/output/", "./output/"),
]

# 个人化措辞通用化（按需调整）
special = []

for root, dirs, files in os.walk(DST):
    for fn in files:
        fp = os.path.join(root, fn)
        if not (fn == "SKILL.md" or fn.endswith(".md") or fn.endswith(".py")):
            continue
        with open(fp, "rb") as f:
            data = f.read()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        new = text
        for a, b in rules:
            new = new.replace(a, b)
        for a, b in special:
            new = new.replace(a, b)
        if new != text:
            with open(fp, "wb") as f:
                f.write(new.encode("utf-8"))
            print("modified:", os.path.relpath(fp, DST))
print("DONE")
