import requests
from lxml import etree
from typing import List, Tuple
from requests.utils import quote


class Job51(object):
    # 总页数。第一次获取会设置真实页数
    all_page = 9999
    # 正在获取的页数
    page_num = 1
    # Job_name 和 url 列表
    job_url_data: List[Tuple[str, str]] = list()
    # 职位详情页列表 [name,url,说明]
    job_explain: Tuple[str, str, List[str]] = None

    session = requests.session()


    def get_data(self, page_num: str, city: List[str], search: str) -> bool:
        """
        # 获取该关键词所有的 职位名称与链接
        :param page_num: 当前页数
        :param city: 城市列表
        :param search: 搜索词
        :return:
        """
        r = self.session.get(
            url=f"https://search.51job.com/list/{'%252c'.join(city)},000000,0000,00,9,99,{quote(search)},2,{page_num}.html",
            headers={
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Host": "search.51job.com",
                "Referer": "https://www.51job.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            },
            params={
                "lang": "c",
                "postchannel": "0000",
                "workyear": "99",
                "cotype": "99",
                "degreefrom": "99",
                "jobterm": "99",
                "companysize": "99",
                "ord_field": "0",
                "dibiaoid": "0",
                "line": "",
                "welfare": "",
            }
        )
        self.all_page = int(r.json().get("total_page")) # 设置全部页码
        print(f"第 {page_num} \\ {self.all_page} 页获取完成。。。链接：{r.url}")

        for _ in r.json().get("engine_search_result"):
            # 这个 json 里面有其他很多信息，比如 工资 地区
            self.job_url_data.append((_.get("job_name"), _.get("job_href")))
        return True


    def get_job_explain(self, job_name: str, url: str) -> bool:
        """
        # 获取一个职业的要求
        :param job_name: 职位名称
        :param url: 职位的详情页
        :return:
        """
        r = self.session.get(
            url=url,
            headers={
                "Accept": "atext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Host": "search.51job.com",
                "Connection": "keep-alive",
                "Referer": "https://www.51job.com/",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
            },
        )
        r.encoding = r.apparent_encoding
        html = etree.HTML(r.text)
        job_str = html.xpath(r'//div[@class="tBorderTop_box"]/div[@class="bmsg job_msg inbox"]/p/text()')
        self.job_explain = (job_name, url, job_str)
        return True
