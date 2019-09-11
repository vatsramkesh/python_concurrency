
import pathlib
from typing import IO
import urllib.error
import urllib.parse
import sys

import re
import logging
import asyncio
from aiohttp import ClientSession
import aiofiles

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("areq")
logging.getLogger("chardet.charsetprober").disabled = True

HREF_RE = re.compile(r'href="(.*?)"')


def main():
    file_path = pathlib.Path(__file__).parent
    with open(file_path.joinpath("urls.txt")) as f:
        urls = set(map(str.strip, f))

    outpath = file_path.joinpath("foundurls.txt")
    with open(outpath, "w") as outfile:
        outfile.write("source_url\tparsed_url\n")

    asyncio.run(bulk_crawl_and_write(outfile, urls))


async def bulk_crawl_and_write(file, urls: set):
    async with ClientSession() as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(
                    file=file, url=url, session=session
                )
            )
        await asyncio.gather(*tasks)


async def fetch_url(url: str, session: ClientSession):
    resp = await session.request(method="GET", url=url)
    print(resp)
    resp.raise_for_status()
    logger.info("Got response [%s] for URL: %s", resp.status, url)
    text = await resp.text()
    return text


async def parse_html(url: str, session: ClientSession):
    found = set()
    try:
        text_response = await fetch_url(url=url, session=session)
    except (
            aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError
    ) as e:
        logger.error(
            "aiohttp exception for %s [%s]: %s",
            url,
            getattr(e, "status", None),
            getattr(e, "message", None),
        )
        return found
    except Exception as e:
        logger.exception(
            "Non-aiohttp exception occured:  %s", getattr(e, "__dict__", {})
        )
        return found
    else:
        for href in HREF_RE.findall(text_response):
            try:
                abslink = urllib.parse.urljoin(url, href)
            except (urllib.error.URLError, ValueError):
                logger.exception("Error parsing URL: %s", href)
                pass
            else:
                found.add(abslink)
        logger.info("Found %d links for %s", len(found), url)
        return found


async def write_one(file, url: str, session: ClientSession):
    res = await fetch_url(
        url=url, session=session
    )
    if not res:
        return None
    async with aiofiles.open(file, 'a') as f:
        for content in res:
            await f.write(f"{url}\t{content}\n")
        logger.info("Wrote results for source URL: %s", url)


main()

# https://docs.python.org/3/this-url-will-404.html
# https://www.bloomberg.com/markets/economics
