# 全渠道足迹发现（P1.5）

目标：把"一个已锁定身份的主体"扩展成"它的全渠道版图"，并为每一条渠道归属提供可复核的证据。

执行时机：P1 身份核验通过之后、P2 证据采集之前。本阶段的产出直接决定 P4 横向对比纳入哪些对象。

**两类错误都致命**：
- **误并**：把两家无关公司当成一家 → 整个对比矩阵作废
- **漏并**：矩阵店铺没找全 → 严重低估对手体量

宁可标"疑似关联未确认"，也不要为了矩阵好看而强行合并。

---

## 一、八条反查路径

按证据强度排序执行，不要跳步。

### 1. Amazon 店铺 → 运营主体（强）

卖家页 → `Detailed Seller Information` → 公开显示 Business Name、Business Address、有时含营业执照号。这是平台一手披露（L2），可达 VERIFIED。

拿到公司名后，反向在其他平台搜同名卖家，以及去工商库核验主体。

### 2. 独立站 → 法律实体（强）

按顺序翻这些页面，跨境独立站通常至少有一处披露实体名：
`Privacy Policy` → `Terms of Service` → `Returns & Refunds` → `Imprint`（德国站强制）→ `Contact Us` → 页脚版权行

欧盟市场还应查 `EU Responsible Person` 声明（GPSR 要求），会直接给出欧盟境内责任主体。

### 3. 独立站 → 关联站群（中，**注意准确性限制**）

通过共享的跟踪代码找同一主体的其他站点。查看页面源码，搜索：
- `G-XXXXXXXXXX`（GA4，当前主流）
- `GTM-XXXXXXX`（Google Tag Manager）
- `UA-XXXXXXX`（旧版 Universal Analytics，**已停止服务**，仅存量老站可见）
- Meta Pixel ID
- Google AdSense `pub-XXXXXXXXXX`

反查工具：BuiltWith 的 Relationship Profiles、HackerTarget Reverse Analytics Search、SpyOnWeb、SameID。

**必须知道的四个限制**（这决定了它只能算 B 级证据）：

1. **可被伪造** —— 任何人都能把别人的跟踪 ID 贴到自己站上，制造虚假关联。HackerTarget 官方文档明确提示了这种 misdirection 风险。
2. **数据可能过期** —— 这类工具基于 Common Crawl 等爬虫快照做正则匹配，不保证实时准确。UA 停服后，大量工具的存量数据尤其陈旧。
3. **共享 IP 不可用于判定** —— 共享主机上完全无关的网站会同 IP。
4. **需交叉验证** —— 命中后还要比对建站程序、主题模板、页面结构、联系地址、客服邮箱域名，多项一致才可采信。

来源：HackerTarget Reverse Analytics Search 文档（hackertarget.com/reverse-analytics-search/，2026-08-02 访问）；BuiltWith 关联站点查法（雨果跨境 m.cifnews.com/article/114954，2026-08-02 访问）。

### 4. 独立站 → 关联域名（中）

证书透明日志 `crt.sh` 按组织名或域名关键词检索，能挖出同一主体申请过证书的其他域名与子域名。适合发现测试站、备用站、区域站。

### 5. 品牌名 → 商标持有人 → 全平台（强）

商标库（USPTO / EUIPO / CNIPA / J-PlatPat 等）反查持有人 → 拿到持有人法律名称 → 用该名称在各平台卖家信息、Amazon Brand Registry 展示、独立站法律页面中反查。

一个持有人名下多个商标 = 多品牌矩阵的直接线索。

### 6. 广告透明库 → 广告主实体名（强，**易被忽略**）

**Google Ads Transparency Center 按"广告主名称"匹配，而这个名称通常是法律实体名，不是消费者看到的品牌名。** 这意味着：如果两个不同品牌在该库中显示同一个广告主实体，这是很强的同主体证据。

同理，TikTok Commercial Content Library（欧盟透明度合规产物）支持按广告主搜索，也会暴露投放主体。

来源：Google Ads Transparency Center 广告主名称匹配机制（adlibrary.com/posts/how-to-find-competitor-ads，2026-08-02 访问）。

### 7. 产品图 → 其他平台同款（中）

反向图搜（Google Lens / TinEye / Yandex）用**独家实拍图**（不是供应商通用图）去搜，能找到同一批图片在其他平台的 listing。

注意：1688 通用图、供应商图库图会命中大量无关卖家，不可作为归属依据。只有自拍场景图、带自有 Logo 包装图才有效。

### 8. 公司名 → 海外收发货人 → 关联店（中）

