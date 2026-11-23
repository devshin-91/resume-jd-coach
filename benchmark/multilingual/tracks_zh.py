#!/usr/bin/env python3
"""China Simplified Chinese (zh) 4-job-family real-JD benchmark track definitions for resume-jd-coach v2.0."""

from __future__ import annotations

ZH_TRACKS = [
    {
        "slug": "track_zh01_dev_tencent",
        "country": "China",
        "language": "zh",
        "family": "技术研发 / Java 后端",
        "company": "腾讯（Tencent）",
        "role": "营销与交易产品部-云mallJava后端开发工程师",
        "jd_url": "https://careers.tencent.com/jobdesc.html?postId=2089960263330742272",
        "location": "深圳",
        "scenario": "Failing Chinese 熟悉/了解 skill-stacking + self-contradiction (AI Agent) in legacy gb18030 .txt -> R2 honest quantified Java e-commerce proof -> PASS",
        "format": "txt_gb18030",
        "jd_text": """公司：腾讯（Tencent）
职位：营销与交易产品部-云mallJava后端开发工程师
地点：深圳 | 三年以上工作经验 | 更新于2026年11月20日
URL：https://careers.tencent.com/jobdesc.html?postId=2089960263330742272

岗位职责：
1. 负责电商核心系统从需求分析、方案设计到开发上线的完整交付；
2. 参与电商业务模型和平台架构设计，支撑复杂交易场景及业务持续发展；
3. 负责系统性能、稳定性和线上问题治理，推动系统持续演进；
4. 在研发过程中合理使用 AI，提高研发效率和交付质量，并对最终结果负责；
5. 与产品、前端、测试及相关团队协作，将业务规则、技术约束和工程经验转化为 AI 可理解、可验证、可复用的项目知识和研发工作流。

岗位要求：
1. 具备扎实的 Java 基础和良好的工程实践；
2. 熟悉 Spring Boot、Spring Cloud、MySQL、Redis、消息队列等常用技术，具备数据库设计、性能优化及相关项目经验；
3. 具备分布式系统设计和生产实践能力，能够保障系统稳定运行，并独立定位和解决线上问题；
4. 具备电商或其他复杂交易系统的分析与建模能力；
5. 能够熟练使用 AI 开发工具，准确描述问题并提供上下文，能独立判断和验证生成结果，对最终质量和数据安全负责。

加分项：
1. 有电商平台、零售 SaaS 或其他复杂交易系统经验；
2. 有大型平台系统、多租户系统建设或架构治理经验；
3. 有 AI Agent 或智能化研发流程建设经验。
""",
        "rubric": {
            "company": "腾讯（Tencent）",
            "role_title": "营销与交易产品部-云mallJava后端开发工程师",
            "language": "zh",
            "domain_mode": "resume_only",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 45, "portfolio_impact": 25, "preferred": 15, "ats_framing": 15},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "Java / Spring Boot / Spring Cloud 后端工程实践（3年以上）", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "MySQL、Redis、消息队列设计与分布式高并发线上治理", "weight": 3, "is_knockout": True},
                    {"id": "MH-3", "title": "电商或复杂交易核心链路建模与全流程交付", "weight": 2, "is_knockout": False},
                    {"id": "MH-4", "title": "AI 开发工具提效与生成结果独立验证、数据安全把关", "weight": 2, "is_knockout": False},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "高并发交易稳定性、QPS/耗时优化等量化成果", "weight": 3, "is_knockout": False},
                    {"id": "PI-2", "title": "个人架构设计决策与线上排障复盘深度", "weight": 2, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "零售 SaaS / 多租户大型平台架构建设经验", "weight": 2, "is_knockout": False},
                    {"id": "PR-2", "title": "AI Agent 或智能化研发工作流建设经验", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "岗位定位清晰度与项目背景-职责-成果结构化表达", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "Java", "aliases": [], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "Spring Boot", "aliases": ["Spring Cloud"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "MySQL", "aliases": [], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "Redis", "aliases": [], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "消息队列", "aliases": ["Kafka", "RocketMQ", "MQ"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "分布式", "aliases": ["高并发"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "电商", "aliases": ["零售 SaaS", "复杂交易"], "tier": "must", "linked_item_id": "MH-3"},
                {"term": "多租户", "aliases": ["架构治理"], "tier": "preferred", "linked_item_id": "PR-1"},
                {"term": "AI Agent", "aliases": ["智能化研发"], "tier": "preferred", "linked_item_id": "PR-2"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "txt_gb18030",
                    "filename": "lin_hao_resume_r1_gb18030.txt",
                    "content": """林浩 — 后端开发工程师（深圳，4年经验）

个人简介：热爱编程，学习能力强，能吃苦耐劳，有团队精神。

专业技能：
熟练掌握 Java、Spring Boot、Spring Cloud、MySQL、Redis、消息队列、分布式架构、AI Agent。

工作经历：
2022.05 - 至今 | 某网络科技有限公司 | Java开发工程师
- 负责公司商城日常后端接口开发和维护工作。
- 配合产品和测试完成需求上线，及时修复线上Bug。
- 参与数据库表结构编写和日常代码评审。

尚未接触领域：
暂无 AI Agent 研发工作流落地及多租户大型平台架构治理经验。
""",
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "WEAK", "evidence_quote": "熟练掌握 Java、Spring Boot、Spring Cloud、MySQL、Redis、消息队列", "source": "gb18030 txt", "gap_type": "expression_gap", "action_hint": "脱离项目的“熟练掌握”清单最高仅计 WEAK(0.25)；请在商城核心交易项目中写明 Java/Spring Cloud 实际架构与模块职责。"},
                        {"id": "MH-2", "grade": "WEAK", "evidence_quote": "参与数据库表结构编写和日常代码评审", "source": "gb18030 txt", "gap_type": "expression_gap", "action_hint": "补充 MySQL 慢查询/索引优化、Redis 缓存防击穿、MQ 异步削峰及线上故障排查实例。"},
                        {"id": "MH-3", "grade": "WEAK", "evidence_quote": "负责公司商城日常后端接口开发和维护工作", "source": "gb18030 txt", "gap_type": "expression_gap", "action_hint": "具体展开商城订单/营销/库存核心链路建模，而非笼统写“接口开发和维护”。"},
                        {"id": "MH-4", "grade": "MISSING", "evidence_quote": "", "source": "gb18030 txt", "gap_type": "expression_gap", "action_hint": "如实说明你在研发中如何借助 AI 工具提效并通过单测/代码审查确保质量与数据安全。"},
                        {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "source": "gb18030 txt", "gap_type": "expression_gap", "action_hint": "补充大促 QPS、接口 P99 耗时、可用性（如 99.99%）等前后对比量化成果。"},
                        {"id": "PI-2", "grade": "MISSING", "evidence_quote": "", "source": "gb18030 txt", "gap_type": "expression_gap", "action_hint": "写清一项由你主导的方案选型权衡或高危线上故障定位复盘。"},
                        {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "source": "gb18030 txt", "gap_type": "true_gap", "action_hint": "多租户平台治理属真实能力缺口，切勿虚构；可通过电商复杂交易实战佐证弥补。"},
                        {"id": "PR-2", "grade": "MISSING", "evidence_quote": "", "source": "gb18030 txt", "gap_type": "true_gap", "action_hint": "你在专业技能写了 AI Agent 却在尚未接触领域写暂无落地经验，产生自相矛盾；请从技能栏移除。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "热爱编程，学习能力强，能吃苦耐劳，有团队精神", "source": "gb18030 txt", "gap_type": "expression_gap", "action_hint": "去掉空泛自我评价，改为“4年电商交易 Java 后端经验 + 核心量化成果”，并按项目背景-职责-成果重构。"},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "txt_gb18030",
                    "filename": "lin_hao_resume_r2_gb18030.txt",
                    "content": """林浩 — 高级 Java 后端开发工程师（电商营销与交易方向 · 深圳 · 4年经验）

核心优势：4年电商交易与营销中台 Java/Spring Cloud 实战经验，主导高并发订单链路重构与线上稳定性治理，熟练运用 AI 辅助编码并建立严格单测校验机制。

项目经历：
1. 电商大促订单与营销优惠交易系统重构（核心负责人 | 2023.06 - 至今）
- 项目背景：双11期间优惠券叠加与库存扣减并发激增，原有单体交易链路出现死锁与超时。
- 核心职责：基于 Java 17、Spring Boot、Spring Cloud 重新建模“营销计价—库存预占—支付回调”核心交易状态机；使用 Redis Lua 原子扣减库存与 RocketMQ 消息队列异步削峰，通过分布式幂等键防止重复扣款；对 MySQL 订单表实施冷热分离与联合索引重构。
- 量化成果：大促峰值支撑 8,500 QPS 零超卖，下单接口 P99 延迟由 680ms 降至 95ms，核心交易链路全年可用率达 99.98%。

2. 线上稳定性治理与 AI 辅助研发实践（2024.03 - 至今）
- 独立定位并根治大促期间线程池耗尽导致的级联超时故障，沉淀全链路慢 SQL 巡检与熔断降级规范，线上 P1 故障同比下降 75%。
- 团队内推行 AI 编程助手结合业务领域文档生成边界单测与代码重构建议，坚持脱敏上下文输入与人工 Code Review 双重验证，核心模块单测覆盖率由 42% 提升至 81%，需求交付周期缩短 28%。

尚未接触领域：
暂无多租户大型平台架构治理及独立搭建企业级 AI Agent 平台经验。
""",
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "基于 Java 17、Spring Boot、Spring Cloud 重新建模“营销计价—库存预占—支付回调”核心交易状态机", "source": "gb18030 txt"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "使用 Redis Lua 原子扣减库存与 RocketMQ 消息队列异步削峰，通过分布式幂等键防止重复扣款；对 MySQL 订单表实施冷热分离与联合索引重构", "source": "gb18030 txt"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "重新建模“营销计价—库存预占—支付回调”核心交易状态机", "source": "gb18030 txt"},
                        {"id": "MH-4", "grade": "FULL", "evidence_quote": "推行 AI 编程助手结合业务领域文档生成边界单测与代码重构建议，坚持脱敏上下文输入与人工 Code Review 双重验证", "source": "gb18030 txt"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "大促峰值支撑 8,500 QPS 零超卖，下单接口 P99 延迟由 680ms 降至 95ms，核心交易链路全年可用率达 99.98%", "source": "gb18030 txt"},
                        {"id": "PI-2", "grade": "FULL", "evidence_quote": "独立定位并根治大促期间线程池耗尽导致的级联超时故障，线上 P1 故障同比下降 75%", "source": "gb18030 txt"},
                        {"id": "PR-1", "grade": "PARTIAL", "evidence_quote": "4年电商交易与营销中台 Java/Spring Cloud 实战经验", "source": "gb18030 txt", "gap_type": "true_gap", "action_hint": "具备电商交易经验，多租户大型治理为诚实保留项。"},
                        {"id": "PR-2", "grade": "MISSING", "evidence_quote": "", "source": "gb18030 txt", "gap_type": "true_gap", "action_hint": "已从技能栏移除矛盾声明，保持诚实即可。"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "高级 Java 后端开发工程师（电商营销与交易方向 · 深圳 · 4年经验）", "source": "gb18030 txt"},
                    ],
                },
            },
        ],
    },
    {
        "slug": "track_zh02_design_bytedance",
        "country": "China",
        "language": "zh",
        "family": "用户体验设计（作品集）",
        "company": "字节跳动（ByteDance）",
        "role": "高级用户体验设计师-财经",
        "jd_url": "https://jobs.bytedance.com/experienced/position/7675656615622428933/detail",
        "location": "北京",
        "scenario": "Failing visual-only .pptx portfolio -> R2 stall (<+3%p) triggers Chinese Grace Tier 1->2 coaching -> R3 FinTech conversion & AI design proof -> PASS",
        "format": "pptx",
        "jd_text": """公司：字节跳动（ByteDance）
职位：高级用户体验设计师-财经
地点：北京 | 职位 ID：A102557A
URL：https://jobs.bytedance.com/experienced/position/7675656615622428933/detail

职位描述：
1、负责金融产品体验、设计、增长类工作；
2、与产品经理协作完善产品需求，保证产品体验及易用性；
3、关注产品数据，持续迭代产品功能点，分析、监控产品变化；
4、关注AI设计相关的能力，能够使用AI工具进行工作提效。

职位要求：
1、设计类专业本科及以上学历；
2、具备5年以上UI产品设计经验，有较强的设计审美和逻辑思考能力；
3、面对产品需求有自己的判断力，并能协助产品改善体验，提升业务转化；
4、具备较强的团队合作意识，善于沟通、相互协作；
5、有成熟的产品设计经验、案例、作品集。
""",
        "rubric": {
            "company": "字节跳动（ByteDance）",
            "role_title": "高级用户体验设计师-财经",
            "language": "zh",
            "domain_mode": "portfolio",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 40, "portfolio_impact": 35, "preferred": 10, "ats_framing": 15},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "设计类本科及以上学历 + 5年以上 UI/产品设计经验", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "成熟产品设计案例作品集与业务转化判断力", "weight": 3, "is_knockout": True},
                    {"id": "MH-3", "title": "金融/增长类产品体验优化与数据监控迭代", "weight": 2, "is_knockout": False},
                    {"id": "MH-4", "title": "AI 设计工具提效落地能力", "weight": 2, "is_knockout": False},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "需求拆解、方案权衡逻辑与易用性重构深度", "weight": 3, "is_knockout": False},
                    {"id": "PI-2", "title": "业务转化率、留存或设计提效量化数据佐证", "weight": 2, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "财经/金融科技产品全链路增长设计沉淀", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "高级体验/增长设计师定位与作品集叙事结构", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "金融产品", "aliases": ["财经", "理财", "信贷"], "tier": "must", "linked_item_id": "MH-3"},
                {"term": "用户体验", "aliases": ["UX", "UI"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "业务转化", "aliases": ["增长", "转化率"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "数据", "aliases": ["埋点", "漏斗"], "tier": "must", "linked_item_id": "MH-3"},
                {"term": "AI工具", "aliases": ["AI设计", "Midjourney", "Figma AI"], "tier": "must", "linked_item_id": "MH-4"},
                {"term": "作品集", "aliases": ["案例"], "tier": "must", "linked_item_id": "MH-2"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "pptx",
                    "filename": "su_ying_portfolio_r1.pptx",
                    "slides": [
                        "苏莹 — UI设计师 | 视觉传达设计本科 | 6年设计经验",
                        "作品集案例1：理财App首页改版 — 重新排版了图标和配色，整体页面更大气简洁。",
                        "作品集案例2：运营活动海报与弹窗 — 配合产品经理按时输出多套高清视觉稿。",
                    ],
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "视觉传达设计本科 | 6年设计经验", "source": "pptx Slide 1"},
                        {"id": "MH-2", "grade": "WEAK", "evidence_quote": "重新排版了图标和配色，整体页面更大气简洁", "source": "pptx Slide 2", "gap_type": "expression_gap", "action_hint": "仅展示视觉美化不足以过初筛，需补充你对产品需求的独立判断与业务转化优化逻辑。"},
                        {"id": "MH-3", "grade": "WEAK", "evidence_quote": "理财App首页改版", "source": "pptx Slide 2", "gap_type": "expression_gap", "action_hint": "补充理财产品核心漏斗数据监控与迭代复盘。"},
                        {"id": "MH-4", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "补充你使用 AI 设计工具（如 Figma AI / Midjourney / 生图工作流）提升出图或原型效率的实例。"},
                        {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "按“业务问题→用户痛点→方案对比取舍→最终上线”重构作品集页面。"},
                        {"id": "PI-2", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "补充开户/申购转化率、点击率或设计交付提效量化结果。"},
                        {"id": "PR-1", "grade": "WEAK", "evidence_quote": "理财App首页改版", "source": "pptx Slide 2", "gap_type": "expression_gap", "action_hint": "深化财经场景（合规信息披露、风险提示与转化平衡）的设计沉淀。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "苏莹 — UI设计师", "source": "pptx Slide 1", "gap_type": "expression_gap", "action_hint": "聚焦“高级用户体验设计师（金融增长方向）”定位。"},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "pptx",
                    "filename": "su_ying_portfolio_r2_stall.pptx",
                    "slides": [
                        "苏莹 — 高级UI/用户体验设计师 | 视觉传达设计本科 | 6年设计经验",
                        "作品集案例1：理财App首页改版 — 配合产品优化了信息层级，页面更清晰，用户反馈体验更好。",
                        "作品集案例2：运营活动海报与弹窗 — 按时高质量输出多套视觉方案，获得团队好评。",
                    ],
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "视觉传达设计本科 | 6年设计经验", "source": "pptx Slide 1"},
                        {"id": "MH-2", "grade": "WEAK", "evidence_quote": "配合产品优化了信息层级，页面更清晰，用户反馈体验更好", "source": "pptx Slide 2", "gap_type": "expression_gap", "action_hint": "仍停留在“用户反馈更好”的定性描述，缺少产品需求质疑与具体漏斗数据。"},
                        {"id": "MH-3", "grade": "WEAK", "evidence_quote": "理财App首页改版", "source": "pptx Slide 2", "gap_type": "expression_gap", "action_hint": "未补充数据监控指标与迭代轮次。"},
                        {"id": "MH-4", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "仍缺少 AI 工具提效案例。"},
                        {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "缺少方案取舍逻辑。"},
                        {"id": "PI-2", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "缺少任何量化业务转化指标。"},
                        {"id": "PR-1", "grade": "WEAK", "evidence_quote": "理财App首页改版", "source": "pptx Slide 2", "gap_type": "expression_gap", "action_hint": "需展开金融产品增长体验案例。"},
                        {"id": "AF-1", "grade": "PARTIAL", "evidence_quote": "高级UI/用户体验设计师", "source": "pptx Slide 1", "gap_type": "expression_gap", "action_hint": "标题有改善，但作品集正文结构仍停留在纯视觉展示。"},
                    ],
                },
            },
            {
                "round": 3,
                "candidate_doc": {
                    "type": "pptx",
                    "filename": "su_ying_portfolio_r3_grace.pptx",
                    "slides": [
                        "苏莹 — 高级用户体验设计师（金融产品与增长方向）| 视觉传达设计本科 | 6年 UI/UX 实战经验",
                        "作品集案例1：稳健理财申购链路体验与业务转化重构 — 通过漏斗数据监控发现风险测评页跳出率高达 58%，主动向产品经理提出拆解长表单并前置收益测算器，否决了“强弹窗引导”旧方案；A/B 迭代 3 轮后，新手首购转化率提升 +14.6%，申购完成耗时缩短 37%。",
                        "作品集案例2：财经资讯卡片与持仓页增长设计 — 搭建核心页面埋点监控看板，持续跟踪点击率与7日复访率，将关键行情模块次日留存提升 +6.8%p。",
                        "AI设计提效实践：引入 Figma AI 与内部 LoRA 生图工作流自动化产出金融营销素材与多端交互草图，团队日常运营设计交付周期由 3 天压缩至 0.8 天（提效 73%）。",
                    ],
                },
                "eval": {
                    "round": 3,
                    "grace_tier_used": 2,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "视觉传达设计本科 | 6年 UI/UX 实战经验", "source": "pptx Slide 1"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "主动向产品经理提出拆解长表单并前置收益测算器，否决了“强弹窗引导”旧方案；A/B 迭代 3 轮后，新手首购转化率提升 +14.6%", "source": "pptx Slide 2"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "搭建核心页面埋点监控看板，持续跟踪点击率与7日复访率，将关键行情模块次日留存提升 +6.8%p", "source": "pptx Slide 3"},
                        {"id": "MH-4", "grade": "FULL", "evidence_quote": "引入 Figma AI 与内部 LoRA 生图工作流自动化产出金融营销素材与多端交互草图，交付周期由 3 天压缩至 0.8 天", "source": "pptx Slide 4"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "通过漏斗数据监控发现风险测评页跳出率高达 58%，主动向产品经理提出拆解长表单并前置收益测算器", "source": "pptx Slide 2"},
                        {"id": "PI-2", "grade": "FULL", "evidence_quote": "新手首购转化率提升 +14.6%，申购完成耗时缩短 37%", "source": "pptx Slide 2"},
                        {"id": "PR-1", "grade": "FULL", "evidence_quote": "稳健理财申购链路体验与业务转化重构", "source": "pptx Slide 2"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "高级用户体验设计师（金融产品与增长方向）", "source": "pptx Slide 1"},
                    ],
                },
            },
        ],
    },
    {
        "slug": "track_zh03_pm_mihoyo",
        "country": "China",
        "language": "zh",
        "family": "产品策划 / AI 增长 PM",
        "company": "米哈游（miHoYo）",
        "role": "增长产品经理（AI方向）",
        "jd_url": "https://jobs.mihoyo.com/#/position/8574",
        "location": "上海",
        "scenario": "Honest true_gap ceiling + Chinese clause-comma negation (暂未接触SQL、A/B实验及大模型) -> Stays REVISE (<80%) with honest_fit_advisory",
        "format": "md",
        "jd_text": """公司：米哈游（miHoYo）
职位：增长产品经理（AI方向）
地点：上海 | 全职
URL：https://jobs.mihoyo.com/#/position/8574

工作职责：
1、负责 AI 驱动的用户增长产品设计，覆盖拉新、激活、留存、转化全链路；
2、落地 AI 增长能力：智能推荐、个性化触达、自动化运营、A/B 实验体系；
3、搭建数据指标体系，通过数据分析与实验迭代优化增长效果。

任职要求：
1、本科及以上，3年以上用户增长 / 产品经理经验，有 AI 产品经验优先；
2、了解大模型 / 推荐 / 用户画像等 AI 能力，熟悉增长策略、数据驱动与实验方法论，能输出产品方案；
3、具备 SQL 数据分析能力，结果导向、强执行与跨部门协作力。
""",
        "rubric": {
            "company": "米哈游（miHoYo）",
            "role_title": "增长产品经理（AI方向）",
            "language": "zh",
            "domain_mode": "portfolio",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 50, "portfolio_impact": 25, "preferred": 10, "ats_framing": 15},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "本科及以上 + 3年以上用户增长/产品经理经验", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "AI 增长能力落地（智能推荐、个性化触达、A/B 实验体系）", "weight": 3, "is_knockout": True},
                    {"id": "MH-3", "title": "SQL 数据分析与指标体系搭建能力", "weight": 2, "is_knockout": True},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "拉新/激活/留存/转化全链路量化增长案例", "weight": 3, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "大模型或 AI 原生产品落地经验", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "AI 增长产品经理定位与数据驱动叙事", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "用户增长", "aliases": ["拉新", "留存"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "SQL", "aliases": [], "tier": "must", "linked_item_id": "MH-3"},
                {"term": "A/B 实验", "aliases": ["AB实验", "A/B实验"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "智能推荐", "aliases": ["用户画像", "个性化触达"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "大模型", "aliases": ["LLM", "AI产品"], "tier": "preferred", "linked_item_id": "PR-1"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "md",
                    "filename": "zhou_ran_r1.md",
                    "content": """# 周然 — 社区内容运营专员（上海，本科学历，2年经验）

## 个人简介
负责手游社区日常推文排版、发帖互动与线下活动执行，熟练使用 Excel 整理活动报名表，暂未接触 SQL 数据分析、A/B 实验体系、智能推荐及大模型产品设计。

## 工作经历
- 2024.07 - 至今 | 星云互娱 | 社区运营
  - 负责官方社区拉新裂变海报策划与发奖执行，提升社区活跃度。
  - 协助策划老玩家回流活动，收集玩家反馈给运营组长。
""",
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "WEAK", "evidence_quote": "社区内容运营专员（上海，本科学历，2年经验）", "source": "md", "gap_type": "true_gap", "action_hint": "真实年限与职能差距（2年运营 vs 3年以上增长PM硬性要求），无法仅靠话术弥补。"},
                        {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "尚无智能推荐、个性化触达与 A/B 实验体系落地经历，严禁虚构。"},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "真实技能缺口：尚未掌握 SQL 数据分析。"},
                        {"id": "PI-1", "grade": "WEAK", "evidence_quote": "负责官方社区拉新裂变海报策划与发奖执行，提升社区活跃度", "source": "md", "gap_type": "expression_gap", "action_hint": "可如实补充真实裂变拉新人数和老玩家回流转化率。"},
                        {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "无大模型产品经验，如实留空。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "社区内容运营专员", "source": "md", "gap_type": "true_gap", "action_hint": "建议优先投递社区运营/初级用户运营岗位，同时系统补齐 SQL 与增长实验基础。"},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "md",
                    "filename": "zhou_ran_r2.md",
                    "content": """# 周然 — 游戏社区用户增长运营（上海，本科学历，2年经验）

## 个人简介
专注游戏社区拉新与老玩家召回运营，熟练使用 Excel 复盘活动漏斗，暂未接触 SQL 数据分析、A/B 实验体系、智能推荐及大模型产品设计。

## 工作经历
- 2024.07 - 至今 | 星云互娱 | 社区增长运营
  - 独立统筹周年庆拉新裂变与老玩家回流活动，带动新增注册 3.2 万人，活动次周留存率由 18% 提升至 27%。
""",
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "WEAK", "evidence_quote": "上海，本科学历，2年经验", "source": "md", "gap_type": "true_gap", "action_hint": "仍为 2 年运营背景（低于 3 年增长 PM 门槛）。"},
                        {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "真实能力缺口：无 AI 增长与实验平台经验。"},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "真实能力缺口：无 SQL 实战能力。"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "独立统筹周年庆拉新裂变与老玩家回流活动，带动新增注册 3.2 万人，活动次周留存率由 18% 提升至 27%", "source": "md"},
                        {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "真实缺口。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "游戏社区用户增长运营", "source": "md", "gap_type": "true_gap", "action_hint": "与 AI 增长产品经理定位仍有客观差距，建议匹配更契合岗位。"},
                    ],
                },
            },
        ],
    },
    {
        "slug": "track_zh04_nonit_bilibili",
        "country": "China",
        "language": "zh",
        "family": "非技术职能（HRBP）",
        "company": "哔哩哔哩（Bilibili）",
        "role": "内容安全业务HRBP",
        "jd_url": "https://jobs.bilibili.com/social/positions/28324",
        "location": "上海",
        "scenario": "Non-IT resume_only failing admin-duty HRBP -> R2 accidental deletion triggers Chinese Regression Alert -> R3 complete restoration -> PASS",
        "format": "md",
        "jd_text": """公司：哔哩哔哩（Bilibili）
职位：内容安全业务HRBP
地点：上海 | 2026-07-15 发布
URL：https://jobs.bilibili.com/social/positions/28324

工作职责：
1. 理解业务部门战略，对业务进行组织诊断，为业务战略落地提供建议、规划并参与实施；
2. 为组织发展提供人力资源支持，定期进行组织盘点，在招聘、培训、绩效考核、薪酬、员工关系等方面提供有效解决方案；
3. 推动变革，完善业务部门人力资源制度、流程、体系，提升运作效率；
4. 传承公司文化，建设沟通渠道，保证组织健康成长。

工作要求：
1. 本科及以上学历，4年及以上人力资源工作经验，有互联网公司或跨城市HRBP经验优先；
2. 具有良好的业务理解力和洞察力；
3. 对人和组织有敏感度，能够进行组织和人员诊断并推动方案落地；
4. 与业务协作能保持独立判断，及时给出专业意见；
5. 优秀的沟通协调和关系建立能力，能够胜任跨多个城市的业务协作界面，能接受偶尔出差。
""",
        "rubric": {
            "company": "哔哩哔哩（Bilibili）",
            "role_title": "内容安全业务HRBP",
            "language": "zh",
            "domain_mode": "resume_only",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 45, "portfolio_impact": 25, "preferred": 15, "ats_framing": 15},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "本科及以上 + 4年以上人力资源工作经验", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "组织诊断、组织盘点与全模块 HR 解决方案落地", "weight": 3, "is_knockout": True},
                    {"id": "MH-3", "title": "业务独立判断与跨城市业务协作界面管理", "weight": 2, "is_knockout": False},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "组织效率、关键岗位保留或绩效变革量化成效", "weight": 3, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "互联网公司或跨城市 HRBP 经验", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "业务导向 HRBP 定位与结构化表达", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "HRBP", "aliases": ["人力资源业务合作伙伴"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "组织诊断", "aliases": ["组织盘点"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "员工关系", "aliases": ["绩效考核", "薪酬"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "跨城市", "aliases": ["多城市", "出差"], "tier": "preferred", "linked_item_id": "MH-3"},
                {"term": "互联网", "aliases": ["内容安全", "审核团队"], "tier": "preferred", "linked_item_id": "PR-1"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "md",
                    "filename": "chen_mo_r1.md",
                    "content": """# 陈默 — 人事专员（上海 · 本科 · 5年人力资源经验）

## 工作经历
- 2021.06 - 至今 | 某互联网视频平台 | HR专员 / HRBP
  - 负责员工入转调离手续办理、考勤统计与社保核对。
  - 协助业务部门发布招聘职位，整理面试日程与组织部门团建活动。
  - 偶尔出差至武汉、成都职场支持新员工入职培训。
""",
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "上海 · 本科 · 5年人力资源经验", "source": "md"},
                        {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "expression_gap", "action_hint": "摆脱纯事务性入离职清单，补充你主导的组织诊断、人才盘点、绩效与员工关系专项方案。"},
                        {"id": "MH-3", "grade": "PARTIAL", "evidence_quote": "偶尔出差至武汉、成都职场支持新员工入职培训", "source": "md", "gap_type": "expression_gap", "action_hint": "展示你在跨城市业务协作中提出独立专业判断、推动管理层共识的案例。"},
                        {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "expression_gap", "action_hint": "补充离职率下降、核心人效提升或关键岗位满编周期缩短等数据。"},
                        {"id": "PR-1", "grade": "PARTIAL", "evidence_quote": "某互联网视频平台 | HR专员 / HRBP", "source": "md", "gap_type": "expression_gap", "action_hint": "明确你在互联网多城市业务线作为 HRBP 支持的团队规模。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "陈默 — 人事专员", "source": "md", "gap_type": "expression_gap", "action_hint": "将抬头调整为业务型 HRBP，突出战略支撑而非行政事务。"},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "md",
                    "filename": "chen_mo_r2_regressed.md",
                    "content": """# 陈默 — 互联网业务 HRBP（上海 · 本科 · 5年人力资源经验）

## 工作经历
- 2021.06 - 至今 | 某互联网视频平台 | 内容审核业务 HRBP
  - 针对 350 人内容安全与审核团队开展年度组织诊断与人才盘点，重构班次绩效考核与薪酬激励方案，主动离职率由 28% 降至 16%。
  - 独立主导多起高风险员工关系合规处置与业务组织变革，守住劳资零仲裁底线，并将审核团队人均产能提升 19%。
""",
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "上海 · 本科 · 5年人力资源经验", "source": "md"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "针对 350 人内容安全与审核团队开展年度组织诊断与人才盘点，重构班次绩效考核与薪酬激励方案", "source": "md"},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "expression_gap", "action_hint": "注意回退：第2轮误删了第1轮原有的武汉/成都跨城市业务对接与出差佐证，请补回并写清独立判断案例。"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "主动离职率由 28% 降至 16%，并将审核团队人均产能提升 19%", "source": "md"},
                        {"id": "PR-1", "grade": "STRONG_PARTIAL", "evidence_quote": "某互联网视频平台 | 内容审核业务 HRBP", "source": "md", "gap_type": "expression_gap", "action_hint": "补回跨城市 HRBP 协作范围即可满分。"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "互联网业务 HRBP", "source": "md"},
                    ],
                },
            },
            {
                "round": 3,
                "candidate_doc": {
                    "type": "md",
                    "filename": "chen_mo_r3.md",
                    "content": """# 陈默 — 互联网内容安全业务 HRBP（上海 · 本科 · 5年人力资源经验）

## 工作经历
- 2021.06 - 至今 | 某互联网视频平台 | 跨城市内容审核业务 HRBP
  - 针对上海、武汉、成都三地 350 人内容安全与审核团队开展年度组织诊断与人才盘点，重构班次绩效考核与薪酬激励方案，主动离职率由 28% 降至 16%。
  - 长期统筹跨城市业务协作界面并定期出差驻场，针对业务急于扩编的诉求给出独立专业判断，以排班优化替代盲目加编节省年度人力成本 240 万元。
  - 独立主导高风险员工关系合规处置与组织变革落地，实现全年零劳动仲裁，核心审核团队人均产能提升 19%。
""",
                },
                "eval": {
                    "round": 3,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "上海 · 本科 · 5年人力资源经验", "source": "md"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "开展年度组织诊断与人才盘点，重构班次绩效考核与薪酬激励方案", "source": "md"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "长期统筹跨城市业务协作界面并定期出差驻场，针对业务急于扩编的诉求给出独立专业判断", "source": "md"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "主动离职率由 28% 降至 16%，节省年度人力成本 240 万元，人均产能提升 19%", "source": "md"},
                        {"id": "PR-1", "grade": "FULL", "evidence_quote": "某互联网视频平台 | 跨城市内容审核业务 HRBP", "source": "md"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "互联网内容安全业务 HRBP", "source": "md"},
                    ],
                },
            },
        ],
    },
]
