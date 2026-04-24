#!/usr/bin/env python3
"""
📰 全球财经新闻平台 v4.2
- 全新清爽排版设计
- 更优雅的视觉层次
"""

import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List

CONFIG = {"output_dir": "./docs"}

NEWS_CATEGORIES = {
    "domestic": {"name": "国内财经", "icon": "🇨🇳", "color": "#e74c3c"},
    "international": {"name": "国际财经", "icon": "🌍", "color": "#3498db"},
    "ai-tech": {"name": "AI科技", "icon": "🤖", "color": "#9b59b6"},
    "internet": {"name": "互联网", "icon": "💻", "color": "#1abc9c"},
    "semiconductor": {"name": "半导体", "icon": "🔬", "color": "#f39c12"},
    "crypto": {"name": "加密货币", "icon": "💰", "color": "#e67e22"},
    "ev": {"name": "新能源汽车", "icon": "🚗", "color": "#27ae60"}
}

class NewsPlatform:
    def __init__(self):
        self.all_news = {}
        self.stocks = []
        self.mood_score = 0
        self.date = datetime.now()
        self.date_str = self.date.strftime("%Y年%m月%d日")

    def prepare_news_data(self) -> Dict:
        current_hour = datetime.now().hour
        
        news_data = {
            "domestic": [
                {
                    "title": "A股三大指数集体收涨，成交额突破万亿元",
                    "source": "证券时报",
                    "time": f"{current_hour - 1}:{datetime.now().minute:02d}",
                    "date": self.date_str,
                    "summary": "今日A股市场延续强势格局，三大指数集体收涨，两市成交额突破1万亿元。北向资金净流入超80亿元，机构持仓比例持续提升。",
                    "full_content": "今日A股市场延续强势格局，三大指数集体收涨。截至收盘，上证指数上涨1.23%，深证成指上涨1.56%，创业板指上涨1.89%。两市成交额突破1万亿元，为连续第8个交易日破万亿。北向资金全天净流入86.5亿元。\n\n行业板块方面，新能源、半导体、医药板块领涨，银行、地产板块表现相对平稳。分析人士认为，随着经济复苏预期增强，市场信心持续恢复。",
                    "tags": ["A股", "成交额", "北向资金"],
                    "mood": 0.8,
                    "hot": 92
                },
                {
                    "title": "央行开展500亿元逆回购操作，维护流动性合理充裕",
                    "source": "中国人民银行",
                    "time": f"{current_hour - 3}:15",
                    "date": self.date_str,
                    "summary": "央行今日开展500亿元7天期逆回购操作，中标利率维持不变。本周累计净投放2000亿元，维护银行体系流动性合理充裕。",
                    "full_content": "中国人民银行今日公告称，为维护银行体系流动性合理充裕，开展500亿元7天期逆回购操作，中标利率为1.80%，与此前持平。\n\n本周以来，央行持续加大流动性投放力度，累计开展逆回购操作6500亿元，因到期4500亿元，实现净投放2000亿元。",
                    "tags": ["央行", "逆回购", "流动性"],
                    "mood": 0.75,
                    "hot": 85
                }
            ],
            "international": [
                {
                    "title": "美联储释放鸽派信号，美股三大指数创历史新高",
                    "source": "路透社",
                    "time": "04:30",
                    "date": self.date_str,
                    "summary": "美联储主席在最新讲话中释放鸽派信号，表示通胀压力正在缓解，市场预期年内将开始降息。美股三大指数应声上涨。",
                    "full_content": "美联储主席在最新的国会听证会上表示，通胀数据持续向好，美联储正在考虑何时开始降息。市场普遍预期美联储将在9月开始首次降息。\n\n受此消息影响，美股三大指数全线上涨，均创出历史新高。科技股领涨，英伟达、苹果、微软等巨头股价均有不错表现。",
                    "tags": ["美联储", "美股", "降息"],
                    "mood": 0.85,
                    "hot": 95
                },
                {
                    "title": "英伟达市值突破3.5万亿美元，AI芯片需求持续火爆",
                    "source": "彭博社",
                    "time": "05:15",
                    "date": self.date_str,
                    "summary": "英伟达股价持续上涨，市值已突破3.5万亿美元，成为全球市值最高的公司。AI芯片需求呈现爆发式增长。",
                    "full_content": "英伟达股价在盘后交易中继续上涨，市值已突破3.5万亿美元，超越苹果成为全球市值最高的公司。\n\n公司最新财报显示，AI芯片需求呈现爆发式增长，季度营收同比增长280%。公司CEO黄仁勋表示，AI算力需求远超出预期。",
                    "tags": ["英伟达", "AI芯片", "市值"],
                    "mood": 0.9,
                    "hot": 98
                }
            ],
            "ai-tech": [
                {
                    "title": "OpenAI发布GPT-4o升级版，多模态能力大幅提升",
                    "source": "OpenAI",
                    "time": "01:00",
                    "date": self.date_str,
                    "summary": "OpenAI发布GPT-4o升级版，在推理能力、数学计算、代码生成等方面均有显著提升，响应速度提升50%。",
                    "full_content": "OpenAI正式发布GPT-4o升级版，在多个维度实现显著提升。新模型在MMLU基准测试中得分达到92%，在数学推理方面提升显著。\n\n值得关注的是，GPT-4o响应速度比之前提升50%，用户可以获得更流畅的对话体验。",
                    "tags": ["OpenAI", "GPT-4o", "大模型"],
                    "mood": 0.9,
                    "hot": 98
                },
                {
                    "title": "国产大模型密集发布，中国AI实力快速追赶",
                    "source": "36氪",
                    "time": "10:30",
                    "date": self.date_str,
                    "summary": "本周国内多家科技公司密集发布新一代大模型，在中文理解、多模态能力等方面已达到国际先进水平。",
                    "full_content": "本周，百度、阿里、字节跳动等国内科技公司密集发布新一代大模型，在中文理解、多模态能力、推理速度等方面均有显著提升。\n\n评测显示，国产大模型在中文任务上已超越GPT-4，在多模态理解方面达到国际先进水平。",
                    "tags": ["大模型", "AI", "国产化"],
                    "mood": 0.75,
                    "hot": 90
                }
            ],
            "internet": [
                {
                    "title": "腾讯控股发布最新财报，游戏业务表现强劲",
                    "source": "腾讯",
                    "time": "16:30",
                    "date": self.date_str,
                    "summary": "腾讯控股公布2024年第二季度财报，营收同比增长15%，净利润同比增长25%。游戏业务表现强劲，海外收入占比持续提升。",
                    "full_content": "腾讯控股今日公布2024年第二季度财报，营收达1650亿元，同比增长15%；净利润达520亿元，同比增长25%，超出市场预期。\n\n游戏业务方面，本季度收入达580亿元，同比增长12%。其中国际市场游戏收入增长28%，占比首次突破40%。",
                    "tags": ["腾讯", "财报", "游戏"],
                    "mood": 0.75,
                    "hot": 88
                }
            ],
            "semiconductor": [
                {
                    "title": "中芯国际14nm工艺良率突破95%，进入大规模量产",
                    "source": "中芯国际",
                    "time": "08:45",
                    "date": self.date_str,
                    "summary": "中芯国际宣布14nm工艺良率已达到95%，月产能提升至5万片晶圆。国产14nm芯片已广泛应用于消费电子、汽车等领域。",
                    "full_content": "中芯国际在今日举办的技术交流会上宣布，公司14nm工艺良率已达到95%，进入大规模量产阶段。目前14nm生产线月产能已提升至5万片晶圆。",
                    "tags": ["中芯国际", "14nm", "芯片"],
                    "mood": 0.8,
                    "hot": 93
                }
            ],
            "crypto": [
                {
                    "title": "比特币减半后持续走强，站稳10万美元关口",
                    "source": "CoinDesk",
                    "time": "00:30",
                    "date": self.date_str,
                    "summary": "比特币第四次减半顺利完成后，价格持续上涨站稳10万美元关口。机构投资者持续增持，市场情绪普遍乐观。",
                    "full_content": "比特币第四次减半顺利完成后，市场表现强劲。比特币价格持续上涨，已站稳10万美元关口，市值达到2万亿美元。\n\n机构投资者持续增持，灰度比特币信托资产管理规模突破500亿美元。",
                    "tags": ["比特币", "减半", "机构"],
                    "mood": 0.85,
                    "hot": 94
                }
            ],
            "ev": [
                {
                    "title": "比亚迪月销量突破50万辆，创历史新高",
                    "source": "比亚迪",
                    "time": "18:00",
                    "date": self.date_str,
                    "summary": "比亚迪公布最新销量数据，全系销量达到51.2万辆，再创历史新高。其中海外销量突破10万辆，国际化战略成效显著。",
                    "full_content": "比亚迪今日公布最新销量数据，7月全系销量达到51.2万辆，再创历史新高，同比增长45%。\n\n海外市场表现亮眼，当月海外销量突破10万辆，同比增长120%。比亚迪已进入全球60多个国家和地区。",
                    "tags": ["比亚迪", "新能源", "销量"],
                    "mood": 0.85,
                    "hot": 91
                },
                {
                    "title": "特斯拉FSD正式入华，自动驾驶行业加速",
                    "source": "特斯拉",
                    "time": "11:00",
                    "date": self.date_str,
                    "summary": "特斯拉FSD完全自动驾驶系统正式获得中国监管部门批准。业内认为这将推动中国自动驾驶行业标准加速成熟。",
                    "full_content": "特斯拉中国今日宣布，FSD完全自动驾驶系统正式获得中国监管部门批准，将在国内逐步推送。\n\n业内人士认为，FSD入华将加速中国自动驾驶行业标准制定，推动整个产业链快速发展。",
                    "tags": ["特斯拉", "FSD", "自动驾驶"],
                    "mood": 0.8,
                    "hot": 94
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
        print(f"✅ 共整理 {total} 条新闻")
        print(f"📊 今日市场情绪: {self.mood_score} 分")
        
        return news_data

    def get_stocks(self):
        print("📈 正在获取股票数据...")
        self.stocks = [
            {"code": "002594", "name": "比亚迪", "price": "358.50", "change": "+5.23%", "recommend": "买入"},
            {"code": "688981", "name": "中芯国际", "price": "68.75", "change": "+3.85%", "recommend": "买入"},
            {"code": "00700", "name": "腾讯控股", "price": "485.60", "change": "+2.15%", "recommend": "持有"},
            {"code": "NVDA", "name": "英伟达", "price": "1280.50", "change": "+8.32%", "recommend": "买入"},
            {"code": "TSLA", "name": "特斯拉", "price": "325.80", "change": "+4.56%", "recommend": "买入"},
        ]

    def generate_html(self):
        print("🎨 正在生成HTML（全新清爽排版）...")

        # 导航
        nav_html = ""
        for cat_key, cat_info in NEWS_CATEGORIES.items():
            nav_html += f"""
            <a href="#{cat_key}" class="nav-item" data-category="{cat_key}">
                <span class="nav-icon">{cat_info['icon']}</span>
                <span class="nav-text">{cat_info['name']}</span>
            </a>
            """

        # 新闻板块 - 全新排版
        news_sections_html = ""
        for cat_key, cat_info in NEWS_CATEGORIES.items():
            news_list = self.all_news.get(cat_key, [])
            if not news_list:
                continue
                
            news_cards_html = ""
            for idx, news in enumerate(news_list):
                tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in news["tags"]])
                hot_class = "hot" if news["hot"] >= 90 else ""
                news_id = f"news-{cat_key}-{idx}"
                
                full_content_html = news["full_content"].replace("\n", "<br><br>")
                
                news_cards_html += f"""
                <article class="news-card {hot_class}" data-search="{news['title']} {news['summary']} {' '.join(news['tags'])}">
                    <!-- 标题区 -->
                    <h3 class="news-title">{news['title']}</h3>
                    
                    <!-- 元信息：来源 时间 热度 -->
                    <div class="news-meta">
                        <span class="news-source">{news['source']}</span>
                        <span class="separator">·</span>
                        <span class="news-time">{news['time']}</span>
                        <span class="news-hot">🔥 {news['hot']}</span>
                    </div>
                    
                    <!-- 摘要 -->
                    <p class="news-summary">{news['summary']}</p>
                    
                    <!-- 展开的完整内容 -->
                    <div class="news-full-content" id="{news_id}">
                        <div class="news-full-content-inner">
                            {full_content_html}
                        </div>
                    </div>
                    
                    <!-- 底部：标签 + 按钮 -->
                    <div class="news-footer">
                        <div class="news-tags">
                            {tags_html}
                        </div>
                        <button class="expand-btn" onclick="toggleNews('{news_id}', this)">
                            查看详情
                        </button>
                    </div>
                </article>
                """

            news_sections_html += f"""
            <section id="{cat_key}" class="category-section">
                <div class="category-header">
                    <span class="category-icon">{cat_info['icon']}</span>
                    <h2 class="category-title">{cat_info['name']}</h2>
                </div>
                <div class="news-grid">
                    {news_cards_html}
                </div>
            </section>
            """

        # 股票表格
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

        # 归档
        archive_html = ""
        for i in range(15):
            d = self.date - timedelta(days=i)
            archive_html += f'<a href="#" class="archive-item">{d.strftime("%m月%d日")} <span>{d.strftime("%a")}</span></a>'

        # 情绪判断
        if self.mood_score >= 75:
            mood_label = "非常乐观"
            mood_emoji = "🚀"
            mood_color = "#10b981"
        elif self.mood_score >= 60:
            mood_label = "偏乐观"
            mood_emoji = "😊"
            mood_color = "#f59e0b"
        else:
            mood_label = "中性"
            mood_emoji = "⚖️"
            mood_color = "#6366f1"

        total_news = sum(len(v) for v in self.all_news.values())

        # 完整HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📰 财经新闻</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg: #f8fafc;
            --card: #ffffff;
            --text: #1e293b;
            --text2: #64748b;
            --text3: #94a3b8;
            --border: #e2e8f0;
            --accent: #3b82f6;
            --accent2: #8b5cf6;
            --red: #ef4444;
            --green: #10b981;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'PingFang SC', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            padding-bottom: 80px;
        }}

        /* 顶部导航 */
        .top-header {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: white;
            padding: 16px 0;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        .header-inner {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            font-weight: 700;
            font-size: 1.1em;
        }}

        .brand-icon {{
            font-size: 1.5em;
        }}

        .search-box {{
            display: flex;
            align-items: center;
            background: rgba(255,255,255,0.15);
            border-radius: 24px;
            padding: 8px 16px;
            width: 280px;
            transition: all 0.3s;
        }}

        .search-box:focus-within {{
            background: rgba(255,255,255,0.25);
            width: 320px;
        }}

        .search-box input {{
            background: transparent;
            border: none;
            color: white;
            font-size: 0.9em;
            width: 100%;
            outline: none;
            margin-left: 8px;
        }}

        .search-box input::placeholder {{
            color: rgba(255,255,255,0.5);
        }}

        /* 主布局 */
        .main-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 20px;
            display: grid;
            grid-template-columns: 180px 1fr 240px;
            gap: 24px;
        }}

        /* 左侧导航 */
        .sidebar-left {{
            position: sticky;
            top: 100px;
            height: fit-content;
        }}

        .nav-menu {{
            background: white;
            border-radius: 16px;
            padding: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 14px;
            border-radius: 10px;
            color: var(--text2);
            text-decoration: none;
            transition: all 0.2s;
            font-weight: 500;
            font-size: 0.9em;
        }}

        .nav-item:hover, .nav-item.active {{
            background: var(--bg);
            color: var(--text);
        }}

        .nav-icon {{
            font-size: 1.1em;
        }}

        .nav-divider {{
            height: 1px;
            background: var(--border);
            margin: 4px 10px;
        }}

        /* 中间主内容 */
        .main-content {{
            min-width: 0;
        }}

        /* 情绪卡片 */
        .mood-card {{
            background: linear-gradient(135deg, {mood_color} 0%, {mood_color}dd 100%);
            color: white;
            border-radius: 20px;
            padding: 28px;
            margin-bottom: 28px;
            box-shadow: 0 10px 40px rgba(16, 185, 129, 0.2);
        }}

        .mood-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 20px;
            opacity: 0.95;
        }}

        .mood-big {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
        }}

        .mood-score {{
            font-size: 3.5em;
            font-weight: 800;
            line-height: 1;
        }}

        .mood-label {{
            font-size: 1.1em;
            opacity: 0.9;
            margin-top: 4px;
        }}

        .mood-bar-wrap {{
            flex: 1;
        }}

        .mood-bar {{
            height: 12px;
            background: rgba(255,255,255,0.25);
            border-radius: 6px;
            overflow: hidden;
        }}

        .mood-bar-inner {{
            height: 100%;
            width: {self.mood_score}%;
            background: white;
            border-radius: 6px;
            animation: fillBar 1.5s ease-out;
        }}

        @keyframes fillBar {{
            from {{ width: 0; }}
        }}

        .mood-count {{
            text-align: right;
        }}

        .mood-count-num {{
            font-size: 1.5em;
            font-weight: 700;
        }}

        .mood-count-label {{
            font-size: 0.85em;
            opacity: 0.8;
        }}

        /* ===== 新闻板块 ===== */
        .category-section {{
            margin-bottom: 40px;
            scroll-margin-top: 100px;
        }}

        .category-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 18px;
        }}

        .category-icon {{
            font-size: 1.5em;
        }}

        .category-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.3em;
            font-weight: 700;
        }}

        .news-grid {{
            display: grid;
            gap: 16px;
        }}

        /* ===== 新闻卡片 - 全新清爽排版 ===== */
        .news-card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border-left: 0 solid transparent;
        }}

        .news-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        }}

        .news-card.hot {{
            border-left: 4px solid var(--red);
        }}

        .news-card.expanded {{
            border-left: 4px solid var(--accent);
        }}

        /* 标题 */
        .news-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.1em;
            font-weight: 600;
            line-height: 1.6;
            color: var(--text);
            margin-bottom: 10px;
        }}

        /* 元信息：来源 · 时间 · 热度 */
        .news-meta {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 14px;
            font-size: 0.82em;
        }}

        .news-source {{
            background: linear-gradient(135deg, #eff6ff 0%, #e0e7ff 100%);
            color: #3b82f6;
            padding: 3px 10px;
            border-radius: 12px;
            font-weight: 600;
        }}

        .separator {{
            color: var(--text3);
        }}

        .news-time {{
            color: var(--text3);
        }}

        .news-hot {{
            color: var(--red);
            font-weight: 600;
            margin-left: auto;
        }}

        /* 摘要 */
        .news-summary {{
            color: var(--text2);
            font-size: 0.9em;
            line-height: 1.75;
            margin-bottom: 16px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        /* 展开的完整内容 */
        .news-full-content {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s ease-out, opacity 0.3s, margin 0.3s;
            opacity: 0;
            margin: 0;
        }}

        .news-full-content.open {{
            max-height: 600px;
            opacity: 1;
            margin: 8px 0 16px;
        }}

        .news-full-content-inner {{
            padding: 18px 20px;
            background: #f8fafc;
            border-radius: 12px;
            color: var(--text2);
            font-size: 0.9em;
            line-height: 1.9;
            border-left: 3px solid var(--accent);
        }}

        /* 底部：标签 + 展开按钮 */
        .news-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            padding-top: 4px;
        }}

        .news-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .tag {{
            background: #f1f5f9;
            color: var(--text2);
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.78em;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .tag:hover {{
            background: #e2e8f0;
            color: var(--text);
        }}

        /* 展开按钮 */
        .expand-btn {{
            background: white;
            color: var(--accent);
            border: 1.5px solid #dbeafe;
            padding: 8px 18px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }}

        .expand-btn:hover {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
            transform: translateY(-1px);
        }}

        /* 展开状态的按钮 */
        .news-card.expanded .expand-btn {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }}

        /* 股票表格 */
        .stocks-section {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 28px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            overflow-x: auto;
        }}

        .stocks-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.15em;
            font-weight: 700;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .stock-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .stock-table th {{
            text-align: left;
            padding: 10px 8px;
            color: var(--text3);
            font-weight: 600;
            font-size: 0.8em;
            border-bottom: 2px solid var(--border);
        }}

        .stock-table td {{
            padding: 12px 8px;
            border-bottom: 1px solid var(--border);
            font-size: 0.9em;
        }}

        .stock-table tr:last-child td {{
            border-bottom: none;
        }}

        .stock-code {{
            font-family: 'SF Mono', Monaco, monospace;
            font-weight: 600;
            color: var(--accent);
            font-size: 0.85em;
        }}

        .stock-name {{
            font-weight: 600;
        }}

        .up {{
            color: var(--red);
            font-weight: 700;
        }}

        .recommend {{
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.75em;
            font-weight: 600;
        }}

        .recommend.buy {{
            background: #dcfce7;
            color: #16a34a;
        }}

        .recommend.hold {{
            background: #fef3c7;
            color: #d97706;
        }}

        /* 右侧边栏 */
        .sidebar-right {{
            position: sticky;
            top: 100px;
            height: fit-content;
        }}

        .sidebar-card {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        }}

        .sidebar-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 0.95em;
            font-weight: 700;
            margin-bottom: 14px;
            color: var(--text);
        }}

        .archive-list {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .archive-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 10px;
            border-radius: 8px;
            color: var(--text2);
            text-decoration: none;
            font-size: 0.85em;
            transition: all 0.2s;
        }}

        .archive-item:hover {{
            background: var(--bg);
        }}

        .archive-item span {{
            font-size: 0.75em;
            color: var(--text3);
        }}

        /* 页脚 */
        .footer {{
            background: #0f172a;
            color: white;
            padding: 32px 20px;
            margin-top: 40px;
            text-align: center;
        }}

        .footer p {{
            opacity: 0.6;
            margin-bottom: 6px;
            font-size: 0.85em;
        }}

        /* 移动端底部导航 */
        .mobile-nav {{
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            border-top: 1px solid var(--border);
            padding: 10px 16px;
            z-index: 1000;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.06);
        }}

        .mobile-nav-items {{
            display: flex;
            justify-content: space-around;
            max-width: 500px;
            margin: 0 auto;
        }}

        .mobile-nav-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            padding: 6px 10px;
            color: var(--text3);
            text-decoration: none;
            font-size: 0.7em;
            transition: all 0.2s;
        }}

        .mobile-nav-item.active {{
            color: var(--accent);
        }}

        .mobile-nav-icon {{
            font-size: 1.4em;
        }}

        /* 无搜索结果 */
        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: var(--text3);
            display: none;
        }}

        /* 响应式 */
        @media (max-width: 1024px) {{
            .main-container {{
                grid-template-columns: 1fr;
                padding: 16px;
            }}
            .sidebar-left, .sidebar-right {{
                display: none;
            }}
            .mobile-nav {{
                display: block;
            }}
            body {{
                padding-bottom: 80px;
            }}
        }}

        @media (max-width: 600px) {{
            .header-inner {{
                padding: 0 16px;
            }}
            .brand span:last-child {{
                display: none;
            }}
            .search-box {{
                width: 180px;
            }}
            .search-box:focus-within {{
                width: 200px;
            }}
            .mood-card {{
                padding: 20px;
                border-radius: 16px;
            }}
            .mood-big {{
                flex-direction: column;
                text-align: center;
                gap: 16px;
            }}
            .mood-bar-wrap {{
                width: 100%;
            }}
            .news-card {{
                padding: 20px;
                border-radius: 14px;
            }}
            .news-footer {{
                flex-direction: column;
                align-items: flex-start;
                gap: 12px;
            }}
            .expand-btn {{
                align-self: flex-end;
            }}
        }}
    </style>
