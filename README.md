# bilibili_firstKing
b站抢楼工具

### 功能
利用b站的接口以mid获取用户的关注列表（关注者的mid），然后每隔一个很短的时间遍历关注者，检测是否发表新的视频，如果有发送评论。

### 使用方式
* 复制mail.conf.example到mail.conf，修改对应邮箱字段
* 登录b站，复制json格式的cookie信息，保存到cookie.txt文件
