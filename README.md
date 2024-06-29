Demo: https://t.me/anon2anonbot
# 怎么用
- 安装 python3
- pip 安装各种依赖
- 填写 bot_token 以及工作目录
- 运行 `python3 anonbot.py`
# 功能
- 对机器人发送 /match 可以与一位匿名人匹配并聊天
- 对话结束后对对方投票
- 优先匹配与机器人有过互动的人
- 头像按性别分别显示男女表情包
- 显示匹配到的人多长时间前在线
- 支持修改发送的文字
- 支持视频、照片、圆视频等各种类型的消息（不支持组图、组视频）
- 显示匹配到的人的评价
- 匹配到的人加入两天并且没有发过一次言，头像显示为骷髅
- 如果已匹配用户两天不说话会收到解除连接的建议。此功能主要是为了唤醒沉睡用户。
# 后语
这个机器人主要是练手做的，测试期间进行了 N 多优化，代码精炼只有不到 700 行。由于加入了中英文双语言支持，因此代码阅读性可能稍微差一些。为了保持单文件，语言提示语等部分写在了代码的上半部分。 数据库内做了 is_admin 字段，但是没有做任何 admin 特权内容。