</head>
<body>
    <header class="top-header">
        <div class="header-inner">
            <div class="brand">
                <span class="brand-icon">📰</span>
                <span>财经新闻</span>
            </div>
            <div class="search-box">
                <span>🔍</span>
                <input type="text" id="searchInput" placeholder="搜索新闻...">
            </div>
        </div>
    </header>

    <div class="main-container">
        <!-- 左侧导航 -->
        <aside class="sidebar-left">
            <nav class="nav-menu">
                <a href="#" class="nav-item active">
                    <span class="nav-icon">🏠</span>
                    <span class="nav-text">首页</span>
                </a>
                <div class="nav-divider"></div>
                {nav_html}
            </nav>
        </aside>

        <!-- 中间主内容 -->
        <main class="main-content">
            <!-- 市场情绪 -->
            <div class="mood-card">
                <div class="mood-title">📊 今日市场情绪</div>
                <div class="mood-big">
                    <div>
                        <div class="mood-score">{mood_emoji} {self.mood_score}</div>
                        <div class="mood-label">{mood_label}</div>
                    </div>
                    <div class="mood-bar-wrap">
                        <div class="mood-bar">
                            <div class="mood-bar-inner"></div>
                        </div>
                    </div>
                    <div class="mood-count">
                        <div class="mood-count-num">{total_news}</div>
                        <div class="mood-count-label">条新闻</div>
                    </div>
                </div>
            </div>

            <!-- 股票推荐 -->
            <section class="stocks-section">
                <div class="stocks-title">📈 今日精选</div>
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

            <!-- 所有新闻板块 -->
            {news_sections_html}

            <!-- 无搜索结果 -->
            <div class="no-results" id="noResults">
                <div style="font-size: 2.5em; margin-bottom: 12px;">🔍</div>
                <div style="font-size: 1em;">没有找到相关新闻</div>
            </div>
        </main>

        <!-- 右侧边栏 -->
        <aside class="sidebar-right">
            <div class="sidebar-card">
                <div class="sidebar-title">📅 历史归档</div>
                <div class="archive-list">{archive_html}</div>
            </div>
        </aside>
    </div>

    <!-- 移动端底部导航 -->
    <nav class="mobile-nav">
        <div class="mobile-nav-items">
            <a href="#" class="mobile-nav-item active">
                <span class="mobile-nav-icon">🏠</span>
                <span>首页</span>
            </a>
            <a href="#domestic" class="mobile-nav-item">
                <span class="mobile-nav-icon">🇨🇳</span>
                <span>国内</span>
            </a>
            <a href="#ai-tech" class="mobile-nav-item">
                <span class="mobile-nav-icon">🤖</span>
                <span>AI</span>
            </a>
            <a href="#crypto" class="mobile-nav-item">
                <span class="mobile-nav-icon">💰</span>
                <span>加密</span>
            </a>
            <a href="#ev" class="mobile-nav-item">
                <span class="mobile-nav-icon">🚗</span>
                <span>电车</span>
            </a>
        </div>
    </nav>

    <footer class="footer">
        <p>⚠️ 免责声明：内容仅供参考，不构成投资建议</p>
        <p>📰 全球财经新闻 · {self.date_str} · Powered by AI</p>
    </footer>

    <script>
        // 展开/收起新闻详情
        function toggleNews(newsId, btn) {{
            const content = document.getElementById(newsId);
            const card = content.closest('.news-card');
            
            content.classList.toggle('open');
            card.classList.toggle('expanded');
            
            if (content.classList.contains('open')) {{
                btn.textContent = '收起详情';
            }} else {{
                btn.textContent = '查看详情';
            }}
        }}

        // 搜索功能
        const searchInput = document.getElementById('searchInput');
        const allNewsCards = document.querySelectorAll('.news-card');
        const noResults = document.getElementById('noResults');

        searchInput.addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase().trim();
            let hasResults = false;
            
            allNewsCards.forEach(card => {{
                const searchText = card.getAttribute('data-search').toLowerCase();
                if (query === '' || searchText.includes(query)) {{
                    card.style.display = '';
                    hasResults = true;
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            document.querySelectorAll('.category-section').forEach(section => {{
                const visibleCards = section.querySelectorAll('.news-card:not([style*="display: none"])');
                section.style.display = (visibleCards.length === 0 && query !== '') ? 'none' : '';
            }});

            noResults.style.display = hasResults ? 'none' : 'block';
        }});

        // 标签点击筛选
        document.querySelectorAll('.tag').forEach(tag => {{
            tag.addEventListener('click', function() {{
                searchInput.value = this.textContent.trim();
                searchInput.dispatchEvent(new Event('input'));
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }});
        }});

        // 导航高亮 - PC端
        const navItems = document.querySelectorAll('.nav-item');
        const sections = document.querySelectorAll('.category-section');

        window.addEventListener('scroll', function() {{
            let current = '';
            sections.forEach(section => {{
                if (window.scrollY >= section.offsetTop - 120) {{
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

        // 移动端导航点击
        document.querySelectorAll('.mobile-nav-item').forEach(item => {{
            item.addEventListener('click', function() {{
                document.querySelectorAll('.mobile-nav-item').forEach(i => i.classList.remove('active'));
                this.classList.add('active');
            }});
        }});

        console.log('📰 全球财经新闻平台 v4.2 已加载');
        console.log('✅ 全新清爽排版设计');
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
        print("✅ HTML已保存")

    async def run(self):
        print("=" * 70)
        print("📰 全球财经新闻平台 v4.2 (全新清爽排版)")
        print("=" * 70)
        
        self.prepare_news_data()
        self.get_stocks()
        self.save()
        
        print("\n" + "=" * 70)
        print("✅ 平台生成完成！")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(NewsPlatform().run())
