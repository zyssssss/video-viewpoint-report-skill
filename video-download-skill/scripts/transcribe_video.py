#!/usr/bin/env python3
"""Transcribe a local media file with faster-whisper to timestamped Markdown."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from faster_whisper import WhisperModel


def timestamp(seconds: float) -> str:
    total = round(seconds)
    hours, remainder = divmod(total, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--model", default="small")
    args = parser.parse_args()

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        str(args.audio), language="zh", vad_filter=True, beam_size=5,
    )

    lines = [
        f"# {args.title}",
        "",
        f"- 来源：{args.source_url}",
        f"- 转写时间：{datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
        f"- 识别方式：本地 faster-whisper（{args.model}，中文）",
        "- 说明：自动语音识别稿，专有名词、数字与停顿可能需要人工校对。",
        "",
        "## 转写正文",
        "",
    ]
    for segment in segments:
        text = segment.text.strip()
        if text:
            lines.append(f"[{timestamp(segment.start)}] {text}")
            lines.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"已写入 {args.output}")


if __name__ == "__main__":
    main()
