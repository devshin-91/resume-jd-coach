#!/usr/bin/env python3
"""Japan Japanese (ja) 4-job-family real-JD benchmark track definitions for resume-jd-coach v2.0."""

from __future__ import annotations

JA_TRACKS = [
    {
        "slug": "track_ja01_dev_smarthr",
        "country": "Japan",
        "language": "ja",
        "family": "エンジニア / バックエンド",
        "company": "株式会社SmartHR",
        "role": "【情シス領域】シニアウェブアプリケーションエンジニア（バックエンドエンジニア）",
        "jd_url": "https://open.talentio.com/r/1/c/smarthr/pages/127964",
        "location": "フルリモート（日本国内）",
        "scenario": "Failing passive/humble Japanese 職務経歴書 in Shift-JIS (cp932) + full-width ＡＷＳ/ＧｉｔＨｕｂ -> R2 concrete ownership & RDB/CI/CD/AI proof -> PASS",
        "format": "txt_cp932",
        "jd_text": """企業名：株式会社SmartHR
募集職種：【情シス領域】シニアウェブアプリケーションエンジニア（バックエンドエンジニア）
勤務地：フルリモート可能（国内に限る）
URL：https://open.talentio.com/r/1/c/smarthr/pages/127964

業務内容：
ID管理プロダクトの機能開発・改善、多様なSaaSからのアカウント情報収集、AIを活用したWeb画面解析・ブラウザ自動操作の高度化、SLO/SLIに基づく可用性・信頼性の向上、アーキテクチャ意思決定。

必須条件：
- フレームワークを使用したウェブアプリケーション開発の実務経験5年以上
- 複雑な商用プロダクトにおけるRDBの論理設計・物理設計やパフォーマンスチューニング経験
- 課題整理から設計・実装・リリース・運用改善まで主導した経験
- 複数選択肢のトレードオフを検討し、アーキテクチャや技術方針の意思決定をリードした経験
- セキュリティや障害時の影響を考慮した設計・開発・運用経験
- CI/CD環境（CircleCI、GitHub Actionsなど）を活用した開発経験
- AIを活用した開発経験
- GitHubを用いた複数人でのチーム開発経験

歓迎条件：
- IDaaS・SaaS管理・IT資産管理など情シス領域プロダクト開発経験
- React / TypeScriptフロントエンド開発経験
- SLO/SLIサービス信頼性指標の運用経験
- GCP / AWSによるインフラ構築・運用経験
""",
        "rubric": {
            "company": "株式会社SmartHR",
            "role_title": "シニアウェブアプリケーションエンジニア（バックエンド）",
            "language": "ja",
            "domain_mode": "resume_only",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 45, "portfolio_impact": 25, "preferred": 15, "ats_framing": 15},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "Webアプリケーション開発実務5年以上＋チーム開発（GitHub）", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "商用プロダクトでのRDB論理/物理設計・性能チューニング", "weight": 3, "is_knockout": True},
                    {"id": "MH-3", "title": "要件整理〜運用改善の一貫主導とアーキテクチャ意思決定", "weight": 2, "is_knockout": False},
                    {"id": "MH-4", "title": "セキュリティ/障害耐性設計・CI/CDおよびAI活用開発", "weight": 2, "is_knockout": False},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "性能改善・障害削減・開発生産性向上の定量実績", "weight": 3, "is_knockout": False},
                    {"id": "PI-2", "title": "トレードオフ判断の背景と自律的な改善推進プロセス", "weight": 2, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "IDaaS/情シス領域またはSLO/SLI・AWS/GCPインフラ運用経験", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "シニアバックエンドとしての主体的オーナーシップ訴求", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "RDB", "aliases": ["PostgreSQL", "MySQL", "リレーショナルデータベース"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "パフォーマンスチューニング", "aliases": ["性能チューニング", "クエリ最適化"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "CI/CD", "aliases": ["GitHub Actions", "CircleCI"], "tier": "must", "linked_item_id": "MH-4"},
                {"term": "GitHub", "aliases": [], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "AI", "aliases": ["GitHub Copilot", "生成AI"], "tier": "must", "linked_item_id": "MH-4"},
                {"term": "SLO/SLI", "aliases": ["SLO", "SLI"], "tier": "preferred", "linked_item_id": "PR-1"},
                {"term": "AWS", "aliases": ["GCP"], "tier": "preferred", "linked_item_id": "PR-1"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "txt_cp932",
                    "filename": "takahashi_shokumu_r1_sjis.txt",
                    "content": """職務経歴書：高橋 誠（エンジニア・実務経験6年）

■ 職務要約
これまで6年間、受託開発会社にてWebアプリケーションのバックエンド開発を担当いたしました。チームメンバーと協力し、丁寧な実装を心がけてまいりました。

■ 保有スキル
Ｒｕｂｙ ｏｎ Ｒａｉｌｓ、ＰｏｓｔｇｒｅＳＱＬ、ＧｉｔＨｕｂ、ＡＷＳ（運用補助）

■ 職務経歴
2020年4月〜現在：株式会社ネクストシステム（Webエンジニア）
・クライアント向け業務システムの機能追加や不具合修正を担当いたしました。
・チームの指示に従いAPI実装とテストを行いました。

■ 今後の課題（未経験領域）
SLO/SLIの運用やIDaaS領域の開発は未経験です。
""",
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "STRONG_PARTIAL", "evidence_quote": "これまで6年間、受託開発会社にてWebアプリケーションのバックエンド開発を担当いたしました", "source": "cp932 txt", "gap_type": "expression_gap", "action_hint": "GitHubを用いたプルリクエストレビューなど複数人開発の具体規模を追記してください。"},
                        {"id": "MH-2", "grade": "WEAK", "evidence_quote": "ＰｏｓｔｇｒｅＳＱＬ", "source": "cp932 txt", "gap_type": "expression_gap", "action_hint": "スキル名の記載のみのため WEAK(0.25) です。商用プロダクトでのRDB論理/物理設計やスロークエリ改善事例を記載してください。"},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "cp932 txt", "gap_type": "expression_gap", "action_hint": "「指示に従い実装」ではシニア要件を満たしません。要件整理から設計・運用改善まで自ら主導した案件を具体化してください。"},
                        {"id": "MH-4", "grade": "MISSING", "evidence_quote": "", "source": "cp932 txt", "gap_type": "expression_gap", "action_hint": "セキュリティ・障害対策、CI/CD（GitHub Actions等）、AI活用開発の実務例を追記してください。"},
                        {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "source": "cp932 txt", "gap_type": "expression_gap", "action_hint": "応答速度改善や障害件数削減などの定量成果を入れてください。"},
                        {"id": "PI-2", "grade": "MISSING", "evidence_quote": "", "source": "cp932 txt", "gap_type": "expression_gap", "action_hint": "複数案のトレードオフ比較と技術的意思決定の根拠を明記してください。"},
                        {"id": "PR-1", "grade": "WEAK", "evidence_quote": "ＡＷＳ（運用補助）", "source": "cp932 txt", "gap_type": "expression_gap", "action_hint": "AWSでの具体的な構築・運用内容を記載してください（SLO/SLI未経験は正直なままで問題ありません）。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "チームの指示に従いAPI実装とテストを行いました", "source": "cp932 txt", "gap_type": "expression_gap", "action_hint": "丁寧な文体は保ちつつ、受動表現を「主導・設計・改善」の主体的表現へ見直してください。"},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "txt_cp932",
                    "filename": "takahashi_shokumu_r2_sjis.txt",
                    "content": """職務経歴書：高橋 誠（シニアバックエンドエンジニア・実務経験6年）

■ 職務要約
商用B2B SaaSおよび基幹Webアプリケーションのバックエンド開発を6年間主導いたしました。PostgreSQLの論理・物理設計からパフォーマンスチューニング、セキュリティ・障害耐性設計、GitHub ActionsによるCI/CD整備、AI活用開発まで一貫して推進しております。

■ 職務経歴
2020年4月〜現在：株式会社ネクストシステム（リードバックエンドエンジニア／8名チーム）
・【RDB設計・性能チューニング】月間1,200万件のトランザクションを処理する商用管理基盤にてPostgreSQLの論理・物理設計および複合インデックス・パーティショニングによるパフォーマンスチューニングを主導し、重要APIのP99応答時間を1.8秒から240msへ短縮いたしました。
・【技術的意思決定・一貫主導】外部SaaS連携の同期処理ボトルネックに対し、同期API案と非同期ジョブキュー案のトレードオフを検証のうえ後者を採用。要件整理〜設計・実装・リリース・監視改善まで主導し、連携エラー率を4.2%から0.08%へ低減いたしました。
・【セキュリティ・CI/CD・AI開発】認証権限チェックの多層防御設計とAWS（ECS/RDS）上の自動フェイルオーバー構築を実施。GitHub ActionsによるCI/CDおよびGitHub Copilotを活用したテストコード自動生成フローをチーム導入し、デプロイ頻度を週1回から日次へ、レビュー待ち時間を45%削減いたしました。

■ 今後の課題（未経験領域）
SLO/SLIの本格運用およびIDaaS専用プロダクト開発は未経験です。
""",
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "商用B2B SaaSおよび基幹Webアプリケーションのバックエンド開発を6年間主導いたしました", "source": "cp932 txt"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "PostgreSQLの論理・物理設計および複合インデックス・パーティショニングによるパフォーマンスチューニングを主導", "source": "cp932 txt"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "同期API案と非同期ジョブキュー案のトレードオフを検証のうえ後者を採用。要件整理〜設計・実装・リリース・監視改善まで主導", "source": "cp932 txt"},
                        {"id": "MH-4", "grade": "FULL", "evidence_quote": "GitHub ActionsによるCI/CDおよびGitHub Copilotを活用したテストコード自動生成フローをチーム導入", "source": "cp932 txt"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "重要APIのP99応答時間を1.8秒から240msへ短縮いたしました", "source": "cp932 txt"},
                        {"id": "PI-2", "grade": "FULL", "evidence_quote": "連携エラー率を4.2%から0.08%へ低減いたしました", "source": "cp932 txt"},
                        {"id": "PR-1", "grade": "PARTIAL", "evidence_quote": "AWS（ECS/RDS）上の自動フェイルオーバー構築を実施", "source": "cp932 txt", "gap_type": "true_gap", "action_hint": "AWS構築実績は評価済み。IDaaS/SLO未経験は正直に維持。"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "シニアバックエンドエンジニア・実務経験6年", "source": "cp932 txt"},
                    ],
                },
            },
        ],
    },
    {
        "slug": "track_ja02_design_smarthr",
        "country": "Japan",
        "language": "ja",
        "family": "プロダクトデザイン（ポートフォリオ）",
        "company": "株式会社SmartHR",
        "role": "プロダクトデザイナー（マネージャー候補）",
        "jd_url": "https://open.talentio.com/r/1/c/smarthr/pages/129618",
        "location": "フルリモート（日本国内）",
        "scenario": "Failing B2C visual .pptx portfolio -> R2 Japanese keyword stuffing capped at WEAK(0.25) -> R3 OOUI, B2B IA & Design Review org proof -> PASS",
        "format": "pptx",
        "jd_text": """企業名：株式会社SmartHR
募集職種：プロダクトデザイナー（マネージャー候補）
勤務地：フルリモート(ただし国内在住)もOK
URL：https://open.talentio.com/r/1/c/smarthr/pages/129618

必須条件：
- OOUI（オブジェクト指向UI）におけるUIモデリング、またはそれに準ずる概念やプロセスへの理解
- 組織の課題を捉え、体制や業務の進め方を見直すなど、組織変革を推進した経験
- デザイン品質を継続的に担保するための仕組みを構築・改善した経験
- デザインレビューと具体的なフィードバックを通じて、アウトプットの品質を担保・向上させた経験
- B2B業務アプリケーションの情報設計・UIについて良し悪しを判断し、その理由と改善の方向性を言語化して伝えられること

歓迎条件：
- B2Bサービス・SaaSのプロダクト開発経験、スクラムでの開発経験
- デザインシステムの構築・運用経験
- ユーザーリサーチやインクルーシブデザイン、大規模企業・組織における情報設計の実務経験
- デザイン組織のマネジメント経験
""",
        "rubric": {
            "company": "株式会社SmartHR",
            "role_title": "プロダクトデザイナー（マネージャー候補）",
            "language": "ja",
            "domain_mode": "portfolio",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 40, "portfolio_impact": 35, "preferred": 10, "ats_framing": 15},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "OOUI（オブジェクト指向UI）モデリングとB2B業務アプリ情報設計", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "デザイン品質担保の仕組み構築とレビュー・言語化フィードバック", "weight": 3, "is_knockout": True},
                    {"id": "MH-3", "title": "組織課題の特定と体制・プロセス変革の推進経験", "weight": 2, "is_knockout": False},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "情報設計の判断根拠・改善プロセスを示すポートフォリオ事例", "weight": 3, "is_knockout": False},
                    {"id": "PI-2", "title": "品質・開発速度・ユーザー業務効率の定量成果", "weight": 2, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "B2B SaaS・デザインシステム構築・組織マネジメント経験", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "デザインマネージャー候補としての組織・品質視点訴求", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "OOUI", "aliases": ["オブジェクト指向UI", "UIモデリング"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "情報設計", "aliases": ["B2B"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "デザインレビュー", "aliases": ["品質担保"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "組織変革", "aliases": ["体制", "デザイン組織"], "tier": "must", "linked_item_id": "MH-3"},
                {"term": "デザインシステム", "aliases": ["SaaS", "スクラム"], "tier": "preferred", "linked_item_id": "PR-1"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "pptx",
                    "filename": "sato_haruka_portfolio_r1.pptx",
                    "slides": [
                        "佐藤 遥 — Web・UIデザイナー ポートフォリオ",
                        "作品1：ECキャンペーンLP制作 — 季節感のあるビジュアルとバナーを作成いたしました。",
                        "作品2：自社サービス管理画面の配色リニューアル — 見た目を明るく整理しました。",
                    ],
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "OOUIモデリングやB2B業務アプリの情報設計判断を具体事例として示してください。"},
                        {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "デザインレビューの観点や品質担保の仕組み構築事例を明記してください。"},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "組織のボトルネックや体制・プロセス改善を主導した経験があれば追記してください。"},
                        {"id": "PI-1", "grade": "WEAK", "evidence_quote": "見た目を明るく整理しました", "source": "pptx Slide 3", "gap_type": "expression_gap", "action_hint": "表層ビジュアルだけでなく、課題定義・構造判断の理由を言語化してください。"},
                        {"id": "PI-2", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "業務時間短縮や手戻り削減などの定量効果を加えてください。"},
                        {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "B2B SaaS・デザインシステム・マネジメント経験があれば記載してください。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "Web・UIデザイナー ポートフォリオ", "source": "pptx Slide 1", "gap_type": "expression_gap", "action_hint": "マネージャー候補にふさわしい品質・組織リード視点へ再構成してください。"},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "pptx",
                    "filename": "sato_haruka_portfolio_r2_stuffed.pptx",
                    "slides": [
                        "佐藤 遥 — プロダクトデザイナー ポートフォリオ",
                        "作品1：ECキャンペーンLP制作 — 季節感のあるビジュアルとバナーを作成いたしました。",
                        "作品2：自社サービス管理画面の配色リニューアル — 見た目を明るく整理しました。",
                        "スキル一覧：OOUI、情報設計、B2B、デザインレビュー、組織変革、デザインシステム、SaaS。",
                    ],
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "WEAK", "evidence_quote": "スキル一覧：OOUI、情報設計、B2B", "source": "pptx Slide 4", "gap_type": "expression_gap", "action_hint": "スキル羅列のみは WEAK(0.25) 上限です。実際のOOUIモデリング事例をスライド化してください。"},
                        {"id": "MH-2", "grade": "WEAK", "evidence_quote": "デザインレビュー、組織変革、デザインシステム", "source": "pptx Slide 4", "gap_type": "expression_gap", "action_hint": "具体的なレビュー基準や品質担保の仕組みを実例で示してください。"},
                        {"id": "MH-3", "grade": "WEAK", "evidence_quote": "デザインレビュー、組織変革", "source": "pptx Slide 4", "gap_type": "expression_gap", "action_hint": "組織変革の具体アクションと結果を明記してください。"},
                        {"id": "PI-1", "grade": "WEAK", "evidence_quote": "見た目を明るく整理しました", "source": "pptx Slide 3", "gap_type": "expression_gap", "action_hint": "設計判断の理由を事例ごとに言語化してください。"},
                        {"id": "PI-2", "grade": "MISSING", "evidence_quote": "", "source": "pptx", "gap_type": "expression_gap", "action_hint": "定量成果がまだありません。"},
                        {"id": "PR-1", "grade": "WEAK", "evidence_quote": "デザインシステム、SaaS", "source": "pptx Slide 4", "gap_type": "expression_gap", "action_hint": "デザインシステム運用の具体実績が必要です。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "スキル一覧：OOUI、情報設計、B2B", "source": "pptx Slide 4", "gap_type": "expression_gap", "action_hint": "キーワード羅列スライドを廃止し、ケーススタディ中心へ差し替えてください。"},
                    ],
                },
            },
            {
                "round": 3,
                "candidate_doc": {
                    "type": "pptx",
                    "filename": "sato_haruka_portfolio_r3.pptx",
                    "slides": [
                        "佐藤 遥 — プロダクトデザインマネージャー（B2B SaaS・OOUI・デザイン組織推進）",
                        "事例1：B2B労務・請求SaaS管理画面のOOUI情報設計刷新 — タスク起点で分断されていた18画面を、オブジェクト指向UI（OOUI）モデリングにより5つの主要オブジェクトへ再統合。エンジニア・PMとスクラムで検証し、顧客の月次処理時間を34%短縮・問い合わせ件数を41%削減。",
                        "事例2：デザイン組織変革と品質担保・レビュー基盤構築 — デザイナー6名の属人化課題を解消するため、週次デザインレビュー基準と言語化ルーブリックおよびFigmaデザインシステムを整備。設計手戻り率を52%低減し、メンバー2名のシニア昇格・採用オンボーディングを主導。",
                    ],
                },
                "eval": {
                    "round": 3,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "タスク起点で分断されていた18画面を、オブジェクト指向UI（OOUI）モデリングにより5つの主要オブジェクトへ再統合", "source": "pptx Slide 2"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "週次デザインレビュー基準と言語化ルーブリックおよびFigmaデザインシステムを整備", "source": "pptx Slide 3"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "デザイナー6名の属人化課題を解消するため、週次デザインレビュー基準と言語化ルーブリックおよびFigmaデザインシステムを整備", "source": "pptx Slide 3"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "B2B労務・請求SaaS管理画面のOOUI情報設計刷新", "source": "pptx Slide 2"},
                        {"id": "PI-2", "grade": "FULL", "evidence_quote": "顧客の月次処理時間を34%短縮・問い合わせ件数を41%削減", "source": "pptx Slide 2"},
                        {"id": "PR-1", "grade": "FULL", "evidence_quote": "エンジニア・PMとスクラムで検証", "source": "pptx Slide 2"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "プロダクトデザインマネージャー（B2B SaaS・OOUI・デザイン組織推進）", "source": "pptx Slide 1"},
                    ],
                },
            },
        ],
    },
    {
        "slug": "track_ja03_pm_mercari",
        "country": "Japan",
        "language": "ja",
        "family": "プロダクトマネージャー（PM）",
        "company": "株式会社メルカリ（Mercari）",
        "role": "Product Manager / プロダクトマネージャー - Mercari Marketplace",
        "jd_url": "https://careers.mercari.com/",
        "location": "東京・六本木（Hybrid）",
        "scenario": "R1 failing feature-list PM -> R2 crosses 80% BUT SQL Knockout is WEAK -> Japanese PASS_WITH_RISK -> R3 substantiates SQL analysis -> PASS",
        "format": "md",
        "jd_text": """企業名：株式会社メルカリ（Mercari, Inc.）
募集職種：Product Manager / プロダクトマネージャー - Mercari Marketplace
勤務地：六本木（東京 / Hybrid）
採用サイト参照元：https://careers.mercari.com/

必須条件：
- AIツールを調査・仮説検証・プロトタイピングに使い、意思決定の質とスピードを上げた経験
- 機能数ではなくKPIなどの事業成果に責任を持ち、発見→開発→学習の一連をリードした経験
- リリース後のGTM・関係部門連携・学習まで推進した経験
- インターネットサービスにおけるプロダクトマネジメント経験（3年以上）
- アジャイル等ソフトウェア開発の基礎知識とエンジニア協働経験
- SQL等を用いたデータ分析によるインサイト抽出の経験
- 日本語：Proficient (CEFR C1) 必須

歓迎条件：
- CtoCマーケットプレイス・EC領域の知見
- 0→1と1→Nの両方の経験、A/Bテストに基づく意思決定
- 英語（CEFR B2）歓迎
""",
        "rubric": {
            "company": "株式会社メルカリ（Mercari）",
            "role_title": "プロダクトマネージャー - Mercari Marketplace",
            "language": "ja",
            "domain_mode": "portfolio",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 45, "portfolio_impact": 25, "preferred": 15, "ats_framing": 15},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "WebサービスPM実務3年以上・エンジニア協働・日本語C1", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "KPI事業成果オーナーシップ（発見→開発→GTM→学習）", "weight": 3, "is_knockout": False},
                    {"id": "MH-3", "title": "AIツールを活用した仮説検証・プロトタイピング実績", "weight": 2, "is_knockout": False},
                    {"id": "MH-4", "title": "SQLを用いたデータ分析・インサイト抽出実務", "weight": 2, "is_knockout": True},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "GMV/転換率など定量KPI改善の事業成果ケース", "weight": 3, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "EC/マーケットプレイス知見・A/Bテスト・0→1/1→N経験", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "成果・AI駆動プロダクトマネージャーとしての訴求構成", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "プロダクトマネジメント", "aliases": ["PM", "プロダクトマネージャー"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "KPI", "aliases": ["GMV", "CVR"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "SQL", "aliases": ["BigQuery"], "tier": "must", "linked_item_id": "MH-4"},
                {"term": "AI", "aliases": ["Gemini", "Claude", "生成AI"], "tier": "must", "linked_item_id": "MH-3"},
                {"term": "アジャイル", "aliases": ["スクラム"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "A/Bテスト", "aliases": ["ABテスト"], "tier": "preferred", "linked_item_id": "PR-1"},
                {"term": "マーケットプレイス", "aliases": ["EC", "CtoC"], "tier": "preferred", "linked_item_id": "PR-1"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "md",
                    "filename": "suzuki_ryo_r1.md",
                    "content": """# 鈴木 涼 — プロジェクト進行担当（東京・日本語ネイティブ）

## 職務経歴
- 2022年4月〜現在：株式会社コマースリンク（WebサービスPM・4年）
  - ECアプリの新機能リリースを年間20本以上スケジュール通りに進行管理いたしました。
  - エンジニア・デザイナーとアジャイル開発で連携し、仕様書作成を担当しました。

## 補足
SQLによるデータ抽出はアナリストへ依頼しており実務経験なし、A/Bテストの統計設計も未経験です。
""",
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "WebサービスPM・4年", "source": "md"},
                        {"id": "MH-2", "grade": "WEAK", "evidence_quote": "新機能リリースを年間20本以上スケジュール通りに進行管理いたしました", "source": "md", "gap_type": "expression_gap", "action_hint": "「機能数・納期管理」ではなく、KPIなどの事業成果に責任を持った発見→GTM→学習事例へ書き換えてください。"},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "expression_gap", "action_hint": "生成AIを用いた顧客リサーチ・仮説検証・プロトタイピング事例があれば具体化してください。"},
                        {"id": "MH-4", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "expression_gap", "action_hint": "KNOCKOUT必須要件：ご自身でSQLを書いてインサイト抽出した実績がある場合は必ず明記してください。"},
                        {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "source": "md", "gap_type": "expression_gap", "action_hint": "GMVや購入転換率などリリース後の定量KPI変化を追記してください。"},
                        {"id": "PR-1", "grade": "PARTIAL", "evidence_quote": "ECアプリの新機能リリース", "source": "md", "gap_type": "expression_gap", "action_hint": "EC/マーケットプレイスでの0→1または1→N改善とA/Bテスト意思決定事例があれば追記してください。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "プロジェクト進行担当", "source": "md", "gap_type": "expression_gap", "action_hint": "進行管理型ではなく事業成果オーナー型プロダクトマネージャーとして再配置してください。"},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "md",
                    "filename": "suzuki_ryo_r2_pass_with_risk.md",
                    "content": """# 鈴木 涼 — プロダクトマネージャー（EC・マーケットプレイス領域 / 日本語ネイティブ C1）

## 職務経歴
- 2022年4月〜現在：株式会社コマースリンク（プロダクトマネージャー・4年）
  - **KPI事業成果・発見→開発→GTM→学習（1→N / 0→1）：** CtoCマーケットプレイス出品フローの離脱課題をUXリサーチャーと特定し、アジャイル開発チーム8名をリード。法務・CSと連携したGTMとリリース後のA/Bテスト改善により、出品完了率を+18.4%・月間GMVを+1.4億円向上。
  - **AI活用ディスカバリー：** Gemini・NotebookLMによるユーザーインタビュー要約と、Cursorを用いたインタラクティブプロトタイプ検証を導入し、仮説検証リードタイムを3週間から5日へ短縮。
  - **保有スキル：** プロダクトマネジメント、SQL（基礎学習）、アジャイル、A/Bテスト。
""",
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "プロダクトマネージャー・4年", "source": "md"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "CtoCマーケットプレイス出品フローの離脱課題をUXリサーチャーと特定し、法務・CSと連携したGTMとリリース後のA/Bテスト改善", "source": "md"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "Gemini・NotebookLMによるユーザーインタビュー要約と、Cursorを用いたインタラクティブプロトタイプ検証を導入", "source": "md"},
                        {"id": "MH-4", "grade": "WEAK", "evidence_quote": "SQL（基礎学習）", "source": "md", "gap_type": "expression_gap", "action_hint": "KNOCKOUT警告：スキル欄の「SQL（基礎学習）」のみでは WEAK(0.25) です。実務で自らBigQuery/SQLを叩いて意思決定した事例を追記してください。"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "出品完了率を+18.4%・月間GMVを+1.4億円向上", "source": "md"},
                        {"id": "PR-1", "grade": "FULL", "evidence_quote": "CtoCマーケットプレイス出品フロー", "source": "md"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "プロダクトマネージャー（EC・マーケットプレイス領域 / 日本語ネイティブ C1）", "source": "md"},
                    ],
                },
            },
            {
                "round": 3,
                "candidate_doc": {
                    "type": "md",
                    "filename": "suzuki_ryo_r3.md",
                    "content": """# 鈴木 涼 — プロダクトマネージャー（EC・マーケットプレイス領域 / 日本語ネイティブ C1）

## 職務経歴
- 2022年4月〜現在：株式会社コマースリンク（プロダクトマネージャー・4年）
  - **KPI事業成果・発見→開発→GTM→学習（1→N / 0→1）：** CtoCマーケットプレイス出品フローの離脱課題をUXリサーチャーと特定し、アジャイル開発チーム8名をリード。法務・CSと連携したGTMとリリース後のA/Bテスト改善により、出品完了率を+18.4%・月間GMVを+1.4億円向上。
  - **SQLによる自律データ分析：** 自らBigQuery SQLで出品者コホート・検索ファネルクエリを作成し、初出品後72時間以内の価格改定行動が売却率を2.3倍高めるインサイトを抽出。自動値下げ提案機能の企画・実装へ直結させた。
  - **AI活用ディスカバリー：** Gemini・NotebookLMによるユーザーインタビュー要約と、Cursorを用いたインタラクティブプロトタイプ検証を導入し、仮説検証リードタイムを3週間から5日へ短縮。
""",
                },
                "eval": {
                    "round": 3,
                    "items": [
                        {"id": "MH-1", "grade": "FULL", "evidence_quote": "プロダクトマネージャー・4年", "source": "md"},
                        {"id": "MH-2", "grade": "FULL", "evidence_quote": "法務・CSと連携したGTMとリリース後のA/Bテスト改善により、出品完了率を+18.4%・月間GMVを+1.4億円向上", "source": "md"},
                        {"id": "MH-3", "grade": "FULL", "evidence_quote": "Gemini・NotebookLMによるユーザーインタビュー要約と、Cursorを用いたインタラクティブプロトタイプ検証を導入", "source": "md"},
                        {"id": "MH-4", "grade": "FULL", "evidence_quote": "自らBigQuery SQLで出品者コホート・検索ファネルクエリを作成し、初出品後72時間以内の価格改定行動が売却率を2.3倍高めるインサイトを抽出", "source": "md"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "出品完了率を+18.4%・月間GMVを+1.4億円向上", "source": "md"},
                        {"id": "PR-1", "grade": "FULL", "evidence_quote": "CtoCマーケットプレイス出品フロー", "source": "md"},
                        {"id": "AF-1", "grade": "FULL", "evidence_quote": "プロダクトマネージャー（EC・マーケットプレイス領域 / 日本語ネイティブ C1）", "source": "md"},
                    ],
                },
            },
        ],
    },
    {
        "slug": "track_ja04_nonit_freee",
        "country": "Japan",
        "language": "ja",
        "family": "非IT・コーポレート（連結経理・税務）",
        "company": "フリー株式会社（freee）",
        "role": "経理（連結・税務・M&A/PMI）｜グループ経理の中核メンバー",
        "jd_url": "https://hire.wantedly.com/careers/freee/career_page_all_jobs/4793",
        "location": "東京・品川",
        "scenario": "Real multi-sheet Japanese .xlsx (履歴書+職務経歴書) + true_gap Knockout ceiling -> Stays REVISE (<80%) with honest_fit_advisory",
        "format": "xlsx",
        "jd_text": """企業名：フリー株式会社（freee K.K.）
募集職種：経理（連結・税務・M&A/PMI）｜グループ経理の中核メンバー
勤務地：東京都品川区大崎
URL：https://hire.wantedly.com/careers/freee/career_page_all_jobs/4793

業務内容：
①M&A・PMI対応（会計方針すり合わせ、連結パッケージ作成、標準化）
②連結・子会社管理（連結決算、開示書類作成、連結統制、監査法人対応）
③税務（税金計算、税効果会計、税務統制）

必須要件（以下いずれか）：
- 監査法人での会計監査（目安：3年以上）
- FASなどでのDD・PMI支援（目安：3年以上）
- 事業会社での経理（目安：3年以上）＋連結決算実務経験（目安：1年以上）

歓迎要件：
- 上場企業の連結決算・開示監査、税効果会計、財務DD/PPA、J-SOX整備
- 公認会計士、USCPA
""",
        "rubric": {
            "company": "フリー株式会社（freee）",
            "role_title": "経理（連結・税務・M&A/PMI）",
            "language": "ja",
            "domain_mode": "resume_only",
            "pass_threshold": 80.0,
            "ats_lexical_share": 0.5,
            "category_weights": {"must_have": 55, "portfolio_impact": 20, "preferred": 15, "ats_framing": 10},
            "categories": {
                "must_have": [
                    {"id": "MH-1", "title": "監査法人3年 / FAS 3年 / 事業会社経理3年＋連結決算1年以上", "weight": 3, "is_knockout": True},
                    {"id": "MH-2", "title": "連結決算・子会社管理・監査法人との論点協議完結力", "weight": 3, "is_knockout": True},
                    {"id": "MH-3", "title": "税金計算・税効果会計および業務標準化・統制整備", "weight": 2, "is_knockout": False},
                ],
                "portfolio_impact": [
                    {"id": "PI-1", "title": "決算早期化・統制構築・マニュアル標準化の定量実績", "weight": 2, "is_knockout": False},
                ],
                "preferred": [
                    {"id": "PR-1", "title": "M&A・PMI/財務DD経験または公認会計士・USCPA資格", "weight": 2, "is_knockout": False},
                ],
                "ats_framing": [
                    {"id": "AF-1", "title": "グループ経理中核メンバーとしての専門性訴求", "weight": 2, "is_knockout": False},
                ],
            },
            "keywords": [
                {"term": "連結決算", "aliases": ["連結パッケージ", "開示書類"], "tier": "must", "linked_item_id": "MH-1"},
                {"term": "監査法人", "aliases": ["会計監査"], "tier": "must", "linked_item_id": "MH-2"},
                {"term": "税効果会計", "aliases": ["税金計算", "税務"], "tier": "must", "linked_item_id": "MH-3"},
                {"term": "PMI", "aliases": ["M&A", "財務DD"], "tier": "preferred", "linked_item_id": "PR-1"},
                {"term": "公認会計士", "aliases": ["USCPA", "J-SOX"], "tier": "preferred", "linked_item_id": "PR-1"},
            ],
        },
        "rounds": [
            {
                "round": 1,
                "candidate_doc": {
                    "type": "xlsx",
                    "filename": "nakamura_rirekisho_r1.xlsx",
                    "sheets": [
                        ("職務経歴書", [
                            ["氏名", "中村 彩花（経理実務2年）"],
                            ["職務要約", "中小企業にて単体経理の仕訳入力、経費精算、請求書発行を2年間担当いたしました。"],
                            ["業務内容", "日々の入出金消込、売掛買掛管理、月次試算表の作成補助を担当。"],
                            ["今後の課題", "連結決算・税効果会計・監査法人対応・M&AおよびPMI会計はいずれも未経験です。"],
                        ]),
                        ("履歴書", [
                            ["学歴", "商学部 卒業"],
                            ["資格", "日商簿記2級"],
                        ]),
                    ],
                },
                "eval": {
                    "round": 1,
                    "items": [
                        {"id": "MH-1", "grade": "MISSING", "evidence_quote": "", "source": "xlsx 職務経歴書", "gap_type": "true_gap", "action_hint": "必須要件（事業会社経理3年＋連結1年、または監査/FAS 3年）を満たさない真の要件ギャップです。"},
                        {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "source": "xlsx 職務経歴書", "gap_type": "true_gap", "action_hint": "連結決算・監査法人対応は未経験のため虚偽記載厳禁です。"},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "xlsx 職務経歴書", "gap_type": "true_gap", "action_hint": "税効果会計未経験のため、まずは単体月次・年次決算の標準化実績を伸ばす方向をご検討ください。"},
                        {"id": "PI-1", "grade": "MISSING", "evidence_quote": "", "source": "xlsx 職務経歴書", "gap_type": "expression_gap", "action_hint": "現在の単体経理で行った決算業務効率化やマニュアル化の定量実績があれば追記できます。"},
                        {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "source": "xlsx 職務経歴書", "gap_type": "true_gap", "action_hint": "歓迎要件のM&A/会計士資格は未保有です。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "中小企業にて単体経理の仕訳入力、経費精算、請求書発行を2年間担当いたしました", "source": "xlsx 職務経歴書", "gap_type": "true_gap", "action_hint": "中核グループ経理ポジションとの実務レンジ差が大きいため、単体決算主担当ポジションとの併願をおすすめします。"},
                    ],
                },
            },
            {
                "round": 2,
                "candidate_doc": {
                    "type": "xlsx",
                    "filename": "nakamura_rirekisho_r2.xlsx",
                    "sheets": [
                        ("職務経歴書", [
                            ["氏名", "中村 彩花（単体経理・月次決算改善担当・実務2年）"],
                            ["職務要約", "単体経理実務2年間にて月次決算早期化および業務マニュアル標準化を推進いたしました。"],
                            ["主な実績", "経費精算・請求書処理フローを標準化しチェックリストを整備。月次試算表の締め日数を10営業日から6営業日へ40%短縮し、仕訳修正件数を月平均14件から2件へ削減。"],
                            ["今後の課題", "連結決算・税効果会計・監査法人対応・M&AおよびPMI会計はいずれも未経験です。"],
                        ]),
                        ("履歴書", [
                            ["学歴", "商学部 卒業"],
                            ["資格", "日商簿記2級"],
                        ]),
                    ],
                },
                "eval": {
                    "round": 2,
                    "items": [
                        {"id": "MH-1", "grade": "MISSING", "evidence_quote": "", "source": "xlsx 職務経歴書", "gap_type": "true_gap", "action_hint": "真の必須要件ギャップ（経理3年＋連結1年未達）。"},
                        {"id": "MH-2", "grade": "MISSING", "evidence_quote": "", "source": "xlsx 職務経歴書", "gap_type": "true_gap", "action_hint": "連結決算・監査法人対応は未経験。"},
                        {"id": "MH-3", "grade": "MISSING", "evidence_quote": "", "source": "xlsx 職務経歴書", "gap_type": "true_gap", "action_hint": "税効果会計は未経験。"},
                        {"id": "PI-1", "grade": "FULL", "evidence_quote": "月次試算表の締め日数を10営業日から6営業日へ40%短縮し、仕訳修正件数を月平均14件から2件へ削減", "source": "xlsx 職務経歴書"},
                        {"id": "PR-1", "grade": "MISSING", "evidence_quote": "", "source": "xlsx 職務経歴書", "gap_type": "true_gap", "action_hint": "未保有の歓迎要件。"},
                        {"id": "AF-1", "grade": "WEAK", "evidence_quote": "単体経理・月次決算改善担当・実務2年", "source": "xlsx 職務経歴書", "gap_type": "true_gap", "action_hint": "単体決算での改善実績は明確ですが、本求人の連結・M&A必須要件には届かないため他求人併願が現実的です。"},
                    ],
                },
            },
        ],
    },
]
