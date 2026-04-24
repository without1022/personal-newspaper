#!/usr/bin/env python3
"""
📰 个人报纸自动生成系统
自动采集新闻、AI分析、生成HTML静态页面
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
    "template_file": "./templates/newspaper.html",
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
        
        # 模拟新闻数据（实际部署后换成真实API）
        mock_news = [
            {
                "title": "🍶 白酒概念涨0.64%，主力资金净流入29股",
                "source": "东方财富",
                "summary": "白酒板块今日表现强势，主力资金大幅流入。贵州茅台、五粮液等龙头股均有不错表现。分析认为，随着消费复苏，白酒行业有望迎来新一轮增长周期。",
                "tags": ["白酒", "主力资金"],
                "mood": 0.8
            },
            {
                "title": "💰 两融余额十连升，15股获融资净买入超10亿元",
                "source": "东方财富",
                "summary": "两市融资余额实现十连升，杠杆资金持续入场。15只个股获得融资净买入超10亿元，显示机构投资者对后市持乐观态度。",
                "tags": ["两融", "融资买入"],
                "mood": 0.7
            },
            {
                "title": "🔬 半导体板块持续走强，国产替代进程加速",
                "source": "36氪",
                "summary": "半导体板块今日涨幅居前，中芯国际、北方华创等龙头股表现活跃。随着国内芯片自主可控政策的持续推进，半导体行业迎来历史性发展机遇。",
                "tags": ["半导体", "国产替代"],
                "mood": 0.6
            },
            {
                "title": "🚗 新能源汽车销量超预期30%，产业链受益明显",
                "source": "财新网",
                "summary": "3月份新能源汽车销量同比增长30%，超出市场预期。比亚迪、特斯拉等头部厂商销量创历史新高，产业链上下游公司均有望受益。",
                "tags": ["新能源汽车", "销量"],
                "mood": 0.75
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
            {"code": "002290", "name": "禾盛新材", "price": "81.35", "change": "+10.01%", "recommend": "买入"},
            {"code": "600770", "name": "综艺股份", "price": "6.97", "change": "+9.94%", "recommend": "买入"},
            {"code": "603318", "name": "水发燃气", "price": "11.39", "change": "+10.05%", "recommend": "买入"},
            {"code": "000925", "name": "众合科技", "price": "9.20", "change": "+10.05%", "recommend": "买入"},
            {"code": "300422", "name": "博世科", "price": "5.56", "change": "+20.09%", "recommend": "买入"},
        ]
        
        self.stocks = mock_stocks
        return mock_stocks

    def generate_html(self) -> str:
        """生成HTML页面"""
        print("🎨 正在生成HTML...")

        # 生成新闻HTML
        news_html = ""
        for item in self.news:
            tags_html = "".join([f'<span class="tag">{tag}</span>' for tag in item["tags"]])
            news_html += f"""
            <div class="news-item">
                <div class="news-title">
                    {item['title']}
                </div>
                <span class="news-source">{item['source']}</span>
                {tags_html}
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
                        <td>{stock['code']}</td>
                        <td>{stock['name']}</td>
                        <td>{stock['price']}</td>
                        <td class="up">{stock['change']}</td>
                        <td><span class="recommend-buy">🟢 {stock['recommend']}</span></td>
                    </tr>
            """

        # 情绪判断
        if self.mood_score >= 70:
            mood_label = "乐观"
            mood_emoji = "😊"
        elif self.mood_score >= 50:
            mood_label = "偏乐观"
            mood_emoji = "⚖️"
        else:
            mood_label = "谨慎"
            mood_emoji = "⚠️"

        # 完整HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📰 AI 每日投资内参</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            border-radius: 16px 16px 0 0;
            padding: 30px;
            text-align: center;
            border-bottom: 4px solid #667eea;
        }}

        .header h1 {{
            font-size: 2.5em;
            font-weight: 800;
            color: #1a1a2e;
            margin-bottom: 10px;
            letter-spacing: 2px;
        }}

        .header .date {{
            color: #666;
            font-size: 1.1em;
            font-weight: 500;
        }}

        .mood-section {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .mood-score {{
            font-size: 2em;
            font-weight: 800;
        }}

        .mood-label {{
            font-size: 1.2em;
            opacity: 0.9;
        }}

        .news-section {{
            background: white;
            padding: 30px;
        }}

        .section-title {{
            font-size: 1.5em;
            font-weight: 700;
            color: #1a1a2e;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: inline-block;
        }}

        .news-item {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .news-item:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}

        .news-title {{
            font-size: 1.1em;
            font-weight: 600;
            color: #1a1a2e;
            margin-bottom: 10px;
        }}

        .news-source {{
            font-size: 0.85em;
            color: #667eea;
            font-weight: 500;
            display: inline-block;
            margin-right: 10px;
        }}

        .news-summary {{
            color: #666;
            line-height: 1.6;
            font-size: 0.95em;
        }}

        .stock-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 12px;
            overflow: hidden;
            margin-top: 15px;
        }}

        .stock-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}

        .stock-table td {{
            padding: 15px;
            border-bottom: 1px solid #eee;
            background: #f8f9fa;
        }}

        .stock-table tr:last-child td {{
            border-bottom: none;
        }}

        .up {{
            color: #e74c3c;
            font-weight: 600;
        }}

        .recommend-buy {{
            background: #d4edda;
            color: #155724;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            display: inline-block;
        }}

        .footer {{
            background: #1a1a2e;
            color: white;
            padding: 25px 30px;
            border-radius: 0 0 16px 16px;
            text-align: center;
        }}

        .footer p {{
            opacity: 0.8;
            margin-bottom: 5px;
        }}

        .tag {{
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-right: 5px;
            margin-bottom: 5px;
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .news-section {{
                padding: 20px 15px;
            }}

            .stock-table {{
                font-size: 0.85em;
            }}

            .stock-table th, .stock-table td {{
                padding: 10px 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 AI 每日投资内参</h1>
            <div class="date">{self.date} · {self.weekday_cn}</div>
        </div>

        <div class="mood-section">
            <div>
                <div class="mood-label">今日市场情绪</div>
                <div class="mood-score">{mood_emoji} {self.mood_score} 分</div>
            </div>
            <div style="text-align: right;">
                <div class="mood-label">情绪判断</div>
                <div style="font-size: 1.3em; font-weight: 600;">{mood_label}</div>
            </div>
        </div>

        <div class="news-section">
            <h2 class="section-title">🎯 今日头条</h2>
            {news_html}
        </div>

        <div class="news-section" style="border-top: 1px solid #eee;">
            <h2 class="section-title">📈 个股推荐</h2>
            
            <table class="stock-table">
                <thead>
                    <tr>
                        <th>代码</th>
                        <th>名称</th>
                        <th>现价</th>
                        <th>涨跌幅</th>
                        <th>推荐</th>
                    </tr>
                </thead>
                <tbody>
                    {stocks_html}
                </tbody>
            </table>
        </div>

        <div class="news-section" style="border-top: 1px solid #eee;">
            <h2 class="section-title">💰 加密货币</h2>
            <p style="color: #999; padding: 20px; text-align: center;">
                🔄 数据更新中...（部署到海外服务器后自动获取）
            </p>
        </div>

        <div class="footer">
            <p>⚠️ 免责声明：本报告由AI生成，仅供参考，不构成投资建议</p>
            <p>🤖 Powered by Hermes AI · 每日 9:30 自动更新</p>
        </div>
    </div>
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
        print("📰 个人报纸自动生成系统")
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
