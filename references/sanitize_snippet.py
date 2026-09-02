# 脱敏脚本片段（复制干净副本 + 路径通用化）
# 用法：改 SRC / DST 后运行，生成开源发布目录
import shutil, os

SRC = r"C:\Users\<you>\.workbuddy\skills\<skill-name>"
DST = r"<发布目录>\<skill-name>"

def ignore(d, names):
    return {n for n in names if n in (".eia_key", "__pycache__", ".git") or n.endswith(".zip")}

shutil.copytree(SRC, DST, ignore=ignore, dirs_exist_ok=True)

# 路径替换规则（长路径优先）
rules = [
    ("C:\\Users\\<you>\\Desktop\\output\\financial-dashboard\\daily_data.json", "./daily_data.json"),
    ("C:/Users/<you>/Desktop/output/financial-dashboard/daily_data.json", "./daily_data.json"),
    ("C:\\Users\\<you>\\Desktop\\output\\", "./output/"),
    ("C:/Users/<you>/Desktop/output/", "./output/"),
]

# 个人化措辞通用化（按需调整）
special = [
    ('**用户"全球金融日报"系统** | 自用一手 |', '**本地宏观日报系统(可选)** | 自用 |'),
    ('- **用户日报系统**:读取', '- **本地日报系统(可选)**:读取'),
]

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
