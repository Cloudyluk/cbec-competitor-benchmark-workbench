# 公开来源手册与检索式

**使用前提**：所有来源必须本次实际联网访问，记录 URL 与访问日期。来源可用性会变化（改版、加登录墙、地区封锁），访问失败一律写入不可达清单。

## 时效强制规则（检索前必读，详见 `references/freshness-policy.md`）

联网核验 ≠ 数据最新。搜索引擎缓存旧内容、主体自述停在旧财年，是过期数据的主因。每次采集遵守：

1. **显式追最新期**：财务/销量/投放类检索用"最新""最新年报""2025 年报""2026 一季报""最新季报"等动态词，**不要写死年份**（写死年份拿到的就是旧数据）。
2. **反查更新窗口**：取到数据后，去主体披露渠道确认"是否还有更新的未被检索到"——A 股/港股查巨潮网/披露易"最新公告"，美股 SEC EDGAR 按 10-K/10-Q 倒序，平台侧看"since joined + last 30 days""加入时间 + 近 30 天"。
3. **每条带数字事实必填 `data_as_of` + `metric_type`**：否则 `ledger_check.py` 视作口径不全。`data_as_of` 是数据本身时点，不是访问日期。

> 检索式模板见文末，已尽量使用动态时间词；固定年份的模板仅用于"查某特定历史期"的定点核验。

## L1 官方登记来源

### 工商与主体

| 法域 | 入口 | 可得信息 |
|---|---|---|
| 中国大陆 | 国家企业信用信息公示系统 `gsxt.gov.cn` | 注册号、成立日期、注册资本、法人、股东、经营范围、行政处罚、经营异常 |
| 中国大陆（商业库） | 企查查 / 天眼查 / 爱企查 | 股权穿透、关联企业、诉讼、商标、招聘（部分需登录/付费，注意降级） |
| 中国香港 | 公司注册处 ICRIS `www.icris.cr.gov.hk` | 公司编号、成立日、状态、董事（需付费查册） |
| 美国 | 各州 Secretary of State（DE / CA / NY / FL / TX 等） | 注册状态、注册代理、成立日 |
| 美国上市 | SEC EDGAR `www.sec.gov/edgar` | 10-K / 20-F / S-1 / 8-K，最高质量财务与风险披露 |
| 英国 | Companies House `find-and-update.company-information.service.gov.uk` | 免费全量：董事、股东、年报、财务报表 |
| 新加坡 | ACRA BizFile | 注册信息（付费） |
| 全球聚合 | OpenCorporates、GLEIF LEI 查询 | 跨法域主体索引 |
| A 股/港股 | 巨潮资讯网 `cninfo.com.cn`、港交所披露易 `hkexnews.hk` | 年报、公告、股权变动 |

### 进出口与海关

- 中国海关企业信用信息公示平台 `credit.customs.gov.cn` —— 进出口收发货人备案、信用等级（AEO 高级认证 / 一般认证 / 失信）
- 商务部对外贸易经营者备案登记
- 美国 CBP、各国海关公开处罚与查扣通报

### 知识产权

- USPTO Trademark Search / TSDR —— 商标状态、持有人、异议、撤销
- USPTO Patent Full-Text —— 专利（重点查目标类目是否有外观/实用新型壁垒）
- 中国商标网 `sbj.cnipa.gov.cn`
- EUIPO eSearch plus；WIPO Global Brand Database（跨国一站式）
- US Copyright Office（图片/包装版权侵权高发）

### 合规与监管（跨境电商高危区）

