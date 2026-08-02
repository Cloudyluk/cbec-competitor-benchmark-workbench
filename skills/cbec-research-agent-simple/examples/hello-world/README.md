# 极简范例（hello-world）：最小交付格式演示

> ⚠️ **本目录是「格式模板 / 教学范例」，数据为演示占位，请勿当作真实调研结论。**
> 真实调研请联网核验后用真实数据替换本例中的 `示例品牌 / 示例科技 / example.com` 等占位内容。

## 它演示什么
完整流程要 8 个文件、走 P0→P6；但**最小可用交付只要 3 个文件**。本例就用这 3 个文件，展示一份「快路径」报告长什么样：

| 文件 | 作用 | 对应阶段 |
|---|---|---|
| `00_brief.md` | 范围 + 身份卡（锁死「查的是谁」+ 排除同名实体） | P0 + P1 |
| `10_evidence_ledger.csv` | 证据账本（≥3 条核心事实，挂等级与来源） | P2 + P3 |
| `50_report.md` | 一页结论：一档决策 + 身份 + 核心证据 + 不确定项 | P5 + 快路径报告 |

## 怎么用
1. 复制本目录，把文件名/`示例品牌` 换成你的真实对象。
2. 按 SKILL.md P1 填身份卡，`10_evidence_ledger.csv` 逐行联网核验后填（每条带 `data_as_of` + `metric_type`）。
3. 运行校验，看决策上限：
   ```bash
   python ../../scripts/ledger_check.py 10_evidence_ledger.csv --scenario competitor
   ```
4. 用 `../../assets/report-template-quick.md` 的字段填 `50_report.md`。

## 为什么从这里开始
- 想看「一份能用的调研报告」长什么样 → 读 `50_report.md`。
- 想抄「证据账本怎么填」→ 读 `10_evidence_ledger.csv`（注意 `level` 五档 + `data_as_of`/`metric_type` 列）。
- 跑熟了再上完整流程（见 `../anker-financial-refresh/`、`../sme-benchmark/`、`../vankyo-wantuo/`）。
