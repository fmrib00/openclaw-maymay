#!/usr/bin/env python3
"""搜索川渝小吃店信息"""

from zhipuai import ZhipuAI

api_key = "079182be63a44a99b3df6682bac1b3db.KIXZJPBZ0Ft8oO40"
client = ZhipuAI(api_key=api_key)

try:
    print("搜索川渝小吃店...")
    result = client.web_search.web_search(
        search_engine="search_pro",
        search_query="台北川渝小吃店 订位电话 中山站",
        count=5,
        search_recency_filter="noLimit",
        content_size="high"
    )

    print("\n✅ 搜索成功！")
    print("\n搜索结果:")
    print("=" * 80)

    for i, item in enumerate(result.search_result, 1):
        print(f"\n【结果 {i}】")
        print(f"标题: {item.title}")
        print(f"链接: {item.link}")
        print(f"媒体: {item.media}")
        print(f"发布时间: {item.publish_date}")
        print(f"内容摘要: {item.content[:200]}...")

except Exception as e:
    print(f"搜索失败: {e}")
