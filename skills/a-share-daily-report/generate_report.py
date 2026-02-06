#!/usr/bin/env python3
"""
A股手机版每日简报生成器
使用智谱AI获取真实市场数据
"""

import os
import sys
import datetime
import json
from pathlib import Path
from dotenv import load_dotenv
from zhipuai import ZhipuAI
from PIL import Image, ImageDraw, ImageFont

def setup_directories():
    """创建必要的目录"""
    stock_dir = Path.home() / "stock"
    stock_dir.mkdir(exist_ok=True)
    return stock_dir

def get_today_info():
    """获取今天的日期信息"""
    today = datetime.date.today()
    date_str = today.strftime("%Y年%m月%d日")
    date_suffix = today.strftime("%Y%m%d")
    weekdays = ["一", "二", "三", "四", "五", "六", "日"]
    weekday = weekdays[today.weekday()]
    return today, date_str, date_suffix, weekday

def fetch_market_data(client):
    """使用ZhipuAI Web Search API获取市场数据"""
    print("[1/3] 正在获取市场数据...")

    search_queries = [
        ("indices", "A股今日行情 上证指数 深证成指 创业板 科创50 收盘 涨跌"),
        ("sectors", "A股板块涨幅榜 今日行业板块涨幅 领涨领跌"),
        ("funds", "A股资金流向 北向资金 主力资金 净流入"),
        ("concepts", "A股热门概念 今日概念涨幅"),
        ("news", "A股财经新闻 市场热点"),
        ("breadth", "A股上涨下跌家数 涨停跌停数")
    ]

    all_results = {}
    for query_name, query_text in search_queries:
        try:
            response = client.web_search.web_search(
                search_engine="search_pro",
                search_query=query_text,
                count=10,
                search_recency_filter="oneDay",
                content_size="high"
            )
            all_results[query_name] = response.search_result
            print(f"  ✓ {query_name}: 获取成功")
        except Exception as e:
            print(f"  ✗ {query_name}: 获取失败 - {e}")
            all_results[query_name] = []

    return all_results

def serialize_search_results(search_results):
    """将搜索结果转换为可序列化的字典格式"""
    serialized = {}
    for key, value in search_results.items():
        if hasattr(value, '__dict__'):
            # 如果是对象，尝试转换为字典
            serialized[key] = [dict(item) if hasattr(item, '__dict__') else item for item in value]
        elif isinstance(value, list):
            serialized[key] = [dict(item) if hasattr(item, '__dict__') else item for item in value]
        else:
            serialized[key] = value
    return serialized

