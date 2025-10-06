# 测试不同RSS源的新闻数量
test_feeds = {
    "新浪新闻": "http://rss.sina.com.cn/news/china/focus15.xml",
    "搜狐新闻": "http://rss.news.sohu.com/rss/focus.xml", 
}

def analyze_rss_count():
    import feedparser
    results = {}
    
    for name, url in test_feeds.items():
        try:
            feed = feedparser.parse(url)
            results[name] = len(feed.entries)
            print(f"{name}: {len(feed.entries)} 条")
        except Exception as e:
            print(f"{name}: 获取失败 - {e}")
    
    return results

# 运行测试
counts = analyze_rss_count()