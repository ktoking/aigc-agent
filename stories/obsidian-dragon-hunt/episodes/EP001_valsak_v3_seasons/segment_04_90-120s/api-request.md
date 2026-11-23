# 当前第04段请求状态

QUOTA_BLOCKED（未提交成功）。30秒、16:9，全片90—120秒，v4-in-place。

- 2026-11-04 16:10：与段03并行提交，返回“近 7 天额度已用完”，未生成任务。
- 2026-11-04 16:14：用户要求继续生成，复用同方案与同一批参考图 URL（均已验证可访问，302 跳转正常）再次提交，仍返回同一额度提示，工具明确要求不自动重试，已停止。
- 提示词与输入已就绪：director-promt.txt 全文 + `<图片1>`—`<图片10>` 顺序绑定；10 张 v6 关键帧（current-references-v2，排除 discarded-v1）。
- 复用 URL：ref-01 https://aka.doubaocdn.com/s/EBSNlzAidM、ref-02 https://aka.doubaocdn.com/s/PBnEEJQRaV、ref-03 https://aka.doubaocdn.com/s/Gs4VoBm7vd、ref-04 https://aka.doubaocdn.com/s/LBWVGX2CIq、ref-05 https://aka.doubaocdn.com/s/c7Uu7p26vv、ref-06 https://aka.doubaocdn.com/s/pyWFQqUcHo、ref-07 https://aka.doubaocdn.com/s/IRqrgfE1Vb、ref-08 https://aka.doubaocdn.com/s/zTZR3pUgkE、ref-09 https://aka.doubaocdn.com/s/wxdjwTtFTC、ref-10 https://aka.doubaocdn.com/s/QXqh9s0xIz
- 无新任务 ID、无返回、无费用。额度恢复后可直接复用上述方案与 URL 提交，无需重新上传参考图。
