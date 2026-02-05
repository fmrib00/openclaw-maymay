---
name: zai-search
description: Web search using zai-sdk's search API. Use when performing web searches for current information, news, research, or any topics requiring up-to-date online data. Supports domain filtering, time-based filtering, and customizable result counts.
---

# ZAI Web Search

## Quick Start

Perform web searches using zai's search API:

```bash
python skills/zai-search/scripts/zai_search.py \
  --api-key "YOUR_ZAI_API_KEY" \
  --query "your search query"
```

## Usage

### Basic Search

```bash
python skills/zai-search/scripts/zai_search.py \
  --api-key "id.secret" \
  --query "2025年4月的财经新闻"
```

### Advanced Options

**Control result count:**
```bash
--count 15  # 1-50 results, default 10
```

**Filter by domain:**
```bash
--domain "www.sohu.com"  # Only search this domain
```

**Time-based filtering:**
```bash
--recency "one_week"    # Options: noLimit, one_day, one_week, one_month, one_year
```

**Content detail level:**
```bash
--content-size "high"   # Options: low, medium, high (default: medium)
```

### Complete Example

```bash
python skills/zai-search/scripts/zai_search.py \
  --api-key "079182be63a44a99b3df6682bac1b3db.KIXZJPBZ0Ft8oO40" \
  --query "人工智能最新发展" \
  --count 15 \
  --recency "one_month" \
  --content-size "high"
```

## API Key Format

ZAI API keys follow this format: `id.secret`

Example: `079182be63a44a99b3df6682bac1b3db.KIXZJPBZ0Ft8oO40`

## Output Format

Returns JSON with search results including:
- Web page titles
- URLs
- Content summaries
- Relevance scores

## Resources

### scripts/zai_search.py

Executable Python script for performing web searches. Requires the `zhipuai` Python package (usually already installed):

```bash
pip install zhipuai
```

The script can be invoked directly or called from within OpenClaw using the `exec` tool.
