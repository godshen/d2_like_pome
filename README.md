# 若榴机器人项目
## by 校友会频道
### by 石家庄二中
```
项目名 d2_like_pome
 - d2取自谐音帝二
 - like_pomo是若榴直译的like pomegranate的简写
```

# 相关设计
 - 语言: Python 3.9
 - 依赖库: qq-bot sdk，文档: https://bot.q.qq.com/wiki/develop/pythonsdk/
 - 云主机: 腾讯云， 文档: https://cloud.tencent.com/document/product/213
 - 服务器: CentOS 8.2
 - 数据库: MySql 8.0.29
 - 缓存: Redis 7.0.2
 - 其他: to be continued

# 项目结构
- config              # 配置目录
  - http.yaml         ## 配置文件
- dao                 # 数据接入(data access object)
  - \_\_init\_\_.py   ## 接口文件
  - business.py       ## 业务逻辑
  - cache.py          ## 缓存底层
  - database.py       ## 数据库底层
  - main.py           ## 调试文件
- net                 # 网络功能
  - \_\_init\_\_.py   ## 接口文件
  - business.py       ## 业务逻辑
  - weather.py        ## 天气接口调用
- pic                 # 图片功能
  - output            # 文件输出
  - template          # 图片\字体模板
  - \_\_init\_\_.py   ## 接口文件
  - main.py           ## 调试文件
  - picture.py        ## 处理图片逻辑
- server              # 服务器目录
  - config            # 初始化依赖配置
  - \_\_init\_\_.py   ## 接口文件
  - always.py         ## 机器人服务器初始化
- service             # 服务目录
  - \_\_init\_\_.py   ## 接口文件
  - activity.py       ## 抽奖等活动
  - always.py         ## 初始化接口
  - default.py        ## 默认返回
  - manage.py         ## 管理员功能
  - sign.py           ## 签到功能
  - weather.py        ## 天气功能
- main.py             ## 主文件

# 开发人员
 - shenzhonghao
   - nickname: godshen
   - qq: 449208388
   - email: shenzh0713@gmail
