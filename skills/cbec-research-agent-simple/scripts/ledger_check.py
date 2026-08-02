#!/usr/bin/env python3
"""校验证据账本，输出等级分布与决策等级上限提示。

用法:
    python ledger_check.py <evidence_ledger.csv> [--scenario <场景代码>]
"""

import argparse
import csv
import datetime as _dt
import re
import sys
from collections import Counter
from pathlib import Path

LEVELS = ["VERIFIED", "STRONG", "WEAK", "UNVERIFIED", "CONFLICT"]
SOURCE_TYPES = ["L1_official", "L2_platform", "L3_authoritative", "L4_tool_or_community"]
REQUIRED = ["fact_id", "category", "claim", "level", "source_type", "accessed_at"]

# 第三方估算工具关键词：出现在 source_url 中却标 VERIFIED 属违规
TOOL_HOSTS = [
    "keepa", "junglescout", "helium10", "sellersprite", "卖家精灵", "sellerspirit",
    "kalodata", "fastmoss", "echotik", "chanmama", "蝉妈妈", "similarweb",
    "semrush", "ahrefs", "importyeti", "panjiva", "builtwith",
]

# 各场景核心事实类别（缺失或未达 VERIFIED 会压低决策上限）
CORE_CATEGORIES = {
    "sourcing":    ["product", "compliance", "market"],
    "supplier":    ["identity", "operational", "compliance", "supply_chain"],
    "competitor":  ["identity", "market", "product"],
    "voc":         ["product", "market"],
    "content":     ["product", "compliance"],
    "livescript":  ["product", "compliance"],
    "investment":  ["identity", "financial", "operational", "compliance"],
    "riskwatch":   ["compliance", "identity"],
}

# 新鲜度阈值（staleness_days = 今天 − data_as_of）
# 取值见 references/freshness-policy.md
FRESHNESS_THRESHOLDS = {
    "fast":    (90, 180),     # FRESH<=90, AGED 91-180, STALE>180
    "medium":  (180, 365),    # FRESH<=180, AGED 181-365, STALE>365
    "slow":    (365, 540),    # FRESH<=365, AGED 366-540, STALE>540(>18个月，上市公司年报超此即应补最新期)
    "structural": None,       # 不参与新鲜度
    "na": None,
}
VALID_METRIC_TYPES = set(FRESHNESS_THRESHOLDS.keys())

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_RE = re.compile(r"^https?://", re.I)
ASOF_RE = re.compile(r"^(\d{4})-(\d{2})$|^(\d{4})-Q([1-4])$")


