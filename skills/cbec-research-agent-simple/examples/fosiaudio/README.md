# 范例：Fosi Audio 佛斯/弗西音响 — SME 私企「谨慎通过」完整跑通（SME 模式）

> 本目录是一个**完整可复用的「真实标的跑通」范例**，覆盖 CBEC-research-agent 全工作流程（P0→P6）。
> 所有数据均为公开来源、本次（2026-08-02）联网核验，附 URL 与 `data_as_of` 时点。
> 用途：新用户或新标的调研时，直接复制本目录结构作为起点，或对照本范例检查自家输出是否达标。

## 1. 场景与标的

- **场景**：竞品对标分析 / 投融资初筛（含全渠道足迹发现 + 曝光度量 + 参考价值评分）
- **标的**：Fosi Audio（中文「弗西音频」；用户清单音译"佛斯"），深圳远虑科技旗下 HiFi 音频品牌
- **运营主体**：深圳远虑科技有限公司（USCC **91440300MA5DT7DQ0G**，法人黄庆龙，2017-01-12 成立）
- **调研日期**：2026-08-02
- **模式**：私有公司 / SME（`ledger_check.py --scenario competitor --mode sme`）
- **为什么选它**：用于演示**未上市私企、无审计财报、核心数据 STALE** 时，SME 模式如何把决策封顶在「谨慎通过」而非「补充尽调」；同时验证 `references/brand-entity-map.md` 中"Fosi Audio↔远虑科技"映射（已 VERIFIED）。

## 2. 工作流执行摘要

```
P0 需求澄清（竞品对标；音译"佛斯"≠不同主体，统一为 Fosi Audio）
 → P1 身份核验（天眼查锁定 USCC 91440300MA5DT7DQ0G，门禁通过；无同名混淆）
 → P1.5 全渠道足迹（8 条渠道 → 3 条入矩阵：独立站 A + 官方社区 A + Amazon 2B 高度可能）
 → P2 联网采集（边采边记账，2023/2024/2025/2026 多时点）
 → P3 证据账本（13 条事实，data_as_of/metric_type/reported_at 齐备）
 → P4 纵向发展 + 横向竞品对比 + 曝光度量 + 参考价值评分
 → P5 决策（谨慎通过，受 STALE 时效闸门 + SME 核心类别缺口双重约束）
 → P6 六件套输出（结论/账本/来源/冲突/不可达/下一步问题）
```

## 3. 关键学习点：SME 私企的时效封顶

**问题**：未上市私企无强制披露，核心 market/financial 数据通常停留在媒体报道时点（本例 2023–2024），与调研日（2026-08）相差 1.5–2.5 年 → 触发 STALE。

**本范例演示的正确处理**：
- F004（覆盖 150+ 国家，`data_as_of=2024-12`）→ STALE
- F007（2023 亚马逊破 1 亿，`data_as_of=2023-12`）→ STALE
- `ledger_check --mode sme` 自动将 STALE 类事实封顶为「谨慎通过 + 建议补最新披露」，而非「补充尽调」。

**附带演示：品牌↔公司消歧**。Fosi Audio 英文名与"远虑科技"无字面关联，仅靠名称搜索会漏；本例用官网 About 页自述 + 工商登记闭合映射（见 `references/brand-entity-map.md` FosiAudio 行，已标 VERIFIED）。

## 4. 可复制：SME 私企检索式

```
"<品牌名>" 天眼查 / 企查查            # 反查运营主体 USCC 与法人（P1 门禁必备）
"<品牌名>" "about" "brand of"         # 官网自述品牌归属，闭合品牌↔公司映射
"<品牌名>" 雨果跨境 / 亿恩 / 36氪      # 找最近销售/营收披露时点（定 data_as_of）
"<品牌名>" 创始人 专访                # 补复购率/增长等 STRONG 级市场事实
```

## 5. 目录文件说明

| 文件 | 对应阶段 | 用途 |
|---|---|---|
| `00_brief.md` | P0 / P1 | 需求澄清 + 身份卡 |
| `omnichannel-footprint.csv` | P1.5 | 全渠道足迹（含 A/B/C 归因证据） |
| `footprint_scan_result.csv` | P1.5 | `footprint_scan.py` 准入判定结果 |
| `10_evidence_ledger.csv` | P3 | 证据账本（含 `data_as_of`/`metric_type`/`reported_at`，演示 STALE） |
| `20_sources.csv` | P3 / P6 | 来源清单（含不可达） |
| `30_conflicts.md` | P3 / P6 | 冲突事实记录 |
| `40_unreachable.md` | P6 | 不可达来源说明 |
| `60_matrix.csv` | P4 | 竞品对比矩阵（Fosi Audio vs Soundcore/Anker vs Aiyima） |
| `50_report.md` | P6 | 主报告（六件套，含数据时效声明） |
| `90_next_questions.md` | P6 | 下一步尽调问题 |

## 6. 用本范例验证工作流

```bash
# 校验账本（SME 模式：含新鲜度汇总 + STALE→决策封顶；预期 0 错误，决策「谨慎通过」）
python scripts/ledger_check.py \
  examples/fosiaudio/10_evidence_ledger.csv --scenario competitor --mode sme

# 全渠道足迹判定（A/B/C 归因 → 矩阵准入；预期 3/8 入矩阵）
python scripts/footprint_scan.py \
  examples/fosiaudio/omnichannel-footprint.csv -o /tmp/fosiaudio_footprint.csv
```

## 7. 复用建议

1. **新 SME 标的**：`cp -r examples/fosiaudio <新标的目录>`，先查 `references/brand-entity-map.md` 是否已有已知映射，再逐文件替换。
2. **防漏映射**：英文名与中文名无关联的标的，P1 必须靠官网 About + 工商登记双源闭合，勿仅依赖名称搜索。
3. **时效**：数字型事实务必带 `data_as_of` + `metric_type`，`ledger_check` 会自动拦截过期并封顶决策。
