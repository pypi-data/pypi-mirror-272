import asyncio
from time import sleep
from typing import List

from telegraph import Telegraph
from tqdm import tqdm

from grabber.core.bot.core import send_message
from grabber.core.utils import (
    create_html_template,
    create_page,
    query_mapping,
    headers_mapping,
    get_tags,
    get_soup,
)


def get_pages_from_pagination(url: str) -> List[str]:
    pagination_pages_query = "div.oceanwp-pagination.clr ul.page-numbers a.page-numbers"
    articles_from_pagination_query = "div.entries article.blog-entry a"
    next_page_url_base = f"{url}page/"
    source_urls = set()
    
    first_page = get_soup(url)
    articles = set(first_page.select(articles_from_pagination_query))
    pages = first_page.select(pagination_pages_query)

    if pages:
        pages_links = set()
        last_page = pages[-2]
        number_last_page = last_page.text
        for idx in range(2, int(number_last_page) + 1):
            pages_links.add(f"{next_page_url_base}{idx}")

        for link in pages_links:
            soup = get_soup(link)
            articles.update(set(soup.select(articles_from_pagination_query)))

    for a_tag in articles:
        if a_tag is not None and a_tag.attrs["href"] not in source_urls:
            source_urls.add(a_tag.attrs["href"])

    return source_urls


def get_sources_for_everia(
    sources: List[str],
    entity: str,
    telegraph_client: Telegraph,
    **kwargs,
) -> None:
    is_tag = kwargs.get('is_tag', False)
    query, src_attr = query_mapping[entity]
    headers = headers_mapping.get(entity, None)
    title = None
    posted_title = False

    if is_tag:
        soup = get_soup(target_url=sources[0], headers=headers)
        title = soup.get_text(strip=True).split(" – EVERIA.CLUB")[0]
        sources = list(get_pages_from_pagination(sources[0]))

    tqdm_sources_iterable = tqdm(
        enumerate(sources),
        total=len(sources),
        desc="Retrieving URLs...",
    )
    is_tag = kwargs.get('is_tag', False)
    posts_sent_counter = 0

    for idx, source_url in tqdm_sources_iterable:
        image_tags, soup = get_tags(source_url, headers=headers, query=query)
        page_title = soup.get_text(strip=True).split(" – EVERIA.CLUB")[0]

        if title is None:
            title = soup.get_text(strip=True)

        unique_img_urls = set()

        for idx, img_tag in enumerate(image_tags):
            img_src = img_tag.attrs[src_attr]
            img_name: str = img_src.split("/")[-1].split("?")[0]
            img_name = img_name.strip().rstrip()
            unique_img_urls.add((f"{page_title} {idx + 1}", img_src))

        html_post = create_html_template(unique_img_urls)
        post_url = create_page(title=page_title, html_content=html_post, telegraph_client=telegraph_client)
        telegraph_post_link = f"{page_title} - {post_url}"

        if posts_sent_counter == 10:
            sleep(10)

        try:
            if not posted_title:
                asyncio.run(send_message(title))
                posted_title = True

            asyncio.run(send_message(telegraph_post_link))
            posts_sent_counter += 1
        except Exception:
            sleep(20)
            asyncio.run(send_message(telegraph_post_link))

