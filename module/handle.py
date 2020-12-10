from module.job51 import Job51
from typing import List, Dict, Tuple


msg = {
    1: "获取成功",
    -1: "获取职位链接获取失败",
    -2: "获取职位详情失败"
}

class Handle(object):
    job = Job51()
    job_num = 0  # job 总个数
    job_explain: Tuple[str, str, List[str]] = None
    # Job_name 和 url 列表
    job_url_data: List[Tuple[str, str]] = list()

    def __init__(self, city: List[str], search: str):
        self.get_data(city, search)

    def get_data(self, city: List[str], search: str):
        """
        # 获取所有页数的职位名称及URL
        :param city: 城市列表
        :param search: 搜索词
        :return:
        """
        # 获取职位详情链接
        while self.job.page_num <= self.job.all_page:
            if not self.job.get_data(str(self.job.page_num), city, search):
                return -1
            self.job.page_num += 1
        # 总Job个数
        self.job_num = self.job.job_url_data.__len__()
        self.job_url_data = self.job.job_url_data

    def get_job_explain(self, job_name: str, job_url: str):
        """
        # 获取单个职位的详细信息
        :param job_name: 城市名称
        :param job_url: 城市url
        :return:
        """
        job_url_data = self.job.job_url_data
        self.job_len = job_url_data.__len__()
        if not self.job.get_job_explain(job_name, job_url):
            return -2
        self.job_explain = self.job.job_explain
        return 1