| 主题 | 来源 |
|---|---|
| 制裁与实体清单 | OFAC SDN List、BIS Entity List、**UFLPA Entity List**（涉疆强迫劳动，对纺织/太阳能/番茄/多晶硅链条极关键） |
| 美国产品召回 | CPSC `cpsc.gov/Recalls`、SaferProducts.gov 投诉库 |
| 美国食品药械化妆品 | FDA 注册与警告信 `fda.gov`（Warning Letters、Import Alert 红名单） |
| 美国无线电子 | FCC ID 查询 `fcc.gov/oet/ea/fccid` |
| 欧盟产品安全 | Safety Gate / RAPEX 周报 `ec.europa.eu/safety-gate` |
| 欧盟 GPSR | 2024-12-13 起生效，非欧盟卖家必须有 EU Responsible Person 且在包装/Listing 披露 |
| 欧盟 EPR | 德国 LUCID 包装登记（verpackungsregister.org 可公开查企业是否登记）、法国 EPR UIN、WEEE / 电池法规 |
| 美国 ITC | ITC EDIS / Section 337 调查列表（跨境卖家批量被诉的主渠道之一） |
| 美国法院 | CourtListener / RECAP（免费）、Justia；重点关注 **N.D. Illinois** 的批量商标侵权（Schedule A）案件，跨境卖家冻结资金高发地 |
| 中国司法 | 中国裁判文书网、信用中国、失信被执行人 |

## L2 平台一手来源

| 平台 | 关键页面 | 可得信息 |
|---|---|---|
| Amazon | Seller Profile → Detailed Seller Information | 登记主体名、地址、有时含执照号/VAT |
| Amazon | 商品页 / Best Sellers / New Releases / Movers & Shakers | BSR、评分、评价数、变体、A+ 内容、品牌旗舰店、发货方式(FBA/FBM) |
| Amazon | Customer Reviews + Q&A | 差评主因、使用场景、竞品提及 |
| Walmart Marketplace | Seller page | 卖家名、评分、SKU 数 |
| eBay | Seller profile + Feedback | 注册时间、地区、好评率、历史反馈 |
| Shopee / Lazada | 店铺主页 | 加入时间、粉丝、评分、聊天回复率、商品数 |
| TikTok Shop | 店铺页 + 商品页 + 达人主页 | 店铺评分、销量标签、关联达人、直播回放 |
| Temu / SHEIN | 商品页与评价 | 卖家信息极少，主要靠价格带与评价反推 |
| AliExpress / 1688 / Alibaba.com | 旺铺、企业认证、交易勋章 | 认证类型、成交等级、主营类目 |
| Etsy / Ozon / Coupang / Mercado Libre / Allegro / Noon | 店铺页 | 各平台字段不同，以实际页面为准 |
| 独立站 | Terms / Privacy / Imprint / Contact / `/products.json` / `/sitemap.xml` | 运营方、SKU 全量、上新节奏 |

### 广告素材（免费且高价值，常被忽略）

- **Meta Ad Library** `facebook.com/ads/library` —— 按主页查全部在投广告素材、投放地区与起投时间
- **TikTok Creative Center** `ads.tiktok.com/business/creativecenter` —— Top Ads、热门商品、关键词与话题趋势
- **Google Ads Transparency Center** `adstransparency.google.com` —— 按广告主查在投素材

这三个能直接看出竞品的**投放力度、主打卖点、素材迭代节奏**，属 L2，可标 VERIFIED（对"该广告存在"这一事实）。

## L3 权威二手

上市公司年报与招股书中的行业数据 · 主流财经媒体原创报道 · 券商/咨询机构署名报告 · 行业协会统计 · 平台官方发布的行业白皮书。

引用时注明原始出处，不要引用"转述的转述"。

## L4 工具估算与社区（上限 WEAK）