def load(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def parse_asof(raw: str):
    """把 data_as_of (YYYY-MM 或 YYYY-Qn) 解析为近似日期（取月末/季末）。失败返回 None。"""
    if not raw:
        return None
    m = ASOF_RE.match(raw.strip())
    if not m:
        return None
    if m.group(1):  # YYYY-MM
        y, mo = int(m.group(1)), int(m.group(2))
        if not (1 <= mo <= 12):
            return None
        # 月末
        if mo == 12:
            return _dt.date(y, 12, 31)
        nxt = _dt.date(y, mo + 1, 1)
        return nxt - _dt.timedelta(days=1)
    else:  # YYYY-Qn
        y, q = int(m.group(3)), int(m.group(4))
        end_month = q * 3
        return _dt.date(y, end_month, [31, 30, 30, 31][q - 1])


def freshness_band(metric_type: str, asof: _dt.date, today: _dt.date):
    """返回 ('FRESH'|'AGED'|'STALE'|'N/A', staleness_days)"""
    if metric_type not in FRESHNESS_THRESHOLDS or FRESHNESS_THRESHOLDS.get(metric_type) is None:
        return "N/A", None
    if asof is None:
        return "N/A", None
    days = (today - asof).days
    fresh_max, aged_max = FRESHNESS_THRESHOLDS[metric_type]
    if days <= fresh_max:
        return "FRESH", days
    if days <= aged_max:
        return "AGED", days
    return "STALE", days


def check(rows):
    """返回 (errors, warnings, freshness)"""
    errors, warnings = [], []
    seen = set()
    today = _dt.date.today()
    freshness = {}  # fact_id -> (band, days, data_as_of, metric_type)

    for i, r in enumerate(rows, start=2):  # 表头占第 1 行
        fid = (r.get("fact_id") or "").strip() or f"<第{i}行>"

        for col in REQUIRED:
            if not (r.get(col) or "").strip():
                errors.append(f"{fid}: 缺少必填字段 `{col}`")

        if fid in seen:
            errors.append(f"{fid}: fact_id 重复")
        seen.add(fid)

        level = (r.get("level") or "").strip().upper()
        if level and level not in LEVELS:
            errors.append(f"{fid}: level 非法值 `{level}`，应为 {'/'.join(LEVELS)}")

        st = (r.get("source_type") or "").strip()
        if st and st not in SOURCE_TYPES:
            warnings.append(f"{fid}: source_type `{st}` 不在推荐取值内 {SOURCE_TYPES}")

        url = (r.get("source_url") or "").strip()
        if not url:
            if level in ("VERIFIED", "STRONG"):
                errors.append(f"{fid}: {level} 级事实必须提供 source_url 或明确的获取方式")
        elif not URL_RE.match(url):
            warnings.append(f"{fid}: source_url 不是 http(s) 链接（若为线下获取请在 note 中说明）")

        acc = (r.get("accessed_at") or "").strip()
        if acc and not DATE_RE.match(acc):
            errors.append(f"{fid}: accessed_at 格式应为 YYYY-MM-DD，实为 `{acc}`")
        elif acc:
            try:
                d = _dt.date.fromisoformat(acc)
                if d > today:
                    errors.append(f"{fid}: accessed_at `{acc}` 晚于今天")
                elif (today - d).days > 180:
                    warnings.append(f"{fid}: 访问日期距今 {(today - d).days} 天，考虑重新核验")
            except ValueError:
                errors.append(f"{fid}: accessed_at 无法解析 `{acc}`")

        # 媒体日锚点 reported_at（私有公司模式关键）：记媒体/工具发布该数据的日期
        rp = (r.get("reported_at") or "").strip()
        if rp:
            if not DATE_RE.match(rp):
                warnings.append(f"{fid}: reported_at 格式应为 YYYY-MM-DD，实为 `{rp}`")
            else:
                try:
                    rd = _dt.date.fromisoformat(rp)
                    if rd > today:
                        errors.append(f"{fid}: reported_at `{rp}` 晚于今天")
                    elif (today - rd).days > 365:
                        warnings.append(
                            f"{fid}: 知识陈旧（数据来自 {rp} 的媒体/工具报道，距今 {(today - rd).days} 天）— 建议重新检索最新报道（黄旗 Y30）")
                except ValueError:
                    warnings.append(f"{fid}: reported_at 无法解析 `{rp}`")

        if level in ("VERIFIED", "STRONG") and not (r.get("source_quote") or "").strip():
            errors.append(f"{fid}: {level} 级事实必须提供 source_quote 原文摘录以便复现")

        if level == "VERIFIED":
            low = (url + " " + (r.get("note") or "")).lower()
            hit = [t for t in TOOL_HOSTS if t in low]
            if hit:
                errors.append(
                    f"{fid}: 来自第三方估算工具 {hit} 的数据不得标为 VERIFIED，最高 WEAK")
            if st == "L4_tool_or_community":
                errors.append(f"{fid}: source_type=L4 不可能达到 VERIFIED")

        if level == "CONFLICT" and not (r.get("conflicts_with") or "").strip():
            errors.append(f"{fid}: CONFLICT 必须用 conflicts_with 指向对立的 fact_id")

        # 口径启发式：数字型事实需要具体时间锚点（年份 / 近N期 / 季度 / 截至日期）
        claim = (r.get("claim") or "") + " " + (r.get("note") or "")
        has_number = bool(re.search(r"\d", r.get("claim") or ""))
        has_time_kw = bool(re.search(r"20\d{2}|近\s*\d+|Q[1-4]\b|FY\d|截至|trailing|TTM|LTM", claim, re.I))
        mt = (r.get("metric_type") or "").strip().lower()
        ao = (r.get("data_as_of") or "").strip()
        is_timed_metric = mt in ("fast", "medium", "slow")

        # 口径启发式：数字型且非 structural/na 的事实应带时间锚点
        if has_number and mt not in ("structural", "na"):
            if not has_time_kw:
                warnings.append(
                    f"{fid}: 数字型事实缺少具体时间锚点（如 2026-06 / 近12个月 / 截至日期），按口径规则应降一级")

        # 时效强制：以 metric_type 为驱动信号
        if is_timed_metric:
            if not ao:
                warnings.append(f"{fid}: 时效型事实缺少 data_as_of（数据截至时点），违反时效强制规则")
            asof = parse_asof(ao) if ao else None
            if ao and asof is None:
                warnings.append(f"{fid}: data_as_of `{ao}` 无法解析（应为 YYYY-MM 或 YYYY-Qn）")
            band, days = freshness_band(mt, asof, today)
            freshness[fid] = (band, days, ao, mt)
            if band == "STALE":
                warnings.append(
                    f"{fid}: 数据已过期（data_as_of={ao}，距今 {days} 天，类型={mt}）— STALE，相关核心事实将限制决策上限")
        elif mt == "":
            if has_number or has_time_kw:
                warnings.append(f"{fid}: 数字/时点型事实缺少 metric_type（fast/medium/slow/structural/na），违反时效强制规则")
                if not ao:
                    warnings.append(f"{fid}: 数字/时点型事实缺少 data_as_of（数据截至时点），违反时效强制规则")
            freshness[fid] = ("N/A", None, ao, "")
        else:  # structural / na / 非法
            if mt and mt not in VALID_METRIC_TYPES:
                warnings.append(f"{fid}: metric_type `{mt}` 不在取值 {sorted(VALID_METRIC_TYPES)} 内")
            freshness[fid] = ("N/A", None, ao, mt)

    # 冲突指向双向性
    by_id = {(r.get("fact_id") or "").strip(): r for r in rows}
    for r in rows:
        fid = (r.get("fact_id") or "").strip()
        for target in [t.strip() for t in (r.get("conflicts_with") or "").split(",") if t.strip()]:
            if target not in by_id:
                errors.append(f"{fid}: conflicts_with 指向不存在的 fact_id `{target}`")
            else:
                back = [t.strip() for t in (by_id[target].get("conflicts_with") or "").split(",")]
                if fid not in back:
                    warnings.append(f"{fid} <-> {target}: 冲突指向不是双向的")

    return errors, warnings, freshness


def ceiling(rows, scenario, freshness, mode="standard"):
    """计算决策等级上限

    mode="sme"（私有公司模式）：核心类别 financial/operational 仅因缺 VERIFIED（SME 无官方财务源，属预期），
    封顶由"补充尽调"降为"谨慎通过"，并标注未上市口径；CONFLICT / STALE 仍按标准封顶。
    """
    counts = Counter((r.get("level") or "").strip().upper() for r in rows)
    reasons = []
    cap = "通过"

    if counts.get("CONFLICT"):
        cap = "补充尽调"
        reasons.append(f"存在 {counts['CONFLICT']} 条 CONFLICT 事实，须先解决冲突")

    core = CORE_CATEGORIES.get(scenario or "", [])
    if core:
        by_cat = {}
        for r in rows:
            by_cat.setdefault((r.get("category") or "").strip(), []).append(
                (r.get("level") or "").strip().upper())
        for c in core:
            lv = by_cat.get(c)
            if not lv:
                cap = "补充尽调"
                reasons.append(f"核心类别 `{c}` 无任何证据记录")
            elif "VERIFIED" not in lv:
                if mode == "sme" and c != "identity":
                    # SME 未上市：除 identity（工商可核验）外，市场/产品/运营/财务均无官方 VERIFIED 源，
                    # 缺口属预期，降为谨慎通过，以 WEAK/L4 估算+交叉验证替代
                    if cap == "通过":
                        cap = "谨慎通过"
                    reasons.append(
                        f"核心类别 `{c}` 无 VERIFIED 级证据（现有：{sorted(set(lv))}）—— SME 未上市，无官方源可达 VERIFIED 属预期，以 WEAK/L4 估算+交叉验证替代")
                else:
                    cap = "补充尽调"
                    reasons.append(f"核心类别 `{c}` 无 VERIFIED 级证据（现有：{sorted(set(lv))}）")

    # 时效闸门：核心类别存在 STALE 事实 → 补充尽调（详见 freshness-policy.md）
    if cap not in ("补充尽调", "淘汰") and core:
        by_cat_levels = {}
        for r in rows:
            by_cat_levels.setdefault((r.get("category") or "").strip(), []).append(r)
        stale_core = []
        for c in core:
            for r in by_cat_levels.get(c, []):
                fid = (r.get("fact_id") or "").strip()
                band, days, ao, mt = freshness.get(fid, ("N/A", None, "", ""))
                if band == "STALE":
                    stale_core.append((c, fid, ao, days, mt))
        if stale_core:
            if mode == "sme":
                # SME 未上市：data_as_of 业务期偏早多因无可更新审计期，不直接封顶补充尽调，
                # 降为谨慎通过并提示重新检索最新媒体/工具披露（详见 freshness-policy.md 第七节）
                if cap == "通过":
                    cap = "谨慎通过"
                for c, fid, ao, days, mt in stale_core:
                    reasons.append(
                        f"核心类别 `{c}` 数据偏旧（{fid} data_as_of={ao}，距今 {days} 天，类型={mt}）；SME 未上市无更新审计期，建议重新检索最新媒体/工具披露（Y29）")
            else:
                cap = "补充尽调"
                for c, fid, ao, days, mt in stale_core:
                    reasons.append(f"核心类别 `{c}` 存在 STALE 事实 {fid}（data_as_of={ao}，距今 {days} 天，类型={mt}），须补最新一期披露")

    if cap == "通过":
        weak_ratio = (counts.get("WEAK", 0) + counts.get("UNVERIFIED", 0)) / max(len(rows), 1)
        if weak_ratio > 0.5:
            cap = "谨慎通过"
            reasons.append(f"WEAK+UNVERIFIED 占比 {weak_ratio:.0%}，证据基础偏薄")

    return cap, reasons, counts


def main():
    ap = argparse.ArgumentParser(description="校验跨境电商调研证据账本")
    ap.add_argument("path")
    ap.add_argument("--scenario", default="", choices=[""] + list(CORE_CATEGORIES))
    ap.add_argument("--mode", default="standard", choices=["standard", "sme"],
                    help="standard=上市公司标准；sme=私有公司/中小卖家模式（财务 VERIFIED 缺口降为谨慎通过）")
    args = ap.parse_args()

    p = Path(args.path).expanduser()
    if not p.exists():
        print(f"文件不存在: {p}", file=sys.stderr)
        return 2

    rows = load(p)
    if not rows:
        print("账本为空，无法校验", file=sys.stderr)
        return 2

    errors, warnings, freshness = check(rows)
    cap, reasons, counts = ceiling(rows, args.scenario, freshness, args.mode)

    mode_tag = "（私有公司/SME 模式）" if args.mode == "sme" else ""
    print(f"账本: {p}   共 {len(rows)} 条事实   模式: {args.mode}{mode_tag}\n")
    print("证据等级分布")
    label = {"VERIFIED": "已核验", "STRONG": "强推断", "WEAK": "弱推断",
             "UNVERIFIED": "未证实", "CONFLICT": "冲突"}
    for lv in LEVELS:
        n = counts.get(lv, 0)
        bar = "#" * min(n, 40)
        print(f"  {label[lv]:<5} {lv:<11} {n:>4}  {bar}")
    other = {k: v for k, v in counts.items() if k not in LEVELS}
    if other:
        print(f"  非法等级值: {dict(other)}")

    # 新鲜度汇总
    fb = Counter(v[0] for v in freshness.values())
    print("\n数据新鲜度（基于 data_as_of）")
    for band in ("FRESH", "AGED", "STALE", "N/A"):
        n = fb.get(band, 0)
        note = {"FRESH": "新鲜", "AGED": "偏旧", "STALE": "⚠ 过期-限制决策", "N/A": "非时间型/未标注"}[band]
        print(f"  {band:<6} {n:>4}  {note}")
    stale_list = [fid for fid, v in freshness.items() if v[0] == "STALE"]
    if stale_list:
        print(f"  STALE 事实: {', '.join(stale_list)}")

    print(f"\n错误 {len(errors)} 项 / 警告 {len(warnings)} 项")
    for e in errors:
        print(f"  [错误] {e}")
    for w in warnings:
        print(f"  [警告] {w}")

    print(f"\n决策等级上限: 【{cap}】")
    if reasons:
        for r in reasons:
            print(f"  · {r}")
    else:
        print("  · 证据基础满足最高档决策的形式要求（红旗/黄旗仍须按 decision-rubric.md 单独判定）")

    if errors:
        print("\n存在错误，修正后重跑再进入 P5 决策。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
