---
name: technews
description: Fetches top stories from TechMeme and presents them in a clean format. Use when user wants tech news or says /technews.
metadata: {"openclaw":{"emoji":"📰"}}
---

# TechNews Skill

Fetches top stories from TechMeme and presents them in a clean, readable format.

## Usage

**Command:** `/technews` or `technews`

Fetches the top tech news stories from TechMeme RSS feed and displays them with titles, summaries, and links.

## How to Use

### Option 1: Direct command
```bash
~/.openclaw/workspace/skills/technews/scripts/technews.py -n 5
```

### Option 2: Via skill trigger
Simply say `/technews` or "获取科技新闻" and the skill will activate.

## Features

- **Fast RSS-based fetching** - Gets latest stories from TechMeme feed
- **Smart caching** - Avoids duplicate fetches within 2 hours
- **Clean formatting** - Easy to read summaries with links
- **JSON output option** - For programmatic use

## Examples

- `technews` - Show top 5 stories (default)
- `technews -n 10` - Show top 10 stories
- `technews --json` - Output in JSON format

## What It Does

1. Fetches latest stories from TechMeme RSS feed
2. Parses and extracts titles, summaries, and links
3. Formats output for easy reading
4. Caches results to avoid redundant fetches

## State

- `~/.cache/technews/stories.json` - Cache of recently fetched stories

## Requirements

✅ All dependencies installed:
- Python 3.9+
- requests (2.31.0)
- beautifulsoup4 (4.14.3)

## Script Files

- `techmeme_scraper.py` - TechMeme RSS fetcher
- `article_fetcher.py` - Article content extractor (for future use)
- `technews.py` - Main workflow script

## Future Enhancements

- Full article fetching and AI summarization
- Social media reaction extraction
- Multiple source support (Hacker News, Reddit)
- Custom topic filtering
