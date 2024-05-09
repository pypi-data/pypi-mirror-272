import pathlib
from typing import List, Optional

from telegraph import Telegraph
from tqdm import tqdm

from grabber.core.settings import get_media_root
from grabber.core.utils import (
    downloader,
    query_mapping,
    headers_mapping,
    get_tags,
    telegraph_uploader,
)


def get_images_from_pagination(url: str, headers: Optional[dict] = None) -> List[str]:
    page_nav_query = "div.page-link-box li a.page-numbers"
    tags, _ = get_tags(url, headers=headers, query=page_nav_query)
    return [a.attrs["href"] for a in tags if tags]


def get_sources_for_4khd(
    sources: List[str],
    entity: str,
    telegraph_client: Telegraph,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    **kwargs,
) -> None:
    send_to_telegram = kwargs.get("send_to_telegram", False)
    titles = set()
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

    if final_dest:
        final_dest = pathlib.Path(final_dest)
        if not final_dest.exists():
            final_dest.mkdir(parents=True, exist_ok=True)

    for idx, source_url in tqdm_sources_iterable:
        current_folder = None
        current_title = None
        folder_name = ""
        urls = [
            source_url,
            *get_images_from_pagination(url=source_url, headers=headers),
        ]
        image_tags = []

        for index, url in enumerate(urls):
            tags, soup = get_tags(
                url,
                headers=headers,
                query=query,
            )
            image_tags.extend(tags or [])

            if index == 0:
                folder_name = soup.select("title")[0].get_text()  # type: ignore
                title = folder_name.strip().rstrip()
                titles.add(title)
                titles_and_folders.add((title, folder_name))
                current_title = title

        if final_dest:
            new_folder = final_dest / folder_name
        else:
            new_folder = get_media_root() / folder_name

        if not new_folder.exists():
            new_folder.mkdir(parents=True, exist_ok=True)

        current_folder = new_folder
        folders.add(current_folder)
        unique_img_urls = set()

        for idx, img_tag in enumerate(image_tags):
            img_src = img_tag.attrs[src_attr]
            img_name: str = img_src.split("/")[-1].split("?")[0]
            img_name = img_name.strip().rstrip()
            unique_img_urls.add((f"{idx + 1}-{img_name}", img_src))
        title_folder_mapping[current_title] = (unique_img_urls, new_folder)

    downloader(title_folder_mapping, headers)
    telegraph_uploader(
        title_folder_mapping=title_folder_mapping,
        send_to_telegram=send_to_telegram,
        save_to_telegraph=save_to_telegraph,
        telegraph_client=telegraph_client,
    )