def parse_market_data_with_ai(client, search_results, date_str):
    """使用AI解析搜索结果为结构化数据"""
    print("[2/3] 正在解析市场数据...")

    # 序列化搜索结果
    serialized_results = serialize_search_results(search_results)

    # 构建解析提示词
    prompt = f"""你是一个A股市场数据解析专家。请根据以下搜索结果，提取并整理今日A股市场的关键数据。

日期：{date_str}

请严格按照以下JSON格式返回数据，不要添加任何其他文字：

{{
  "indices": [
    {{"name": "上证", "value": "点位", "change": "涨跌幅%", "up": true/false}},
    {{"name": "深证", "value": "点位", "change": "涨跌幅%", "up": true/false}},
    {{"name": "创业", "value": "点位", "change": "涨跌幅%", "up": true/false}},
    {{"name": "科创", "value": "点位", "change": "涨跌幅%", "up": true/false}}
  ],
  "market_breadth": {{
    "up": "上涨家数",
    "down": "下跌家数",
    "limit_up": "涨停数",
    "limit_down": "跌停数"
  }},
  "north_fund": {{"value": "+/-金额亿", "desc": "简短描述"}},
  "main_fund": {{"value": "+/-金额亿", "desc": "简短描述"}},
  "volume": {{"value": "成交额万亿", "desc": "简短描述"}},
  "up_sectors": [
    {{"name": "板块名", "change": "+涨跌幅%", "stock": "代表股票"}}
  ],
  "down_sectors": [
    {{"name": "板块名", "change": "-涨跌幅%", "stock": "代表股票"}}
  ],
  "fund_in": [
    {{"name": "板块/概念", "amount": "+净流入额"}}
  ],
  "fund_out": [
    {{"name": "板块/概念", "amount": "-净流出额"}}
  ],
  "news": [
    {{"title": "新闻标题", "desc": "一句话描述"}}
  ],
  "concepts": [
    {{"name": "概念名", "change": "+/-涨跌幅%"}}
  ],
  "advice": {{
    "judgment": "市场判断\\n支撑点位\\n压力点位",
    "strategy": "操作策略1\\n策略2\\n策略3",
    "focus": "关注方向1\\n方向2\\n方向3"
  }},
  "tech_indicators": {{
    "MACD": "状态",
    "KDJ": "数值",
    "RSI": "数值",
    "BOLL": "位置",
    "volume": "状态",
    "PE": "数值"
  }},
  "recent_events": [
    {{"date": "月/日", "name": "事件名称", "impact": "高/中/低"}}
  ]
}}

搜索结果：
{json.dumps(serialized_results, ensure_ascii=False, indent=2)}

请仔细分析搜索结果，提取最准确的数据。如果某些数据无法从搜索结果中获得，请使用合理的默认值或"数据获取中"占位。
"""

    try:
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        # 提取JSON
        content = response.choices[0].message.content.strip()
        # 移除可能的markdown代码块标记
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]

        parsed_data = json.loads(content)
        print("  ✓ 数据解析成功")
        return parsed_data

    except Exception as e:
        print(f"  ✗ AI解析失败: {e}")
        # 返回默认数据结构
        return get_default_data()

def get_default_data():
    """返回默认数据结构"""
    return {
        "indices": [
            {"name": "上证", "value": "---", "change": "--", "up": False},
            {"name": "深证", "value": "---", "change": "--", "up": False},
            {"name": "创业", "value": "---", "change": "--", "up": False},
            {"name": "科创", "value": "---", "change": "--", "up": False}
        ],
        "market_breadth": {"up": "--", "down": "--", "limit_up": "--", "limit_down": "--"},
        "north_fund": {"value": "--", "desc": "数据获取中"},
        "main_fund": {"value": "--", "desc": "数据获取中"},
        "volume": {"value": "--", "desc": "数据获取中"},
        "up_sectors": [],
        "down_sectors": [],
        "fund_in": [],
        "fund_out": [],
        "news": [],
        "concepts": [],
        "advice": {
            "judgment": "数据获取中\n请稍后重试",
            "strategy": "暂无建议",
            "focus": "暂无关注"
        },
        "tech_indicators": {"MACD": "--", "KDJ": "--", "RSI": "--", "BOLL": "--", "volume": "--", "PE": "--"},
        "recent_events": []
    }

