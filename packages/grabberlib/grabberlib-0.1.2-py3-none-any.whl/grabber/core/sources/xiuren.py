import pathlib
from typing import List

import telegraph
from tqdm import tqdm

from grabber.core.settings import get_media_root
from grabber.core.utils import (
    downloader,
    get_pages_from_pagination,
    query_mapping,
    headers_mapping,
    get_tags,
    telegraph_uploader,
)


def get_sources_for_xiuren(
    sources: List[str],
    entity: str,
    telegraph_client: telegraph.Telegraph,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    **kwargs,
) -> None:
    titles = set()
    is_tag: bool = kwargs.get("is_tag", False)
    limit: int = kwargs.get("limit", 0)
    tqdm_sources_iterable = tqdm(
        enumerate(sources),
        total=len(sources),
        desc="Retrieving URLs...",
    )
    query, src_attr = query_mapping[entity]
    headers = headers_mapping.get(entity, None)
    folders = set()
    titles_and_folders = set()
    title_folder_mapping = {}
    posts_sent_counter = 0

    if final_dest:
        final_dest_folder = get_media_root() / final_dest
        if not final_dest_folder.exists():
            final_dest_folder.mkdir(parents=True, exist_ok=True)
            final_dest = final_dest_folder

    for idx, source_url in tqdm_sources_iterable:
        folder_name = ""

        if is_tag:
            urls = get_pages_from_pagination(url=source_url, target="xiuren")
            targets = urls[:limit] if limit else urls
            return get_sources_for_xiuren(
                sources=targets,
                entity=entity,
                final_dest=final_dest,
                save_to_telegraph=save_to_telegraph,
                is_tag=False,
            )

        tags, soup = get_tags(
            source_url,
            headers=headers,
            query=query,
        )

        title_tag = soup.select("title")[0]  # type: ignore
        folder_name = title_tag.get_text().strip().rstrip()
        page_title = folder_name
        titles.add(page_title)
        titles_and_folders.add((page_title, folder_name))

        if final_dest:
            new_folder = get_media_root() / final_dest / folder_name
        else:
            new_folder = get_media_root() / folder_name

        if not new_folder.exists():
            new_folder.mkdir(parents=True, exist_ok=True)

        folders.add(new_folder)
        unique_img_urls = set()

        for idx, img_tag in enumerate(tags or []):
            img_src = img_tag.attrs[src_attr]
            img_name: str = img_src.split("/")[-1]
            img_name = img_name.strip().rstrip()
            unique_img_urls.add((f"{idx + 1}-{img_name}", img_src))

        title_folder_mapping[page_title] = (unique_img_urls, new_folder)
        if save_to_telegraph:
            telegraph_uploader(
                unique_img_urls=unique_img_urls,
                page_title=page_title,
                posts_sent_counter=posts_sent_counter,
                telegraph_client=telegraph_client,
            )
            posts_sent_counter += 1

    if final_dest:
        downloader(
            titles=titles,
            title_folder_mapping=title_folder_mapping,
            headers=headers,
        )
