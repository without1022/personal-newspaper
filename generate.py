#!/usr/bin/env python3
"""
📰 个人报纸自动生成系统 v2.0
优化版：更美观、更多功能、更好的用户体验
"""

import os
import sys
import json
import httpx
import asyncio
from datetime import datetime
from typing import List, Dict

# 配置
CONFIG = {
    "news_sources": [
        {
            "name": "东方财富",
            "url": "https://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult.ashx",
            "type": "finance"
        }
    ],
    "output_dir": "./docs",
}

class NewspaperGenerator:
    def __init__(self):
        self.news = []
        self.stocks = []
        self.mood_score = 0
        self.date = datetime.now().strftime("%Y年%m月%d日")
        self.weekday = datetime.now().strftime("%A")
        
        # 中文星期
        weekdays = {
            "Monday": "星期一",
            "Tuesday": "星期二",
            "Wednesday": "星期三",
            "Thursday": "星期四",
            "Friday": "星期五",
            "Saturday": "星期六",
            "Sunday": "星期日"
        }
        self.weekday_cn = weekdays.get(self.weekday, self.weekday)

    async def fetch_news(self) -> List[Dict]:
        """采集新闻"""
        print("📰 正在采集新闻...")
        
        mock_news = [
            {
                "title": "🍶 白酒概念涨0.64%，主力资金净流入29股",
                "source": "东方财富",
                "summary": "白酒板块今日表现强势，主力资金大幅流入。贵州茅台、五粮液等龙头股均有不错表现。分析认为，随着消费复苏，白酒行业有望迎来新一轮增长周期。",
                "tags": ["白酒", "主力资金"],
                "mood": 0.8,
                "hot": 95
            },
            {
                "title": "💰 两融余额十连升，15股获融资净买入超10亿元",
                "source": "东方财富",
                "summary": "两市融资余额实现十连升，杠杆资金持续入场。15只个股获得融资净买入超10亿元，显示机构投资者对后市持乐观态度。",
                "tags": ["两融", "融资买入"],
                "mood": 0.7,
                "hot": 88
            },
            {
                "title": "🔬 半导体板块持续走强，国产替代进程加速",
                "source": "36氪",
                "summary": "半导体板块今日涨幅居前，中芯国际、北方华创等龙头股表现活跃。随着国内芯片自主可控政策的持续推进，半导体行业迎来历史性发展机遇。",
                "tags": ["半导体", "国产替代"],
                "mood": 0.6,
                "hot": 82
            },
            {
                "title": "🚗 新能源汽车销量超预期30%，产业链受益明显",
                "source": "财新网",
                "summary": "3月份新能源汽车销量同比增长30%，超出市场预期。比亚迪、特斯拉等头部厂商销量创历史新高，产业链上下游公司均有望受益。",
                "tags": ["新能源汽车", "销量"],
                "mood": 0.75,
                "hot": 90
            }
        ]
        
        self.news = mock_news
        
        # 计算市场情绪
        mood_values = [n["mood"] for n in self.news]
        self.mood_score = int(sum(mood_values) / len(mood_values) * 100)
        
        print(f"✅ 采集到 {len(self.news)} 条新闻")
        print(f"📊 市场情绪: {self.mood_score} 分")
        
        return mock_news

    def fetch_stocks(self) -> List[Dict]:
        """获取股票推荐"""
        print("📈 正在获取股票数据...")
        
        mock_stocks = [
            {"code": "002290", "name": "禾盛新材", "price": "81.35", "change": "+10.01%", "recommend": "买入", "rating": "⭐⭐⭐⭐⭐"},
            {"code": "600770", "name": "综艺股份", "price": "6.97", "change": "+9.94%", "recommend": "买入", "rating": "⭐⭐⭐⭐"},
            {"code": "603318", "name": "水发燃气", "price": "11.39", "change": "+10.05%", "recommend": "买入", "rating": "⭐⭐⭐⭐"},
            {"code": "000925", "name": "众合科技", "price": "9.20", "change": "+10.05%", "recommend": "买入", "rating": "⭐⭐⭐⭐"},
            {"code": "300422", "name": "博世科", "price": "5.56", "change": "+20.09%", "recommend": "买入", "rating": "⭐⭐⭐⭐⭐"},
        ]
        
        self.stocks = mock_stocks
        return mock_stocks

    def generate_html(self) -> str:
        """生成HTML页面"""
        print("🎨 正在生成HTML...")

        # 生成新闻HTML
        news_html = ""
        for i, item in enumerate(self.news):
            tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in item["tags"]])
            hot_icon = "🔥" if item["hot"] >= 90 else ""
            delay = i * 0.1
            
            news_html += f"""
            <div class="news-item" style="animation-delay: {delay}s">
                <div class="news-header">
                    <div class="news-title">
                        {hot_icon} {item['title']}
                    </div>
                    <div class="hot-score">热度 {item['hot']}%</div>
                </div>
                <div class="news-meta">
                    <span class="news-source">{item['source']}</span>
                    {tags_html}
                </div>
                <div class="news-summary">
                    {item['summary']}
                </div>
            </div>
            """

        # 生成股票HTML
        stocks_html = ""
        for stock in self.stocks:
            stocks_html += f"""
                    <tr>
                        <td class="stock-code">{stock['code']}</td>
                        <td class="stock-name">{stock['name']}</td>
                        <td class="stock-price">¥{stock['price']}</td>
                        <td class="up">{stock['change']}</td>
                        <td><span class="recommend-buy">🟢 {stock['recommend']}</span></td>
                        <td class="rating">{stock['rating']}</td>
                    </tr>
            """

        # 情绪判断
        if self.mood_score >= 70:
            mood_label = "乐观"
            mood_emoji = "😊"
            mood_color = "#10b981"
        elif self.mood_score >= 50:
            mood_label = "偏乐观"
            mood_emoji = "⚖️"
            mood_color = "#f59e0b"
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
    <meta name="description" content="AI每日投资内参 - 智能新闻分析，股票推荐，市场情绪指数">
    <meta name="keywords" content="AI投资,股票推荐,财经新闻,市场情绪">
    <title>📰 AI 每日投资内参</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📰</text></svg>">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            min-height: 100vh;
            padding: 20px 15px;
            color: #333;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
        }}

        /* 导航栏 */
        .navbar {{
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 15px 30px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        .navbar-brand {{
            font-weight: 700;
            font-size: 1.2em;
            color: #667eea;
        }}

        .navbar-date {{
            color: #666;
            font-size: 0.95em;
        }}

        /* 头部 */
        .header {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            border-top: 4px solid #667eea;
        }}

        .header h1 {{
            font-size: 3em;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
            letter-spacing: 2px;
        }}

        .header .date {{
            color: #888;
            font-size: 1.2em;
            font-weight: 500;
        }}

        /* 情绪卡片 */
        .mood-section {{
            background: linear-gradient(135deg, {mood_color} 0%, #8b5cf6 100%);
            color: white;
            padding: 30px 40px;
            border-radius: 20px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}

        .mood-score {{
            font-size: 3em;
            font-weight: 800;
        }}

        .mood-label {{
            font-size: 1.1em;
            opacity: 0.9;
            margin-bottom: 5px;
        }}

        .mood-bar-container {{
            flex: 1;
            margin: 0 40px;
        }}

        .mood-bar {{
            height: 12px;
            background: rgba(255,255,255,0.3);
            border-radius: 6px;
            overflow: hidden;
        }}

        .mood-bar-fill {{
            height: 100%;
            width: {self.mood_score}%;
            background: white;
            border-radius: 6px;
            transition: width 1s ease;
            animation: fillBar 1.5s ease-out;
        }}

        @keyframes fillBar {{
            from {{ width: 0; }}
            to {{ width: {self.mood_score}%; }}
        }}

        .mood-bar-labels {{
            display: flex;
            justify-content: space-between;
            margin-top: 8px;
            font-size: 0.85em;
            opacity: 0.8;
        }}

        /* 新闻板块 */
        .news-section {{
            background: white;
            border-radius: 20px;
            padding: 35px;
            margin-bottom: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        }}

        .section-title {{
            font-size: 1.6em;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .section-title::after {{
            content: '';
            flex: 1;
            height: 3px;
            background: linear-gradient(90deg, #667eea, transparent);
            border-radius: 2px;
        }}

        .news-item {{
            background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 18px;
            border-left: 4px solid #667eea;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: slideIn 0.6s ease-out forwards;
            opacity: 0;
            transform: translateY(20px);
        }}

        @keyframes slideIn {{
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .news-item:hover {{
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15);
            border-left-color: #764ba2;
        }}

        .news-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }}

        .news-title {{
            font-size: 1.15em;
            font-weight: 600;
            color: #1a1a2e;
            line-height: 1.5;
            flex: 1;
        }}

        .hot-score {{
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            white-space: nowrap;
            margin-left: 15px;
        }}

        .news-meta {{
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .news-source {{
            font-size: 0.85em;
            color: #667eea;
            font-weight: 600;
            background: #e3f2fd;
            padding: 4px 12px;
            border-radius: 12px;
        }}

        .news-summary {{
            color: #555;
            line-height: 1.8;
            font-size: 0.95em;
        }}

        .tag {{
            display: inline-block;
            background: #f3e8ff;
            color: #7c3aed;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
        }}

        /* 股票表格 */
        .stock-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 16px;
            overflow: hidden;
            margin-top: 15px;
        }}

        .stock-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 18px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.95em;
        }}

        .stock-table td {{
            padding: 16px 15px;
            border-bottom: 1px solid #f0f0f0;
            background: #fafbff;
            transition: background 0.2s;
        }}

        .stock-table tr:hover td {{
            background: #f0f4ff;
        }}

        .stock-table tr:last-child td {{
            border-bottom: none;
        }}

        .stock-code {{
            font-family: 'SF Mono', Monaco, monospace;
            font-weight: 600;
            color: #667eea;
        }}

        .stock-name {{
            font-weight: 600;
            color: #1a1a2e;
        }}

        .stock-price {{
            font-weight: 600;
            color: #1a1a2e;
        }}

        .up {{
            color: #ef4444;
            font-weight: 700;
        }}

        .down {{
            color: #22c55e;
            font-weight: 700;
        }}

        .rating {{
            color: #f59e0b;
            font-size: 0.9em;
            letter-spacing: -2px;
        }}

        .recommend-buy {{
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            display: inline-block;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }}

        /* 加密货币板块 */
        .crypto-placeholder {{
            text-align: center;
            padding: 40px 20px;
            color: #888;
            background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
            border-radius: 16px;
        }}

        .crypto-placeholder-icon {{
            font-size: 3em;
            margin-bottom: 15px;
            opacity: 0.5;
        }}

        /* 页脚 */
        .footer {{
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(10px);
            color: white;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 -10px 30px rgba(0,0,0,0.1);
        }}

        .footer p {{
            opacity: 0.7;
            margin-bottom: 8px;
            line-height: 1.6;
        }}

        .footer-links {{
            margin-top: 15px;
            display: flex;
            justify-content: center;
            gap: 20px;
        }}

        .footer-links a {{
            color: rgba(255,255,255,0.7);
            text-decoration: none;
            font-size: 0.9em;
            transition: color 0.2s;
        }}

        .footer-links a:hover {{
            color: white;
        }}

        /* 订阅按钮 */
        .subscribe-btn {{
            display: inline-block;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            padding: 12px 30px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: 600;
            margin-top: 15px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        }}

        .subscribe-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
        }}

        /* 响应式设计 */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}

            .header {{
                padding: 30px 20px;
            }}

            .news-section {{
                padding: 25px 20px;
            }}

            .mood-section {{
                padding: 25px;
                flex-direction: column;
                text-align: center;
                gap: 20px;
            }}

            .mood-bar-container {{
                width: 100%;
                margin: 0;
            }}

            .stock-table {{
                font-size: 0.8em;
                display: block;
                overflow-x: auto;
            }}

            .stock-table th, .stock-table td {{
                padding: 12px 8px;
            }}

            .news-header {{
                flex-direction: column;
                gap: 10px;
            }}

            .hot-score {{
                margin-left: 0;
                align-self: flex-start;
            }}

            .navbar {{
                padding: 12px 20px;
                flex-direction: column;
                gap: 8px;
                text-align: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <nav class="navbar">
            <div class="navbar-brand">📰 AI 每日投资内参</div>
            <div class="navbar-date">{self.date} · {self.weekday_cn}</div>
        </nav>

        <div class="header">
            <h1>AI 每日投资内参</h1>
            <div class="date">您专属的智能财经助手</div>
        </div>

        <div class="mood-section">
            <div>
                <div class="mood-label">今日市场情绪</div>
                <div class="mood-score">{mood_emoji} {self.mood_score}</div>
            </div>
            <div class="mood-bar-container">
                <div class="mood-bar">
                    <div class="mood-bar-fill"></div>
                </div>
                <div class="mood-bar-labels">
                    <span>悲观</span>
                    <span>中性</span>
                    <span>乐观</span>
                </div>
            </div>
            <div style="text-align: right;">
                <div class="mood-label">情绪判断</div>
                <div style="font-size: 1.4em; font-weight: 700;">{mood_label}</div>
            </div>
        </div>

        <div class="news-section">
            <h2 class="section-title">🎯 今日头条</h2>
            {news_html}
        </div>

        <div class="news-section">
            <h2 class="section-title">📈 个股推荐</h2>
            
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
        </div>

        <div class="news-section">
            <h2 class="section-title">💰 加密货币</h2>
            <div class="crypto-placeholder">
                <div class="crypto-placeholder-icon">🔄</div>
                <p>数据更新中...（部署到海外服务器后自动获取）</p>
            </div>
        </div>

        <div class="footer">
            <p>⚠️ 免责声明：本报告由AI自动生成，仅供参考，不构成任何投资建议</p>
            <p>投资有风险，入市需谨慎。请根据自身风险承受能力制定投资策略。</p>
            <p>🤖 Powered by Hermes AI · 每日 9:30 自动更新</p>
            <div class="footer-links">
                <a href="https://github.com/without1022/personal-newspaper" target="_blank">GitHub</a>
                <a href="https://news.without202.com">官网</a>
            </div>
        </div>
    </div>

    <script>
        // 页面加载动画
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('📰 AI每日投资内参已加载');
            
            // 添加平滑滚动
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    document.querySelector(this.getAttribute('href')).scrollIntoView({{
                        behavior: 'smooth'
                    }});
                }});
            }});
        }});
    </script>
</body>
</html>
"""
        return html

    def save_html(self, html: str):
        """保存HTML文件"""
        os.makedirs(CONFIG["output_dir"], exist_ok=True)
        filepath = os.path.join(CONFIG["output_dir"], "index.html")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"✅ HTML已保存到: {filepath}")

    async def run(self):
        """运行完整流程"""
        print("=" * 60)
        print("📰 个人报纸自动生成系统 v2.0")
        print("=" * 60)
        
        await self.fetch_news()
        self.fetch_stocks()
        html = self.generate_html()
        self.save_html(html)
        
        print("\n" + "=" * 60)
        print("✅ 报纸生成完成！")
        print("=" * 60)


if __name__ == "__main__":
    generator = NewspaperGenerator()
    asyncio.run(generator.run())