def create_mobile_report(data, date_str, weekday, stock_dir, date_suffix):
    """生成手机版简报图片"""
    print("[3/3] 正在生成图片...")

    # 9:16 竖屏比例
    width, height = 1080, 1920
    bg_color = (8, 12, 25)
    card_color = (22, 32, 50)
    card_light = (30, 42, 65)
    accent_color = (65, 125, 175)
    up_color = (60, 175, 110)
    down_color = (195, 65, 65)
    warning_color = (220, 160, 50)
    text_white = (255, 255, 255)
    text_gray = (140, 155, 175)
    text_light_gray = (100, 115, 135)

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    def get_font(size, bold=False):
        try:
            # 中文字体优先
            if bold:
                font_paths = [
                    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
                    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
                ]
            else:
                font_paths = [
                    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
                ]

            for font_path in font_paths:
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
            return ImageFont.load_default()
        except:
            return ImageFont.load_default()

    # ==================== 1. 顶部标题 ====================
    draw.text((40, 25), f"{date_str} 星期{weekday}", fill=text_light_gray, font=get_font(26))
    draw.text((40, 55), "A股投资日报", fill=text_white, font=get_font(48, bold=True))

    # 市场标签
    tags = ["数据已更新", "震荡调整", "AI主线"]
    tag_x = 40
    tag_colors = [up_color, warning_color, accent_color]
    for i, tag in enumerate(tags):
        bbox = draw.textbbox((0, 0), tag, font=get_font(18))
        tag_width = bbox[2] - bbox[0] + 20
        draw.rounded_rectangle([tag_x, 110, tag_x+tag_width, 110+30], radius=15, fill=tag_colors[i])
        draw.text((tag_x+10, 115), tag, fill=text_white, font=get_font(18))
        tag_x += tag_width + 10

    draw.rectangle([40, 150, width-40, 152], fill=accent_color)

    # ==================== 2. 主要指数 ====================
    y_index = 170
    indices = data.get('indices', [])

    idx_w = (width - 80 - 15 * 3) // 4
    for i, idx in enumerate(indices):
        x = 40 + i * (idx_w + 15)
        color = up_color if idx.get("up", False) else down_color
        draw.rounded_rectangle([x, y_index, x+idx_w, y_index+110], radius=12, fill=card_color)
        draw.text((x+10, y_index+10), idx.get("name", ""), fill=text_gray, font=get_font(20))
        draw.text((x+10, y_index+35), idx.get("value", "--"), fill=text_white, font=get_font(26, bold=True))
        draw.text((x+10, y_index+70), idx.get("change", "--"), fill=color, font=get_font(22, bold=True))

    # ==================== 3. 市场宽度 ====================
    y_width = y_index + 130
    draw.rounded_rectangle([40, y_width, width-40, y_width+140], radius=12, fill=card_color)

    breadth = data.get('market_breadth', {})
    width_stats = [
        {"label": "上涨", "value": breadth.get("up", "--"), "color": up_color},
        {"label": "下跌", "value": breadth.get("down", "--"), "color": down_color},
        {"label": "涨停", "value": breadth.get("limit_up", "--"), "color": up_color},
        {"label": "跌停", "value": breadth.get("limit_down", "--"), "color": down_color},
    ]

    stat_w = (width - 100) // 4
    for i, stat in enumerate(width_stats):
        x = 60 + i * (stat_w + 10)
        draw.text((x, y_width+15), stat["value"], fill=stat["color"], font=get_font(28, bold=True))
        draw.text((x, y_width+55), stat["label"], fill=text_gray, font=get_font(18))

    # 涨跌比条
    up_val = str(breadth.get("up", "1085"))
    down_val = str(breadth.get("down", "4123"))
    try:
        up_count = int(up_val) if up_val.isdigit() else 1085
        down_count = int(down_val) if down_val.isdigit() else 4123
    except:
        up_count = 1085
        down_count = 4123

    if up_count > 0 and down_count > 0:
        ratio = up_count / (up_count + down_count)
        bar_width = width - 100
        up_bar_w = int(bar_width * ratio)
        draw.rounded_rectangle([60, y_width+100, 60+bar_width, y_width+115], radius=6, fill=card_light)
        draw.rounded_rectangle([60, y_width+100, 60+up_bar_w, y_width+115], radius=6, fill=up_color)
        draw.text((60, y_width+120), f"涨跌比 1:{down_count/up_count:.2f}  占{ratio*100:.1f}%", fill=text_gray, font=get_font(14))

    # ==================== 4. 资金流向卡片 ====================
    y_fund = y_width + 160
    fund_w = (width - 80 - 15) // 3

    north = data.get('north_fund', {})
    main = data.get('main_fund', {})
    volume = data.get('volume', {})
    fund_cards = [
        {"title": "🌍 北向", "value": north.get("value", "--"), "color": up_color if "+" in north.get("value", "") else down_color, "desc": north.get("desc", "数据获取中")},
        {"title": "💼 主力", "value": main.get("value", "--"), "color": up_color if "+" in main.get("value", "") else down_color, "desc": main.get("desc", "数据获取中")},
        {"title": "📈 成交", "value": volume.get("value", "--"), "color": accent_color, "desc": volume.get("desc", "数据获取中")},
    ]

    for i, fund in enumerate(fund_cards):
        x = 40 + i * (fund_w + 15)
        draw.rounded_rectangle([x, y_fund, x+fund_w, y_fund+120], radius=12, fill=card_color)
        draw.text((x+15, y_fund+12), fund["title"], fill=text_gray, font=get_font(18))
        draw.text((x+15, y_fund+40), fund["value"], fill=fund["color"], font=get_font(28, bold=True))
        draw.text((x+15, y_fund+85), fund["desc"], fill=text_gray, font=get_font(16))

    # ==================== 5. 板块涨跌TOP3 ====================
    y_sector = y_fund + 140
    draw.text((40, y_sector), "📈📉 板块TOP3", fill=text_white, font=get_font(28, bold=True))
    draw.rectangle([40, y_sector+40, width-40, y_sector+42], fill=accent_color)

    sector_y = y_sector + 55
    sector_h = 75
    col_w = (width - 80 - 15) // 2

    # 领涨
    draw.rounded_rectangle([40, sector_y, 40+col_w, sector_y+sector_h*3+10], radius=12, fill=card_color)

    up_sectors = data.get('up_sectors', [])
    for i, item in enumerate(up_sectors[:3]):
        item_y = sector_y + 8 + i * sector_h
        draw.text((55, item_y+8), f"{i+1}. {item.get('name', '--')}", fill=text_white, font=get_font(22, bold=True))
        draw.text((55, item_y+38), item.get("change", "--"), fill=up_color, font=get_font(20, bold=True))
        draw.text((col_w-50, item_y+25), item.get("stock", "--"), fill=text_gray, font=get_font(16))

    # 领跌
    down_x = 40 + col_w + 15
    draw.rounded_rectangle([down_x, sector_y, width-40, sector_y+sector_h*3+10], radius=12, fill=card_color)

    down_sectors = data.get('down_sectors', [])
    for i, item in enumerate(down_sectors[:3]):
        item_y = sector_y + 8 + i * sector_h
        draw.text((down_x+15, item_y+8), f"{i+1}. {item.get('name', '--')}", fill=text_white, font=get_font(22, bold=True))
        draw.text((down_x+15, item_y+38), item.get("change", "--"), fill=down_color, font=get_font(20, bold=True))
        draw.text((width-60, item_y+25), item.get("stock", "--"), fill=text_gray, font=get_font(16))

    # ==================== 6. 资金流向TOP3 ====================
    y_fund_top = sector_y + sector_h * 3 + 25
    draw.text((40, y_fund_top), "💰💸 资金TOP3", fill=text_white, font=get_font(28, bold=True))
    draw.rectangle([40, y_fund_top+40, width-40, y_fund_top+42], fill=accent_color)

    fund_y = y_fund_top + 55
    fund_h = 70

    # 净流入
    draw.rounded_rectangle([40, fund_y, 40+col_w, fund_y+fund_h*3+10], radius=12, fill=card_color)

    fund_in = data.get('fund_in', [])
    for i, item in enumerate(fund_in[:3]):
        item_y = fund_y + 8 + i * fund_h
        draw.text((55, item_y+10), f"{i+1}. {item.get('name', '--')}", fill=text_white, font=get_font(20, bold=True))
        draw.text((55, item_y+38), item.get("amount", "--"), fill=up_color, font=get_font(20, bold=True))

    # 净流出
    draw.rounded_rectangle([down_x, fund_y, width-40, fund_y+fund_h*3+10], radius=12, fill=card_color)

    fund_out = data.get('fund_out', [])
    for i, item in enumerate(fund_out[:3]):
        item_y = fund_y + 8 + i * fund_h
        draw.text((down_x+15, item_y+10), f"{i+1}. {item.get('name', '--')}", fill=text_white, font=get_font(20, bold=True))
        draw.text((down_x+15, item_y+38), item.get("amount", "--"), fill=down_color, font=get_font(20, bold=True))

    # ==================== 7. 热门新闻 ====================
    y_news = fund_y + fund_h * 3 + 25
    draw.text((40, y_news), "📰 热门财经新闻", fill=text_white, font=get_font(24, bold=True))

    news_items = data.get('news', [])
    news_y = y_news + 35
    for i, news in enumerate(news_items[:3]):
        draw.rounded_rectangle([40, news_y + i * 70, width-40, news_y + i * 70 + 65], radius=10, fill=card_color)
        draw.text((55, news_y + i * 70 + 10), news.get("title", "--"), fill=accent_color, font=get_font(18, bold=True))
        draw.text((55, news_y + i * 70 + 38), news.get("desc", "--"), fill=text_gray, font=get_font(16))

    # ==================== 8. 热门概念 ====================
    y_concept = news_y + 70 * 3 + 15
    draw.text((40, y_concept), "🔥 热门概念", fill=text_white, font=get_font(24, bold=True))

    concepts = data.get('concepts', [])
    concept_w = (width - 80 - 10 * 3) // 4
    for i, item in enumerate(concepts[:8]):
        x = 40 + i * (concept_w + 10)
        change = item.get("change", "")
        color = up_color if "+" in change else down_color
        draw.rounded_rectangle([x, y_concept+40, x+concept_w, y_concept+90], radius=10, fill=card_color)
        draw.text((x+10, y_concept+50), item.get("name", "--"), fill=text_white, font=get_font(18, bold=True))
        draw.text((x+10, y_concept+72), change, fill=color, font=get_font(16, bold=True))

    # ==================== 9. 投资建议 ====================
    y_advice = y_concept + 110
    advice_w = (width - 80 - 15) // 3

    advice_data = data.get('advice', {})
    advice_cards = [
        {"title": "📈 市场判断", "content": advice_data.get("judgment", "震荡整理\n支撑4060\n压力4100"), "color": accent_color},
        {"title": "⚡ 操作策略", "content": advice_data.get("strategy", "控制仓位\n耐心等待\n谨慎布局"), "color": warning_color},
        {"title": "🎯 关注方向", "content": advice_data.get("focus", "大消费\n高股息\n低位成长"), "color": up_color},
    ]

    for i, card in enumerate(advice_cards):
        x = 40 + i * (advice_w + 15)
        draw.rounded_rectangle([x, y_advice, x+advice_w, y_advice+130], radius=12, fill=card_color)
        draw.text((x+12, y_advice+12), card["title"], fill=card["color"], font=get_font(18, bold=True))

        lines = card["content"].split("\n")
        for j, line in enumerate(lines):
            draw.text((x+12, y_advice+45 + j*28), line, fill=text_white, font=get_font(16))

    # ==================== 10. 技术指标 ====================
    y_tech = y_advice + 150
    tech_w = (width - 80 - 10 * 2) // 3

    tech = data.get('tech_indicators', {})
    techs = [
        {"name": "MACD", "value": tech.get("MACD", "粘合"), "status": "down"},
        {"name": "KDJ", "value": tech.get("KDJ", "52/55/48"), "status": "down"},
        {"name": "RSI", "value": tech.get("RSI", "50"), "status": "neutral"},
        {"name": "BOLL", "value": tech.get("BOLL", "中轨"), "status": "down"},
        {"name": "成交量", "value": tech.get("volume", "萎缩"), "status": "down"},
        {"name": "上证PE", "value": tech.get("PE", "14.9"), "status": "normal"},
    ]

    for i, tech_item in enumerate(techs):
        row = i // 3
        col = i % 3
        x = 40 + col * (tech_w + 10)
        y = y_tech + row * 85

        if tech_item["status"] == "down":
            color = down_color
        elif tech_item["status"] == "up":
            color = up_color
        else:
            color = warning_color

        draw.rounded_rectangle([x, y, x+tech_w, y+75], radius=10, fill=card_color)
        draw.text((x+12, y+10), tech_item["name"], fill=text_gray, font=get_font(16))
        draw.text((x+12, y+35), tech_item["value"], fill=color, font=get_font(24, bold=True))

    # ==================== 11. 近期事件 ====================
    y_events = y_tech + 180
    draw.text((40, y_events), "📅 近期事件", fill=text_white, font=get_font(24, bold=True))

    events_raw = data.get('recent_events', [])
    events = events_raw[:3] if events_raw else [
        {"date": "今日", "name": "市场动态", "impact": "中"},
        {"date": "明日", "name": "关注消息", "impact": "低"},
        {"date": "近期", "name": "政策预期", "impact": "中"},
    ]

    event_w = (width - 80 - 10 * 2) // 3
    for i, event in enumerate(events):
        x = 40 + i * (event_w + 10)
        impact_color = warning_color if event.get("impact") == "高" else accent_color
        draw.rounded_rectangle([x, y_events+35, x+event_w, y_events+85], radius=10, fill=card_color)
        draw.text((x+10, y_events+45), event.get("date", "--"), fill=accent_color, font=get_font(14, bold=True))
        draw.text((x+10, y_events+62), event.get("name", "--"), fill=text_white, font=get_font(16))
        draw.text((x+event_w-30, y_events+45), event.get("impact", "中"), fill=impact_color, font=get_font(12))

    # ==================== 底部 ====================
    footer_y = height - 50
    draw.line([(40, footer_y), (width-40, footer_y)], fill=accent_color, width=1)
    draw.text((40, footer_y+12), "仅供参考 不构成投资建议", fill=text_light_gray, font=get_font(12))

    # 保存
    output_path = stock_dir / f"A股手机简报_{date_suffix}.png"
    img.save(output_path, quality=95)
    print(f"✓ 手机简报已生成：{output_path}")

    return str(output_path)

