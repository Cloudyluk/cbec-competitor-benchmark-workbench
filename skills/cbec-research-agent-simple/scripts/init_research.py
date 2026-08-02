#!/usr/bin/env python3
"""初始化一次跨境电商调研的标准工作区。

用法:
    python init_research.py "<调研对象名>" --type <类型> --scenario <场景代码> [--out <输出根目录>]

示例:
    python init_research.py "Shenzhen ABC Tech" --type supplier --scenario supplier
    python init_research.py "B0XXXXXXX 保温杯" --type product --scenario sourcing --out ./research
"""

import argparse
import datetime as _dt
import re
import shutil
import sys
from pathlib import Path

OBJECT_TYPES = [
    "company", "store", "product", "supplier",
    "brand", "competitor", "partner", "investment",
]

SCENARIOS = {
    "sourcing": "S1 采购选品",
    "supplier": "S2 供应商准入",
    "competitor": "S3 竞品与直播间分析",
    "voc": "S4 客户评价洞察",
    "content": "S5 商品内容生成",
    "livescript": "S6 直播话术辅助",
    "investment": "S7 投融资初筛",
    "riskwatch": "S8 风险预警",
}

SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s[:60] or "research"


def brief_md(name, otype, scenario, date):
    return f"""# 00 调研范围与身份卡 · {name}

## 范围声明

- 调研对象: {name}
- 对象类型: {otype}
- 使用场景: {SCENARIOS.get(scenario, scenario)}
- 目标市场: <!-- US / EU / UK / JP / SEA / LATAM ... -->
- 平台范围: <!-- Amazon / TikTok Shop / Temu / Shopee / 独立站 ... -->
- 时间窗: 近 24 个月（默认，如调整请注明）
- 报告日期: {date}
- **本次不覆盖**: <!-- 必填，显式写出范围外的内容 -->

## 身份卡（P1 门禁，未完成不得进入分析）

| 字段 | 值 | 证据 fact_id | 等级 |
|---|---|---|---|
| 唯一标识符 | | | |
| 官方登记名称 | | | |
| 平台展示名 | | | |
| 关联品牌 | | | |
| 注册法域 | | | |
| 成立日期 | | | |
| 主体状态 | | | |
| 母公司链条 | | | |
| 关联主体 | | | |
| 平台与店铺 ID | | | |
| 独立站域名 | | | |

### 已排除的同名 / 近名实体

| 被排除实体 | 唯一标识 | 排除依据 | 来源 URL |
|---|---|---|---|
| | | | |

> 若确实未发现同名实体，写明"已检索 <渠道列表> 未发现同名实体"并附检索式。

### 门禁自检

- [ ] 唯一标识符 = VERIFIED
- [ ] 官方登记名称 = VERIFIED
- [ ] 排除清单已填写
- [ ] 母公司链条已追溯到已知最上层（未知处显式标注）
- [ ] 若对象为店铺/商品，其运营主体已明确（否则在报告首页声明该限制）
"""


CONFLICTS_MD = """# 30 冲突事实

对每一组冲突，原样并列双方说法，不取平均、不择优采信。

先排除伪冲突：财年 vs 自然年 / GMV vs 净销售额 / 含税 vs 不含税 / 合并 vs 单体 /
平台口径 vs 卖家口径 / 汇率与时点差异 / 统计范围不同。

| # | 冲突项 | A 方说法 + 来源 + 等级 | B 方说法 + 来源 + 等级 | 可能原因 | 证伪路径 | 关联 fact_id |
|---|---|---|---|---|---|---|
| C1 | | | | | | |

*（若无冲突，保留本文件并写"无"）*
"""

UNREACHABLE_MD = """# 40 不可达来源

尝试访问但未取得的来源。这是交付物之一，不是失败记录。

| # | 来源名称 | URL | 尝试日期 | 失败原因 | 替代路径 | 对结论的影响 |
|---|---|---|---|---|---|---|
| U1 | | | | 付费墙 / 需登录 / 地区限制 / 404 / 反爬 / 需线下查册 | | |

*（若全部可达，保留本文件并写"无"）*
"""

NEXT_Q_MD = """# 90 下一步尽调问题

质量标准：每条必须是**可执行且能改变结论**的。

不合格示例：建议进一步了解该公司经营状况。
合格示例：向对方索取近 12 个月 Amazon Seller Central 后台业绩截图（含 Order Defect Rate），
用于验证 F007 中来自第三方工具的销量估算；若实际销量低于估算 50%，决策将由"谨慎通过"下调为"暂缓"。

| 优先级 | 问题 | 向谁问 / 如何取证 | 拿到后会改变什么判断 | 关联 fact_id |
|---|---|---|---|---|
| P0 | | | | |
| P1 | | | | |
| P2 | | | | |
"""


