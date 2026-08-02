#!/usr/bin/env python3
"""渠道足迹归属判定：按 A/B/C 证据规则决定每条渠道能否进入对比矩阵。

用法:
    python footprint_scan.py <omnichannel-footprint.csv> [-o <输出路径>]

规则（详见 references/omnichannel-discovery.md）:
    >=1 条 A 级                 -> 确认同主体   VERIFIED  可进矩阵
    >=2 条相互独立的 B 级        -> 高度可能     STRONG    可进矩阵
    1 条 B 级                   -> 疑似关联     WEAK      不进矩阵
    仅 C 级 / 无证据             -> 不予判定     WEAK      不进矩阵

"相互独立"：同一性质的证据只计一次。共享 GA ID 与共享 Pixel ID 同属
tracking_id 性质，合并计为一条。
"""

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

# 证据代码 -> (等级, 性质分组)
EVIDENCE = {
    "A_platform_disclosure": ("A", "official"),
    "A_site_legal_page":     ("A", "official"),
    "A_trademark_holder":    ("A", "official"),
    "A_ad_library_entity":   ("A", "official"),
    "A_corporate_registry":  ("A", "official"),
    "A_official_statement":  ("A", "official"),
    "B_tracking_id":         ("B", "tracking_id"),
    "B_return_address":      ("B", "contact"),
    "B_support_email":       ("B", "contact"),
    "B_sku_scheme":          ("B", "product_ops"),
    "B_exclusive_image":     ("B", "product_ops"),
    "B_packaging":           ("B", "product_ops"),
    "B_crtsh_domain":        ("B", "infra"),
    "B_bill_of_lading":      ("B", "trade"),
    "C_similar_name":        ("C", "weak_signal"),
    "C_similar_logo":        ("C", "weak_signal"),
    "C_same_category":       ("C", "weak_signal"),
    "C_same_supplier":       ("C", "weak_signal"),
    "C_shared_ip":           ("C", "weak_signal"),
    "C_same_theme":          ("C", "weak_signal"),
}

STRENGTH = ["无", "试水", "在营", "主力", "核心"]


def judge(codes):
    """返回 (结论, 账本等级, 可否进矩阵, 说明)"""
    valid, unknown = [], []
    for c in codes:
        (valid if c in EVIDENCE else unknown).append(c)

    a_list = [c for c in valid if EVIDENCE[c][0] == "A"]
    b_groups = {EVIDENCE[c][1] for c in valid if EVIDENCE[c][0] == "B"}
    c_list = [c for c in valid if EVIDENCE[c][0] == "C"]

    if a_list:
        return ("确认同主体", "VERIFIED", True,
                f"A 级证据 {len(a_list)} 条: {', '.join(a_list)}", unknown)
    if len(b_groups) >= 2:
        return ("高度可能", "STRONG", True,
                f"独立 B 级证据 {len(b_groups)} 类: {', '.join(sorted(b_groups))}", unknown)
    if len(b_groups) == 1:
        return ("疑似关联", "WEAK", False,
                f"仅 1 类 B 级证据({list(b_groups)[0]})，需补第二类独立证据", unknown)
    if c_list:
        return ("不予判定", "WEAK", False,
                f"仅 C 级线索 {len(c_list)} 条，不可作为归属依据", unknown)
    return ("无证据", "UNVERIFIED", False, "未填写任何归属证据", unknown)


def main():
    ap = argparse.ArgumentParser(description="渠道足迹归属判定")
    ap.add_argument("path")
    ap.add_argument("-o", "--output", help="判定结果输出 CSV")
    args = ap.parse_args()

    p = Path(args.path).expanduser()
    if not p.exists():
        print(f"文件不存在: {p}", file=sys.stderr)
        return 2

    with p.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("足迹表为空", file=sys.stderr)
        return 2

    results, stats, admitted = [], Counter(), []
    all_unknown = set()

    for r in rows:
        codes = [c.strip() for c in (r.get("attribution_evidence") or "").split("|") if c.strip()]
        verdict, level, ok, why, unknown = judge(codes)
        all_unknown.update(unknown)
        stats[verdict] += 1

        strength = (r.get("channel_strength") or "").strip()
        notes = []
        if strength and strength not in STRENGTH:
            notes.append(f"强度档位非法值 `{strength}`，应为 {'/'.join(STRENGTH)}")
        if ok and not strength:
            notes.append("已入矩阵但未填渠道强度分档")
        if strength == "核心":
            admitted.append(r.get("channel") or "")

        results.append({
            "channel": r.get("channel", ""),
            "platform": r.get("platform", ""),
            "account_or_store": r.get("account_or_store", ""),
            "verdict": verdict,
            "ledger_level": level,
            "in_matrix": "YES" if ok else "NO",
            "reason": why,
            "channel_strength": strength,
            "issues": "; ".join(notes),
        })

    print(f"足迹表: {p}   共 {len(rows)} 条渠道\n")
    print("归属判定分布")
    for k, v in stats.most_common():
        print(f"  {k:<8} {v:>3}")

    in_n = sum(1 for r in results if r["in_matrix"] == "YES")
    print(f"\n可进入对比矩阵: {in_n} / {len(rows)}")

    problems = [r for r in results if r["in_matrix"] == "NO" or r["issues"]]
    if problems:
        print("\n需要处理的条目")
        for r in problems:
            tag = "排除" if r["in_matrix"] == "NO" else "提醒"
            print(f"  [{tag}] {r['platform']}/{r['account_or_store']}: {r['reason']}")
            if r["issues"]:
                print(f"          {r['issues']}")

    core = [r for r in results if r["channel_strength"] == "核心"]
    if len(core) > 2:
        print(f"\n[警告] 标为「核心」的渠道有 {len(core)} 个，判定可能过松（建议全局不超过 2 个）")

    if all_unknown:
        print(f"\n[警告] 无法识别的证据代码: {sorted(all_unknown)}")
        print("       合法取值见 references/omnichannel-discovery.md")

    if args.output:
        out = Path(args.output).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
            w.writeheader()
            w.writerows(results)
        print(f"\n判定结果已写入: {out}")

    print("\n提醒: 仅 in_matrix=YES 的渠道可参与 P4 横向对比；其余在报告中单列「疑似关联，未确认」。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
