import os
import pathlib
from pathlib import Path

from dotenv import load_dotenv
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, RunReportRequest
from cachetools.func import ttl_cache
from time import sleep


class 统计类:
    def __init__(self) -> None:
        # 载入 .env 文件
        load_dotenv(pathlib.Path(__file__).parent / "生成器" / ".env")
        self.property_id = os.getenv("PROPERTY_ID")

    @ttl_cache(ttl=60 * 60 * 1, maxsize=1)
    def 获得统计信息(self) -> tuple[int, int]:
        client = BetaAnalyticsDataClient()

        request = RunReportRequest(
            property=f"properties/{self.property_id}",
            metrics=[Metric(name="activeUsers"), Metric(name="screenPageViews")],
            # GA4（新版） 统计创建于 2022-12-10
            date_ranges=[DateRange(start_date="2022-12-10", end_date="today")],
        )
        response = client.run_report(request)
        # UA （旧版） 统计在 2019-12-04 到 2022-12-10 共 171,701 用户
        active_users: int = int(response.rows[0].metric_values[0].value) + 171701
        # UA （旧版） 统计在 2019-12-04 到 2022-12-10 共 831,318 次浏览
        page_views: int = int(response.rows[0].metric_values[1].value) + 831318
        return (active_users, page_views)


if __name__ == "__main__":
    谷歌统计 = 统计类()
    for i in range(20):
        print(谷歌统计.获得统计信息())
        sleep(1)
