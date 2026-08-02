# 竞品对标 AI 工作台 HTML 工具与 Skill 完善方案

## 一、项目目标

基于现有 `cbec-research-agent-simple` skill，进一步封装成一个普通人可以直接使用的竞品对标 AI 工具。

最终目标：

> 用户打开一个 HTML 页面，接入自己的大模型 API Key，输入竞品信息和本公司情况，即可生成竞品对标报告、能力评分卡和 30/60/90 天量化提升计划。

本项目同时包含两部分：

1. **完善 Skill**
   - 让 Agent 环境中的用户可以直接调用
   - 输出结构更稳定
   - 方便后续网页工具复用提示词和评分逻辑

2. **封装 HTML 工具**
   - 普通用户双击打开即可使用
   - 用户自带 API Key
   - 接入 OpenAI 兼容大模型 API
   - 自动生成结构化竞品对标报告

## 二、产品定位

### 产品名称

跨境竞品对标 AI 工作台

### 英文名

CBEC Competitor Benchmark Workbench

### 一句话定位

一个面向跨境电商公司的本地 HTML AI 工具，帮助用户调研竞品、量化公司能力差距，并生成可执行的 30/60/90 天提升计划。

### 虚拟岗位定位

跨境竞品对标分析师

负责：

- 调研竞品
- 核验竞品身份
- 分析竞品优势
- 评估本公司差距
- 输出能力评分卡
- 生成量化提升计划

## 三、目标用户

### 核心用户

- 跨境电商老板
- 运营负责人
- 类目负责人
- 产品开发负责人
- 市场调研人员
- 竞品分析人员

### 次核心用户

- Amazon 运营
- TikTok Shop 运营
- 独立站运营
- 广告投放人员
- 内容/品牌负责人
- 供应链负责人

## 四、核心使用场景

### 1. 竞品调研

用户输入竞品品牌、店铺、官网、ASIN 或社媒账号，系统帮助分析：

- 竞品是谁
- 竞品在哪些渠道活跃
- 竞品有哪些核心优势
- 竞品有哪些风险或不可复制点

### 2. 公司能力对标

用户补充本公司信息后，系统帮助对比：

- 产品能力差距
- 平台运营差距
- 内容能力差距
- 广告增长差距
- 品牌信任差距
- 供应链履约差距
- 数据管理差距

### 3. 量化提升计划

系统根据差距生成：

- 30 天可执行动作
- 60 天阶段性改进动作
- 90 天体系化提升动作
- 每个动作对应 KPI、目标值和负责人建议

### 4. 管理层复盘

管理层可以用它定期做：

- 月度竞品复盘
- 季度能力评估
- 新品立项前分析
- 类目战略对标
- 团队 OKR 输入

## 五、产品形态

### 形态一：Skill 版

适合已经在 Codex 或 Agent 环境中的用户。

调用方式示例：

```text
用 $cbec-research-agent-simple 调研 JISULIFE 几素，对标我们公司，输出能力评分卡和 90 天提升计划。
```

特点：

- 适合专业用户
- 可结合 Agent 联网检索能力
- 可生成 Markdown、CSV、证据账本
- 适合深度调研

### 形态二：HTML 工具版

适合普通业务用户。

使用方式：

1. 打开 `index.html`
2. 填入 API Base URL、API Key、Model
3. 输入竞品信息和本公司信息
4. 点击“生成对标报告”
5. 查看并导出 Markdown 报告

特点：

- 打开即用
- 不需要安装
- 不需要懂命令行
- 数据保存在浏览器本地
- 支持 OpenAI 兼容大模型 API

## 六、HTML 工具功能设计

### 1. API 设置区

字段：

- API Base URL
- API Key
- Model
- Temperature
- Max Tokens

按钮：

- 保存设置
- 测试连接
- 清除设置

说明：

- API Key 只保存在用户本地浏览器
- 不上传到除用户填写的模型接口之外的任何地方
- 支持 OpenAI 兼容接口

### 2. 竞品输入区

字段：

