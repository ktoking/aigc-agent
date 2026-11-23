# Segment 01 视频API拟提交单

Story：skyward-first-day；Episode：EP001_first-day；全片0–15秒；本段15秒。
状态：NOT_SUBMITTED。没有任务ID、提交时间、完成时间或返回记录。

## 参数计划

| 参数 | 计划值 | 状态 |
| --- | --- | --- |
| model | doubao-seedance-2-0-mini-260615 | 仓库草稿默认，尚未探测当前平台权限 |
| duration | 15秒 | 提交前验证支持范围 |
| ratio | 16:9 | 提交前核对脚本字段 |
| resolution | 720p | 草稿计划，非原生1080p承诺 |
| text prompt | director-promt.txt | 文字已准备 |
| seed / guidance / motion_strength | 不指定 | 不假设平台支持 |

## 拟输入顺序

| 序号 | 文件 | 职责 | 当前状态 |
| --- | --- | --- | --- |
| 1 | frames/first-frame.png | 本段0秒起始构图和角色道具初始状态 | 缺失 |
| 2 | frames/last-frame.png | 本段15秒结束状态与下一段衔接；不是要求整段从首帧直接变形到尾帧 | 缺失 |
| 3 | frames/ref-lin-tao-home.png | 林桃居家身份、睡衣、右腕手环；洗漱发带仅在洗手台出现 | 缺失 |
| 4 | frames/ref-home-layout.png | 卧室至浴室的空间、床头闹钟位置与晨光 | 缺失 |

首尾帧与补充图必须是真实文件；frames/reference-manifest.json目前全部missing。当前不能直接提交带图任务。引用路径不是已存在图像。补充图复制进本段后再提交，核对输入编号与导演词一致；不上传故事板表格。若API不支持首尾帧与多参考图组合，依据真实能力选择输入方式并同步改写编号，不声称此组合已验证。

## 请求与返回

未提交，故不伪造请求载荷、成功响应或费用。真实提交后保存output/api-submit.json、output/api-result.json，访问凭据及签名URL不写入文档。

## 返工

拳头只击中闹钟一次；先接触后裂壳再飞出圆耳，床头柜不塌，林桃手无伤。镜头4关掉助力后不能再次发力。

优先缩短偏差镜头、减少同时动作，再单镜或单段重试；不整集无差别重跑。人物漂移时补正确角色图；运动穿模时补路线/动作参考并明确仅供空间理解。清除重复模型人声，统一以对白时间线的后期配音为准。