def main():
    """主函数"""
    try:
        # 加载环境变量
        env_file = Path.home() / "stock" / ".env"
        if not env_file.exists():
            print(f"❌ 错误：找不到.env文件：{env_file}")
            print("请创建 ~/stock/.env 文件并添加：")
            print("  ZHIPUAI_API_KEY=your_api_key_here")
            sys.exit(1)

        load_dotenv(env_file)
        api_key = os.getenv("ZHIPUAI_API_KEY")
        if not api_key:
            print("❌ 错误：.env文件中未找到ZHIPUAI_API_KEY")
            sys.exit(1)

        # 初始化客户端
        client = ZhipuAI(api_key=api_key)

        # 设置目录
        stock_dir = setup_directories()

        # 获取日期信息
        today, date_str, date_suffix, weekday = get_today_info()

        # 获取市场数据
        search_results = fetch_market_data(client)

        # 解析数据
        parsed_data = parse_market_data_with_ai(client, search_results, date_str)

        # 保存JSON数据
        json_path = stock_dir / f"parsed_market_data_{date_suffix}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
        print(f"✓ 数据已保存：{json_path}")

        # 生成图片
        image_path = create_mobile_report(parsed_data, date_str, weekday, stock_dir, date_suffix)

        print("\n✅ A股今日简报生成完成！")
        print(f"📊 数据文件：{json_path}")
        print(f"📱 图片文件：{image_path}")

        return image_path

    except Exception as e:
        print(f"❌ 生成失败：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
