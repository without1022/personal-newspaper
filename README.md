# 📰 AI 每日投资内参

> 一个人的报纸，AI驱动的每日投资资讯平台

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/personal-newspaper)

## ✨ 特性

- 🤖 **AI驱动**：自动采集新闻、智能分析、情绪判断
- 📈 **股票推荐**：每日热门股票推荐
- 💰 **加密货币行情**：实时加密货币数据
- 🎨 **精美排版**：专业的报纸风格设计
- ⚡ **自动更新**：GitHub Actions 每日9:30自动生成
- 🌍 **全球部署**：Vercel CDN 全球加速
- 📱 **响应式设计**：完美适配手机/平板/电脑

## 🚀 快速开始

### 1. 生成报纸

```bash
python3 generate.py
```

### 2. 本地预览

```bash
cd docs
python3 -m http.server 8080
```

然后访问: http://localhost:8080

### 3. 部署到 Vercel

1. Fork 本仓库
2. 打开 [Vercel](https://vercel.com)
3. Import 你的仓库
4. 配置 Root Directory 为 `docs`
5. 部署完成！

## ⚙️ 自动更新配置

在 GitHub 仓库设置 Secrets：

```
# 不需要额外配置，GitHub Actions 会自动运行
```

## 📁 项目结构

```
personal-newspaper/
├── docs/
│   └── index.html          # 生成的静态页面
├── generate.py             # 报纸生成脚本
├── requirements.txt        # Python依赖
├── .github/
│   └── workflows/
│       └── daily.yml       # GitHub Actions 自动配置
└── README.md               # 说明文档
```

## 🎯 自定义配置

编辑 `generate.py` 中的 `CONFIG` 字典：

```python
CONFIG = {
    "news_sources": [...],  # 添加你的新闻源
    "output_dir": "./docs", # 输出目录
}
```

## 📄 报纸内容展示

- 📊 **市场情绪指数**：基于新闻AI分析的市场情绪
- 🎯 **今日头条**：每日重要财经新闻
- 📈 **个股推荐**：热门股票推荐
- 💰 **加密货币行情**：BTC/ETH等主流币种

## ⚠️ 免责声明

本报告由AI自动生成，仅供参考，不构成任何投资建议。投资有风险，入市需谨慎。

---

**Powered by Hermes AI 🤖**
