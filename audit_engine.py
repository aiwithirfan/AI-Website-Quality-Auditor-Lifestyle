import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


SOCIAL_DOMAINS = (
    "facebook.com", "instagram.com", "youtube.com", "tiktok.com",
    "linkedin.com", "pinterest.com", "x.com", "twitter.com"
)

CTA_TERMS = (
    "book", "booking", "shop", "buy", "order", "subscribe", "sign up",
    "contact", "get started", "learn more", "schedule", "reserve",
    "appointment", "join", "download", "discover"
)

CONTACT_TERMS = (
    "contact", "email", "mailto:", "phone", "tel:", "address",
    "location", "reach us"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0 Safari/537.36"
    )
}


def normalize_url(url: str) -> str:
    url = url.strip()
    if not re.match(r"^https?://", url, flags=re.I):
        url = "https://" + url
    return url


def _same_domain(url_a: str, url_b: str) -> bool:
    a = urlparse(url_a).netloc.lower().replace("www.", "")
    b = urlparse(url_b).netloc.lower().replace("www.", "")
    return a == b


def _is_social(url: str) -> bool:
    host = urlparse(url).netloc.lower().replace("www.", "")
    return any(host == d or host.endswith("." + d) for d in SOCIAL_DOMAINS)


def _has_contact_form(soup: BeautifulSoup) -> bool:
    for form in soup.find_all("form"):
        text = form.get_text(" ", strip=True).lower()
        fields = [x.get("name", "").lower() for x in form.find_all(["input", "textarea"])]
        joined = " ".join(fields) + " " + text
        if any(term in joined for term in ("email", "message", "contact", "phone", "name")):
            return True
    return False


def _count_ctas(soup: BeautifulSoup) -> int:
    count = 0
    for element in soup.find_all(["a", "button", "input"]):
        text = element.get_text(" ", strip=True).lower()
        value = element.get("value", "").lower()
        aria = element.get("aria-label", "").lower()
        label = " ".join([text, value, aria])
        if any(term in label for term in CTA_TERMS):
            count += 1
    return count


def audit_website(url: str) -> dict:
    url = normalize_url(url)

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=20,
        allow_redirects=True,
    )
    response.raise_for_status()

    final_url = response.url
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.get_text(" ", strip=True) if soup.title else ""

    all_links = []
    internal_links = []
    social_links = []

    for tag in soup.find_all("a", href=True):
        href = urljoin(final_url, tag["href"].strip())
        if href.startswith(("mailto:", "tel:")):
            all_links.append(href)
            continue

        parsed = urlparse(href)
        if parsed.scheme not in ("http", "https"):
            continue

        all_links.append(href)

        if _same_domain(href, final_url):
            clean = href.split("#")[0].rstrip("/")
            if clean and clean != final_url.rstrip("/"):
                internal_links.append(clean)

        if _is_social(href):
            social_links.append(href)

    internal_links = sorted(set(internal_links))
    social_links = sorted(set(social_links))

    page_text = soup.get_text(" ", strip=True)
    lower_text = page_text.lower()

    has_contact_info = any(term in lower_text for term in CONTACT_TERMS)
    has_viewport_meta = soup.find(
        "meta",
        attrs={"name": lambda x: x and x.lower() == "viewport"}
    ) is not None

    styles = " ".join(
        style.get_text(" ", strip=True).lower()
        for style in soup.find_all("style")
    )
    linked_css = " ".join(
        link.get("href", "").lower()
        for link in soup.find_all("link", href=True)
        if "stylesheet" in (link.get("rel") or [])
    )
    responsive_css_indicators = bool(
        re.search(r"@media|width\s*:\s*100%|max-width|flex|grid", styles + linked_css)
    )

    headings = [
        h.get_text(" ", strip=True)
        for h in soup.find_all(["h1", "h2", "h3"])
    ][:20]

    summary_text = " ".join(page_text.split())[:5000]

    return {
        "url": url,
        "final_url": final_url,
        "status_code": response.status_code,
        "https": final_url.lower().startswith("https://"),
        "title": title,
        "internal_links_count": len(internal_links),
        "sample_internal_links": internal_links[:25],
        "social_links_count": len(social_links),
        "social_platforms": sorted({
            urlparse(x).netloc.lower().replace("www.", "")
            for x in social_links
        }),
        "has_contact_info": has_contact_info,
        "has_contact_form": _has_contact_form(soup),
        "cta_count": _count_ctas(soup),
        "has_viewport_meta": has_viewport_meta,
        "responsive_css_indicators": responsive_css_indicators,
        "h1_h2_h3_sample": headings,
        "text_summary": summary_text,
    }