ImportYeti / Panjiva 用公司名查提单，收货人（Consignee）栏可能暴露其海外关联主体、分销商或自营海外仓公司。

---

## 二、归属证据 A/B/C 分级

### A 级 —— 可确认同一主体

- 平台官方披露的公司信息一致（Amazon Detailed Seller Information、Shopee/Lazada 店铺资质页）
- 独立站法律页面（Privacy / Terms / Imprint）实体名一致
- 商标持有人一致
- 广告透明库中广告主法律实体名一致
- 工商登记文件显示直接持股或同一实控人
- 主体官方公开声明（官网、年报、招股书中列明）

### B 级 —— 高度可能，需第二条独立佐证

- **共享 GA4 / GTM / Pixel / AdSense ID**（因可伪造 + 数据时效问题，单独不足以定案）
- 退货地址完全一致
- 客服邮箱域名一致
- SKU 编码体系一致
- 独家实拍图完全一致
- 包装印刷、说明书排版一致
- crt.sh 显示同一组织名下的关联域名
- 提单收发货人关系

### C 级 —— 仅线索，不可用于判定

- 品牌名相似或同词根
- Logo 风格相似
- 经营同一品类
- 同一供应商供货
- 共享 IP（共享主机极常见）
- 建站主题模板相同（模板是公开售卖的）

### 判定规则

| 证据组合 | 归属结论 | 账本等级 | 能否进对比矩阵 |
|---|---|---|---|
| ≥1 条 A 级 | 确认同主体 | VERIFIED | 是 |
| ≥2 条相互独立的 B 级 | 高度可能 | STRONG | 是，标注证据强度 |
| 1 条 B 级 | 疑似关联 | WEAK | 否，单列观察 |
| 仅 C 级 | 不予判定 | WEAK | 否 |

"相互独立"指两条证据来自不同性质的信息源。共享 Pixel ID + 共享 GA ID 属**同一性质**，只算一条。

---

## 三、分区域平台清单

### 欧美区

| 渠道 | 发现入口 | 主体信息可得性 |
|---|---|---|
| Amazon（US/CA/UK/DE/FR/IT/ES/JP…） | 品牌搜索、Brand Store、卖家页 | 高，Detailed Seller Information |
| eBay | 卖家 Store 页、feedback 页 | 中，展示注册地与加入时间 |
| Walmart Marketplace | 卖家页 | 中 |
| 独立站（Shopify / WooCommerce / BigCommerce） | 域名、法律页面 | 高 |
| Etsy | 店铺页 About | 中 |
| Meta Ad Library | facebook.com/ads/library | 广告主主页名 |
| Google Ads Transparency | adstransparency.google.com | **广告主法律实体名** |
| TikTok / Instagram / YouTube / Pinterest | 账号 bio、link-in-bio | 低，需交叉 |

### 东南亚区

| 渠道 | 发现入口 | 主体信息可得性 |
|---|---|---|
| Shopee（SG/MY/TH/PH/VN/ID/TW） | 店铺页、Shopee Mall 标识 | 中，部分站点披露公司信息 |
| Lazada（同区域 + LazMall） | 店铺页 | 中 |
| TikTok Shop | 店铺页、关联达人 | 中 |
| Tokopedia | 店铺页 | 中 |
| TikTok Commercial Content Library | 按广告主搜索 | 广告主名 |

### 新兴/有限公开平台

Temu、SHEIN、Ozon、Mercado Libre、Coupang —— 公开字段少、主体信息基本不披露、销量多为分档展示（"已售 1000+"）。这些平台**只做存在性登记，不参与量化对比**，并在报告中明确说明口径局限。

---

## 四、矩阵店铺归并去重

跨境卖家普遍做店铺矩阵。发现多个店铺后：

1. 逐个跑上述八条路径，为每个店铺独立建立归属证据
2. 按 A/B/C 规则判定是否并入同一主体
3. **归并后重新统计规模**（SKU 总数、店铺总数、覆盖平台数），单店数据会严重低估对手
4. 识别矩阵结构类型：
   - **同品牌多店**（防封号备份）
   - **多品牌矩阵**（分层定价或分市场）
   - **测品店 + 主力店**（测品店 SKU 多、单品评价少）
5. 在足迹表中标注每个店铺的角色定位

## 五、产出

填写 `assets/omnichannel-footprint.csv`，并运行：

```bash
python scripts/footprint_scan.py research/<slug>/61_footprint.csv
```

脚本按 A/B/C 规则自动判定每条渠道归属能否成立、能否进入对比矩阵，并列出证据不足需补强的条目。
