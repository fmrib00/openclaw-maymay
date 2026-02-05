#!/usr/bin/env python3
"""
ZAI Web Search Script
Uses zai-sdk's web_search API to perform searches.
"""

import sys
import json
import argparse
import traceback
from zhipuai import ZhipuAI

def zai_web_search(api_key, query, count=10, search_engine="search_pro",
                   search_domain_filter=None, search_recency_filter="noLimit",
                   content_size="medium"):
    """
    Perform web search using ZhipuAI SDK.

    Args:
        api_key: ZhipuAI API key (format: id.secret)
        query: Search query string
        count: Number of results (1-50, default 10)
        search_engine: Search engine to use (default "search_pro")
        search_domain_filter: Filter results to specific domain
        search_recency_filter: Time filter (noLimit, one_day, one_week, one_month, one_year)
        content_size: Content size (low, medium, high)

    Returns:
        dict: Search results
    """
    try:
        client = ZhipuAI(api_key=api_key)

        # Build parameters
        params = {
            "search_engine": search_engine,
            "search_query": query,
            "count": count,
            "search_recency_filter": search_recency_filter,
            "content_size": content_size
        }

        if search_domain_filter:
            params["search_domain_filter"] = search_domain_filter

        # Execute search
        response = client.web_search.web_search(**params)

        # Manual extraction to avoid serialization issues
        results = []
        for item in getattr(response, 'search_result', []):
            results.append({
                "title": getattr(item, 'title', ''),
                "link": getattr(item, 'link', ''),
                "content": getattr(item, 'content', ''),
                "media": getattr(item, 'media', ''),
                "publish_date": getattr(item, 'publish_date', ''),
                "refer": getattr(item, 'refer', '')
            })

        return {
            "request_id": getattr(response, 'request_id', ''),
            "search_intent": [
                {
                    "query": getattr(si, 'query', ''),
                    "intent": getattr(si, 'intent', ''),
                    "keywords": getattr(si, 'keywords', '')
                }
                for si in getattr(response, 'search_intent', [])
            ],
            "search_results": results
        }

    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}

def main():
    parser = argparse.ArgumentParser(description="ZAI Web Search")
    parser.add_argument("--api-key", required=True, help="ZAI API key")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--count", type=int, default=10, help="Number of results (1-50)")
    parser.add_argument("--domain", help="Filter to specific domain")
    parser.add_argument("--recency", default="noLimit",
                       choices=["noLimit", "one_day", "one_week", "one_month", "one_year"],
                       help="Time filter")
    parser.add_argument("--content-size", default="medium",
                       choices=["low", "medium", "high"],
                       help="Content size")

    args = parser.parse_args()

    result = zai_web_search(
        api_key=args.api_key,
        query=args.query,
        count=args.count,
        search_domain_filter=args.domain,
        search_recency_filter=args.recency,
        content_size=args.content_size
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
