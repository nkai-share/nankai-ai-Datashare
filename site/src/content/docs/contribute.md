---
title: 投稿指南
description: 通过邮件或 GitHub Pull Request 向 NKAI DataShare 分享课程资料。
sidebar:
  order: 2
---

# 投稿指南

感谢你愿意补充课程资料。每一份清晰、合规的资料，都可能帮助后来的同学减少重复整理。

:::note[项目原则]
本项目坚持无偿分享，禁止商业化使用。投稿前请确认资料不包含个人隐私、受限制内容或不适合公开传播的信息。
:::

## 邮件投稿

将文件发送到 [nkai_share@163.com](mailto:nkai_share@163.com)，邮件标题建议使用“学期 + 课程 + 资料类型”，例如：`大二下 自动控制原理 期末真题`。

请在正文中说明：

- 资料所属学期和课程；
- 资料类型与大致年份；
- 是否希望署名，以及署名方式；
- 文件来源及是否允许公开分享。

## GitHub Pull Request

1. Fork [项目仓库](https://github.com/nkai-share/nankai-ai-Datashare)。
2. 将文件放入“学期 / 课程 / 分类”对应目录。
3. 使用清晰、可检索的文件名，避免“新建文档”“最终版2”等模糊名称。
4. 运行 `python scripts/generate_resource_index.py` 更新资源索引。
5. 提交 Pull Request，并说明资料来源和主要内容。

## 文件与目录命名

- 尽量包含课程名、年份、试卷类型或资料用途；
- 同一资料不要重复上传多个压缩版本；
- 推荐使用 PDF 保存定稿文档，同时可保留可编辑源文件；
- 不要在文件名中加入手机号、学号等个人信息；
- 大文件上传前请确认 GitHub 单文件限制。

## 审核与合规

维护团队可能对目录、文件名和分类进行整理。明显侵权、包含隐私、存在安全风险或用于商业推广的内容不会合入。如需更正或下架资料，请通过 [Issue](https://github.com/nkai-share/nankai-ai-Datashare/issues) 或邮箱联系我们。
