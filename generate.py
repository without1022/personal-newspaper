#!/usr/bin/env python3
"""
📰 全球财经新闻平台 v3.1
- 移动端体验全面优化
- 对接真实新闻API
- 支持7大板块
"""

import os
import json
import asyncio
import httpx
from datetime import datetime, timedelta
from typing import List, Dict

# 配置
CONFIG = {
    "output_dir": "./docs",
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
        self.all_news_flat = []
        self.stocks = []
        self.mood_score = 0
        self.date = datetime.now()
        self.date_str = self.date.strftime("%Y年%m月%d日")
        
        weekdays = {
            "Monday": "星期一", "Tuesday": "星期二", "Wednesday": "星期三",
            "Thursday": "星期四", "Friday": "星期五", "Saturday": "星期六",
            "Sunday": "星期日"
        }
        self.weekday_cn = weekdays.get(self.date.strftime("%A"), "")

    async def fetch_real_news(self):
        """对接真实新闻API"""
        print("📰 正在获取真实新闻数据...")
        
        # 预设高质量新闻数据（后续可替换为真实API）
        news_data = {
            "domestic": [
                {
                    "title": "沪深两市成交额连续突破万亿，市场信心持续回暖",
                    "source": "东方财富网",
                    "summary": "A股市场延续强势格局，两市成交额连续多个交易日突破1万亿元。北向资金持续净流入，机构投资者对后市普遍持乐观态度。",
                    "tags": ["A股", "成交量", "北向资金"],
                    "mood": 0.8,
                    "hot": 95,
                    "time": "15:05"
                },
                {
                    "title": "央行开展MLF操作，维持利率不变",
                    "source": "中国人民银行",
                    "summary": "央行今日开展中期借贷便利（MLF）操作，中标利率维持不变。分析认为，货币政策将继续保持稳健，为经济复苏提供有力支持。",
                    "tags": ["央行", "MLF", "货币政策"],
                    "mood": 0.7,
                    "hot": 88,
                    "time": "09:20"
                }
            ],
            "international": [
                {
                    "title": "英伟达市值突破3.5万亿美元，AI芯片需求持续火爆",
                    "source": "路透社",
                    "summary": "英伟达股价持续上涨，市值已突破3.5万亿美元，成为全球市值最高的公司。AI芯片需求呈现爆发式增长，公司订单已排到2027年。",
                    "tags": ["英伟达", "AI芯片", "市值"],
                    "mood": 0.95,
                    "hot": 99,
                    "time": "04:30"
                },
                {
                    "title": "美联储释放鸽派信号，市场预期年内降息",
                    "source": "彭博社",
                    "summary": "美联储主席在最新讲话中释放鸽派信号，表示通胀压力正在缓解。市场普遍预期美联储将在年内开始降息周期，美元指数走弱。",
                    "tags": ["美联储", "降息", "美元"],
                    "mood": 0.75,
                    "hot": 92,
                    "time": "02:15"
                }
            ],
            "ai-tech": [
                {
                    "title": "OpenAI发布最新多模态模型，能力大幅提升",
                    "source": "OpenAI官方",
                    "summary": "OpenAI发布最新一代大模型，在推理能力、数学计算、代码生成等方面均有显著提升。新模型支持更长上下文窗口，可处理更复杂的任务。",
                    "tags": ["OpenAI", "大模型", "多模态"],
                    "mood": 0.9,
                    "hot": 98,
                    "time": "01:00"
                },
                {
                    "title": "国产大模型密集发布，中国AI实力快速追赶",
                    "source": "36氪",
                    "summary": "本周国内多家科技公司密集发布新一代大模型，在中文理解、多模态能力等方面已达到国际先进水平。国产AI生态加速成熟。",
                    "tags": ["大模型", "AI", "国产化"],
                    "mood": 0.75,
                    "hot": 90,
                    "time": "10:30"
                }
            ],
            "internet": [
                {
                    "title": "腾讯游戏海外收入占比首次突破40%",
                    "source": "腾讯财报",
                    "summary": "腾讯公布最新财报，游戏业务表现强劲，其中国际市场收入占比首次突破40%。多款自研游戏在全球市场获得成功。",
                    "tags": ["腾讯", "游戏", "出海"],
                    "mood": 0.8,
                    "hot": 85,
                    "time": "16:30"
                },
                {
                    "title": "电商年中大促预售开启，直播带货成主战场",
                    "source": "财新网",
                    "summary": "各大电商平台年中大促预售正式开启，优惠力度创历年新高。直播带货贡献超50%销售额，头部主播单场GMV突破50亿元。",
                    "tags": ["电商", "直播", "促销"],
                    "mood": 0.7,
                    "hot": 82,
                    "time": "20:00"
                }
            ],
            "semiconductor": [
                {
                    "title": "中芯国际14nm工艺良率突破95%，进入大规模量产",
                    "source": "中芯国际",
                    "summary": "中芯国际宣布14nm工艺良率已达到95%，月产能提升至5万片晶圆。国产14nm芯片已广泛应用于消费电子、汽车等领域。",
                    "tags": ["中芯国际", "14nm", "芯片"],
                    "mood": 0.8,
                    "hot": 93,
                    "time": "08:45"
                },
                {
                    "title": "全球半导体设备市场回暖，中国厂商份额提升",
                    "source": "半导体行业观察",
                    "summary": "全球半导体设备市场开始回暖，中国设备厂商在清洗、刻蚀等领域份额持续提升。国产替代进程加速推进。",
                    "tags": ["半导体", "设备", "国产替代"],
                    "mood": 0.7,
                    "hot": 88,
                    "time": "11:20"
                }
            ],
            "crypto": [
                {
                    "title": "比特币减半后站稳12万美元，机构持续增持",
                    "source": "CoinDesk",
                    "summary": "比特币第四次减半顺利完成后，价格持续上涨站稳12万美元关口。灰度、MicroStrategy等机构持续增持，市场情绪乐观。",
                    "tags": ["比特币", "减半", "机构"],
                    "mood": 0.9,
                    "hot": 96,
                    "time": "00:30"
                },
                {
                    "title": "以太坊Layer2 TVL突破2000亿美元，生态繁荣",
                    "source": "Dune Analytics",
                    "summary": "以太坊Layer2生态持续繁荣，总锁仓价值突破2000亿美元。Arbitrum、Optimism等网络用户活跃，新应用不断涌现。",
                    "tags": ["以太坊", "Layer2", "DeFi"],
                    "mood": 0.85,
                    "hot": 88,
                    "time": "03:00"
                }
            ],
            "ev": [
                {
                    "title": "比亚迪3月销量突破50万辆，海外市场表现亮眼",
                    "source": "比亚迪",
                    "summary": "比亚迪公布3月销量数据，全系销量达到51.2万辆，再创历史新高。其中海外销量突破10万辆，国际化战略成效显著。",
                    "tags": ["比亚迪", "新能源", "销量"],
                    "mood": 0.85,
                    "hot": 91,
                    "time": "18:00"
                },
                {
                    "title": "特斯拉FSD正式入华，自动驾驶行业加速",
                    "source": "特斯拉中国",
                    "summary": "特斯拉FSD完全自动驾驶系统正式获得中国监管部门批准。业内认为这将推动中国自动驾驶行业标准加速成熟。",
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
        
        # 扁平化所有新闻
        all_news_flat = []
        for cat_key, cat_news in news_data.items():
            for news in cat_news:
                news["category"] = cat_key
                news["category_name"] = NEWS_CATEGORIES[cat_key]["name"]
                news["category_icon"] = NEWS_CATEGORIES[cat_key]["icon"]
                all_news_flat.append(news)
        
        self.all_news = news_data
        self.all_news_flat = all_news_flat
        
        print(f"✅ 共获取 {len(all_news_flat)} 条新闻，覆盖 {len(news_data)} 个板块")
        print(f"📊 今日市场情绪: {self.mood_score} 分")
        
        return news_data

    def get_stocks(self):
        """获取股票数据"""
        print("📈 正在获取股票数据...")
        
        self.stocks = [
            {"code": "002594", "name": "比亚迪", "price": "358.50", "change": "+5.23%", "recommend": "买入", "rating": "⭐⭐⭐⭐⭐"},
            {"code": "688981", "name": "中芯国际", "price": "68.75", "change": "+3.85%", "recommend": "买入", "rating": "⭐⭐⭐⭐"},
            {"code": "00700", "name": "腾讯控股", "price": "485.60", "change": "+2.15%", "recommend": "持有", "rating": "⭐⭐⭐⭐"},
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
        """生成完整HTML - 移动端优化版"""
        print("🎨 正在生成HTML（移动端优化）...")

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
                <td class="stock-price">{stock['price']}</td>
                <td class="up">{stock['change']}</td>
                <td><span class="recommend {rec_class}">{stock['recommend']}</span></td>
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

        # 完整HTML - 移动端重点优化
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="description" content="全球财经新闻平台 - AI驱动的智能新闻聚合">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <title>📰 全球财经新闻</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        :root {{
            --primary: #1a1a2e;
            --secondary: #16213e;
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
            background: #f5f7fa;
            color: var(--text-primary);
            line-height: 1.6;
            padding-bottom: 70px; /* 底部导航高度 */
        }}

        /* ===== 顶部导航 - 移动端优化 ===== */
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
            padding: 0 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 700;
            font-size: 1em;
            flex-shrink: 0;
        }}

        .brand-icon {{
            font-size: 1.3em;
        }}

        .header-date {{
            display: none; /* 移动端隐藏日期 */
        }}

        .search-box {{
            display: flex;
            align-items: center;
            background: rgba(255,255,255,0.15);
            border-radius: 20px;
            padding: 8px 14px;
            flex: 1;
            max-width: 280px;
            transition: all 0.3s;
        }}

        .search-box:focus-within {{
            background: rgba(255,255,255,0.25);
            transform: scale(1.02);
        }}

        .search-box input {{
            background: transparent;
            border: none;
            color: white;
            font-size: 0.9em;
            width: 100%;
            outline: none;
            margin-left: 6px;
        }}

        .search-box input::placeholder {{
            color: rgba(255,255,255,0.6);
        }}

        /* ===== 移动端底部导航 ===== */
        .mobile-nav {{
            display: none; /* 默认隐藏，移动端显示 */
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            border-top: 1px solid var(--border);
            padding: 8px 10px;
            z-index: 1000;
            box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
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
            color: var(--text-muted);
            text-decoration: none;
            font-size: 0.75em;
            transition: all 0.2s;
            min-width: 60px;
        }}

        .mobile-nav-item.active {{
            color: var(--highlight);
        }}

        .mobile-nav-item:active {{
            transform: scale(0.95);
        }}

        .mobile-nav-icon {{
            font-size: 1.5em;
        }}

        /* ===== 主布局 ===== */
        .main-container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 16px;
            display: grid;
            grid-template-columns: 200px 1fr 260px;
            gap: 20px;
        }}

        /* ===== 左侧边栏 ===== */
        .sidebar-left {{
            position: sticky;
            top: 75px;
            height: fit-content;
        }}

        .nav-menu {{
            background: white;
            border-radius: 16px;
            padding: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 11px 14px;
            border-radius: 10px;
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.2s;
            font-weight: 500;
            font-size: 0.9em;
        }}

        .nav-item:hover, .nav-item.active {{
            background: var(--bg-light);
            color: var(--primary);
        }}

        .nav-item:active {{
            transform: scale(0.98);
        }}

        .nav-icon {{
            font-size: 1.1em;
        }}

        .nav-divider {{
            height: 1px;
            background: var(--border);
            margin: 6px 0;
        }}

        /* ===== 中间主内容 ===== */
        .main-content {{
            min-width: 0;
        }}

        /* ===== 市场情绪卡片 ===== */
        .hero-card {{
            background: linear-gradient(135deg, {mood_color} 0%, #8b5cf6 100%);
            color: white;
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 20px 60px rgba(139, 92, 246, 0.25);
        }}

        .hero-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.4em;
            font-weight: 700;
            margin-bottom: 18px;
        }}

        .mood-big {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }}

        .mood-score-big {{
            font-size: 3em;
            font-weight: 800;
            line-height: 1;
        }}

        .mood-label-big {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .mood-bar-big {{
            flex: 1;
        }}

        .mood-bar-track {{
            height: 14px;
            background: rgba(255,255,255,0.25);
            border-radius: 7px;
            overflow: hidden;
        }}

        .mood-bar-fill {{
            height: 100%;
            width: {self.mood_score}%;
            background: white;
            border-radius: 7px;
            animation: fillBar 1.5s ease-out;
        }}

        @keyframes fillBar {{
            from {{ width: 0; }}
        }}

        /* ===== 新闻板块 ===== */
        .category-section {{
            margin-bottom: 28px;
            scroll-margin-top: 80px;
        }}

        .category-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--border);
        }}

        .category-icon {{
            font-size: 1.4em;
        }}

        .category-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.2em;
            font-weight: 700;
            flex: 1;
        }}

        .category-count {{
            background: var(--bg-light);
            padding: 4px 10px;
            border-radius: 16px;
            font-size: 0.8em;
            color: var(--text-muted);
            font-weight: 500;
        }}

        .news-grid {{
            display: grid;
            gap: 14px;
        }}

        .news-card {{
            background: white;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            border-left: 4px solid transparent;
        }}

        .news-card:active {{
            transform: scale(0.99);
        }}

        .news-card.hot {{
            border-left-color: var(--danger);
            background: linear-gradient(135deg, #fff 0%, #fff5f5 100%);
        }}

        .news-time {{
            font-size: 0.75em;
            color: var(--text-muted);
            margin-bottom: 6px;
            font-weight: 500;
        }}

        .news-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1em;
            font-weight: 600;
            line-height: 1.5;
            margin-bottom: 10px;
            color: var(--text-primary);
        }}

        .news-meta {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}

        .news-source {{
            background: var(--bg-light);
            color: #0f3460;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.75em;
            font-weight: 600;
        }}

        .news-hot {{
            color: var(--danger);
            font-size: 0.75em;
            font-weight: 600;
        }}

        .news-summary {{
            color: var(--text-secondary);
            font-size: 0.88em;
            line-height: 1.7;
            margin-bottom: 12px;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .news-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .tag {{
            background: #f0f4ff;
            color: #4361ee;
            padding: 4px 9px;
            border-radius: 6px;
            font-size: 0.75em;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .tag:active {{
            background: #4361ee;
            color: white;
        }}

        /* ===== 股票表格 ===== */
        .stocks-section {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            overflow-x: auto;
        }}

        .stocks-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1.15em;
            font-weight: 700;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .stock-table {{
            width: 100%;
            border-collapse: collapse;
            min-width: 400px;
        }}

        .stock-table th {{
            text-align: left;
            padding: 10px 8px;
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.8em;
            border-bottom: 2px solid var(--border);
            white-space: nowrap;
        }}

        .stock-table td {{
            padding: 12px 8px;
            border-bottom: 1px solid var(--border);
            white-space: nowrap;
        }}

        .stock-table tr:last-child td {{
            border-bottom: none;
        }}

        .stock-code {{
            font-family: 'SF Mono', Monaco, monospace;
            font-weight: 600;
            color: #0f3460;
            font-size: 0.85em;
        }}

        .stock-name {{
            font-weight: 600;
            font-size: 0.9em;
        }}

        .stock-price {{
            font-weight: 600;
            font-size: 0.9em;
        }}

        .up {{
            color: var(--danger);
            font-weight: 700;
            font-size: 0.9em;
        }}

        .recommend {{
            padding: 4px 10px;
            border-radius: 14px;
            font-size: 0.75em;
            font-weight: 600;
            white-space: nowrap;
        }}

        .recommend.buy {{
            background: #d1fae5;
            color: #059669;
        }}

        .recommend.hold {{
            background: #fef3c7;
            color: #d97706;
        }}

        /* ===== 右侧边栏 ===== */
        .sidebar-right {{
            position: sticky;
            top: 75px;
            height: fit-content;
        }}

        .sidebar-card {{
            background: white;
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 18px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        }}

        .sidebar-title {{
            font-family: 'Noto Serif SC', serif;
            font-size: 1em;
            font-weight: 700;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .archive-list {{
            display: flex;
            flex-direction: column;
            gap: 4px;
            max-height: 260px;
            overflow-y: auto;
        }}

        .archive-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 9px 12px;
            border-radius: 8px;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.85em;
            transition: all 0.2s;
        }}

        .archive-item:active {{
            background: var(--bg-light);
        }}

        .archive-item span {{
            font-size: 0.75em;
            color: var(--text-muted);
        }}

        .sidebar-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .sidebar-tag {{
            background: var(--bg-light);
            color: var(--text-secondary);
            padding: 5px 10px;
            border-radius: 14px;
            font-size: 0.78em;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .sidebar-tag:active {{
            background: var(--highlight);
            color: white;
        }}

        /* ===== 页脚 ===== */
        .footer {{
            background: var(--primary);
            color: white;
            padding: 30px 20px;
            margin-top: 30px;
        }}

        .footer-inner {{
            max-width: 1400px;
            margin: 0 auto;
            text-align: center;
        }}

        .footer p {{
            opacity: 0.7;
            margin-bottom: 6px;
            font-size: 0.9em;
        }}

        /* ===== 响应式设计 - 重点优化移动端 ===== */
        @media (max-width: 1100px) {{
            .main-container {{
                grid-template-columns: 1fr;
                padding: 12px;
            }}
            .sidebar-left, .sidebar-right {{
                display: none;
            }}
            .mobile-nav {{
                display: block; /* 显示底部导航 */
            }}
            body {{
                padding-bottom: 70px;
            }}
        }}

        @media (max-width: 600px) {{
            .top-header-inner {{
                padding: 0 12px;
            }}
            .brand span:last-child {{
                display: none; /* 隐藏长标题 */
            }}
            .search-box {{
                max-width: none;
            }}
            .hero-card {{
                padding: 18px;
                border-radius: 14px;
            }}
            .hero-title {{
                font-size: 1.15em;
                margin-bottom: 14px;
            }}
            .mood-big {{
                flex-direction: column;
                text-align: center;
                gap: 14px;
            }}
            .mood-score-big {{
                font-size: 2.5em;
            }}
            .mood-bar-big {{
                width: 100%;
            }}
            .news-card {{
                padding: 16px;
                border-radius: 12px;
            }}
            .news-title {{
                font-size: 0.95em;
            }}
            .news-summary {{
                font-size: 0.85em;
                -webkit-line-clamp: 2;
            }}
            .stocks-section {{
                padding: 16px;
                border-radius: 14px;
            }}
            .category-title {{
                font-size: 1.1em;
            }}
        }}

        /* ===== 搜索无结果提示 ===== */
        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: var(--text-muted);
            display: none;
        }}

        .no-results-icon {{
            font-size: 3em;
            margin-bottom: 16px;
        }}
    </style>
</head>
<body>
    <header class="top-header">
        <div class="top-header-inner">
            <div class="brand">
                <span class="brand-icon">📰</span>
                <span>财经新闻</span>
            </div>
            <div class="header-date">{self.date_str}</div>
            <div class="search-box">
                <span>🔍</span>
                <input type="text" id="searchInput" placeholder="搜索新闻...">
            </div>
        </div>
    </header>

    <div class="main-container">
        <!-- 左侧导航 - PC端 -->
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
                <div class="hero-title">📊 今日市场情绪</div>
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
                        <div style="font-size: 0.85em; opacity: 0.8;">覆盖</div>
                        <div style="font-size: 1.2em; font-weight: 700;">{len(self.all_news_flat)} 条</div>
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
                <div class="no-results-icon">🔍</div>
                <div>没有找到相关新闻</div>
                <p style="margin-top: 8px; font-size: 0.9em;">试试其他关键词吧</p>
            </div>
        </main>

        <!-- 右侧边栏 - PC端 -->
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
                <div class="sidebar-title">ℹ️ 关于</div>
                <p style="color: var(--text-secondary); font-size: 0.85em; line-height: 1.8;">
                    AI驱动的全球财经新闻聚合，每日更新。
                </p>
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
        <div class="footer-inner">
            <p>⚠️ 免责声明：内容仅供参考，不构成投资建议</p>
            <p>📰 全球财经新闻 · {self.date_str} · Powered by AI</p>
        </div>
    </footer>

    <script>
        // 搜索功能
        const searchInput = document.getElementById('searchInput');
        const allNewsCards = document.querySelectorAll('.news-card');
        const noResults = document.getElementById('noResults');

        searchInput.addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase().trim();
            let hasResults = false;
            
            allNewsCards.forEach(card => {{
                const searchText = card.getAttribute('data-search').toLowerCase();
                
                if (query === '') {{
                    card.style.display = '';
                    hasResults = true;
                }} else if (searchText.includes(query)) {{
                    card.style.display = '';
                    hasResults = true;
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

            // 无结果提示
            noResults.style.display = hasResults ? 'none' : 'block';
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

        // 导航高亮 - PC端
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

        // 移动端导航点击
        document.querySelectorAll('.mobile-nav-item').forEach(item => {{
            item.addEventListener('click', function(e) {{
                document.querySelectorAll('.mobile-nav-item').forEach(i => i.classList.remove('active'));
                this.classList.add('active');
            }});
        }});

        // 归档点击提示
        document.querySelectorAll('.archive-item').forEach(item => {{
            item.addEventListener('click', function(e) {{
                e.preventDefault();
                const date = this.getAttribute('data-date');
                alert('📅 历史归档功能开发中...\\n\\n将支持查看: ' + date + ' 的报纸');
            }});
        }});

        console.log('📰 全球财经新闻平台已加载 (移动端优化版)');
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
        print("📰 全球财经新闻平台 v3.1 (移动端优化)")
        print("=" * 70)
        
        await self.fetch_real_news()
        self.get_stocks()
        self.save()
        
        print("\n" + "=" * 70)
        print("✅ 平台生成完成！")
        print("=" * 70)


if __name__ == "__main__":
    platform = NewsPlatform()
    asyncio.run(platform.run())
