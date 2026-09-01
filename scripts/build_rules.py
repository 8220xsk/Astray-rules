import os
from datetime import datetime, timezone, timedelta

# 配置信息（请修改为你自己的用户名和仓库名）
AUTHOR = "8220xsk"
REPO_URL = "https://github.com/8220xsk/Astray-rules"

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

    rule_name = os.path.splitext(os.path.basename(file_path))[0]

    # 定义 Header 专属的关键字前缀
    HEADER_KEYS = (
        "# NAME:", "# AUTHOR:", "# REPO:", "# UPDATED:", 
        "# DOMAIN:", "# DOMAIN-KEYWORD:", "# DOMAIN-SUFFIX:", 
        "# IP-CIDR:", "# IP-CIDR6:", "# TOTAL:"
    )

    clean_lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            # 只有当行是以 Header 关键字开头时才跳过，保留其他所有内容（包括普通 # 注释）
            if any(stripped.startswith(key) for key in HEADER_KEYS):
                continue
            clean_lines.append(stripped)

    # 去除开头的空行，保留有效内容
    while clean_lines and not clean_lines[0]:
        clean_lines.pop(0)

    # 仅对规则行进行统计（忽略以 # 开头的普通注释行）
    rules_only = [l for l in clean_lines if l and not l.startswith("#")]

    counts = {
        "DOMAIN": sum(1 for r in rules_only if r.startswith("DOMAIN,")),
        "DOMAIN-KEYWORD": sum(1 for r in rules_only if r.startswith("DOMAIN-KEYWORD,")),
        "DOMAIN-SUFFIX": sum(1 for r in rules_only if r.startswith("DOMAIN-SUFFIX,")),
        "IP-CIDR": sum(1 for r in rules_only if r.startswith("IP-CIDR,")),
        "IP-CIDR6": sum(1 for r in rules_only if r.startswith("IP-CIDR6,")),
    }
    total = sum(counts.values())

    tz_bj = timezone(timedelta(hours=8))
    now_str = datetime.now(tz_bj).strftime("%Y-%m-%d %H:%M:%S")

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

    # 重新拼接文件：Header + 你的普通注释与规则
    content = header + "\n" + "\n".join(clean_lines) + "\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"成功更新: {file_path}")