- 竞品名称
- 竞品链接，可选
- 竞品类型
  - 品牌
  - 平台店铺
  - 独立站
  - 商品/ASIN
  - 直播间/社媒账号
  - 类目头部品牌
- 目标市场
  - 美国
  - 欧洲
  - 英国
  - 日本
  - 东南亚
  - 其他
- 所属类目
- 调研重点
  - 综合能力
  - 产品组合
  - 平台运营
  - 内容素材
  - 广告投放
  - 独立站
  - 品牌信任
  - 供应链履约

### 3. 本公司信息区

字段：

- 公司/品牌名称
- 主营类目
- 目标市场
- 当前主要平台
- Top SKU
- 当前痛点
- 月销售额区间，可选
- 广告渠道，可选
- 团队规模，可选
- 可补充的内部数据

说明：

如果用户不填写本公司信息，系统只评分竞品，并列出需要本公司补充的数据。

### 4. 分析模式

提供两种模式：

#### 快速模式

适合普通用户。

输出：

- 结论
- 竞品优势
- 能力评分卡
- 关键差距
- 30/60/90 天提升计划

#### 专业模式

适合深度分析。

输出：

- 竞品身份核验
- 证据等级
- 渠道足迹
- 能力评分卡
- 风险与不可复制点
- 数据缺口
- 30/60/90 天提升计划
- Markdown 完整报告

### 5. 结果展示区

结果页面包含：

- 结论卡
- 竞品身份
- 竞品核心优势
- 渠道与经营迹象
- 能力评分卡
- 差距分析
- 可量化提升机会
- 30/60/90 天行动计划
- 需要本公司补充的数据
- 风险与不可复制点

### 6. 导出功能

支持：

- 复制 Markdown
- 下载 Markdown
- 下载 JSON
- 清空结果

## 七、能力评分体系

默认使用 10 个能力项，每项 1-5 分。

| 能力项 | 说明 |
|---|---|
| Product Portfolio | 产品组合、SKU、价格梯度、差异化、认证 |
| Marketplace Operations | 平台店铺、Listing、评论、促销、转化 |
| DTC Website | 独立站体验、信任模块、转化路径、SEO |
| Content and Creatives | 图片、视频、UGC、达人素材、直播内容 |
| Paid Growth | 广告渠道、素材、落地页、优惠、再营销 |
| Social and Community | 社媒矩阵、互动、达人、用户社区 |
| Pricing and Promotion | 价格带、优惠节奏、组合销售、毛利风险 |
| Supply Chain and Fulfillment | 发货、退货、仓储、售后、合规 |
| Brand Trust | 认证、保修、媒体、评论、品牌故事 |
| Data and Management | KPI、实验节奏、复盘、用户反馈闭环 |

评分规则：

- 1 分：明显落后
- 2 分：基础薄弱
- 3 分：行业平均
- 4 分：较强
- 5 分：优秀，值得重点学习

## 八、输出结构

HTML 工具应要求大模型返回结构化 JSON，再渲染成页面和 Markdown。

### JSON 输出结构

```json
{
  "summary": {
    "benchmark_result": "重点学习",
    "one_sentence_reason": "",
    "confidence": "medium"
  },
  "competitor_identity": {
    "name": "",
    "type": "",
    "company_entity": "",
    "official_site": "",
    "channels": [],
    "ambiguities": []
  },
  "key_evidence": [
    {
      "fact": "",
      "confidence": "已核验",
      "source": "",
      "date": ""
    }
  ],
  "strengths": [
    {
      "area": "",
      "observation": "",
      "why_it_matters": "",
      "evidence": ""
    }
  ],
  "scorecard": [
    {
      "capability": "Product Portfolio",
      "competitor_score": 4,
      "our_score": null,
      "gap": null,
      "priority": "high",
      "evidence": ""
    }
  ],
  "improvement_opportunities": [
    {
      "opportunity": "",
      "current_gap": "",
      "target_30_60_90": "",
      "kpi": ""
    }
  ],
  "action_plan": {
    "days_30": [],
    "days_60": [],
    "days_90": []
  },
  "missing_company_data": [],
  "risks_and_non_transferable_points": [],
  "markdown_report": ""
}
```