| 类别 | 工具 | 注意 |
|---|---|---|
| Amazon 数据 | Keepa（价格/BSR 历史，曲线本身极有价值）、卖家精灵、Jungle Scout、Helium 10、SellerSprite | 销量为算法推算，误差大 |
| TikTok / 直播 | Kalodata、FastMoss、EchoTik、蝉妈妈 / 蝉选 | 场观与 GMV 均为估算 |
| 独立站流量 | SimilarWeb、Semrush、Ahrefs | 小流量站点误差极大 |
| 海关提单 | **ImportYeti（免费，美国海运提单）**、Panjiva、Datamyne、52wmb、TradeDataPro | 只覆盖海运且可申请隐藏，缺失不等于无出口 |
| 技术栈 | BuiltWith、Wappalyzer | 判断建站平台与营销工具 |
| 口碑 | Trustpilot、Sitejabber、BBB、Reddit、知无不言、亚马逊卖家之家、Facebook 卖家群 | 样本偏差严重，只作线索 |
| 团队 | LinkedIn 人数曲线、脉脉、Glassdoor、招聘网站在招岗位 | 招聘 JD 常泄露业务方向与规模 |
| 资本 | Crunchbase、IT桔子、企查查融资 | 未披露轮次缺失常见 |

**ImportYeti 特别说明**：输入品牌/公司名可反查其美国进口记录（供应商、柜量、起运港、时间序列），是验证"是否真在出货、出货趋势、供应商是否切换"的高性价比手段。注意它只有美国海运数据，空运与非美市场不覆盖。

## 检索式模板

直接复制替换尖括号内容。

**找运营主体**
```
"<店铺展示名>" ("Business Name" OR "卖家详细信息" OR "Detailed Seller Information")
"<品牌名>" (site:gsxt.gov.cn OR site:opencorporates.com OR site:find-and-update.company-information.service.gov.uk)
```

**找关联店铺矩阵**
```
"<登记主体名>" (amazon OR ebay OR walmart OR "TikTok Shop") -site:<自家域名>
"<注册地址>" seller
```

**查侵权与诉讼风险**
```
"<品牌名>" (lawsuit OR "trademark infringement" OR "Schedule A" OR "TRO")
"<公司名>" site:courtlistener.com
"<品牌名>" site:usitc.gov 337
```

**查合规风险**
```
"<品牌名>" site:cpsc.gov recall
"<品牌名>" site:ec.europa.eu safety-gate
"<公司名>" ("Entity List" OR "UFLPA" OR "SDN")
"<公司名>" site:fda.gov ("warning letter" OR "import alert")
```

**查客户与差评洞察**
```
"<品牌名>" (review OR complaint) (site:reddit.com OR site:trustpilot.com)
"<ASIN>" review 1 star
```

**查竞品直播**
```
"<品牌名>" (live OR 直播) site:tiktok.com
"<类目关键词>" TikTok Shop live GMV
```

**查融资与资本动作**
```
"<公司名>" (融资 OR 轮 OR "Series A" OR IPO OR 招股书 OR 收购)
"<公司名>" site:sec.gov
```

**追最新一期披露（防过期，强烈建议每次必做）**
```
"<公司名>" 最新年报 营收 净利润          # A 股/港股动态取最新
"<公司名>" 2025 年报 2026 一季报          # 显式锁定最近两个报告期
"<公司名>" site:cninfo.com.cn 定期报告     # 巨潮网倒序查最新公告
"<公司名>" site:sec.gov 10-K OR 10-Q       # 美股最近期
"<品牌/店铺>" "last 30 days" sales OR revenue  # 平台侧最近窗口
```

> 取到数据后，务必回看披露渠道"最新公告"列表，确认没有比检索结果更新的定期报告；这是"数据只更新到 X 年"类过期的根本防线。

## 来源不可达时的处理

记录到 `40_unreachable.md`，字段：来源名称 / URL / 尝试日期 / 失败原因（付费墙/需登录/地区限制/404/反爬/需线下查册）/ **替代路径**。

常见替代：
- 香港查册需付费 → 用招股书、年报、媒体报道中的披露交叉验证
- 数据工具需订阅 → 改用 Keepa 免费图表、平台自身排行榜、评价数增速估算
- 平台页需登录 → 用搜索引擎缓存、商品聚合站、平台 App 端公开分享页
