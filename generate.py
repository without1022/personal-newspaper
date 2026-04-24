#!/usr/bin/env python3
"""
📰 魔法财经日报 v5.0
- 老报纸复古排版
- 哈利波特魔法报纸效果
"""

import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List

CONFIG = {"output_dir": "./docs"}

NEWS_CATEGORIES = {
    "domestic": {"name": "国内财经", "icon": "🇨🇳"},
    "international": {"name": "国际财经", "icon": "🌍"},
    "ai-tech": {"name": "魔法科技", "icon": "✨"},
    "internet": {"name": "互联网", "icon": "💻"},
    "semiconductor": {"name": "魔晶工业", "icon": "🔮"},
    "crypto": {"name": "加密金币", "icon": "🪙"},
    "ev": {"name": "魔法飞毯", "icon": "🧹"}
}

class MagicNewspaper:
    def __init__(self):
        self.all_news = {}
        self.stocks = []
        self.mood_score = 0
        self.date = datetime.now()
        self.date_str = self.date.strftime("%Y年%m月%d日")
        self.weekday = self.date.strftime("%A")
        self.issue_no = 1024 + (self.date - datetime(2024, 1, 1)).days

    def prepare_news_data(self) -> Dict:
        current_hour = datetime.now().hour
        
        news_data = {
            "domestic": [
                {
                    "title": "A股三大指数集体收涨，成交额突破万亿元大关",
                    "source": "证券时报",
                    "location": "上海",
                    "summary": "今日A股市场延续强势格局，三大指数集体收涨，两市成交额突破1万亿元。北向资金净流入超80亿元，机构持仓比例持续提升，市场信心稳步恢复。",
                    "tags": ["A股", "成交额", "北向资金"],
                    "mood": 0.8,
                    "hot": 92,
                    "image": "📈"
                },
                {
                    "title": "央行开展500亿元逆回购操作，维护流动性合理充裕",
                    "source": "中国人民银行",
                    "location": "北京",
                    "summary": "央行今日开展500亿元7天期逆回购操作，中标利率维持不变。本周累计净投放2000亿元，维护银行体系流动性合理充裕。",
                    "tags": ["央行", "逆回购", "流动性"],
                    "mood": 0.75,
                    "hot": 85,
                    "image": "🏦"
                }
            ],
            "international": [
                {
                    "title": "美联储释放鸽派信号，美股三大指数创历史新高",
                    "source": "路透社",
                    "location": "纽约",
                    "summary": "美联储主席在最新讲话中释放鸽派信号，表示通胀压力正在缓解，市场预期年内将开始降息。美股三大指数应声上涨，集体创出历史新高。",
                    "tags": ["美联储", "美股", "降息"],
                    "mood": 0.85,
                    "hot": 95,
                    "image": "🗽"
                },
                {
                    "title": "英伟达市值突破3.5万亿美元，AI芯片需求持续火爆",
                    "source": "彭博社",
                    "location": "硅谷",
                    "summary": "英伟达股价持续上涨，市值已突破3.5万亿美元，成为全球市值最高的公司。AI芯片需求呈现爆发式增长，公司订单已排到2027年。",
                    "tags": ["英伟达", "AI芯片", "市值"],
                    "mood": 0.9,
                    "hot": 98,
                    "image": "🚀"
                }
            ],
            "ai-tech": [
                {
                    "title": "OpenAI发布GPT-4o升级版，多模态能力大幅提升",
                    "source": "魔法部公告",
                    "location": "旧金山",
                    "summary": "OpenAI发布GPT-4o升级版，在推理能力、数学计算、代码生成等方面均有显著提升，响应速度提升50%。新模型支持更长上下文窗口。",
                    "tags": ["OpenAI", "GPT-4o", "大模型"],
                    "mood": 0.9,
                    "hot": 98,
                    "image": "🤖"
                }
            ],
            "crypto": [
                {
                    "title": "比特币减半后持续走强，站稳10万美元关口",
                    "source": "CoinDesk",
                    "location": "加密世界",
                    "summary": "比特币第四次减半顺利完成后，价格持续上涨站稳10万美元关口。机构投资者持续增持，市场情绪普遍乐观。",
                    "tags": ["比特币", "减半", "机构"],
                    "mood": 0.85,
                    "hot": 94,
                    "image": "🪙"
                }
            ],
            "ev": [
                {
                    "title": "比亚迪月销量突破50万辆，创历史新高",
                    "source": "比亚迪",
                    "location": "深圳",
                    "summary": "比亚迪公布最新销量数据，全系销量达到51.2万辆，再创历史新高。其中海外销量突破10万辆，国际化战略成效显著。",
                    "tags": ["比亚迪", "新能源", "销量"],
                    "mood": 0.85,
                    "hot": 91,
                    "image": "🚗"
                },
                {
                    "title": "特斯拉FSD正式入华，自动驾驶行业加速",
                    "source": "特斯拉中国",
                    "location": "上海",
                    "summary": "特斯拉FSD完全自动驾驶系统正式获得中国监管部门批准。业内认为这将推动中国自动驾驶行业标准加速成熟。",
                    "tags": ["特斯拉", "FSD", "自动驾驶"],
                    "mood": 0.8,
                    "hot": 94,
                    "image": "⚡"
                }
            ]
        }
        
        # 计算整体情绪
        all_moods = []
        for cat_news in news_data.values():
            for news in cat_news:
                all_moods.append(news.get("mood", 0.6))
        self.mood_score = int(sum(all_moods) / len(all_moods) * 100)
        
        self.all_news = news_data
        
        total = sum(len(v) for v in news_data.values())
        print(f"✅ 共整理 {total} 条魔法新闻")
        print(f"📊 今日魔法指数: {self.mood_score}")
        
        return news_data

    def get_stocks(self):
        print("📈 正在获取魔法股票数据...")
        self.stocks = [
            {"code": "002594", "name": "比亚迪", "price": "358.50", "change": "+5.23%", "recommend": "买入"},
            {"code": "NVDA", "name": "英伟达", "price": "1280.50", "change": "+8.32%", "recommend": "买入"},
            {"code": "TSLA", "name": "特斯拉", "price": "325.80", "change": "+4.56%", "recommend": "买入"},
        ]

    def generate_html(self):
        print("🎨 正在生成魔法报纸（老报纸 + 哈利波特风格）...")

        # 导航
        nav_html = ""
        for cat_key, cat_info in NEWS_CATEGORIES.items():
            nav_html += f"""
            <a href="#{cat_key}" class="nav-item" data-category="{cat_key}">
                {cat_info['icon']} {cat_info['name']}
            </a>
            """

        # 要闻（第一条）
        top_news = self.all_news["international"][0]
        
        # 头版头条
        headline_html = f"""
        <div class="headline-article">
            <div class="headline-image">
                <span class="magic-emoji">{top_news['image']}</span>
            </div>
            <div class="headline-content">
                <div class="headline-location">{top_news['location']} · {top_news['source']}</div>
                <h1 class="headline-title">{top_news['title']}</h1>
                <p class="headline-lead">{top_news['summary']}</p>
                <div class="headline-tags">
                    {"".join([f'<span class="tag">{tag}</span>' for tag in top_news['tags']])}
                </div>
            </div>
        </div>
        """

        # 新闻板块 - 报纸分栏风格
        news_sections_html = ""
        for cat_key, cat_info in NEWS_CATEGORIES.items():
            news_list = self.all_news.get(cat_key, [])
            if not news_list:
                continue
                
            news_cards_html = ""
            for idx, news in enumerate(news_list):
                news_id = f"news-{cat_key}-{idx}"
                tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in news["tags"]])
                
                news_cards_html += f"""
                <article class="news-article" data-newsid="{news_id}">
                    <div class="article-image">
                        <span class="magic-emoji-small">{news['image']}</span>
                    </div>
                    <div class="article-content">
                        <div class="article-meta">
                            <span class="article-location">{news['location']}</span>
                            <span class="article-source">{news['source']}</span>
                        </div>
                        <h3 class="article-title">{news['title']}</h3>
                        <p class="article-summary">{news['summary']}</p>
                        <div class="article-footer">
                            <div class="article-tags">{tags_html}</div>
                            <button class="article-expand" onclick="toggleMagicNews('{news_id}', this)">
                                ✨ 继续阅读
                            </button>
                        </div>
                    </div>
                    <!-- 魔法展开内容 -->
                    <div class="article-full" id="{news_id}">
                        <div class="article-full-inner">
                            <p>📜 据魔法部可靠消息人士透露...</p>
                            <p>{news['summary']}</p>
                            <p>🔮 占星师预测：此消息将在未来几周持续影响市场情绪。</p>
                            <p class="magic-sign">— 预言家日报特派记者</p>
                        </div>
                    </div>
                </article>
                """

            news_sections_html += f"""
            <section id="{cat_key}" class="news-section">
                <div class="section-header">
                    <span class="section-icon">{cat_info['icon']}</span>
                    <h2 class="section-title">{cat_info['name']}</h2>
                    <div class="section-rule"></div>
                </div>
                <div class="section-grid">
                    {news_cards_html}
                </div>
            </section>
            """

        # 股票表格 - 老报纸风格
        stocks_html = ""
        for stock in self.stocks:
            rec_class = "buy" if stock["recommend"] == "买入" else "hold"
            stocks_html += f"""
            <tr>
                <td class="stock-code">{stock['code']}</td>
                <td class="stock-name">{stock['name']}</td>
                <td class="stock-price">{stock['price']}</td>
                <td class="up">{stock['change']}</td>
                <td><span class="recommend {rec_class}">{stock['recommend']}</span></td>
            </tr>
            """

        # 情绪判断
        if self.mood_score >= 75:
            mood_label = "魔法旺盛 ✨"
            mood_emoji = "🌟"
        elif self.mood_score >= 60:
            mood_label = "趋势向好 🌤️"
            mood_emoji = "🌤️"
        else:
            mood_label = "保持谨慎 ☁️"
            mood_emoji = "☁️"

        total_news = sum(len(v) for v in self.all_news.values())

        # 完整HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📰 预言家财经日报</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Playfair+Display:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        /* ===== 魔法报纸基础样式 ===== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --paper: #f5f0e6;
            --paper-dark: #e8e0d0;
            --ink: #1a1a1a;
            --ink-light: #4a4a4a;
            --ink-faint: #7a7a7a;
            --gold: #b8860b;
            --gold-light: #daa520;
            --magic: #6366f1;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-5px); }}
        }}

        @keyframes shimmer {{
            0% {{ opacity: 0.3; }}
            50% {{ opacity: 0.8; }}
            100% {{ opacity: 0.3; }}
        }}

        @keyframes magicGlow {{
            0%, 100% {{ box-shadow: 0 0 20px rgba(99, 102, 241, 0.2); }}
            50% {{ box-shadow: 0 0 40px rgba(99, 102, 241, 0.4); }}
        }}

        @keyframes inkSpread {{
            from {{
                opacity: 0;
                transform: scale(0.95);
            }}
            to {{
                opacity: 1;
                transform: scale(1);
            }}
        }}

        body {{
            font-family: 'Noto Serif SC', 'Playfair Display', Georgia, serif;
            background: var(--paper);
            background-image: 
                url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
            color: var(--ink);
            line-height: 1.7;
        }}

        /* ===== 魔法粒子背景 ===== */
        .magic-particles {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }}

        .particle {{
            position: absolute;
            width: 4px;
            height: 4px;
            background: radial-gradient(circle, var(--gold-light) 0%, transparent 70%);
            border-radius: 50%;
            animation: shimmer 3s infinite;
        }}

        /* ===== 报纸刊头 ===== */
        .newspaper-header {{
            background: var(--paper);
            border-bottom: 4px double var(--ink);
            padding: 30px 20px 20px;
            position: relative;
        }}

        .newspaper-masthead {{
            max-width: 1000px;
            margin: 0 auto;
            text-align: center;
        }}

        .newspaper-title {{
            font-family: 'Playfair Display', 'Noto Serif SC', serif;
            font-size: 3.5em;
            font-weight: 900;
            letter-spacing: 0.1em;
            margin-bottom: 8px;
            animation: float 4s ease-in-out infinite;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }}

        .newspaper-subtitle {{
            font-size: 0.95em;
            color: var(--ink-light);
            letter-spacing: 0.3em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }}

        .newspaper-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid var(--ink-faint);
            border-bottom: 1px solid var(--ink-faint);
            padding: 8px 0;
            font-size: 0.85em;
            color: var(--ink-light);
        }}

        .weather-widget {{
            font-size: 1.2em;
            animation: float 3s ease-in-out infinite;
        }}

        /* ===== 头版头条 ===== */
        .headline-section {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 30px 20px;
            border-bottom: 2px solid var(--ink);
        }}

        .headline-article {{
            display: grid;
            grid-template-columns: 120px 1fr;
            gap: 24px;
            align-items: start;
        }}

        .headline-image {{
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .magic-emoji {{
            font-size: 5em;
            animation: float 3s ease-in-out infinite, magicGlow 2s ease-in-out infinite;
            filter: drop-shadow(0 0 10px rgba(218, 165, 32, 0.5));
        }}

        .magic-emoji-small {{
            font-size: 2.5em;
            animation: float 3s ease-in-out infinite;
        }}

        .headline-location {{
            font-size: 0.8em;
            color: var(--ink-faint);
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 8px;
        }}

        .headline-title {{
            font-family: 'Playfair Display', 'Noto Serif SC', serif;
            font-size: 1.8em;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 12px;
        }}

        .headline-lead {{
            font-size: 1.05em;
            color: var(--ink-light);
            line-height: 1.8;
            margin-bottom: 12px;
        }}

        .headline-tags {{
            display: flex;
            gap: 8px;
        }}

        /* ===== 板块标题 ===== */
        .news-section {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 24px 20px;
            border-bottom: 1px solid var(--ink-faint);
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
        }}

        .section-icon {{
            font-size: 1.5em;
            animation: float 3s ease-in-out infinite;
        }}

        .section-title {{
            font-family: 'Playfair Display', 'Noto Serif SC', serif;
            font-size: 1.3em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .section-rule {{
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, var(--ink) 0%, transparent 100%);
        }}

        .section-grid {{
            display: grid;
            gap: 24px;
        }}

        /* ===== 新闻文章 - 报纸风格 ===== */
        .news-article {{
            display: grid;
            grid-template-columns: 60px 1fr;
            gap: 16px;
            padding: 16px 0;
            border-bottom: 1px dotted var(--ink-faint);
            transition: all 0.3s;
        }}

        .news-article:last-child {{
            border-bottom: none;
        }}

        .news-article:hover {{
            background: rgba(184, 134, 11, 0.05);
            margin: 0 -10px;
            padding: 16px 10px;
            border-radius: 8px;
        }}

        .article-image {{
            display: flex;
            align-items: flex-start;
            justify-content: center;
            padding-top: 4px;
        }}

        .article-meta {{
            font-size: 0.75em;
            color: var(--ink-faint);
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .article-location::after {{
            content: " — ";
        }}

        .article-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.1em;
            font-weight: 600;
            line-height: 1.5;
            margin-bottom: 8px;
            transition: color 0.2s;
        }}

        .news-article:hover .article-title {{
            color: var(--gold);
        }}

        .article-summary {{
            font-size: 0.9em;
            color: var(--ink-light);
            line-height: 1.7;
            margin-bottom: 10px;
        }}

        .article-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }}

        .article-tags {{
            display: flex;
            gap: 6px;
        }}

        .tag {{
            background: var(--paper-dark);
            color: var(--ink-light);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.7em;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s;
            cursor: pointer;
        }}

        .tag:hover {{
            background: var(--gold);
            color: white;
        }}

        /* ===== 魔法展开按钮 ===== */
        .article-expand {{
            background: transparent;
            border: 1px solid var(--gold);
            color: var(--gold);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.75em;
            font-family: 'Noto Serif SC', serif;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .article-expand:hover {{
            background: var(--gold);
            color: white;
            box-shadow: 0 0 15px rgba(184, 134, 11, 0.4);
        }}

        /* ===== 魔法展开内容 ===== */
        .article-full {{
            grid-column: 1 / -1;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.5s ease-out, margin 0.3s;
        }}

        .article-full.open {{
            max-height: 300px;
            margin-top: 16px;
        }}

        .article-full-inner {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(218, 165, 32, 0.05) 100%);
            border-left: 3px solid var(--gold);
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            animation: inkSpread 0.5s ease-out;
        }}

        .article-full-inner p {{
            margin-bottom: 10px;
            color: var(--ink-light);
            font-size: 0.9em;
        }}

        .magic-sign {{
            text-align: right;
            font-style: italic;
            color: var(--gold) !important;
            margin-top: 12px;
        }}

        /* ===== 魔法股票行情 ===== */
        .stocks-section {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 24px 20px;
            border-bottom: 2px solid var(--ink);
        }}

        .stock-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }}

        .stock-table th {{
            text-align: left;
            padding: 10px 8px;
            border-bottom: 2px solid var(--ink);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-size: 0.8em;
        }}

        .stock-table td {{
            padding: 12px 8px;
            border-bottom: 1px solid var(--paper-dark);
        }}

        .stock-table tr:hover {{
            background: rgba(184, 134, 11, 0.05);
        }}

        .stock-code {{
            font-family: 'Courier New', monospace;
            font-weight: 600;
            color: var(--gold);
        }}

        .stock-name {{
            font-weight: 600;
        }}

        .up {{
            color: #b45309;
            font-weight: 700;
        }}

        .recommend {{
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
        }}

        .recommend.buy {{
            background: #dcfce7;
            color: #16a34a;
        }}

        /* ===== 市场情绪魔镜 ===== */
        .mood-section {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 24px 20px;
            border-bottom: 2px solid var(--ink);
        }}

        .mood-mirror {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 50%, #fbbf24 100%);
            border-radius: 20px;
            padding: 24px;
            text-align: center;
            box-shadow: 
                0 0 30px rgba(251, 191, 36, 0.3),
                inset 0 0 30px rgba(255, 255, 255, 0.5);
            animation: magicGlow 3s ease-in-out infinite;
        }}

        .mood-score {{
            font-size: 4em;
            font-weight: 900;
            font-family: 'Playfair Display', serif;
            color: var(--gold);
            text-shadow: 2px 2px 10px rgba(184, 134, 11, 0.3);
            animation: float 4s ease-in-out infinite;
        }}

        .mood-label {{
            font-size: 1.2em;
            color: var(--ink);
            margin-top: 8px;
        }}

        .mood-stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 16px;
            font-size: 0.9em;
            color: var(--ink-light);
        }}

        /* ===== 报纸底部 ===== */
        .newspaper-footer {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 30px 20px;
            text-align: center;
            border-top: 4px double var(--ink);
            font-size: 0.85em;
            color: var(--ink-faint);
        }}

        .newspaper-footer p {{
            margin-bottom: 6px;
        }}

        .magic-quote {{
            font-style: italic;
            color: var(--gold);
            margin-top: 12px;
            font-size: 0.95em;
        }}

        /* ===== 悬浮导航 ===== */
        .floating-nav {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--paper);
            border: 2px solid var(--gold);
            border-radius: 30px;
            padding: 10px 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            z-index: 100;
            display: flex;
            gap: 8px;
        }}

        .nav-item {{
            padding: 8px 14px;
            border-radius: 20px;
            color: var(--ink-light);
            text-decoration: none;
            font-size: 0.8em;
            transition: all 0.2s;
            font-weight: 500;
        }}

        .nav-item:hover, .nav-item.active {{
            background: var(--gold);
            color: white;
        }}

        /* ===== 响应式 ===== */
        @media (max-width: 768px) {{
            .newspaper-title {{
                font-size: 2em;
            }}
            .newspaper-subtitle {{
                font-size: 0.7em;
                letter-spacing: 0.1em;
            }}
            .headline-article {{
                grid-template-columns: 1fr;
                text-align: center;
            }}
            .headline-image {{
                justify-content: center;
            }}
            .news-article {{
                grid-template-columns: 1fr;
            }}
            .article-image {{
                display: none;
            }}
            .floating-nav {{
                padding: 8px 12px;
                gap: 4px;
            }}
            .nav-item {{
                padding: 6px 10px;
                font-size: 0.7em;
            }}
            .article-footer {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            .article-expand {{
                align-self: flex-end;
            }}
        }}

        @media (max-width: 480px) {{
            .floating-nav {{
                bottom: 10px;
                padding: 6px 8px;
            }}
            .nav-item {{
                padding: 5px 8px;
                font-size: 0.65em;
            }}
            .mood-score {{
                font-size: 2.5em;
            }}
            .mood-stats {{
                gap: 20px;
            }}
        }}
    </style>
</head>
<body>
    <!-- 魔法粒子背景 -->
    <div class="magic-particles" id="particles"></div>

    <!-- 报纸刊头 -->
    <header class="newspaper-header">
        <div class="newspaper-masthead">
            <h1 class="newspaper-title">📰 预言家财经日报</h1>
            <p class="newspaper-subtitle">THE DAILY PROPHET FINANCIAL</p>
            <div class="newspaper-meta">
                <span>📅 {self.date_str} {self.weekday}</span>
                <span>🧙 第 {self.issue_no} 期</span>
                <span class="weather-widget">🌤️ 魔法市场晴</span>
                <span>📍 霍格沃茨财经版</span>
            </div>
        </div>
    </header>

    <!-- 头版头条 -->
    <section class="headline-section">
        {headline_html}
    </section>

    <!-- 市场情绪魔镜 -->
    <section class="mood-section">
        <div class="mood-mirror">
            <div class="mood-score">{mood_emoji} {self.mood_score}</div>
            <div class="mood-label">{mood_label}</div>
            <div class="mood-stats">
                <span>📰 {total_news} 条新闻</span>
                <span>🏛️ {len(self.stocks)} 只精选</span>
                <span>🔮 魔法增强版</span>
            </div>
        </div>
    </section>

    <!-- 魔法股票行情 -->
    <section class="stocks-section">
        <div class="section-header">
            <span class="section-icon">📈</span>
            <h2 class="section-title">今日魔法股票</h2>
            <div class="section-rule"></div>
        </div>
        <table class="stock-table">
            <thead>
                <tr>
                    <th>代码</th>
                    <th>名称</th>
                    <th>现价</th>
                    <th>涨跌</th>
                    <th>评级</th>
                </tr>
            </thead>
            <tbody>
                {stocks_html}
            </tbody>
        </table>
    </section>

    <!-- 各板块新闻 -->
    {news_sections_html}

    <!-- 报纸底部 -->
    <footer class="newspaper-footer">
        <p>⚠️ 免责声明：本报由占卜课教授监制，预言仅供参考，不构成投资建议</p>
        <p>📰 预言家财经日报 · 魔法部认证 · 第 {self.issue_no} 期</p>
        <p class="magic-quote">✨ "当你真正想要做一件事的时候，整个宇宙都会联合起来帮你完成" — 保罗·科艾略</p>
    </footer>

    <!-- 悬浮导航 -->
    <nav class="floating-nav">
        <a href="#" class="nav-item active">🏠 首页</a>
        {nav_html}
    </nav>

    <script>
        // 生成魔法粒子
        function createParticles() {{
            const container = document.getElementById('particles');
            for (let i = 0; i < 30; i++) {{
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 3 + 's';
                particle.style.animationDuration = (2 + Math.random() * 2) + 's';
                container.appendChild(particle);
            }}
        }}
        createParticles();

        // 魔法展开新闻
        function toggleMagicNews(newsId, btn) {{
            const content = document.getElementById(newsId);
            content.classList.toggle('open');
            
            if (content.classList.contains('open')) {{
                btn.textContent = '📜 收起';
                // 魔法音效可以在这里加
            }} else {{
                btn.textContent = '✨ 继续阅读';
            }}
        }}

        // 滚动时导航高亮
        const navItems = document.querySelectorAll('.nav-item');
        const sections = document.querySelectorAll('.news-section');

        window.addEventListener('scroll', function() {{
            let current = '';
            sections.forEach(section => {{
                if (window.scrollY >= section.offsetTop - 200) {{
                    current = section.getAttribute('id');
                }}
            }});
            navItems.forEach(item => {{
                item.classList.remove('active');
                if (item.getAttribute('href') === '#' + current) {{
                    item.classList.add('active');
                }}
            }});
        }});

        console.log('✨ 预言家财经日报魔法加载完成！');
        console.log('📰 哈利波特魔法报纸风格');
    </script>
</body>
</html>
"""
        return html

    def save(self):
        os.makedirs(CONFIG["output_dir"], exist_ok=True)
        html = self.generate_html()
        with open(os.path.join(CONFIG["output_dir"], "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ 魔法报纸已保存！")

    async def run(self):
        print("=" * 70)
        print("📰 预言家财经日报 v5.0 (哈利波特魔法报纸风格)")
        print("=" * 70)
        
        self.prepare_news_data()
        self.get_stocks()
        self.save()
        
        print("\n" + "=" * 70)
        print("✨ 魔法报纸生成完成！")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(MagicNewspaper().run())