## 九、Skill 完善方向

现有 `cbec-research-agent-simple` 需要继续补充：

### 1. 增加 API/HTML 模式说明

在 Skill 中说明：

- HTML 工具调用的是同一套竞品对标逻辑
- 用户通过大模型 API 获取分析结果
- 网页工具适合快速对标
- Agent Skill 适合深度联网调研

### 2. 增加结构化输出约束

Skill 应补充：

- JSON 输出结构
- Markdown 报告结构
- 能力评分字段
- 行动计划字段

### 3. 增加普通用户默认行为

Skill 默认不要求用户理解：

- P0/P6
- Evidence Ledger
- Source Tier
- SME Mode

而是自动转换成：

- 竞品是谁
- 哪里强
- 我们差什么
- 怎么提升

### 4. 增加网页版共享资产

可新增：

- `assets/web-prompt.md`
- `assets/output-schema.json`
- `assets/html-usage.md`

用于网页工具和 Skill 共同调用。

## 十、技术实现建议

### 第一版：纯前端单文件 HTML

文件：

```text
cbec-competitor-benchmark-workbench.html
```

特点：

- 单文件
- 无需安装
- 无需后端
- 本地保存 API 设置
- 直接请求用户填写的 OpenAI 兼容接口

适合：

- 个人使用
- 小团队试用
- 快速验证产品价值

### 第二版：HTML + 本地代理

增加一个本地代理服务：

```text
local-api-proxy
```

特点：

- API Key 不暴露在浏览器请求中
- 可接更多数据源 API
- 可做网页抓取与搜索

适合：

- 团队内部使用
- 对密钥安全要求更高的场景

### 第三版：SaaS 版

增加：

- 用户系统
- 项目库
- 竞品库
- 报告库
- 团队协作
- 任务看板
- 数据源管理

适合：

- 商业化产品
- 多团队协作
- 长期数据沉淀

## 十一、安全说明

纯 HTML 版本需要明确提示：

- API Key 保存在本地浏览器
- 不要在不可信电脑上使用
- 不要把带有 API Key 的页面截图或分享给他人
- 如果企业要求更高安全性，应使用本地代理或后端版本

## 十二、MVP 开发范围

第一版只做以下功能：

1. API 设置
2. 竞品输入
3. 本公司信息输入
4. 快速/专业模式选择
5. 调用大模型 API
6. 渲染结构化结果
7. 导出 Markdown
8. 导出 JSON
9. 本地保存配置

暂不做：

- 登录系统
- 团队协作
- 竞品库
- 数据库
- 自动联网搜索
- 多数据源 API 聚合
- 后端服务

## 十三、推荐开发步骤

### Step 1：完善 Skill

- 增加 HTML/API 模式说明
- 增加 JSON 输出 schema
- 增加网页提示词模板
- 重新打包 skill

### Step 2：开发 HTML 工具

- 构建单文件 HTML
- 实现 API 设置
- 实现表单输入
- 实现大模型调用
- 实现结果渲染
- 实现 Markdown/JSON 导出

### Step 3：验证

- 用示例品牌测试
- 测试 API 连接失败场景
- 测试 JSON 解析失败场景
- 测试无本公司数据场景
- 测试导出 Markdown

### Step 4：打包交付

交付物：

- `cbec-research-agent-simple.zip`
- `cbec-competitor-benchmark-workbench.html`
- `竞品对标AI工作台-HTML工具与Skill完善方案.md`

## 十四、最终交付目标

最终用户体验：

1. 打开 HTML
2. 填 API Key
3. 输入竞品和本公司情况
4. 点击生成
5. 得到竞品对标报告、能力评分卡和 30/60/90 天提升计划

最终产品价值：

> 让普通跨境电商团队不需要懂复杂调研方法，也能用 AI 持续对标竞品、发现差距、制定量化提升计划。
