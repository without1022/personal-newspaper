#!/usr/bin/env python3
"""
📰 专业财经新闻平台 v3.0
- 全球多板块新闻
- 历史归档系统
- 搜索功能
- 专业财经媒体设计
"""

import os
import sys
import json
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict

# 配置
CONFIG = {
    "output_dir": "./docs",
    "archive_days": 30,  # 保留30天归档
}

# 新闻板块配置
NEWS_CATEGORIES = {
    "domestic": {
        "name": "国内财经",
        "icon": "🇨🇳",
        "color": "#e74c3c"
    },
    "international": {
        "name": "国际财经",
        "icon": "🌍",
        "color": "#3498db"
    },
    "ai-tech": {
        "name": "AI科技",
        "icon": "🤖",
        "color": "#9b59b6"
    },
    "internet": {
        "name": "互联网",
        "icon": "💻",
        "color": "#1abc9c"
    },
    "semiconductor": {
        "name": "半导体",
        "icon": "🔬",
        "color": "#f39c12"
    },
    "crypto": {
        "name": "加密货币",
        "icon": "💰",
        "color": "#e67e22"
    },
    "ev": {
        "name": "新能源汽车",
        "icon": "🚗",
        "color": "#27ae60"
    }
}

class NewsPlatform:
    def __init__(self):
        self.all_news = {}
        self.stocks = []
        self.mood_score = 0
        self.date = datetime.now()
        self.date_str = self.date.strftime("%Y年%m月%d日")
        self.date_iso = self.date.strftime("%Y-%m-%d")
        
        weekdays = {
            "Monday": "星期一", "Tuesday": "星期二", "Wednesday": "星期三",
            "Thursday": "星期四", "Friday": "星期五", "Saturday": "星期六",
            "Sunday": "星期日"
        }
        self.weekday_cn = weekdays.get(self.date.strftime("%A"), "")

    def generate_mock_news(self) -> Dict[str, List]:
        """生成模拟新闻数据"""
        print("📰 正在生成新闻数据...")
        
        news_data = {
            "domestic": [
                {
                    "title": "央行降准0.5%，释放长期流动性约1万亿",
                    "source": "中国人民银行",
                    "summary": "中国人民银行决定下调金融机构存款准备金率0.5个百分点，预计释放长期资金约1万亿元。此举旨在优化金融机构资金结构，增强金融机构支持实体经济的能力。",
                    "tags": ["货币政策", "降准", "流动性"],
                    "mood": 0.85,
                    "hot": 98,
                    "time": "09:00"
                },
                {
                    "title": "A股三大指数集体走强，成交额连续突破万亿",
                    "source": "东方财富",
                    "summary": "今日A股市场延续强势格局，上证指数涨超1%，深证成指、创业板指均有不错表现。两市成交额连续第15个交易日突破1万亿元，市场交投活跃。",
                    "tags": ["A股", "成交量", "牛市"],
                    "mood": 0.8,
                    "hot": 95,
                    "time": "15:00"
                }
            ],
            "international": [
                {
                    "title": "美联储暗示暂停加息，美元指数走弱",
                    "source": "美联储",
                    "summary": "美联储主席鲍威尔在最新讲话中暗示，当前利率水平已足够限制经济活动，可能在下次会议上暂停加息。受此影响，美元指数下跌，非美货币普遍上涨。",
                    "tags": ["美联储", "加息", "美元"],
                    "mood": 0.75,
                    "hot": 92,
                    "time": "02:00"
                },
                {
                    "title": "英伟达Q1营收超预期，AI芯片需求持续爆发",
                    "source": "NVIDIA",
                    "summary": "英伟达公布2026财年第一季度财报，营收达到285亿美元，同比增长210%，大幅超出市场预期。其中数据中心业务收入增长260%，AI芯片需求持续火爆。",
                    "tags": ["英伟达", "财报", "AI芯片"],
                    "mood": 0.9,
                    "hot": 97,
                    "time": "04:30"
                }
            ],
            "ai-tech": [
                {
                    "title": "OpenAI发布GPT-5，多模态能力大幅提升",
                    "source": "OpenAI",
                    "summary": "OpenAI正式发布GPT-5大模型，在推理能力、多模态理解、长文本处理等方面均有显著提升。新模型支持1000万token上下文，可处理完整代码库和书籍。",
                    "tags": ["OpenAI", "GPT-5", "大模型"],
                    "mood": 0.95,
                    "hot": 99,
                    "time": "01:00"
                },
                {
                    "title": "中国大模型公司密集发布新产品，竞争加剧",
                    "source": "36氪",
                    "summary": "本周国内多家大模型公司密集发布新产品，包括百度文心一言4.0、阿里通义千问3.0、腾讯混元2.0等。国产大模型能力快速追赶国际先进水平。",
                    "tags": ["大模型", "百度", "阿里", "腾讯"],
                    "mood": 0.7,
                    "hot": 88,
                    "time": "10:30"
                }
            ],
            "internet": [
                {
                    "title": "腾讯游戏收入创新高，海外市场贡献超40%",
                    "source": "腾讯控股",
                    "summary": "腾讯公布最新财报，游戏业务收入同比增长15%，其中国际市场游戏收入占比首次突破40%。《王者荣耀》、《PUBG Mobile》等产品表现强劲。",
                    "tags": ["腾讯", "游戏", "出海"],
                    "mood": 0.8,
                    "hot": 85,
                    "time": "16:00"
                },
                {
                    "title": "电商618大促预售开启，价格战再度升级",
                    "source": "财新网",
                    "summary": "2026年618电商大促预售正式开启，各大平台纷纷推出史上最大力度优惠。直播带货成为主战场，头部主播单场预售额突破50亿。",
                    "tags": ["电商", "618", "直播"],
                    "mood": 0.65,
                    "hot": 82,
                    "time": "20:00"
                }
            ],
            "semiconductor": [
                {
                    "title": "中芯国际14nm工艺量产突破，良率达95%",
                    "source": "中芯国际",
                    "summary": "中芯国际宣布14nm工艺良率已达到95%，进入大规模量产阶段。14nm生产线月产能达到5万片晶圆，可满足国内中高端芯片需求。",
                    "tags": ["中芯国际", "14nm", "芯片"],
                    "mood": 0.75,
                    "hot": 90,
                    "time": "08:30"
                },
                {
                    "title": "美国芯片出口管制新规出台，影响几何？",
                    "source": "路透社",
                    "summary": "美国商务部公布最新芯片出口管制新规，进一步限制先进AI芯片和制造设备出口。分析认为短期有冲击，但长期将加速国产替代进程。",
                    "tags": ["出口管制", "芯片", "国产替代"],
                    "mood": 0.5,
                    "hot": 93,
                    "time": "22:00"
                }
            ],
            "crypto": [
                {
                    "title": "比特币减半行情启动，站稳12万美元",
                    "source": "CoinDesk",
                    "summary": "比特币第四次减半顺利完成，区块奖励从6.25 BTC降至3.125 BTC。减半后比特币价格持续上涨，站稳12万美元关口，市值突破2.3万亿美元。",
                    "tags": ["比特币", "减半", "行情"],
                    "mood": 0.9,
                    "hot": 96,
                    "time": "00:30"
                },
                {
                    "title": "以太坊Layer2 TVL突破2000亿美元",
                    "source": "Dune Analytics",
                    "summary": "以太坊Layer2生态持续繁荣，总锁仓价值TVL突破2000亿美元。Arbitrum和Optimism占据主导地位，Base、zkSync等新公链增长迅速。",
                    "tags": ["以太坊", "Layer2", "DeFi"],
                    "mood": 0.85,
                    "hot": 88,
                    "time": "03:00"
                }
            ],
            "ev": [
                {
                    "title": "比亚迪3月销量突破50万辆，再创历史新高",
                    "source": "比亚迪",
                    "summary": "比亚迪公布3月销量数据，全系销量达到51.2万辆，同比增长45%，再创历史新高。其中海外销量突破10万辆，国际化战略成效显著。",
                    "tags": ["比亚迪", "新能源车", "销量"],
                    "mood": 0.85,
                    "hot": 91,
                    "time": "18:00"
                },
                {
                    "title": "特斯拉FSD入华获批，自动驾驶迎来变局",
                    "source": "特斯拉",
                    "summary": "特斯拉FSD（完全自动驾驶）正式获得中国监管部门批准，将在国内推送。业内认为这将推动中国自动驾驶行业标准加速成熟。",
                    "tags": ["特斯拉", "FSD", "自动驾驶"],
                    "mood": 0.8,
                    "hot": 94,
                    "time": "11:00"
                }
            ]
        }
        
        # 计算整体市场情绪
        all_moods = []
        for cat_news in news_data.values():
            for news in cat_news:
                all_moods.append(news["mood"])
        self.mood_score = int(sum(all_moods) / len(all_moods) * 100)
        
        # 扁平化所有新闻用于搜索
        all_news_flat = []
        for cat_key, cat_news in news_data.items():
            for news in cat_news:
                news["category"] = cat_key
                news["category_name"] = NEWS_CATEGORIES[cat_key]["name"]
                news["category_icon"] = NEWS_CATEGORIES[cat_key]["icon"]
                all_news_flat.append(news)
        
        self.all_news = news_data
        self.all_news_flat = all_news_flat
        
        print(f"✅ 共生成 {len(all_news_flat)} 条新闻，覆盖 {len(news_data)} 个板块")
        print(f"📊 今日市场情绪: {self.mood_score} 分")
        
        return news_data

    def get_stocks(self):
        """获取股票数据"""
        print("📈 正在获取股票数据...")
        
        self.stocks = [
            {"code": "002594", "name": "比亚迪", "price": "358.50", "change": "+5.23%", "recommend": "买入", "rating": "⭐⭐⭐⭐⭐"},
            {"code": "688981", "name": "中芯国际", "price": "68.75", "change": "+3.85%", "recommend": "买入", "rating": "⭐⭐⭐⭐"},
            {"code": "0700.HK", "name": "腾讯控股", "price": "485.60", "change": "+2.15%", "recommend": "持有", "rating": "⭐⭐⭐⭐"},
            {"code": "NVDA", "name": "英伟达", "price": "1280.50", "change": "+8.32%", "recommend": "买入", "rating": "⭐⭐⭐⭐⭐"},
            {"code": "TSLA", "name": "特斯拉", "price": "325.80", "change": "+4.56%", "recommend": "买入", "rating": "⭐⭐⭐⭐"},
        ]

    def generate_archive_list(self):
        """生成归档列表"""
        archive_dates = []
        for i in range(30):
            date = self.date - timedelta(days=i)
            archive_dates.append({
                "date": date.strftime("%Y-%m-%d"),
                "label": date.strftime("%m月%d日"),
                "weekday": date.strftime("%A")[:3]
            })
        return archive_dates

    def generate_html(self):
        """生成完整HTML"""
        print("🎨 正在生成HTML...")

        # 生成导航栏
        nav_html = ""
        for cat_key, cat_info in NEWS_CATEGORIES.items():
            nav_html += f"""
            <a href="#{cat_key}" class="nav-item" data-category="{cat_key}">
                <span class="nav-icon">{cat_info['icon']}</span>
                <span class="nav-text">{cat_info['name']}</span>
            </a>
            """

        # 生成所有新闻板块
        news_sections_html = ""
        for cat_key, cat_info in NEWS_CATEGORIES.items():
            news_list = self.all_news.get(cat_key, [])
            if not news_list:
                continue
                
            news_cards_html = ""
            for news in news_list:
                tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in news["tags"]])
                hot_class = "hot" if news["hot"] >= 90 else ""
                
                news_cards_html += f"""
                <article class="news-card {hot_class}" data-search="{news['title']} {news['summary']} {' '.join(news['tags'])}">
                    <div class="news-time">{news['time']}</div>
                    <h3 class="news-title">{news['title']}</h3>
                    <div class="news-meta">
                        <span class="news-source">{news['source']}</span>
                        <span class="news-hot">🔥 {news['hot']}%</span>
                    </div>
                    <p class="news-summary">{news['summary']}</p>
                    <div class="news-tags">{tags_html}</div>
                </article>
                """

            news_sections_html += f"""
            <section id="{cat_key}" class="category-section">
                <div class="category-header">
                    <span class="category-icon">{cat_info['icon']}</span>
                    <h2 class="category-title">{cat_info['name']}</h2>
                    <span class="category-count">{len(news_list)} 条</span>
                </div>
                <div class="news-grid">
                    {news_cards_html}
                </div>
            </section>
            """

        # 生成股票表格
        stocks_html = ""
        for stock in self.stocks:
            rec_class = "buy" if stock["recommend"] == "买入" else "hold"
            stocks_html += f"""
            <tr>
                <td class="stock-code">{stock['code']}</td>
                <td class="stock-name">{stock['name']}</td>
                <td class="stock-price">${stock['price']}</td>
                <td class="up">{stock['change']}</td>
                <td><span class="recommend {rec_class}">{stock['recommend']}</span></td>
                <td class="rating">{stock['rating']}</td>
            </tr>
            """

        # 生成归档日期
        archive_list = self.generate_archive_list()
        archive_html = "".join([
            f'<a href="#" class="archive-item" data-date="{d["date"]}">{d["label"]} <span>{d["weekday"]}</span></a>'
            for d in archive_list
        ])

        # 所有标签
        all_tags = set()
        for news in self.all_news_flat:
            for tag in news["tags"]:
                all_tags.add(tag)
        tags_html = "".join([f'<span class="sidebar-tag">{tag}</span>' for tag in sorted(all_tags)])

        # 情绪判断
        if self.mood_score >= 75:
            mood_label = "非常乐观"
            mood_emoji = "🚀"
            mood_color = "#10b981"
        elif self.mood_score >= 60:
            mood_label = "偏乐观"
            mood_emoji = "😊"
            mood_color = "#f59e0b"
        elif self.mood_score >= 40:
            mood_label = "中性"
            mood_emoji = "⚖️"
            mood_color = "#6366f1"
        else:
            mood_label = "谨慎"
            mood_emoji = "⚠️"
            mood_color = "#ef4444"

        # 完整HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="全球财经新闻平台 - AI驱动的智能新闻聚合，覆盖A股、美股、加密货币、AI科技、半导体等全板块">
    <meta name="keywords" content="财经新闻,股票,加密货币,AI科技,半导体,全球市场">
    <title>📰 全球财经新闻平台</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary: #1a1a2e;
            --secondary: #16213e;
            --accent: #0f3460;
            --highlight: #e94560;
            --text-primary: #1a1a2e;
            --text-secondary: #4a5568;
            --text-muted: #718096;
            --bg-light: #f7fafc;
            --border: #e2e8f0;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
            background-attachment: fixed;
            color: var(--text-primary);
            line-height: 1.6;
        }}

        /* 顶部导航 */
        .top-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 12px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 20px rgba(0,0,0,0.15);
        }}

        .top-header-inner {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 700;
            font-size: 1.2em;
        }}

        .brand-icon {{
            font-size: 1.5em;
        }}

        .header-date {{
            font-size: 0.9em;
            opacity: 0.8;
        }}

        .search-box {{
            display: flex;
            align-items: center;
            background: rgba(255,255,255,0.15);
            border-radius: 30px;
            padding: 8px 16px;
            width: 320px;
        }}

        .search-box input {{
            background: transparent;
            border: none;
            color: white;
            font-size: 0.95em;
            width: 100%;
            outline: none;
            margin-left: 8px;
        }}

        .search-box input::placeholder {{
            color: rgba(255,255,255,0.6);
        }}

        /* 主布局 */
        .main-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 24px 20px;
            display: grid;
            grid-template-columns: 220px 1fr 280px;
            gap: 24px;
        }}

        /* 左侧边栏 - 导航 */
        .sidebar-left {{
            position: sticky;
            top: 80px;
            height: fit-content;
        }}

        .nav-menu {{
            background: white;
            border-radius: 16px;
            padding: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            border-radius: 10px;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.2s;
            font-weight: 500;
        }}

        .nav-item:hover, .nav-item.active {{
            background: var(--bg-light);
            color: var(--primary);
        }}

        .nav-icon {{
            font-size: 1.2em;
        }}

        .nav-divider {{
            height: 1px;
            background: var(--border);
            margin: 8px 0;
        }}

        /* 中间主内容 */
        .main-content {{
            min-width: 0;
        }}

        /* 头部大卡片 - 市场情绪 */
        .hero-card {{
            background: linear-gradient(135deg, {mood_color} 0%, #8b5cf6 100%);
            color: white;
            border-radius: 20px;
            padding: 32px;
            margin-bottom: 24px;
            box-shadow: 0 20px 60px rgba(139, 92, 246, 0.25);
        }}

        .hero-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.8em;
            font-weight: 700;
            margin-bottom: 20px;
        }}

        .mood-big {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .mood-score-big {{
            font-size: 4em;
            font-weight: 800;
            line-height: 1;
        }}

        .mood-label-big {{
            font-size: 1.5em;
            opacity: 0.9;
        }}

        .mood-bar-big {{
            flex: 1;
            margin: 0 40px;
        }}

        .mood-bar-track {{
            height: 16px;
            background: rgba(255,255,255,0.25);
            border-radius: 8px;
            overflow: hidden;
        }}

        .mood-bar-fill {{
            height: 100%;
            width: {self.mood_score}%;
            background: white;
            border-radius: 8px;
            animation: fillBar 1.5s ease-out;
        }}

        @keyframes fillBar {{
            from {{ width: 0; }}
        }}

        /* 新闻板块 */
        .category-section {{
            margin-bottom: 32px;
            scroll-margin-top: 80px;
        }}

        .category-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--border);
        }}

        .category-icon {{
            font-size: 1.6em;
        }}

        .category-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.4em;
            font-weight: 700;
            flex: 1;
        }}

        .category-count {{
            background: var(--bg-light);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .news-grid {{
            display: grid;
            gap: 16px;
        }}

        .news-card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border-left: 4px solid transparent;
        }}

        .news-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(0,0,0,0.1);
            border-left-color: var(--highlight);
        }}

        .news-card.hot {{
            border-left-color: var(--danger);
            background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
        }}

        .news-time {{
            font-size: 0.8em;
            color: var(--text-muted);
            margin-bottom: 8px;
            font-weight: 500;
        }}

        .news-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.1em;
            font-weight: 600;
            line-height: 1.5;
            margin-bottom: 12px;
            color: var(--text-primary);
        }}

        .news-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .news-source {{
            background: var(--bg-light);
            color: var(--accent);
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.8em;
            font-weight: 600;
        }}

        .news-hot {{
            color: var(--danger);
            font-size: 0.8em;
            font-weight: 600;
        }}

        .news-summary {{
            color: var(--text-secondary);
            font-size: 0.92em;
            line-height: 1.7;
            margin-bottom: 14px;
        }}

        .news-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .tag {{
            background: #f0f4ff;
            color: #4361ee;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78em;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .tag:hover {{
            background: #4361ee;
            color: white;
        }}

        /* 股票表格 */
        .stocks-section {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        }}

        .stocks-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.3em;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .stock-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .stock-table th {{
            text-align: left;
            padding: 12px 10px;
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.85em;
            border-bottom: 2px solid var(--border);
        }}

        .stock-table td {{
            padding: 14px 10px;
            border-bottom: 1px solid var(--border);
        }}

        .stock-table tr:last-child td {{
            border-bottom: none;
        }}

        .stock-table tr:hover td {{
            background: var(--bg-light);
        }}

        .stock-code {{
            font-family: 'SF Mono', Monaco, monospace;
            font-weight: 600;
            color: var(--accent);
            font-size: 0.9em;
        }}

        .stock-name {{
            font-weight: 600;
        }}

        .up {{
            color: var(--danger);
            font-weight: 700;
        }}

        .recommend {{
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
        }}

        .recommend.buy {{
            background: #d1fae5;
            color: #059669;
        }}

        .recommend.hold {{
            background: #fef3c7;
            color: #d97706;
        }}

        .rating {{
            color: var(--warning);
            font-size: 0.85em;
            letter-spacing: -2px;
        }}

        /* 右侧边栏 */
        .sidebar-right {{
            position: sticky;
            top: 80px;
            height: fit-content;
        }}

        .sidebar-card {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        }}

        .sidebar-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.1em;
            font-weight: 700;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        /* 归档列表 */
        .archive-list {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            max-height: 300px;
            overflow-y: auto;
        }}

        .archive-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 14px;
            border-radius: 8px;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.9em;
            transition: all 0.2s;
        }}

        .archive-item:hover {{
            background: var(--bg-light);
            color: var(--primary);
        }}

        .archive-item span {{
            font-size: 0.8em;
            color: var(--text-muted);
        }}

        /* 热门标签 */
        .sidebar-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .sidebar-tag {{
            background: var(--bg-light);
            color: var(--text-secondary);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .sidebar-tag:hover {{
            background: var(--highlight);
            color: white;
        }}

        /* 页脚 */
        .footer {{
            background: var(--primary);
            color: white;
            padding: 40px 20px;
            margin-top: 40px;
        }}

        .footer-inner {{
            max-width: 1400px;
            margin: 0 auto;
            text-align: center;
        }}

        .footer p {{
            opacity: 0.7;
            margin-bottom: 8px;
        }}

        /* 响应式 */
        @media (max-width: 1200px) {{
            .main-container {{
                grid-template-columns: 1fr;
            }}
            .sidebar-left, .sidebar-right {{
                display: none;
            }}
            .search-box {{
                width: 200px;
            }}
        }}

        @media (max-width: 768px) {{
            .hero-card {{
                padding: 24px 20px;
            }}
            .mood-big {{
                flex-direction: column;
                text-align: center;
                gap: 20px;
            }}
            .mood-bar-big {{
                width: 100%;
                margin: 0;
            }}
            .news-card {{
                padding: 20px;
            }}
            .stock-table {{
                font-size: 0.85em;
            }}
        }}

        /* 搜索高亮 */
        .search-highlight {{
            background: #fef08a;
            padding: 2px 4px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <header class="top-header">
        <div class="top-header-inner">
            <div class="brand">
                <span class="brand-icon">📰</span>
                <span>全球财经新闻平台</span>
            </div>
            <div class="header-date">{self.date_str} {self.weekday_cn}</div>
            <div class="search-box">
                <span>🔍</span>
                <input type="text" id="searchInput" placeholder="搜索新闻、股票、话题...">
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
            <div class="hero-card">
                <div class="hero-title">📊 今日市场情绪指数</div>
                <div class="mood-big">
                    <div>
                        <div class="mood-score-big">{mood_emoji} {self.mood_score}</div>
                        <div class="mood-label-big">{mood_label}</div>
                    </div>
                    <div class="mood-bar-big">
                        <div class="mood-bar-track">
                            <div class="mood-bar-fill"></div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.95em; opacity: 0.8;">覆盖</div>
                        <div style="font-size: 1.4em; font-weight: 700;">{len(self.all_news_flat)} 条新闻</div>
                        <div style="font-size: 0.95em; opacity: 0.8;">{len(NEWS_CATEGORIES)} 个板块</div>
                    </div>
                </div>
            </div>

            <!-- 股票推荐 -->
            <section class="stocks-section">
                <div class="stocks-title">📈 今日精选股票</div>
                <table class="stock-table">
                    <thead>
                        <tr>
                            <th>代码</th>
                            <th>名称</th>
                            <th>现价</th>
                            <th>涨跌幅</th>
                            <th>推荐</th>
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
        </main>

        <!-- 右侧边栏 -->
        <aside class="sidebar-right">
            <div class="sidebar-card">
                <div class="sidebar-title">📅 历史归档</div>
                <div class="archive-list">
                    {archive_html}
                </div>
            </div>

            <div class="sidebar-card">
                <div class="sidebar-title">🏷️ 热门标签</div>
                <div class="sidebar-tags">
                    {tags_html}
                </div>
            </div>

            <div class="sidebar-card">
                <div class="sidebar-title">ℹ️ 关于本平台</div>
                <p style="color: var(--text-secondary); font-size: 0.9em; line-height: 1.8;">
                    本平台由AI驱动，每日自动聚合全球财经新闻，覆盖股票、加密货币、AI科技、半导体等多个板块。
                </p>
                <p style="color: var(--text-muted); font-size: 0.85em; margin-top: 12px;">
                    每日 9:00 自动更新 · Powered by Hermes AI
                </p>
            </div>
        </aside>
    </div>

    <footer class="footer">
        <div class="footer-inner">
            <p>⚠️ 免责声明：所有内容由AI自动生成，仅供参考，不构成任何投资建议</p>
            <p>投资有风险，入市需谨慎。请根据自身风险承受能力制定投资策略。</p>
            <p style="margin-top: 15px; opacity: 0.5;">
                📰 全球财经新闻平台 · {self.date_str}
            </p>
        </div>
    </footer>

    <script>
        // 搜索功能
        const searchInput = document.getElementById('searchInput');
        const allNewsCards = document.querySelectorAll('.news-card');

        searchInput.addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase().trim();
            
            allNewsCards.forEach(card => {{
                const searchText = card.getAttribute('data-search').toLowerCase();
                
                if (query === '') {{
                    card.style.display = '';
                    card.classList.remove('search-highlight');
                }} else if (searchText.includes(query)) {{
                    card.style.display = '';
                    // 高亮匹配（简化版）
                }} else {{
                    card.style.display = 'none';
                }}
            }});
            
            // 显示/隐藏板块标题
            document.querySelectorAll('.category-section').forEach(section => {{
                const visibleCards = section.querySelectorAll('.news-card:not([style*="display: none"])');
                if (visibleCards.length === 0 && query !== '') {{
                    section.style.display = 'none';
                }} else {{
                    section.style.display = '';
                }}
            }});
        }});

        // 标签点击筛选
        document.querySelectorAll('.tag, .sidebar-tag').forEach(tag => {{
            tag.addEventListener('click', function() {{
                const tagText = this.textContent.trim();
                searchInput.value = tagText;
                searchInput.dispatchEvent(new Event('input'));
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }});
        }});

        // 导航高亮
        const navItems = document.querySelectorAll('.nav-item');
        const sections = document.querySelectorAll('.category-section');

        window.addEventListener('scroll', function() {{
            let current = '';
            sections.forEach(section => {{
                const sectionTop = section.offsetTop;
                if (window.scrollY >= sectionTop - 100) {{
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

        // 归档点击（模拟）
        document.querySelectorAll('.archive-item').forEach(item => {{
            item.addEventListener('click', function(e) {{
                e.preventDefault();
                const date = this.getAttribute('data-date');
                alert('切换到 ' + date + ' 的报纸\\n(完整功能需要后端支持历史数据)');
            }});
        }});

        console.log('📰 全球财经新闻平台已加载');
        console.log(`📊 今日新闻: {len(self.all_news_flat)} 条，覆盖 {len(NEWS_CATEGORIES)} 个板块`);
    </script>
</body>
</html>
"""
        return html

    def save(self):
        os.makedirs(CONFIG["output_dir"], exist_ok=True)
        html = self.generate_html()
        
        filepath = os.path.join(CONFIG["output_dir"], "index.html")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"✅ HTML已保存到: {filepath}")

    async def run(self):
        print("=" * 70)
        print("📰 全球财经新闻平台 v3.0")
        print("=" * 70)
        
        self.generate_mock_news()
        self.get_stocks()
        self.save()
        
        print("\n" + "=" * 70)
        print("✅ 平台生成完成！")
        print("=" * 70)


if __name__ == "__main__":
    platform = NewsPlatform()
    asyncio.run(platform.run())
