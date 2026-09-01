import os
from datetime import datetime, timezone, timedelta

# 配置信息（请修改为你自己的用户名和仓库名）
AUTHOR = "yourname"
REPO_URL = "https://github.com/yourname/your-repo"

# 需要处理的文件相对路径列表
FILES = [
    "Rules/Clash/CN_Domain_Use_Global_Proxy.list",
    "Rules/Clash/Global_Domain_Use_CN_Proxy.list",
    "Rules/Clash/Global_IP_Use_CN_Proxy.list"
]

def process_file(file_path):
    if not os.path.exists(file_path):
        print(f"跳过不存在的文件: {file_path}")
        return

    # 获取文件名（不带扩展名），作为 Header 中的 NAME
    rule_name = os.path.splitext(os.path.basename(file_path))[0]

    raw_lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # 过滤掉旧的 Header 注释行（保留非 # 开头的规则行）
            if not line.strip().startswith("#"):
                raw_lines.append(line.strip())

    # 清除空行
    rules = [l for l in raw_lines if l]

    # 统计各项数量
    counts = {
        "DOMAIN": sum(1 for r in rules if r.startswith("DOMAIN,")),
        "DOMAIN-KEYWORD": sum(1 for r in rules if r.startswith("DOMAIN-KEYWORD,")),
        "DOMAIN-SUFFIX": sum(1 for r in rules if r.startswith("DOMAIN-SUFFIX,")),
        "IP-CIDR": sum(1 for r in rules if r.startswith("IP-CIDR,")),
        "IP-CIDR6": sum(1 for r in rules if r.startswith("IP-CIDR6,")),
    }
    total = sum(counts.values())

    # 获取北京时间 (UTC+8)
    tz_bj = timezone(timedelta(hours=8))
    now_str = datetime.now(tz_bj).strftime("%Y-%m-%d %H:%M:%S")

    # 构造 Header
    header = f"""# NAME: {rule_name}
# AUTHOR: {AUTHOR}
# REPO: {REPO_URL}
# UPDATED: {now_str}
# DOMAIN: {counts['DOMAIN']}
# DOMAIN-KEYWORD: {counts['DOMAIN-KEYWORD']}
# DOMAIN-SUFFIX: {counts['DOMAIN-SUFFIX']}
# IP-CIDR: {counts['IP-CIDR']}
# IP-CIDR6: {counts['IP-CIDR6']}
# TOTAL: {total}
"""

    # 写入更新后的完整内容
    content = header + "\n" + "\n".join(rules) + "\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"成功更新: {file_path}")

if __name__ == "__main__":
    for file_path in FILES:
        process_file(file_path)