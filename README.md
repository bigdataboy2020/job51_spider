# job51_spider
前程无忧协程爬虫，分层架构，模块化开发，减少耦合

## 爬虫目标
爬虫字段：`职位名称`、`职位URL`、`职位要求` （逗号分隔 csv 文件）

完整代码：https://github.com/bigdataboy2020/job51_spider

[![mark](https://bigdataboy-cn.oss-cn-shanghai.aliyuncs.com/bigdataboy/20201210/105010058.png)]()

## 爬虫结构
- 分层结构
- 模块化结构，减少耦合

[![mark](https://bigdataboy-cn.oss-cn-shanghai.aliyuncs.com/bigdataboy/20201210/110743497.png)]()

使用模块：`gevent`、`lxml`、`typing`、`requests`


## 项目说明

### 操作类（job51.py）

> 主要包含发送请求的方法

- `def get_data():`请求获取一页所有的`职位名称`和`职位的URL`
- `def get_job_explain():`  获取一个职业的要求

```Python
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
        return True


    def get_job_explain(self, job_name: str, url: str) -> bool:
        """
        # 获取一个职业的要求
        :param job_name: 职位名称
        :param url: 职位的详情页
        :return:
        """
        return True
```

### 中间处理函数（handle.py）
> 主要包含对`请求的数据`进行`处理的函数` 及 `相应错误提示`

- `def get_data(): `获取所有页数的`职位名称`及`职位URL`
- `def get_job_explain():`获取单个职位的详细信息



```
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
```

### 工具类模块（utils.py）
只有一个写入结果的函数
```Python
# 文件写入
def log(msg:Tuple[str,str,List[str]]):
    with open("msg.csv","a",encoding="utf-8") as f:
        f.write(f"{msg[0]},{msg[1]},{msg[2]}\n")
```

### 主文件（main.py）
> 主要启动文件，协程在这支持
