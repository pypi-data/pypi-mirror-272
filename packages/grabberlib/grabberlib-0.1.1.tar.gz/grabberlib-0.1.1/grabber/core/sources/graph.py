import pathlib
from typing import List

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


def get_for_telegraph(
    sources: List[str],
    entity: str,
    telegraph_client: Telegraph,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    **kwargs,
) -> None:
    posts_sent_counter = 0
    titles = set()
    tqdm_sources_iterable = tqdm(
        enumerate(sources),
        total=len(sources),
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
    else:
        final_dest = get_media_root()

    for idx, source_url in tqdm_sources_iterable:
        folder_name = ""
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

        final_dest = final_dest / folder_name

        if not final_dest.exists():
            final_dest.mkdir(parents=True, exist_ok=True)

        folders.add(final_dest)
        unique_img_urls = set()

        for idx, img_tag in enumerate(tags or []):
            img_src = img_tag.attrs[src_attr]
            img_name: str = img_src.split("/")[-1]
            img_name = img_name.strip().rstrip()
            if "images.hotgirl.asia" not in img_src:
                unique_img_urls.add(
                    (f"{idx + 1}-{img_name}", f"https://telegra.ph{img_src}")
                )
            else:
                unique_img_urls.add((f"{idx + 1}-{img_name}", img_src))

        title_folder_mapping[page_title] = (unique_img_urls, final_dest)

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
