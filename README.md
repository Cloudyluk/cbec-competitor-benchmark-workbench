# 跨境竞品对标 AI 工作台

一个面向跨境电商团队的本地 HTML 工具，用于竞品调查、公司能力对标、评分卡生成和 30/60/90 天量化提升计划。

## 核心功能

- 固定业务输入：竞品、链接、目标市场、产品类目、本公司信息、对标维度
- API 设置收纳在右上角下拉面板，不干扰普通用户主流程
- 支持 OpenAI 兼容大模型接口：`base_url + api_key + model`
- 一键生成网页版竞品调查报告
- 能力评分卡：产品、平台运营、独立站、内容、投放、社媒、定价、供应链、品牌信任、数据管理
- 30/60/90 天行动计划
- 支持下载 Markdown 和 PDF
- 附带 Codex/Agent skill：`cbec-research-agent-simple`

## 快速使用

直接打开：

```text
index.html
```

或用本地服务器预览：

```bash
python3 -m http.server 8137
```

然后访问：

```text
http://127.0.0.1:8137/
```

## API 设置

点击页面右上角 `API 设置`，填写：

- API Base URL
- API Key
- Model
- Temperature
- Max Tokens

本工具使用 OpenAI 兼容的 `/chat/completions` 接口。

## 安全说明

- API Key 只保存在用户本机浏览器的 `localStorage`。
- 纯前端版本会直接从浏览器请求你填写的 API Base URL。
- 不建议在不可信设备上填写真实 API Key。
- 企业团队正式使用时，建议增加本地代理或后端服务保护密钥。

## 文件结构

```text
.
├── index.html
├── dist/
│   └── cbec-research-agent-simple.zip
├── skills/
│   └── cbec-research-agent-simple/
└── docs/
    ├── 竞品对标AI工作台-HTML工具与Skill完善方案.md
    ├── 跨境竞品对标分析师-产品使用说明书.md
    └── 跨境电商岗位全链路AI-后续开发计划.md
```

## Skill 用法

在支持 Codex skills 的环境中，可使用：

```text
用 $cbec-research-agent-simple 调研 JISULIFE 几素，对标我们公司，输出能力评分卡和 90 天提升计划。
```

## 适合用户

- 跨境电商老板
- 运营负责人
- 类目负责人
- 产品开发/选品负责人
- Amazon/TikTok/Shopee/Lazada 运营
- 独立站运营
- 品牌负责人
- 市场调研/竞品分析人员

## 许可证

MIT

