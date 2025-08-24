# 项目简介
    基于wxauto的一个每日微信消息提醒小程序；
    通过微信每日定时给指定的一位好友发送消息；
    前后花了两天多时间，还有一些优化留空了；

# 功能简介
    每日温度 --> 通过和风天气API获取
    小建议 --> 通过DeepSeek API 以及每日温度生成
    纪念日计算 --> 手撸模板以及代码
    每日一句 --> 金山词霸API

# 使用方法
    本项目采用uv用作包管理工具，可自行替换
    微信版本支持 3.9+
    使用前需要电脑先登录微信
#### 第一步 克隆仓库
    git clone https://github.com/SGMakeAFortune/wechat-send-message.git
#### 第二步 安装软件包
    uv pip install -r pyproject.toml
#### 第三步 创建 .env 配置文件
    配置参考：
    APP_ENV=development
    # 私钥
    PRIVATE_KEY_PEM="-----BEGIN PRIVATE KEY-----
    MC*************************************CJ6
    -----END PRIVATE KEY-----"
    # 和风API凭据ID
    CREDENTIALS_ID=C*******W
    # 和风API项目ID
    PROJECT_ID=4********9
    # 纪念日
    ANNIVERSARY=2999-99-99
    # Deepseek API 密钥
    DEEPSEEK_API_KEY=s***********************1
#### 第四步 配置基础配置项
    文件位置：settings
    # 日志文件名
    LOG_FILE_NAME = "daily_message.log"
    # 提醒时间
    HOUR = 7
    # 分钟数
    MINUTE = 30
    # 要发送的用户名
    USER_NAME = "你的用户名"
#### 第五步 终端执行
    python task_messages.py

# 成果演示
![img.png](images/img.png)