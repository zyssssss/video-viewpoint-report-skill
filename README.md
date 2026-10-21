# 视频字幕与文案工具包

从视频链接到带时间戳的文字稿，再到可编辑的原创文案。两个 Skill 可以分别使用，也可以串起来运行。

| Skill | 输入 | 输出 |
|---|---|---|
| [video-download-skill](video-download-skill/SKILL.md) | B 站或 YouTube 视频链接 | 带时间戳、来源和覆盖说明的 Markdown 字幕／自动转写稿 |
| [video-transcript-to-copywriting](video-transcript-to-copywriting/SKILL.md) | 字幕、转写稿或视频链接及创作要求 | 口播稿、公众号文章、小红书笔记或社交帖子初稿，附来源与待核项 |

仓库根目录还保留原有的 [video-viewpoint-report](SKILL.md)，用于深入拆解作者观点和论证；这是可选分析能力。

## 安装与准备

这是供 Codex 等支持 `SKILL.md` 的 Agent 使用的指令包，并非双击运行的视频下载软件。下载、转写由 Agent 调用本机工具完成，文案由 Agent 根据模板撰写。

在 Codex 中可以这样提出安装请求：

```text
请从 https://github.com/zyssssss/video-viewpoint-report-skill
安装 video-download-skill 和 video-transcript-to-copywriting 这两个目录中的 Skill。
```

手动安装时，将仓库中的这两个目录分别复制到 `~/.codex/skills/`，保留目录名称。已有同名 Skill 时先比较内容、备份旧版本，避免覆盖本地修改。安装后按客户端要求重新加载 Skill 列表或新建会话。

只有提取字幕／音频时需要 `yt-dlp`。无可用字幕、需要本地语音识别时，另外需要 FFmpeg、Python 和 faster-whisper。先在独立环境准备依赖：

```bash
git clone https://github.com/zyssssss/video-viewpoint-report-skill.git
cd video-viewpoint-report-skill
python3 -m venv .venv
.venv/bin/pip install -r video-download-skill/requirements.txt
```

FFmpeg 使用操作系统适用的安装方式单独安装。首次语音转写会下载 Whisper 模型；音频在本机处理。依赖版本来自实际执行经验，其中 PyAV 固定在 16 系列，以避开与 faster-whisper 1.2.1 的已知接口冲突；其他系统仍需检查兼容性。

## 怎么用

### 只要完整字幕／转写稿

```text
使用 $video-download-skill 处理这个视频：<视频链接>。
优先取中文平台字幕；没有完整字幕时，用本地语音识别补全。
保存带时间戳的 Markdown，说明覆盖时长和转写方式。
```

### 已有字幕，整理成文案

```text
使用 $video-transcript-to-copywriting，读取 <本地字幕文件路径>。
改写为面向普通读者的公众号文章，约 1000 字，语气自然清楚。
保留核心观点，重新组织表达，文末列出来源和待核事实。
```

### 从视频到文案一次完成

```text
先使用 $video-download-skill 获取这个视频的完整文字：<视频链接>。
再使用 $video-transcript-to-copywriting，把文字整理为 3 分钟口播稿。
受众：<读者是谁>；重点：<希望解释的问题>；语气：<表达偏好>。
交付原始转写稿和文案初稿，标明来源、覆盖范围及待核项。
```

## 实际执行流程

1. 检查链接、视频标题、作者、时长和字幕轨道；多 P 视频先确认处理范围。
2. 有完整平台字幕则优先使用；无完整字幕但公开音频可访问时，下载音频、本机转写。遇到访问限制时说明问题，改用用户有权处理的文件。
3. 保存带时间戳的文字稿，比对末尾时间戳与音频时长。未覆盖的区段标明缺口，自动识别不能标成人工字幕。
4. 从文字稿提取中心观点、论据、例子和限制条件；数字、专名与不确定词进入待核清单。
5. 根据平台、受众和篇幅重新组织文案，用模板生成初稿。需要更深入的观点审计时，可在此之前使用根目录的 `video-viewpoint-report`。
6. 交付原始文字稿、文案和来源说明；发布到外部平台需用户明确要求。

### 本次真实使用记录

2026-10-21，处理用户指定的 B 站视频 `BV1hxug6BEL6`，流程如下：

- 公开字幕检查：游客状态未取得字幕轨道正文。
- 公开音频获取：成功，本地音频时长约 27:02。
- 本地转写：faster-whisper small，中文、CPU、int8。
- 遇到的问题：PyAV 19 不支持转写库传入的 `metadata_errors` 参数；调整为 PyAV 16.1.0 后转写成功。
- 结果：生成带时间戳的 Markdown，最后识别时间为 26:58，末尾约 4 秒未识别出语音；未人工逐字校对。

这条记录说明字幕获取阶段的实际结果。该视频没有在本次记录中被进一步改写为文案，因此下文的文案样式使用虚构教学材料展示。仓库不包含这条视频的全文、音频、登录信息或本机私人路径。

## 输出样式

以下示例完全虚构，只演示格式。

### 字幕／转写稿

```markdown
# 如何整理工作笔记

- 来源：https://example.com/demo-video
- 转写方式：本地 faster-whisper small，中文
- 视频时长：02:00
- 覆盖范围：00:00–01:58；末尾约 2 秒无识别语音
- 质量说明：自动转写，未人工逐字校对

[00:00:00] 今天介绍如何给工作笔记添加索引。
[00:00:08] 先确定你以后会用什么问题查找它。
[00:00:16] 再为笔记添加主题和日期。
```

### 基于同一材料的文案初稿

```markdown
# 记完笔记，怎样才能找得回来？

写笔记之前，可以先问自己：以后会因为什么问题再打开它？
这个问题决定了索引应该怎么做。

例如，项目讨论记录可以同时保留主题和日期。
按主题找内容，按日期还原讨论顺序，就有了两条查找路径。

与其一次调整所有旧笔记，不妨先在下一次会议记录里试用。

来源：虚构教学视频；本文为重新组织的示例表达。
待核项：没有效率提升比例或效果保证。
```

完整空白模板：[copywriting-template.md](video-transcript-to-copywriting/assets/copywriting-template.md)。

## 本地转写命令

Agent 获取有权处理的本地音频后，也可直接运行附带脚本。使用新的输出文件名，避免覆盖旧稿：

```bash
.venv/bin/python video-download-skill/scripts/transcribe_video.py \
  /path/to/audio.mp3 /path/to/transcript-draft.md \
  --title '视频标题' \
  --source-url '原视频链接' \
  --model small
```

脚本生成带开始时间戳的自动转写稿。它不会自动证明转写完整：执行后仍须核对媒体总时长、最后识别时间和语音缺口，将覆盖范围补入稿件；完成前使用 `draft` 或“草稿”名称。

## 使用边界

- 自动转写可能误识别人名、数字、术语；关键内容需要对照原声或原始资料。
- 字幕用来还原作者表达，不能直接证明作者的事实判断正确。
- 文案阶段保留必要来源，重新组织表达；不将长段照搬或逐句换词标作原创。
- 音频、字幕和登录信息默认不上传到第三方服务或本仓库。
