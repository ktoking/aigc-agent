---
workflow: product-launch-video
flow: automation
storyboard: no
message: 一个人，也能拥有自己的内容工作室
destination: xiaohongshu
aspect: 1080x1920
language: zh-CN
length: 57s
angle: 从一个想法到内容发布，再到下一次更懂你
style_preset: capsule
---

## Intent
为XHS Growth Agent做一支57秒竖屏引流动效科普短片。参考近期Opus5.5代码动效作品的连续变形、镜头推进、平面图形叙事。叙事是一个人的灵感如何变成可审核、可发布、可复用的内容工作流。

## Customizations
- 用户明确要求直接交付最终视频及独立字幕文件；不追加阶段审批。
- 完全静音，不生成语音、BGM或音效，不烧录字幕。画面只有必要的设计标题及产品UI词。
- 使用HTML/CSS/SVG、少量Canvas2D与GSAP，HyperFrames逐帧导出。60fps，H.264 MP4，57秒。
- 绘制原创概念图形，不录真实账号界面、不操作平台发布、不暴露账号或凭证。
- 单张首图、正文内容、组合语气、人工审核、审批即队列、真实样本写作Harness为核心卖点。
- 结尾CTA：想看搭建过程，留言「工作室」。不承诺涨粉效果。

## Notes
no-capture mode：用户提供的系统上下文及本地源码是产品事实来源。本片是概念宣传而不是页面录屏。
引用参考：https://oneshotted.io/v/opus-55-motion-video-with-the-full-workflow 。只参考通用运动语言，不复制作者画面。
HyperFrames usage返回unknown/invalid_usage_response。HeyGen未登录；用户要求静音，无需登录或安装任何音频模型。
