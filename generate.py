#!/usr/bin/env python3
"""
📰 预言家财经日报 v5.1
- 严肃黑白报纸风格
- 强化哈利波特元素
- 图片动效升级
"""

import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List

CONFIG = {"output_dir": "./docs"}

NEWS_CATEGORIES = {
    "domestic": {"name": "国内财经", "icon": "🏛️"},
    "international": {"name": "国际要闻", "icon": "🌍"},
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
                    "location": "上海证券交易所",
                    "summary": "今日A股市场延续强势格局，三大指数集体收涨，两市成交额突破1万亿元。北向资金净流入超80亿元，机构持仓比例持续提升，市场信心稳步恢复。",
                    "content": "今日A股市场延续强势格局，三大指数集体收涨。截至收盘，上证指数上涨1.23%，深证成指上涨1.56%，创业板指上涨1.89%。两市成交额突破1万亿元，为连续第8个交易日破万亿。\n\n北向资金全天净流入86.5亿元，其中沪股通净流入48.2亿元，深股通净流入38.3亿元。\n\n行业板块方面，新能源、半导体、医药板块领涨，银行、地产板块表现相对平稳。魔法部分析师认为，随着经济复苏预期增强，市场信心持续恢复，A股有望延续震荡上行走势。",
                    "tags": ["A股", "成交额", "北向资金"],
                    "mood": 0.8,
                    "hot": 92,
                    "image": "📈",
                    "reporter": "丽塔·斯基特"
                },
                {
                    "title": "央行开展500亿元逆回购操作，维护流动性合理充裕",
                    "source": "中国人民银行",
                    "location": "北京",
                    "summary": "央行今日开展500亿元7天期逆回购操作，中标利率维持不变。本周累计净投放2000亿元，维护银行体系流动性合理充裕。",
                    "content": "中国人民银行今日公告称，为维护银行体系流动性合理充裕，开展500亿元7天期逆回购操作，中标利率为1.80%，与此前持平。\n\n本周以来，央行持续加大流动性投放力度，累计开展逆回购操作6500亿元，因到期4500亿元，实现净投放2000亿元。\n\n古灵阁分析师表示，央行灵活开展公开市场操作，有助于平抑短期资金波动，保持市场利率平稳运行。",
                    "tags": ["央行", "逆回购", "流动性"],
                    "mood": 0.75,
                    "hot": 85,
                    "image": "🏦",
                    "reporter": "魔法部财经记者"
                }
            ],
            "international": [
                {
                    "title": "美联储释放鸽派信号，美股三大指数创历史新高",
                    "source": "路透社",
                    "location": "纽约华尔街",
                    "summary": "美联储主席在最新讲话中释放鸽派信号，表示通胀压力正在缓解，市场预期年内将开始降息。美股三大指数应声上涨，集体创出历史新高。",
                    "content": "美联储主席在最新的国会听证会上表示，通胀数据持续向好，美联储正在考虑何时开始降息。市场普遍预期美联储将在9月开始首次降息，年内降息幅度可达75个基点。\n\n受此消息影响，美股三大指数全线上涨。道琼斯工业平均指数上涨1.2%，标准普尔500指数上涨1.5%，纳斯达克综合指数上涨1.8%，三大指数均创出历史新高。\n\n科技股领涨，英伟达、苹果、微软等巨头股价均有不错表现。霍格沃茨投资俱乐部建议投资者保持乐观，但需警惕魔法市场的波动性。",
                    "tags": ["美联储", "美股", "降息"],
                    "mood": 0.85,
                    "hot": 95,
                    "image": "🗽",
                    "reporter": "丽塔·斯基特"
                },
                {
                    "title": "英伟达市值突破3.5万亿美元，AI芯片需求持续火爆",
                    "source": "彭博社",
                    "location": "硅谷",
                    "summary": "英伟达股价持续上涨，市值已突破3.5万亿美元，成为全球市值最高的公司。AI芯片需求呈现爆发式增长，公司订单已排到2027年。",
                    "content": "英伟达股价在盘后交易中继续上涨，市值已突破3.5万亿美元，超越苹果成为全球市值最高的公司。\n\n公司最新财报显示，AI芯片需求呈现爆发式增长，季度营收同比增长280%。公司CEO黄仁勋表示，AI算力需求远超出预期，目前订单已排到2027年，正在全力扩大产能。\n\n魔法部科技司认为，这标志着魔法算力革命的开始。",
                    "tags": ["英伟达", "AI芯片", "市值"],
                    "mood": 0.9,
                    "hot": 98,
                    "image": "🚀",
                    "reporter": "魔法部科技记者"
                }
            ],
            "ai-tech": [
                {
                    "title": "OpenAI发布GPT-4o升级版，多模态能力大幅提升",
                    "source": "魔法部公告",
                    "location": "旧金山",
                    "summary": "OpenAI发布GPT-4o升级版，在推理能力、数学计算、代码生成等方面均有显著提升，响应速度提升50%。新模型支持更长上下文窗口。",
                    "content": "OpenAI正式发布GPT-4o升级版，在多个维度实现显著提升。新模型在MMLU基准测试中得分达到92%，在数学推理方面提升显著。\n\n值得关注的是，GPT-4o响应速度比之前提升50%，用户可以获得更流畅的对话体验。多模态理解能力也大幅增强，支持实时视频分析和复杂图表解读。\n\n此外，新模型支持128K上下文窗口，可以一次性处理约10万字的内容。魔法部将此评为本年度最重要的魔法科技突破。",
                    "tags": ["OpenAI", "GPT-4o", "大模型"],
                    "mood": 0.9,
                    "hot": 98,
                    "image": "🤖",
                    "reporter": "魔法部科技记者"
                }
            ],
            "crypto": [
                {
                    "title": "比特币减半后持续走强，站稳10万美元关口",
                    "source": "CoinDesk",
                    "location": "加密世界",
                    "summary": "比特币第四次减半顺利完成后，价格持续上涨站稳10万美元关口。机构投资者持续增持，市场情绪普遍乐观。",
                    "content": "比特币第四次减半顺利完成后，市场表现强劲。比特币价格持续上涨，已站稳10万美元关口，市值达到2万亿美元。\n\n机构投资者持续增持，灰度比特币信托资产管理规模突破500亿美元，MicroStrategy累计持有超50万枚比特币。\n\n古灵阁分析师认为，随着机构资金持续流入，减半后的供应减少效应将逐步显现，比特币有望继续上行。巫师投资者应保持谨慎乐观。",
                    "tags": ["比特币", "减半", "机构"],
                    "mood": 0.85,
                    "hot": 94,
                    "image": "🪙",
                    "reporter": "古灵阁特派记者"
                }
            ],
            "ev": [
                {
                    "title": "比亚迪月销量突破50万辆，创历史新高",
                    "source": "比亚迪",
                    "location": "深圳",
                    "summary": "比亚迪公布最新销量数据，全系销量达到51.2万辆，再创历史新高。其中海外销量突破10万辆，国际化战略成效显著。",
                    "content": "比亚迪今日公布最新销量数据，7月全系销量达到51.2万辆，再创历史新高，同比增长45%。其中新能源乘用车销量49.8万辆，同比增长48%。\n\n海外市场表现亮眼，当月海外销量突破10万辆，同比增长120%。比亚迪已进入全球60多个国家和地区，在泰国、巴西、澳大利亚等市场市占率持续提升。\n\n霍格沃茨飞行课教授对此表示，这是麻瓜科技追赶魔法飞毯的重要里程碑。",
                    "tags": ["比亚迪", "新能源", "销量"],
                    "mood": 0.85,
                    "hot": 91,
                    "image": "🚗",
                    "reporter": "魔法飞毯专栏"
                },
                {
                    "title": "特斯拉FSD正式入华，自动驾驶行业加速",
                    "source": "特斯拉中国",
                    "location": "上海超级工厂",
                    "summary": "特斯拉FSD完全自动驾驶系统正式获得中国监管部门批准。业内认为这将推动中国自动驾驶行业标准加速成熟。",
                    "content": "特斯拉中国今日宣布，FSD完全自动驾驶系统正式获得中国监管部门批准，将在国内逐步推送。\n\nFSD入华后，特斯拉车主可以通过OTA升级获得完整的自动驾驶能力，包括城市道路自动驾驶、自动泊车、智能召唤等功能。\n\n业内人士认为，FSD入华将加速中国自动驾驶行业标准制定，推动整个产业链快速发展。国内自动驾驶公司也将加速技术迭代，提升竞争力。魔法部交通司将密切关注此事态发展。",
                    "tags": ["特斯拉", "FSD", "自动驾驶"],
                    "mood": 0.8,
                    "hot": 94,
                    "image": "⚡",
                    "reporter": "魔法部交通记者"
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
        current_hour = datetime.now().hour
        print("🎨 正在生成严肃版魔法报纸（黑白严肃 + 哈利波特元素）...")

        # 导航
        nav_html = ""
        for cat_key, cat_info in NEWS_CATEGORIES.items():
            nav_html += f"""
            <a href="#{cat_key}" class="nav-item" data-category="{cat_key}">
                {cat_info['icon']} {cat_info['name']}
            </a>
            """

        # 头版头条（第一条国际新闻）
        top_news = self.all_news["international"][0]
        
        # 头版头条 HTML
        headline_html = f"""
        <article class="frontpage-article">
            <div class="frontpage-image">
                <div class="moving-photo">
                    <span class="photo-emoji">{top_news['image']}</span>
                    <div class="photo-shimmer"></div>
                </div>
                <div class="photo-caption">
                    <span>📷 本报特派记者摄于{top_news['location']}</span>
                </div>
            </div>
            <div class="frontpage-content">
                <div class="article-dateline">{top_news['location']} — {current_hour}:{datetime.now().minute:02d} GMT+8</div>
                <h1 class="frontpage-headline">{top_news['title']}</h1>
                <p class="frontpage-byline">By {top_news['reporter']} · {top_news['source']}</p>
                <div class="frontpage-lead">{top_news['summary']}</div>
                <button class="continue-article-btn" onclick="openMagicArticle('frontpage', this)">
                    ▶ 继续阅读第2版
                </button>
            </div>
            <div class="frontpage-full" id="frontpage">
                <div class="article-continued">
                    <div class="continued-header">— 从第1版续 —</div>
                    {top_news['content'].replace(chr(10), '<br><br>')}
                    <p class="article-end">❧</p>
                </div>
            </div>
        </article>
        """

        # 第二条要闻
        second_news = self.all_news["international"][1]
        second_headline_html = f"""
        <article class="second-article">
            <div class="second-image">
                <div class="moving-photo-small">
                    <span class="photo-emoji">{second_news['image']}</span>
                </div>
            </div>
            <div class="second-content">
                <div class="second-dateline">{second_news['location']}</div>
                <h2 class="second-headline">{second_news['title']}</h2>
                <p class="second-byline">By {second_news['reporter']}</p>
                <p class="second-lead">{second_news['summary']}</p>
            </div>
        </article>
        """

        # 新闻板块 - 报纸分栏风格
        news_sections_html = ""
        for cat_key, cat_info in NEWS_CATEGORIES.items():
            if cat_key == "international": continue  # 国际新闻已经在头版了
                
            news_list = self.all_news.get(cat_key, [])
            if not news_list:
                continue
                
            news_cards_html = ""
            for idx, news in enumerate(news_list):
                news_id = f"news-{cat_key}-{idx}"
                tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in news["tags"]])
                
                news_cards_html += f"""
                <article class="news-item" data-newsid="{news_id}">
                    <div class="news-item-image">
                        <div class="tiny-photo">
                            <span class="tiny-emoji">{news['image']}</span>
                        </div>
                    </div>
                    <div class="news-item-content">
                        <div class="news-item-meta">
                            <span class="news-item-location">{news['location']}</span>
                            <span class="news-item-source"> | {news['source']}</span>
                            <span class="news-item-reporter"> · By {news['reporter']}</span>
                        </div>
                        <h3 class="news-item-title">{news['title']}</h3>
                        <p class="news-item-summary">{news['summary']}</p>
                        <div class="news-item-footer">
                            <div class="news-item-tags">{tags_html}</div>
                            <button class="read-more-btn" onclick="toggleMagicNews('{news_id}', this)">
                                [ 继续阅读 ]
                            </button>
                        </div>
                    </div>
                    <div class="news-item-full" id="{news_id}">
                        <div class="news-item-full-inner">
                            {news['content'].replace(chr(10), '<br><br>')}
                            <p class="article-end">❧</p>
                        </div>
                    </div>
                </article>
                """

            news_sections_html += f"""
            <section id="{cat_key}" class="news-section">
                <div class="section-head">
                    <span class="section-icon">{cat_info['icon']}</span>
                    <h2 class="section-title">{cat_info['name']}</h2>
                    <div class="section-rules"></div>
                </div>
                {news_cards_html}
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
    <title>📰 预言家日报 · 财经版</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700;900&family=Playfair+Display:wght@400;700;900&family=UnifrakturMaguntia&display=swap" rel="stylesheet">
    <style>
        /* ===== 严肃魔法报纸 - 黑白风格 ===== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --paper: #f8f5ee;
            --paper-dark: #e8e4db;
            --ink: #1a1a1a;
            --ink-light: #4a4a4a;
            --ink-faint: #8a8a8a;
            --accent: #2563eb;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-4px); }}
        }}

        @keyframes shimmer {{
            0% {{ opacity: 0.4; }}
            50% {{ opacity: 0.8; }}
            100% {{ opacity: 0.4; }}
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 0.6; }}
            50% {{ opacity: 1; }}
        }}

        body {{
            font-family: 'Noto Serif SC', Georgia, 'Times New Roman', serif;
            background: var(--paper);
            background-image: 
                url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
            color: var(--ink);
            line-height: 1.65;
            font-size: 16px;
        }}

        /* ===== 报纸刊头 - 预言家日报风格 ===== */
        .masthead {{
            background: var(--paper);
            border-bottom: 3px double var(--ink);
            padding: 28px 20px 20px;
            position: relative;
        }}

        .masthead-inner {{
            max-width: 1000px;
            margin: 0 auto;
            text-align: center;
            position: relative;
        }}

        /* 预言家日报装饰元素 */
        .masthead::before {{
            content: "❧";
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 2em;
            color: var(--ink-light);
        }}

        .masthead::after {{
            content: "❧";
            position: absolute;
            right: 20px;
            top: 50%;
            font-size: 2em;
            color: var(--ink-light);
        }}

        .paper-title {{
            font-family: 'Playfair Display', 'Noto Serif SC', serif;
            font-size: 3.8em;
            font-weight: 900;
            letter-spacing: 0.15em;
            margin-bottom: 4px;
            animation: float 5s ease-in-out infinite;
        }}

        .paper-subtitle {{
            font-size: 0.75em;
            color: var(--ink-light);
            letter-spacing: 0.5em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }}

        .paper-edition {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid var(--ink);
            border-bottom: 1px solid var(--ink);
            padding: 6px 0;
            font-size: 0.85em;
            color: var(--ink);
        }}

        .edition-price {{
            font-weight: 600;
        }}

        /* ===== 头版头条 ===== */
        .frontpage {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 24px 20px;
            border-bottom: 2px solid var(--ink);
        }}

        .frontpage-article {{
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }}

        /* ===== 会动的照片 - 哈利波特风格 ===== */
        .moving-photo {{
            position: relative;
            border: 8px solid #2a2a2a;
            border-radius: 2px;
            padding: 10px;
            background: linear-gradient(145deg, #f0f0f0, #ffffff);
            box-shadow: 
                4px 4px 12px rgba(0,0,0,0.15),
                inset 0 0 20px rgba(0,0,0,0.05);
        }}

        .photo-emoji {{
            font-size: 6em;
            display: block;
            text-align: center;
            animation: float 3s ease-in-out infinite;
        }}

        .photo-shimmer {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(
                110deg,
                transparent 20%,
                rgba(255,255,255,0.3) 45%,
                rgba(255,255,255,0.5) 50%,
                rgba(255,255,255,0.3) 55%,
                transparent 80%
            );
            animation: shimmer 4s ease-in-out infinite;
            pointer-events: none;
        }}

        .photo-caption {{
            font-size: 0.7em;
            color: var(--ink-faint);
            text-align: center;
            margin-top: 8px;
            font-style: italic;
        }}

        .moving-photo-small {{
            position: relative;
            border: 5px solid #2a2a2a;
            padding: 8px;
            background: white;
        }}

        .moving-photo-small .photo-emoji {{
            font-size: 3.5em;
        }}

        .tiny-photo {{
            position: relative;
            border: 3px solid #2a2a2a;
            padding: 5px;
            background: white;
        }}

        .tiny-emoji {{
            font-size: 2.2em;
            display: block;
            animation: float 3.5s ease-in-out infinite;
        }}

        /* ===== 头版内容 ===== */
        .article-dateline {{
            font-size: 0.75em;
            color: var(--ink-faint);
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 8px;
            font-family: 'Inter', sans-serif;
        }}

        .frontpage-headline {{
            font-family: 'Playfair Display', 'Noto Serif SC', serif;
            font-size: 1.7em;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 8px;
        }}

        .frontpage-byline {{
            font-size: 0.8em;
            color: var(--ink-light);
            font-style: italic;
            margin-bottom: 12px;
        }}

        .frontpage-lead {{
            font-size: 1em;
            line-height: 1.8;
            color: var(--ink);
        }}

        .continue-article-btn {{
            background: transparent;
            border: 1px solid var(--ink);
            color: var(--ink);
            padding: 6px 16px;
            font-family: 'Noto Serif SC', serif;
            font-size: 0.8em;
            cursor: pointer;
            margin-top: 12px;
            transition: all 0.2s;
        }}

        .continue-article-btn:hover {{
            background: var(--ink);
            color: var(--paper);
        }}

        /* ===== 文章展开 ===== */
        .frontpage-full {{
            grid-column: 1 / -1;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.6s ease-out;
        }}

        .frontpage-full.open {{
            max-height: 800px;
            margin-top: 20px;
        }}

        .article-continued {{
            border-top: 1px solid var(--ink-faint);
            padding-top: 16px;
        }}

        .continued-header {{
            text-align: center;
            font-size: 0.8em;
            color: var(--ink-faint);
            margin-bottom: 12px;
        }}

        .article-end {{
            text-align: center;
            font-size: 1.5em;
            color: var(--ink-faint);
            margin-top: 16px;
        }}

        /* ===== 第二条要闻 ===== */
        .second-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            padding-top: 20px;
            border-top: 1px solid var(--ink-faint);
        }}

        .second-article {{
            display: grid;
            grid-template-columns: 100px 1fr;
            gap: 16px;
        }}

        .second-headline {{
            font-family: 'Playfair Display', 'Noto Serif SC', serif;
            font-size: 1.15em;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 6px;
        }}

        .second-dateline {{
            font-size: 0.7em;
            color: var(--ink-faint);
            text-transform: uppercase;
        }}

        .second-byline {{
            font-size: 0.75em;
            color: var(--ink-faint);
            font-style: italic;
            margin-bottom: 6px;
        }}

        .second-lead {{
            font-size: 0.85em;
            line-height: 1.6;
            color: var(--ink-light);
        }}

        /* ===== 行情板块 ===== */
        .markets-section {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 24px 20px;
            border-bottom: 2px solid var(--ink);
        }}

        .markets-title {{
            font-family: 'Playfair Display', 'Noto Serif SC', serif;
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .market-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95em;
        }}

        .market-table th {{
            text-align: left;
            padding: 10px 8px;
            border-bottom: 2px solid var(--ink);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-size: 0.75em;
        }}

        .market-table td {{
            padding: 12px 8px;
            border-bottom: 1px solid var(--paper-dark);
        }}

        .market-table tr:hover {{
            background: rgba(0,0,0,0.03);
        }}

        .stock-code {{
            font-family: 'Courier New', monospace;
            font-weight: 600;
            color: var(--ink);
        }}

        .stock-name {{
            font-weight: 600;
        }}

        .up {{
            color: #92400e;
            font-weight: 700;
        }}

        .recommend {{
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            border: 1px solid currentColor;
        }}

        .recommend.buy {{
            color: #16a34a;
            background: #f0fdf4;
        }}

        /* ===== 市场情绪魔镜 ===== */
        .mood-section {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 24px 20px;
            border-bottom: 2px solid var(--ink);
        }}

        .mood-box {{
            border: 2px solid var(--ink);
            padding: 20px;
            text-align: center;
            position: relative;
        }}

        .mood-box::before {{
            content: "✦";
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--paper);
            padding: 0 10px;
            font-size: 1.2em;
            animation: pulse 2s ease-in-out infinite;
        }}

        .mood-score {{
            font-family: 'Playfair Display', serif;
            font-size: 3em;
            font-weight: 900;
            animation: float 4s ease-in-out infinite;
        }}

        .mood-label {{
            font-size: 1em;
            margin-top: 4px;
        }}

        .mood-stats {{
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 16px;
            font-size: 0.85em;
            color: var(--ink-light);
        }}

        /* ===== 新闻板块 ===== */
        .news-section {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 24px 20px;
            border-bottom: 1px solid var(--ink-faint);
        }}

        .section-head {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--ink);
        }}

        .section-icon {{
            font-size: 1.3em;
            animation: float 3s ease-in-out infinite;
        }}

        .section-title {{
            font-family: 'Playfair Display', 'Noto Serif SC', serif;
            font-size: 1.1em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        .section-rules {{
            flex: 1;
            height: 3px;
            background: repeating-linear-gradient(
                90deg,
                var(--ink) 0px,
                var(--ink) 8px,
                transparent 8px,
                transparent 12px
            );
        }}

        .news-item {{
            display: grid;
            grid-template-columns: 70px 1fr;
            gap: 16px;
            padding: 16px 0;
            border-bottom: 1px dotted var(--paper-dark);
        }}

        .news-item:last-child {{
            border-bottom: none;
        }}

        .news-item-meta {{
            font-size: 0.7em;
            color: var(--ink-faint);
            margin-bottom: 6px;
        }}

        .news-item-title {{
            font-size: 1.05em;
            font-weight: 600;
            line-height: 1.5;
            margin-bottom: 6px;
            transition: color 0.2s;
        }}

        .news-item:hover .news-item-title {{
            color: var(--accent);
        }}

        .news-item-summary {{
            font-size: 0.85em;
            color: var(--ink-light);
            line-height: 1.7;
            margin-bottom: 8px;
        }}

        .news-item-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }}

        .news-item-tags {{
            display: flex;
            gap: 6px;
        }}

        .tag {{
            background: var(--paper-dark);
            color: var(--ink-light);
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.7em;
            font-family: 'Inter', sans-serif;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .tag:hover {{
            background: var(--ink);
            color: var(--paper);
        }}

        .read-more-btn {{
            background: transparent;
            border: none;
            color: var(--accent);
            font-family: 'Noto Serif SC', serif;
            font-size: 0.75em;
            cursor: pointer;
            padding: 4px 0;
        }}

        .read-more-btn:hover {{
            text-decoration: underline;
        }}

        /* ===== 新闻展开 ===== */
        .news-item-full {{
            grid-column: 1 / -1;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.5s ease-out;
        }}

        .news-item-full.open {{
            max-height: 600px;
            margin-top: 12px;
        }}

        .news-item-full-inner {{
            border-left: 2px solid var(--ink-faint);
            padding: 12px 16px;
            font-size: 0.9em;
            color: var(--ink-light);
            line-height: 1.8;
        }}

        /* ===== 页脚 - 预言家日报风格 ===== */
        .footer {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 30px 20px;
            text-align: center;
            border-top: 3px double var(--ink);
            font-size: 0.8em;
            color: var(--ink-faint);
        }}

        .footer p {{
            margin-bottom: 6px;
        }}

        .footer-quote {{
            font-style: italic;
            margin-top: 12px;
            color: var(--ink-light);
            font-size: 0.95em;
        }}

        .footer-quote::before {{
            content: '"';
        }}

        .footer-quote::after {{
            content: '"';
        }}

        /* ===== 悬浮导航 ===== */
        .floating-nav {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--paper);
            border: 2px solid var(--ink);
            border-radius: 2px;
            padding: 8px 16px;
            box-shadow: 4px 4px 0 rgba(0,0,0,0.1);
            z-index: 100;
            display: flex;
            gap: 6px;
        }}

        .nav-item {{
            padding: 6px 12px;
            color: var(--ink-light);
            text-decoration: none;
            font-size: 0.75em;
            transition: all 0.2s;
            font-weight: 500;
        }}

        .nav-item:hover, .nav-item.active {{
            background: var(--ink);
            color: var(--paper);
        }}

        /* ===== 响应式 ===== */
        @media (max-width: 768px) {{
            .paper-title {{
                font-size: 2.2em;
            }}
            .paper-subtitle {{
                font-size: 0.6em;
                letter-spacing: 0.2em;
            }}
            .frontpage-article {{
                grid-template-columns: 1fr;
            }}
            .moving-photo {{
                max-width: 200px;
                margin: 0 auto 16px;
            }}
            .second-row {{
                grid-template-columns: 1fr;
            }}
            .news-item {{
                grid-template-columns: 1fr;
            }}
            .news-item-image {{
                display: none;
            }}
            .floating-nav {{
                padding: 6px 10px;
                gap: 4px;
                bottom: 10px;
            }}
            .nav-item {{
                padding: 5px 8px;
                font-size: 0.65em;
            }}
            .masthead::before,
            .masthead::after {{
                display: none;
            }}
        }}

        @media (max-width: 480px) {{
            .paper-title {{
                font-size: 1.8em;
            }}
            .paper-edition {{
                flex-direction: column;
                gap: 4px;
                font-size: 0.75em;
            }}
            .mood-score {{
                font-size: 2em;
            }}
            .mood-stats {{
                gap: 20px;
                flex-wrap: wrap;
            }}
            .frontpage-headline {{
                font-size: 1.3em;
            }}
        }}

        @media print {{
            .floating-nav {{
                display: none;
            }}
        }}
    </style>
</head>
<body><div class="newspaper-container">
    <!-- 报纸刊头 - 预言家日报风格 -->
    <header class="masthead">
        <div class="masthead-inner">
            <h1 class="paper-title">预言家日报</h1>
            <p class="paper-subtitle">THE DAILY PROPHET · FINANCIAL EDITION</p>
            <div class="paper-edition">
                <span>📅 {self.date_str} {self.weekday}</span>
                <span>🧙 第 {self.issue_no} 期</span>
                <span>🌡️ 今日宜投资</span>
                <span class="edition-price">💰 售价：5 西可</span>
                <span>📍 霍格沃茨出版社</span>
            </div>
        </div>
    </header>

    <!-- 头版头条 -->
    <section class="frontpage">
        {headline_html}
        <div class="second-row">
            {second_headline_html}
            <div style="border-left: 1px solid var(--paper-dark); padding-left: 24px;">
                <div style="font-size: 0.9em; font-weight: 600; margin-bottom: 8px;">📜 魔法部每日提示</div>
                <p style="font-size: 0.8em; color: var(--ink-light); line-height: 1.7;">
                    🔮 市场有风险，投资需谨慎。魔法部投资保护投资者保护投资者保护<br>
                    📜 本报内容仅供参考，不构成施法建议<br>
                    ⚡ 如遇市场波动，请保持镇定，勿慌张施法
                </p>
            </div>
        </div>
    </section>

    <!-- 市场情绪魔镜 -->
    <section class="mood-section">
        <div class="mood-box">
            <div class="mood-score">{mood_emoji} {self.mood_score}</div>
            <div class="mood-label">今日市场情绪：{mood_label}</div>
            <div class="mood-stats">
                <span>📰 {total_news} 条要闻</span>
                <span>📈 {len(self.stocks)} 只精选</span>
                <span>🔮 魔法增强版</span>
            </div>
        </div>
    </section>

    <!-- 魔法股票行情 -->
    <section class="markets-section">
        <div class="markets-title">
            <span>📈</span>
            <span>今日魔法市场行情</span>
        </div>
        <table class="market-table">
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

    <!-- 页脚 -->
    <footer class="footer">
        <p>📦 版本 v5.2 · 最后魔法更新：{self.date_str} {datetime.now().strftime('%H:%M')}</p>
        <p>魔法部出版署批准 · 统一刊号：HGW-1991-777</p>
        <p>本报由猫头鹰投递 · 古灵阁担保发行</p>
        <p>© {self.date.year} 预言家日报社 保留所有权利</p>
        <p class="footer-quote">不要怜悯死者，哈利。怜悯活着的人，最重要的是，怜悯那些生活中没有爱的人</p>
        <p style="margin-top: 4px;">— 阿不思·邓布利多</p>
    </footer>

    <!-- 悬浮导航 -->
    <nav class="floating-nav">
        <a href="#" class="nav-item active">🏠 第1版</a>
        {nav_html}
    </nav>

    </div><script>
        // 头版文章展开
        function openMagicArticle(newsId, btn) {{
            const content = document.getElementById(newsId);
            content.classList.toggle('open');
            
            if (content.classList.contains('open')) {{
                btn.textContent = '▲ 收起';
            }} else {{
                btn.textContent = '▶ 继续阅读第2版';
            }}
        }}

        // 新闻展开/收起
        function toggleMagicNews(newsId, btn) {{
            const content = document.getElementById(newsId);
            content.classList.toggle('open');
            
            if (content.classList.contains('open')) {{
                btn.textContent = '[ 收起 ]';
            }} else {{
                btn.textContent = '[ 继续阅读 ]';
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

        console.log('📰 预言家日报严肃版已加载完成');
        console.log('🧙 哈利波特魔法报纸风格 · 黑白严肃版');
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
        print("✅ 严肃版魔法报纸已保存！")

    async def run(self):
        print("=" * 70)
        print("📰 预言家日报 v5.1 (严肃黑白版 + 更多哈利波特元素)")
        print("=" * 70)
        
        self.prepare_news_data()
        self.get_stocks()
        self.save()
        
        print("\n" + "=" * 70)
        print("🧙 严肃魔法报纸生成完成！")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(MagicNewspaper().run())
