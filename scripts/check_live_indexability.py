#!/usr/bin/env python3
"""Check that published sitemap URLs are directly indexable and self-canonical."""
import concurrent.futures
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser

ORIGIN = 'https://www.pusulalounge.com'
NS = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9',
      'x': 'http://www.w3.org/1999/xhtml'}
IMAGE_NS = {'i': 'http://www.google.com/schemas/sitemap-image/1.1'}


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.robots = []
        self.alternates = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link':
            rel = attrs.get('rel', '').lower().split()
            if 'canonical' in rel:
                self.canonicals.append(attrs.get('href', ''))
            if 'alternate' in rel and 'hreflang' in attrs:
                self.alternates.append((attrs['hreflang'], attrs.get('href', '')))
        if tag == 'meta' and attrs.get('name', '').lower() in ('robots', 'googlebot'):
            self.robots.append(attrs.get('content', ''))


class Assets(HTMLParser):
    """Collect same-origin resources needed to render crawlable page content."""
    def __init__(self, page_url):
        super().__init__()
        self.page_url = page_url
        self.urls = set()

    def add(self, value):
        if not value:
            return
        url = urljoin(self.page_url, value)
        if urlsplit(url).netloc == urlsplit(ORIGIN).netloc and urlsplit(url).scheme == 'https':
            self.urls.add(url)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('img', 'source', 'script', 'video'):
            self.add(attrs.get('src'))
        if tag == 'video':
            self.add(attrs.get('poster'))
        if tag == 'link':
            rel = set(attrs.get('rel', '').lower().split())
            if rel.intersection({'stylesheet', 'preload', 'icon', 'apple-touch-icon', 'manifest'}):
                self.add(attrs.get('href'))
        for candidate in attrs.get('srcset', '').split(','):
            self.add(candidate.strip().split()[0] if candidate.strip() else '')


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Pusula-SEO-Audit/1.0'})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.geturl(), response.headers, response.read()


def check(url, alternates):
    try:
        final, headers, body = fetch(url)
        issues = []
        if final != url:
            issues.append('redirects to ' + final)
        if 'text/html' not in headers.get('Content-Type', '').lower():
            issues.append('response is not HTML')
        meta = Metadata()
        html = body.decode(headers.get_content_charset() or 'utf-8', errors='replace')
        meta.feed(html)
        if meta.canonicals != [url]:
            issues.append('canonical: ' + repr(meta.canonicals))
        if sorted(meta.alternates) != sorted(alternates):
            issues.append('HTML hreflang does not match the sitemap')
        directives = ','.join(meta.robots + headers.get_all('X-Robots-Tag', [] )).lower()
        if any(word in directives for word in ('noindex', 'none', 'nosnippet')):
            issues.append('restrictive robots directive: ' + directives)
        assets = Assets(url)
        assets.feed(html)
        return url, issues, assets.urls
    except (OSError, ValueError, urllib.error.URLError) as exc:
        return url, [str(exc)], set()


def check_asset(url, image=False):
    try:
        final, headers, _ = fetch(url)
        issues = []
        if final != url:
            issues.append('redirects to ' + final)
        if image and not headers.get('Content-Type', '').lower().startswith('image/'):
            issues.append('sitemap image is not served as an image: ' + headers.get('Content-Type', 'missing Content-Type'))
        return url, issues
    except (OSError, ValueError, urllib.error.URLError) as exc:
        return url, [str(exc)]


def main():
    sitemap = ORIGIN + '/sitemap.xml'
    robots_url = ORIGIN + '/robots.txt'
    robots_final, robots_headers, robots_body = fetch(robots_url)
    if robots_final != robots_url:
        raise ValueError('robots.txt redirected to ' + robots_final)
    if 'text/plain' not in robots_headers.get('Content-Type', '').lower():
        raise ValueError('robots.txt is not served as plain text')
    robots = RobotFileParser()
    robots.parse(robots_body.decode('utf-8', errors='replace').splitlines())
    if sitemap not in (robots.site_maps() or []):
        raise ValueError('robots.txt does not declare the canonical sitemap')

    final, sitemap_headers, body = fetch(sitemap)
    if final != sitemap:
        raise ValueError('Sitemap redirected to ' + final)
    if 'xml' not in sitemap_headers.get('Content-Type', '').lower():
        raise ValueError('sitemap is not served as XML')
    root = ET.fromstring(body)
    urls = [element.text for element in root.findall('s:url/s:loc', NS)]
    if not urls or len(urls) != len(set(urls)):
        raise ValueError('Sitemap has no URLs or contains duplicates')
    if any(not url or urllib.parse.urlsplit(url).scheme != 'https' or
           urllib.parse.urlsplit(url).netloc != urllib.parse.urlsplit(ORIGIN).netloc for url in urls):
        raise ValueError('Sitemap contains a URL outside the canonical HTTPS origin')
    image_urls = {element.text for element in root.findall('.//i:loc', IMAGE_NS)}
    if any(not url or urllib.parse.urlsplit(url).scheme != 'https' or
           urllib.parse.urlsplit(url).netloc != urllib.parse.urlsplit(ORIGIN).netloc for url in image_urls):
        raise ValueError('Sitemap contains an image outside the canonical HTTPS origin')
    alternates = {
        entry.findtext('s:loc', namespaces=NS): [
            (link.attrib['hreflang'], link.attrib['href'])
            for link in entry.findall('x:link[@rel="alternate"]', NS)
        ]
        for entry in root.findall('s:url', NS)
    }
    errors = []
    for url, links in alternates.items():
        languages = dict(links)
        if links and (len(languages) != len(links) or url not in languages.values()
                      or any(dict(alternates.get(target, [])) != languages for target in languages.values())):
            errors.append((url, ['sitemap hreflang group is incomplete or non-reciprocal']))
        blocked = [bot for bot in ('Googlebot', 'Bingbot', 'OAI-SearchBot')
                   if not robots.can_fetch(bot, url)]
        if blocked:
            errors.append((url, ['robots.txt blocks ' + ', '.join(blocked)]))
    assets = set(image_urls)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for url, issues, found_assets in pool.map(lambda url: check(url, alternates[url]), urls):
            assets.update(found_assets)
            if issues:
                errors.append((url, issues))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for url, issues in pool.map(lambda asset: check_asset(asset, asset in image_urls), sorted(assets)):
            if issues:
                errors.append((url, issues))
    for url, issues in errors:
        print(f'FAIL {url}: {"; ".join(issues)}')
    print(f'Checked {len(urls)} live sitemap URLs and {len(assets)} same-origin assets; {len(errors)} failed.')
    return 1 if errors else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, ET.ParseError) as exc:
        sys.exit(f'Live audit failed: {exc}')