def _init_quick(args):
    """快路径：只生成 3 个文件（身份卡 + 证据账本 + 快报告模板）。"""
    date = _dt.date.today()
    workdir = Path(args.out).expanduser().resolve() / f"{slugify(args.name)}-{date:%Y%m%d}"
    if workdir.exists():
        print(f"目录已存在，未覆盖: {workdir}", file=sys.stderr)
        return 1
    workdir.mkdir(parents=True)

    (workdir / "00_brief.md").write_text(
        brief_md(args.name, args.otype, args.scenario, date), encoding="utf-8")

    ledger_src = ASSETS / "evidence-ledger.csv"
    if ledger_src.exists():
        shutil.copyfile(ledger_src, workdir / "10_evidence_ledger.csv")
    else:
        (workdir / "10_evidence_ledger.csv").write_text(
            "fact_id,category,claim,level,source_type,source_url,accessed_at,"
            "source_quote,conflicts_with,data_as_of,metric_type,reported_at,note\n",
            encoding="utf-8")

    quick_src = ASSETS / "report-template-quick.md"
    if quick_src.exists():
        shutil.copyfile(quick_src, workdir / "50_report.md")
    else:
        (workdir / "50_report.md").write_text("", encoding="utf-8")

    print(f"已创建快路径工作区 (3 文件): {workdir}")
    for p in sorted(workdir.iterdir()):
        print(f"  - {p.name}")
    print(f"\n快路径: 填 00_brief.md 身份卡 + 10_evidence_ledger.csv 证据，再用 report-template-quick.md 出 1 页结论")
    print(f"校验: python scripts/ledger_check.py {workdir / '10_evidence_ledger.csv'} --scenario {args.scenario}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="初始化跨境电商调研工作区")
    ap.add_argument("name", help="调研对象名")
    ap.add_argument("--type", dest="otype", required=True, choices=OBJECT_TYPES)
    ap.add_argument("--scenario", required=True, choices=list(SCENARIOS))
    ap.add_argument("--out", default="research", help="输出根目录，默认 ./research")
    ap.add_argument("--quick", action="store_true",
                    help="快路径：只生成 3 个文件（00_brief.md + 10_evidence_ledger.csv + 50_report.md）")
    args = ap.parse_args()

    if args.quick:
        return _init_quick(args)

    date = _dt.date.today()
    workdir = Path(args.out).expanduser().resolve() / f"{slugify(args.name)}-{date:%Y%m%d}"
    if workdir.exists():
        print(f"目录已存在，未覆盖: {workdir}", file=sys.stderr)
        return 1
    workdir.mkdir(parents=True)

    (workdir / "00_brief.md").write_text(
        brief_md(args.name, args.otype, args.scenario, date), encoding="utf-8")
    (workdir / "30_conflicts.md").write_text(CONFLICTS_MD, encoding="utf-8")
    (workdir / "40_unreachable.md").write_text(UNREACHABLE_MD, encoding="utf-8")
    (workdir / "90_next_questions.md").write_text(NEXT_Q_MD, encoding="utf-8")

    (workdir / "20_sources.csv").write_text(
        "no,source_name,url,tier,accessed_at,credibility_note\n", encoding="utf-8")

    copies = [
        ("evidence-ledger.csv", "10_evidence_ledger.csv"),
        ("competitor-matrix.csv", "60_matrix.csv"),
        ("report-template.md", "50_report.md"),
    ]
    missing = []
    for src, dst in copies:
        s = ASSETS / src
        if s.exists():
            shutil.copyfile(s, workdir / dst)
        else:
            missing.append(src)
            (workdir / dst).write_text("", encoding="utf-8")

    print(f"已创建调研工作区: {workdir}")
    for p in sorted(workdir.iterdir()):
        print(f"  - {p.name}")
    if missing:
        print(f"\n警告: 未找到模板 {missing}，已创建空文件", file=sys.stderr)

    print(f"\n场景: {SCENARIOS[args.scenario]} -> 阅读 references/scenario-playbooks.md 对应章节")
    print("下一步: 完成 00_brief.md 的身份卡与门禁自检后，方可进入 P2 联网采集")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
