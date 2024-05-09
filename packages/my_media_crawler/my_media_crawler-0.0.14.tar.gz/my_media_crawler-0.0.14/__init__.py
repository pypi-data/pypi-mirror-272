# pylint: disable=missing-class-docstring
import config
import db
import git
from base.base_crawler import AbstractCrawler
from media_platform.bilibili import BilibiliCrawler
from media_platform.douyin import DouYinCrawler
from media_platform.kuaishou import KuaishouCrawler
from media_platform.weibo import WeiboCrawler
from media_platform.xhs import XiaoHongShuCrawler
from types import List, str

class CrawlerFactory:
    CRAWLERS = {
        "xhs": XiaoHongShuCrawler,
        "dy": DouYinCrawler,
        "ks": KuaishouCrawler,
        "bili": BilibiliCrawler,
        "wb": WeiboCrawler
    }

    @staticmethod
    def create_crawler(platform: str) -> AbstractCrawler:
        crawler_class = CrawlerFactory.CRAWLERS.get(platform)
        if not crawler_class:
            raise ValueError("Invalid Media Platform Currently only supported xhs or dy or ks or bili ...")
        return crawler_class()

async def media_crawle(
    platform: str,
    login_type: str,
    crawler_type: str,
    start_page: int,
    keywords: List[str]
):
    """
      kick off crawler
    """
    if config.SAVE_DATA_OPTION == "db":
        await db.init_db()

    crawler = CrawlerFactory.create_crawler(platform=platform)
    joined_keywords = ",".join(keywords)
    crawler.init_config(
        platform=platform,
        login_type=login_type,
        crawler_type=crawler_type,
        start_page=start_page,
        keyword=joined_keywords,
    )
    await crawler.start()
    if config.SAVE_DATA_OPTION == "db":
        await db.close()

def __version__() -> str: 
    # Get the Git repository object
    repo = git.Repo(search_parent_directories=True)

    # Get the latest commit hash
    latest_commit = repo.head.commit.hexsha

    # Define your version numbering scheme
    version = "v1.0"

    # Append the short commit hash to the version
    version += "+" + latest_commit[:7]
    return version