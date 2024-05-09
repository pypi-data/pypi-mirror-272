import multiprocessing
import pathlib
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import List

import telegraph
from tqdm import tqdm

from grabber.core.settings import get_media_root
from grabber.core.utils import (
    get_pages_from_pagination,
    print_albums_message,
    query_mapping,
    headers_mapping,
    get_tags,
    download_images,
    upload_to_telegraph,
)

DEFAULT_THREADS_NUMBER = multiprocessing.cpu_count()


def get_sources_for_xiuren(
    sources: List[str],
    entity: str,
    telegraph_client: telegraph.Telegraph,
    final_dest: str | pathlib.Path = "",
    save_to_telegraph: bool | None = False,
    **kwargs,
) -> None:
    send_to_telegram = kwargs.get("send_to_telegram", False)
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
        title = folder_name
        titles.add(title)
        titles_and_folders.add((title, folder_name))

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

        title_folder_mapping[title] = (unique_img_urls, new_folder)

    futures = []
    with ThreadPoolExecutor(max_workers=DEFAULT_THREADS_NUMBER) as executor:
        for title, (images_set, folder_dest) in title_folder_mapping.items():
            partial_download = partial(
                download_images,
                new_folder=folder_dest,
                headers=headers,
                title=title,
            )
            future = executor.submit(partial_download, images_set)
            futures.append(future)

    for future in tqdm(
        futures,
        total=len(futures),
        desc="Finishing download...",
    ):
        future.result()

    posts = []
    if save_to_telegraph:
        for title, (_, folder_dest) in title_folder_mapping.items():
            posts.append(
                upload_to_telegraph(
                    folder_dest,
                    page_title=title,
                    send_to_telegram=send_to_telegram,
                    telegraph_client=telegraph_client,
                )
            )

    albums_file = pathlib.Path(get_media_root() / "assets/pages.txt")
    if albums_file.exists():
        albums_links = albums_file.read_text().split("\n")
    else:
        albums_links = posts

    print_albums_message(albums_links)
