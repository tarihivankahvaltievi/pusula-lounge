#!/usr/bin/env python3
"""Check that published sitemap URLs are directly indexable and self-canonical."""
import concurrent.futures
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ORIGIN = 'https://www.pusulalounge.com'
NS = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.robots = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and 'canonical' in attrs.get('rel', '').lower().split():
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'meta' and attrs.get('name', '').lower() in ('robots', 'googlebot'):
            self.robots.append(attrs.get('content', ''))


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Pusula-SEO-Audit/1.0'})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.geturl(), response.headers, response.read()


def check(url):
    try:
        final, headers, body = fetch(url)
        issues = []
        if final != url:
            issues.append('redirects to ' + final)
        if 'text/html' not in headers.get('Content-Type', '').lower():
            issues.append('response is not HTML')
        meta = Metadata()
        meta.feed(body.decode(headers.get_content_charset() or 'utf-8', errors='replace'))
        if meta.canonicals != [url]:
            issues.append('canonical: ' + repr(meta.canonicals))
        directives = ','.join(meta.robots + headers.get_all('X-Robots-Tag', [] )).lower()
        if any(word in directives for word in ('noindex', 'none', 'nosnippet')):
            issues.append('restrictive robots directive: ' + directives)
        return url, issues
    except (OSError, ValueError, urllib.error.URLError) as exc:
        return url, [str(exc)]


def main():
    sitemap = ORIGIN + '/sitemap.xml'
    final, _, body = fetch(sitemap)
    if final != sitemap:
        raise ValueError('Sitemap redirected to ' + final)
    urls = [element.text for element in ET.fromstring(body).findall('s:url/s:loc', NS)]
    if not urls or len(urls) != len(set(urls)):
        raise ValueError('Sitemap has no URLs or contains duplicates')
    if any(not url or urllib.parse.urlsplit(url).scheme != 'https' or
           urllib.parse.urlsplit(url).netloc != urllib.parse.urlsplit(ORIGIN).netloc for url in urls):
        raise ValueError('Sitemap contains a URL outside the canonical HTTPS origin')
    errors = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for url, issues in pool.map(check, urls):
            if issues:
                errors += 1
                print(f'FAIL {url}: {"; ".join(issues)}')
    print(f'Checked {len(urls)} live sitemap URLs; {errors} failed.')
    return 1 if errors else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, ET.ParseError) as exc:
        sys.exit(f'Live audit failed: {exc}')
