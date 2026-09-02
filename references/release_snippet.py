# Release 创建 + zip 资产上传脚本片段（GitHub API）
# 用法：改 TOKEN / OWNER / REPO / ZIP 后运行
import urllib.request, json

TOKEN = "PASTE_YOUR_TOKEN_HERE"
OWNER = "<github-username>"
REPO = "<repo-name>"
ZIP = r"<path-to-skill>.zip"

def call(method, url, data=None, ctype=None):
    headers = {"Authorization": "token " + TOKEN, "Accept": "application/vnd.github+json"}
    body = None
    if ctype == "json":
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode("utf-8")
    elif data is not None:
        headers["Content-Type"] = ctype
        body = data
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode("utf-8"))

# 1. 创建 release
rel = call("POST", f"https://api.github.com/repos/{OWNER}/{REPO}/releases",
           {"tag_name": "v1.0.0", "name": "v1.0.0",
            "body": "First open-source release.", "draft": False, "prerelease": False},
           ctype="json")
print("release_url:", rel["html_url"])

# 2. 上传 zip 资产
with open(ZIP, "rb") as f:
    zipdata = f.read()
asset_url = f"https://uploads.github.com/repos/{OWNER}/{REPO}/releases/{rel['id']}/assets?name={REPO}.zip"
a = call("POST", asset_url, zipdata, ctype="application/zip")
print("asset_download:", a.get("browser_download_url"))
print("DONE")
