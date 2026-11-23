#!/usr/bin/env python3
"""US English (en) 4-job-family real-JD benchmark track definitions for resume-jd-coach v2.0."""

from __future__ import annotations

EN_TRACKS = [
    {
        "slug": "track_en01_dev_ramp",
        "country": "US",
        "language": "en",
        "family": "Software / Backend Engineering",
        "company": "Ramp",
        "role": "Software Engineer, Backend, Comms Platform",
        "jd_url": "https://jobs.ashbyhq.com/ramp/939892e5-5273-4bfc-8c41-a6c51cabb228",
        "location": "Remote (US)",
        "scenario": "Failing passive duty-only US resume (.docx) -> Coach-First self-revision with idempotency, observability & scale metrics -> PASS",
        "format": "docx",
        "jd_text": """Company: Ramp
Role: Software Engineer, Backend, Comms Platform
Location: Remote (US) | Full time
URL: https://jobs.ashbyhq.com/ramp/939892e5-5273-4bfc-8c41-a6c51cabb228

Responsibilities:
- Own the design and evolution of a core part of Ramp's communications platform, from technical design through launch, monitoring, and iteration
- Build and extend integrations with messaging channels and delivery providers, including email, SMS, push, and workplace chat tools such as Slack and Microsoft Teams
- Design delivery workflows that are idempotent, retry safely, and confirm successful delivery, so customers reliably get the messages they need without duplicate sends
- Build communication preferences and controls that let users and administrators decide what they receive and where
- Make the platform simple and safe for other Ramp engineers to build on, with clear abstractions, strong defaults, and good developer tooling
- Improve the reliability, performance, and observability of the platform as message volume grows
- Drive technical direction for your area and raise the engineering bar through design reviews, code reviews, and mentorship

Required Qualifications:
- Experience designing, building, and operating production backend systems, including APIs, data models, and asynchronous workflows
- A track record of owning a system or product area end to end and shaping its technical direction over time
- Strong system design judgment, especially around reliability, idempotency, and correctness in high-volume distributed systems
- Product sense: balance speed with quality for people receiving messages
- Clear communication and collaborative technical decision-making across product, design, and engineering

Preferred Qualifications:
- Experience building notification, messaging, or communications platforms
- Experience integrating with messaging providers or channel APIs (Twilio, SendGrid, Slack, Microsoft Teams, WhatsApp)
- Experience building internal platforms or shared services used by many engineering teams
- Experience scaling high-volume, event-driven, or queue-based systems
""",
        "rubric": {
            "company": "Ramp",
            "role_title": "Software Engineer, Backend, Comms Platform",
            "language": "en",
            "domain_mode": "portfolio",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 45, "portfolio_impact": 25, "preferred": 15, "ats_framing": 15},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "Production backend APIs, data models & async workflows", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "Idempotent delivery, safe retries & distributed reliability", "weight": 3, "is_knockout": True},
                    {"id": "MH-3", "title": "End-to-end system ownership & technical direction", "weight": 2, "is_knockout": False},
                    {"id": "MH-4", "title": "Observability, reliability & platform developer abstractions", "weight": 2, "is_knockout": False},
                    {"id": "MH-5", "title": "Cross-functional collaboration with product & design", "weight": 1, "is_knockout": False},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "Quantified throughput, latency, or delivery-success metrics", "weight": 3, "is_knockout": False},
                    {"id": "PI-2", "title": "Concrete system architecture trade-offs & post-launch iteration", "weight": 2, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "Messaging/notification platform & provider APIs (Twilio/SendGrid/Slack)", "weight": 2, "is_knockout": False},
                    {"id": "PR-2", "title": "Internal shared platform & high-volume queue/event scaling", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "Backend platform headline & recruiter-scannable XYZ impact framing", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "API", "aliases": ["APIs"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "Asynchronous", "aliases": ["Async", "Queue", "Event-Driven"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "Idempotent", "aliases": ["Idempotency"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "Observability", "aliases": ["Monitoring", "Datadog", "OpenTelemetry"], "tier": "must", "linked_item_id": "MH-4"},
                {"term": "Distributed Systems", "aliases": ["High-Volume"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "SendGrid", "aliases": ["Twilio", "Slack", "Notification"], "tier": "preferred", "linked_item_id": "PR-1"},
                {"term": "Retries", "aliases": ["Retry", "Dead-Letter Queue", "DLQ"], "tier": "preferred", "linked_item_id": "MH-2"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "docx",
                    "filename": "jordan_lee_resume_r1.docx",
                    "paragraphs": [
                        "Jordan Lee — Software Developer (US Remote)",
                        "Summary: Hardworking developer who likes building web applications and collaborating with team members.",
                        "Experience — CloudLedger Inc. (2022 – Present), Backend Developer",
                        "- Responsible for maintaining REST APIs and fixing bugs in Python and PostgreSQL.",
                        "- Helped with sending email alerts and internal notifications when invoices were approved.",
                        "- Worked with product managers and frontend engineers during sprint planning.",
                        "- Assisted senior engineers with deployments and on-call tickets.",
                        "Skills: Python, PostgreSQL, REST APIs, Git, Docker.",
                    ],
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "PARTIAL", "evidence_quote": "Responsible for maintaining REST APIs and fixing bugs in Python and PostgreSQL", "source": "docx", "gap_type": "expression_gap", "action_hint": "Specify data model design and asynchronous workflow architecture you built rather than passive maintenance."},
                        {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "source": "docx", "gap_type": "expression_gap", "action_hint": "Detail how you prevented duplicate sends (idempotency keys, safe retries, dead-letter handling) in invoice notifications."},
                        {"id": "MH-3", "grade": "WEAK", "evidence_quote": "Assisted senior engineers with deployments and on-call tickets", "source": "docx", "gap_type": "expression_gap", "action_hint": "Replace 'assisted' with the exact service or feature area you owned end-to-end from RFC to production."},
                        {"id": "MH-4", "grade": "MISSING", "evidence_quote": "", "source": "docx", "gap_type": "expression_gap", "action_hint": "Add observability metrics/alerts and any shared abstractions built for other engineers."},
                        {"id": "MH-5", "grade": "PARTIAL", "evidence_quote": "Worked with product managers and frontend engineers during sprint planning", "source": "docx", "gap_type": "expression_gap", "action_hint": "Show a concrete product trade-off decision made with PM/Design."},
                        {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "source": "docx", "gap_type": "expression_gap", "action_hint": "Add real message volume, delivery rate, or latency numbers before and after your changes."},
                        {"id": "PI-2", "grade": "MISSING", "evidence_quote": "", "source": "docx", "gap_type": "expression_gap", "action_hint": "Explain an architecture decision and post-launch reliability iteration."},
                        {"id": "PR-1", "grade": "WEAK", "evidence_quote": "Helped with sending email alerts and internal notifications when invoices were approved", "source": "docx", "gap_type": "expression_gap", "action_hint": "Name the actual messaging providers (e.g., SendGrid, Twilio, Slack API) and preference controls."},
                        {"id": "PR-2", "grade": "MISSING", "evidence_quote": "", "source": "docx", "gap_type": "expression_gap", "action_hint": "Highlight queue-based scaling or internal platform usage by sibling engineering teams."},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "Hardworking developer who likes building web applications", "source": "docx", "gap_type": "expression_gap", "action_hint": "Rewrite headline for Backend / Distributed Platform engineering and convert passive duties to XYZ impact bullets."},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "docx",
                    "filename": "jordan_lee_resume_r2.docx",
                    "paragraphs": [
                        "Jordan Lee — Senior Backend Engineer, Distributed Messaging & Platform Systems (US Remote)",
                        "Summary: Production backend engineer with 5 years owning high-volume asynchronous notification platforms, idempotent delivery APIs, and internal developer tooling.",
                        "Experience — CloudLedger Inc. (2022 – Present), Backend Engineer (Notifications Platform Owner)",
                        "- Owned end-to-end design, RFC review, launch, and iteration of CloudLedger's multi-channel notification platform (Python, PostgreSQL, Kafka event-driven queues) serving 4.2M transactional alerts/day.",
                        "- Architected idempotent delivery workflows using composite idempotency keys, exponential backoff retries, and dead-letter queues (DLQ), cutting duplicate payment alerts by 99.4% and raising verified delivery SLA from 97.1% to 99.96%.",
                        "- Built channel integrations with SendGrid (email), Twilio (SMS), and Slack webhooks alongside granular admin/user communication preference controls adopted by 6 product engineering teams via a typed internal SDK.",
                        "- Instrumented full observability (OpenTelemetry traces, Datadog SLO dashboards, provider failover alerts), shrinking p99 notification latency from 4.8s to 620ms and cutting on-call pages by 68%.",
                        "- Partnered directly with Product and Design to launch batched approval digests, reducing noisy customer notifications by 41% while accelerating invoice approval turnaround by 22%.",
                    ],
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "Owned end-to-end design, RFC review, launch, and iteration of CloudLedger's multi-channel notification platform (Python, PostgreSQL, Kafka event-driven queues) serving 4.2M transactional alerts/day", "source": "docx"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "Architected idempotent delivery workflows using composite idempotency keys, exponential backoff retries, and dead-letter queues (DLQ), cutting duplicate payment alerts by 99.4%", "source": "docx"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "Owned end-to-end design, RFC review, launch, and iteration of CloudLedger's multi-channel notification platform", "source": "docx"},
                        {"id": "MH-4", "grade": "FULL", "evidence_quote": "Instrumented full observability (OpenTelemetry traces, Datadog SLO dashboards, provider failover alerts), shrinking p99 notification latency from 4.8s to 620ms", "source": "docx"},
                        {"id": "MH-5", "grade": "FULL", "evidence_quote": "Partnered directly with Product and Design to launch batched approval digests, reducing noisy customer notifications by 41%", "source": "docx"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "raising verified delivery SLA from 97.1% to 99.96%", "source": "docx"},
                        {"id": "PI-2", "grade": "FULL", "evidence_quote": "adopted by 6 product engineering teams via a typed internal SDK", "source": "docx"},
                        {"id": "PR-1", "grade": "FULL", "evidence_quote": "Built channel integrations with SendGrid (email), Twilio (SMS), and Slack webhooks alongside granular admin/user communication preference controls", "source": "docx"},
                        {"id": "PR-2", "grade": "FULL", "evidence_quote": "adopted by 6 product engineering teams via a typed internal SDK", "source": "docx"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "Senior Backend Engineer, Distributed Messaging & Platform Systems (US Remote)", "source": "docx"},
                    ],
                },
            },
        ],
    },
    {
        "slug": "track_en02_design_figma",
        "country": "US",
        "language": "en",
        "family": "Product Design (Portfolio)",
        "company": "Figma",
        "role": "Product Designer, Core Experience",
        "jd_url": "https://job-boards.greenhouse.io/figma/jobs/6231027004?gh_jid=6231027004",
        "location": "San Francisco, CA / New York, NY / Remote US",
        "scenario": "Failing screenshot-only .pptx portfolio -> R2 Bare Keyword Stuffing capped at WEAK(0.25) -> R3 Real Interaction & Code-Prototype Proof -> PASS",
        "format": "pptx",
        "jd_text": """Company: Figma
Role: Product Designer, Core Experience
Location: San Francisco, CA • New York, NY • Remote United States
URL: https://job-boards.greenhouse.io/figma/jobs/6231027004?gh_jid=6231027004

Responsibilities:
- Lead the design of core editor experiences, including foundational concepts like Auto Layout, Text, and canvas interactions
- Define and champion a clear vision for how the editor should evolve with product and engineering partners
- Explore how direct manipulation, AI, and code can work together via prototyping
- Ground decisions in user research, product data, and close observation
- Participate in design critiques, mentor peers, and share best practices

Required Qualifications:
- 8+ years of experience in product design, leading complex software projects from exploration through launch and iteration
- A portfolio of shipped work demonstrating interaction design and visual craft, making sophisticated workflows simple
- Structured thinking, clearly articulated rationale, and user-centered research
- Experience researching, prototyping, or building products with AI and other emerging tools

Preferred Qualifications:
- Designing creative tools, editors, canvas interfaces, or direct manipulation interactions
- Design/development hybrid background or code-based prototyping (React/CSS/HTML)
""",
        "rubric": {
            "company": "Figma",
            "role_title": "Product Designer, Core Experience",
            "language": "en",
            "domain_mode": "portfolio",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 40, "portfolio_impact": 35, "preferred": 10, "ats_framing": 15},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "8+ years product design leading complex software E2E", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "Shipped portfolio showing interaction craft on complex workflows", "weight": 3, "is_knockout": True},
                    {"id": "MH-3", "title": "User research, data-grounded rationale & design critiques", "weight": 2, "is_knockout": False},
                    {"id": "MH-4", "title": "AI / emerging tool prototyping & direct-manipulation exploration", "weight": 2, "is_knockout": False},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "Problem framing, interaction trade-offs & iterative prototypes", "weight": 3, "is_knockout": False},
                    {"id": "PI-2", "title": "Measurable adoption, task-speed, or usability improvements", "weight": 2, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "Canvas / creative editor / direct-manipulation tool experience", "weight": 2, "is_knockout": False},
                    {"id": "PR-2", "title": "Code-based prototyping or frontend hybrid craft", "weight": 1, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "Systems-minded core interaction designer positioning", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "Interaction Design", "aliases": ["Direct Manipulation"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "Prototyping", "aliases": ["Prototype", "Prototypes"], "tier": "must", "linked_item_id": "MH-4"},
                {"term": "User Research", "aliases": ["Usability Testing"], "tier": "must", "linked_item_id": "MH-3"},
                {"term": "AI", "aliases": ["LLM", "Generative"], "tier": "must", "linked_item_id": "MH-4"},
                {"term": "Canvas", "aliases": ["Editor", "Auto Layout"], "tier": "preferred", "linked_item_id": "PR-1"},
                {"term": "Code-Based Prototyping", "aliases": ["React", "HTML/CSS"], "tier": "preferred", "linked_item_id": "PR-2"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "pptx",
                    "filename": "maya_chen_portfolio_r1.pptx",
                    "slides": [
                        "Maya Chen — UI/Visual Designer | 9 Years Experience in Marketing Websites & SaaS Dashboards",
                        "Project 1: Dashboard Redesign — Updated color palette, typography, and buttons to look cleaner and more modern.",
                        "Project 2: Mobile App Screens — Final mockups attached. Stakeholders loved the visual polish.",
                        "Skills: Figma, Sketch, Adobe Illustrator, Brand Guidelines.",
                    ],
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "PARTIAL", "evidence_quote": "9 Years Experience in Marketing Websites & SaaS Dashboards", "source": "pptx Slide 1", "gap_type": "expression_gap", "action_hint": "Show end-to-end ownership of complex interactive software workflows, not just marketing/visual refreshes."},
                        {"id": "MH-2", "grade": "WEAK", "evidence_quote": "Updated color palette, typography, and buttons to look cleaner and more modern", "source": "pptx Slide 2", "gap_type": "expression_gap", "action_hint": "Replace visual-only screenshot captions with complex interaction mechanics and shipped workflow artifacts."},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "Document user research findings, usability sessions, and structured trade-off rationale."},
                        {"id": "MH-4", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "Include real AI-assisted workflow exploration or interactive prototyping work if you have done it."},
                        {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "Show problem definition, rejected interaction alternatives, and why the shipped design won."},
                        {"id": "PI-2", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "Add measurable usability, task-completion time, or adoption outcomes."},
                        {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "transferable_gap", "action_hint": "Highlight any node-editor, layout builder, or direct-manipulation canvas interaction work."},
                        {"id": "PR-2", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "Mention React/HTML/CSS code prototypes if built."},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "UI/Visual Designer", "source": "pptx Slide 1", "gap_type": "expression_gap", "action_hint": "Reframe headline around Systems & Core Interaction Product Design."},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "pptx",
                    "filename": "maya_chen_portfolio_r2_stuffed.pptx",
                    "slides": [
                        "Maya Chen — Product Designer | 9 Years Experience in Marketing Websites & SaaS Dashboards",
                        "Project 1: Dashboard Redesign — Updated color palette, typography, and buttons to look cleaner and more modern.",
                        "Project 2: Mobile App Screens — Final mockups attached. Stakeholders loved the visual polish.",
                        "Keywords & Skills: Interaction Design, Direct Manipulation, Prototyping, User Research, AI, Canvas, Auto Layout, Editor, Code-Based Prototyping, React.",
                    ],
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "PARTIAL", "evidence_quote": "9 Years Experience in Marketing Websites & SaaS Dashboards", "source": "pptx Slide 1", "gap_type": "expression_gap", "action_hint": "Still lacks end-to-end complex software case study proof."},
                        {"id": "MH-2", "grade": "WEAK", "evidence_quote": "Keywords & Skills: Interaction Design, Direct Manipulation, Prototyping", "source": "pptx Slide 4", "gap_type": "expression_gap", "action_hint": "Bare keyword stuffing in a skills slide is capped at WEAK (0.25); embed real interaction case studies."},
                        {"id": "MH-3", "grade": "WEAK", "evidence_quote": "Keywords & Skills: Interaction Design, Direct Manipulation, Prototyping, User Research", "source": "pptx Slide 4", "gap_type": "expression_gap", "action_hint": "Mentioning 'User Research' in a keyword list does not prove research-driven decisions."},
                        {"id": "MH-4", "grade": "WEAK", "evidence_quote": "Prototyping, User Research, AI, Canvas", "source": "pptx Slide 4", "gap_type": "expression_gap", "action_hint": "Capped at WEAK (0.25): show an actual AI + direct-manipulation prototype you designed."},
                        {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "Still missing design trade-offs and iteration rationale."},
                        {"id": "PI-2", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "Still missing measurable user or business outcomes."},
                        {"id": "PR-1", "grade": "WEAK", "evidence_quote": "AI, Canvas, Auto Layout, Editor", "source": "pptx Slide 4", "gap_type": "transferable_gap", "action_hint": "Bare keyword list capped at WEAK (0.25)."},
                        {"id": "PR-2", "grade": "WEAK", "evidence_quote": "Code-Based Prototyping, React", "source": "pptx Slide 4", "gap_type": "expression_gap", "action_hint": "Show an actual code prototype shipped with engineers."},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "Keywords & Skills: Interaction Design, Direct Manipulation, Prototyping", "source": "pptx Slide 4", "gap_type": "expression_gap", "action_hint": "Remove keyword-dump slide and lead with real interaction case studies."},
                    ],
                },
            },
            {
                "round": 3,
                "candidate_doc": {
                    "type": "pptx",
                    "filename": "maya_chen_portfolio_r3.pptx",
                    "slides": [
                        "Maya Chen — Staff Product Designer, Core Canvas & Interactive Systems | 9+ Years Leading Complex Software E2E",
                        "Case Study 1 — Visual Workflow Canvas & Auto Layout Engine (Shipped to 180K creators): Led exploration through launch of a constraint-based direct manipulation canvas editor. Ran 24 contextual inquiry user research sessions and rejected nested inspector panels in favor of on-canvas handles, cutting complex layout build time by 44%.",
                        "Case Study 2 — Hybrid AI Generation + Direct Manipulation Editing: Built interactive React & HTML/CSS code-based prototypes letting users prompt layout variations and refine spacing live on canvas without losing manual control. Weekly active AI-assisted edits reached 62% with 4.7/5 craft score.",
                        "Design Org Leadership: Facilitated weekly cross-team design critiques, mentored 4 product designers, and unified interaction tokens with frontend engineering.",
                    ],
                },
                "eval": {
                    "round": 3,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "9+ Years Leading Complex Software E2E", "source": "pptx Slide 1"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "Visual Workflow Canvas & Auto Layout Engine (Shipped to 180K creators): Led exploration through launch of a constraint-based direct manipulation canvas editor", "source": "pptx Slide 2"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "Ran 24 contextual inquiry user research sessions and rejected nested inspector panels in favor of on-canvas handles", "source": "pptx Slide 2"},
                        {"id": "MH-4", "grade": "FULL", "evidence_quote": "Hybrid AI Generation + Direct Manipulation Editing: Built interactive React & HTML/CSS code-based prototypes letting users prompt layout variations and refine spacing live on canvas", "source": "pptx Slide 3"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "rejected nested inspector panels in favor of on-canvas handles, cutting complex layout build time by 44%", "source": "pptx Slide 2"},
                        {"id": "PI-2", "grade": "FULL", "evidence_quote": "Weekly active AI-assisted edits reached 62% with 4.7/5 craft score", "source": "pptx Slide 3"},
                        {"id": "PR-1", "grade": "FULL", "evidence_quote": "constraint-based direct manipulation canvas editor", "source": "pptx Slide 2"},
                        {"id": "PR-2", "grade": "FULL", "evidence_quote": "Built interactive React & HTML/CSS code-based prototypes", "source": "pptx Slide 3"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "Staff Product Designer, Core Canvas & Interactive Systems", "source": "pptx Slide 1"},
                    ],
                },
            },
        ],
    },
    {
        "slug": "track_en03_data_discord",
        "country": "US",
        "language": "en",
        "family": "Data Science / Experimentation",
        "company": "Discord",
        "role": "Staff Data Scientist, Causal Inference & Experimentation",
        "jd_url": "https://job-boards.greenhouse.io/discord/jobs/8652853002",
        "location": "San Francisco Bay Area",
        "scenario": "Honest true_gap ceiling + English long-window negation -> Stays REVISE (<80%) with honest_fit_advisory (no Grace fabrication)",
        "format": "md",
        "jd_text": """Company: Discord
Role: Staff Data Scientist, Causal Inference & Experimentation
Location: San Francisco Bay Area
URL: https://job-boards.greenhouse.io/discord/jobs/8652853002

Responsibilities:
- Formulate vision and roadmap for the Experimentation Platform with engineering, product, and DS stakeholders
- Ensure statistical methodologies are sound and aligned with best practices in causal inference and experimental design
- Lead workshops and training programs on experimentation design and causal inference across 50+ data scientists
- Conduct original causal inference research on high-priority product questions

Required Qualifications:
- Proven experience leading experimentation platform work and validating statistical methodologies
- PhD in a quantitative field or equivalent practical experience, plus 4+ years designing, implementing, and analyzing experiments or causal inference projects
- Experience developing and delivering training programs / educational content on experimentation & statistical methodology
- Proficient with Python, SQL, R, and/or other statistical programming languages

Preferred Qualifications:
- Causal inference methods translated into business decisions & publications
- AI/LLM tools to accelerate causal inference or experimentation education workflows
""",
        "rubric": {
            "company": "Discord",
            "role_title": "Staff Data Scientist, Causal Inference & Experimentation",
            "language": "en",
            "domain_mode": "portfolio",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 55, "portfolio_impact": 20, "preferred": 15, "ats_framing": 10},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "Leading experimentation platform & statistical methodology validation", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "PhD/equivalent + 4+ years causal inference & experimentation", "weight": 3, "is_knockout": True},
                    {"id": "MH-3", "title": "Org-wide experimentation training & data literacy education", "weight": 2, "is_knockout": False},
                    {"id": "MH-4", "title": "Proficiency in Python, SQL, and/or R statistical computing", "weight": 2, "is_knockout": False},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "Quantified product/business impact from rigorous experimentation", "weight": 2, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "Causal inference publications & AI/LLM experimentation workflows", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "Staff Experimentation / Causal Inference role framing", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "Causal Inference", "aliases": ["Quasi-Experiment", "Difference-in-Differences"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "Experimentation Platform", "aliases": ["Experimental Design"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "A/B Testing", "aliases": ["AB Testing"], "tier": "preferred", "linked_item_id": "PI-1"},
                {"term": "Python", "aliases": [], "tier": "must", "linked_item_id": "MH-4"},
                {"term": "SQL", "aliases": [], "tier": "must", "linked_item_id": "MH-4"},
                {"term": "R", "aliases": [], "tier": "preferred", "linked_item_id": "MH-4"},
                {"term": "LLM", "aliases": ["AI"], "tier": "preferred", "linked_item_id": "PR-1"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "md",
                    "filename": "taylor_brooks_r1.md",
                    "content": """# Taylor Brooks — Business Intelligence Analyst (San Francisco, CA)

## Summary
3 years building executive dashboards and ad-hoc analytics in SQL and Python for e-commerce operations.

## Experience
- **RetailPulse (2023 – Present), BI Analyst**
  - Built Looker dashboards and automated weekly KPI reports using SQL and Python.
  - Supported two basic email A/B testing sends by comparing raw click-through rates.

## Gaps & Limitations
- No production experience with experimentation platform architecture, causal inference methods, quasi-experiments, or statistical methodology validation.
- Exposure only to R in an undergraduate course; never taught statistics workshops or published research.
""",
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "Genuine gap: never led an experimentation platform; do not fabricate."},
                        {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "Genuine gap: lacks PhD/4+ yrs causal inference depth; consider Senior Product Analyst roles first."},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "No workshops or statistical curriculum delivered."},
                        {"id": "MH-4", "grade": "PARTIAL", "evidence_quote": "Built Looker dashboards and automated weekly KPI reports using SQL and Python", "source": "md", "gap_type": "expression_gap", "action_hint": "Specify statistical modeling or Python data-pipeline complexity beyond BI reporting."},
                        {"id": "PI-1", "grade": "WEAK", "evidence_quote": "Supported two basic email A/B testing sends by comparing raw click-through rates", "source": "md", "gap_type": "expression_gap", "action_hint": "Quantify business impact and statistical significance checks from those tests if run."},
                        {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "True gap — no causal publications or LLM experimentation tools."},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "Business Intelligence Analyst", "source": "md", "gap_type": "true_gap", "action_hint": "Role level/specialization mismatch with Staff Causal Inference scope."},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "md",
                    "filename": "taylor_brooks_r2.md",
                    "content": """# Taylor Brooks — Product & Experimentation Analyst (San Francisco, CA)

## Summary
3 years of production SQL and Python analytics driving retention reporting and marketing A/B testing measurement.

## Experience
- **RetailPulse (2023 – Present), Analytics Lead (BI & Marketing)**
  - Authored modular Python (pandas, scipy) and SQL warehouse pipelines powering 40+ self-serve revenue dashboards.
  - Analyzed 6 email and landing-page A/B testing campaigns with power/significance validation, lifting checkout conversion by +3.4% (+$420K annualized GMV).

## Gaps & Limitations
- No production experience with experimentation platform architecture, causal inference methods, or statistical methodology validation.
- Exposure only to R in an undergraduate course; never taught statistics workshops or published research.
""",
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "Still a genuine capability gap — cannot be solved via wording edits."},
                        {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "Still lacks 4+ yrs causal inference & PhD/equivalent scope."},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "No org-wide statistical training experience."},
                        {"id": "MH-4", "grade": "FULL", "evidence_quote": "Authored modular Python (pandas, scipy) and SQL warehouse pipelines powering 40+ self-serve revenue dashboards", "source": "md"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "Analyzed 6 email and landing-page A/B testing campaigns with power/significance validation, lifting checkout conversion by +3.4% (+$420K annualized GMV)", "source": "md"},
                        {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "true_gap", "action_hint": "True gap — keep honest."},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "Product & Experimentation Analyst", "source": "md", "gap_type": "true_gap", "action_hint": "Honest seniority gap relative to Staff Data Scientist."},
                    ],
                },
            },
        ],
    },
    {
        "slug": "track_en04_nonit_datadog",
        "country": "US",
        "language": "en",
        "family": "Non-IT Corporate (HR / People Partner)",
        "company": "Datadog",
        "role": "Director, People Business Partner",
        "jd_url": "https://careers.datadoghq.com/detail/8346056/?gh_jid=8346056",
        "location": "New York, NY (Hybrid)",
        "scenario": "Non-IT resume_only PASS_WITH_RISK Knockout (missing 5+ yrs team management proof) -> R2 substantiates PBP team leadership -> PASS",
        "format": "md",
        "jd_text": """Company: Datadog
Role: Director, People Business Partner
Location: New York, New York, USA (Hybrid)
URL: https://careers.datadoghq.com/detail/8346056/?gh_jid=8346056

Responsibilities:
- Lead and develop a team of People Business Partners supporting G&A organizations
- Partner with senior G&A leaders on org design, workforce planning, performance, compensation, talent/succession, and complex employee relations
- Partner with leaders to drive AI transformation across org design and capabilities
- Use people and business data to identify trends, surface risks, and recommend action

Required Qualifications:
- At least 10 years of progressive HR or People Business Partner experience, including at least 5 years leading a team
- Experienced leading and developing People Business Partners in a fast-growing organization
- Deeply experienced in organizational design, workforce planning, talent management, performance management, compensation, change management, and employee relations
- Highly analytical using data to identify issues and recommend action

Preferred Qualifications:
- Supporting global G&A functions
- High-growth technology or public company experience
""",
        "rubric": {
            "company": "Datadog",
            "role_title": "Director, People Business Partner",
            "language": "en",
            "domain_mode": "resume_only",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 45, "portfolio_impact": 25, "preferred": 15, "ats_framing": 15},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "10+ yrs HR/PBP experience INCLUDING 5+ yrs leading a PBP team", "weight": 2, "is_knockout": True},
                    {"id": "MH-2", "title": "Org design, workforce planning, compensation & talent management", "weight": 4, "is_knockout": False},
                    {"id": "MH-3", "title": "Executive G&A advisory, complex employee relations & AI org change", "weight": 4, "is_knockout": False},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "Data-driven people outcomes (retention, engagement, headcount efficiency)", "weight": 3, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "Global G&A functions at a high-growth tech or public company", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "Director-level People Business Partner executive positioning", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "People Business Partner", "aliases": ["HRBP", "PBP"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "Organizational Design", "aliases": ["Org Design"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "Workforce Planning", "aliases": ["Headcount Planning"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "Employee Relations", "aliases": [], "tier": "must", "linked_item_id": "MH-3"},
                {"term": "Compensation", "aliases": ["Performance Management"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "AI Transformation", "aliases": ["Change Management"], "tier": "preferred", "linked_item_id": "MH-3"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "md",
                    "filename": "morgan_patel_r1.md",
                    "content": """# Morgan Patel — Director, People Business Partner (New York, NY)

## Executive Summary
12 years of progressive HR and People Business Partner (PBP) leadership supporting global G&A functions (Finance, Legal, Ops) at a NASDAQ-listed SaaS company.

## Experience — VertexCloud Corp (Public High-Growth SaaS, 2019 – Present), Senior PBP Lead
- Partnered directly with CFO and General Counsel on multi-year organizational design, annual workforce planning (1,200+ global G&A seats), compensation calibration, and performance management cycles.
- Spearheaded G&A AI transformation and change management across Legal and Finance ops, redesigning roles and upskilling 450 employees.
- Resolved 35+ sensitive executive employee relations investigations with zero regulatory escalations and coached 40+ senior managers.
- Built quarterly people-analytics retention dashboards with Finance, lifting top-performer retention from 84% to 93% and reducing voluntary attrition by 6.2%p YoY.
- Collaborated closely with fellow People Business Partners on shared HR initiatives.
""",
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "WEAK", "evidence_quote": "Collaborated closely with fellow People Business Partners on shared HR initiatives", "source": "md", "gap_type": "expression_gap", "action_hint": "KNOCKOUT RISK: You have 12 yrs HR experience, but 'collaborated with fellow PBPs' reads as IC peer collaboration—explicitly state your 5+ years of direct people-management scope if you managed PBPs."},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "multi-year organizational design, annual workforce planning (1,200+ global G&A seats), compensation calibration, and performance management cycles", "source": "md"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "Spearheaded G&A AI transformation and change management across Legal and Finance ops", "source": "md"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "lifting top-performer retention from 84% to 93% and reducing voluntary attrition by 6.2%p YoY", "source": "md"},
                        {"id": "PR-1", "grade": "FULL", "evidence_quote": "supporting global G&A functions (Finance, Legal, Ops) at a NASDAQ-listed SaaS company", "source": "md"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "Director, People Business Partner (New York, NY)", "source": "md"},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "md",
                    "filename": "morgan_patel_r2.md",
                    "content": """# Morgan Patel — Director, People Business Partner (New York, NY)

## Executive Summary
12 years of progressive HR and People Business Partner (PBP) leadership—including 6 years directly managing and scaling teams of up to 7 PBPs—supporting global G&A functions at a NASDAQ-listed SaaS company.

## Experience — VertexCloud Corp (Public High-Growth SaaS, 2019 – Present), Director, People Business Partner (G&A)
- Directly hired, coached, and led a global team of 7 People Business Partners across New York, Dublin, and Tokyo for 6 consecutive years, establishing quarterly PBP service standards and promoting 3 direct reports to Senior/Lead PBP.
- Partnered directly with CFO and General Counsel on multi-year organizational design, annual workforce planning (1,200+ global G&A seats), compensation calibration, and performance management cycles.
- Spearheaded G&A AI transformation and change management across Legal and Finance ops, redesigning roles and upskilling 450 employees.
- Resolved 35+ sensitive executive employee relations investigations with zero regulatory escalations and coached 40+ senior managers.
- Built quarterly people-analytics retention dashboards with Finance, lifting top-performer retention from 84% to 93% and reducing voluntary attrition by 6.2%p YoY.
""",
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "Directly hired, coached, and led a global team of 7 People Business Partners across New York, Dublin, and Tokyo for 6 consecutive years", "source": "md"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "multi-year organizational design, annual workforce planning (1,200+ global G&A seats), compensation calibration, and performance management cycles", "source": "md"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "Spearheaded G&A AI transformation and change management across Legal and Finance ops", "source": "md"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "lifting top-performer retention from 84% to 93% and reducing voluntary attrition by 6.2%p YoY", "source": "md"},
                        {"id": "PR-1", "grade": "FULL", "evidence_quote": "supporting global G&A functions at a NASDAQ-listed SaaS company", "source": "md"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "Director, People Business Partner (New York, NY)", "source": "md"},
                    ],
                },
            },
        ],
    },
]
