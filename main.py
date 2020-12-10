import gevent
from module.handle import Handle
from module.handle import msg
from module.utils import log

city = {
    "全国": "000000",
    # "广东省":"030000",
    # "江苏省":"070000",
    # "浙江省":"080000",
}

search = "Java工程师"

handle = Handle(city=list(city.values()), search=search) #初始化获取 职位名称 & URL
job_urls = handle.job_url_data # 得到职位名称 & URL

# 获取职位详情要求
def work(job_name: str, job_url: str):
    """
    :param job_name: 职位名称：java开发
    :param job_url:  职位Url：https://jobs.51job.com/guangzhou-thq/125427241.html?s=01&t=0
    :return:
    """
    code = handle.get_job_explain(job_name, job_url)
    log(handle.job_explain)
    print(f"code {msg[code]} name: {job_name} url {job_url} job_explain {handle.job_explain}")

def main():
    spawn_list = [gevent.spawn(work, _[0], _[1]) for _ in job_urls]
    gevent.joinall(spawn_list)

if __name__ == '__main__':
    main()
