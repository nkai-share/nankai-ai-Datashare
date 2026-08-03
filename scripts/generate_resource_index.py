#!/usr/bin/env python3
"""Generate deterministic resource metadata for the NKAI DataShare website."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote


REPOSITORY = "nkai-share/nankai-ai-Datashare"
BRANCH = "main"
SEMESTER_RE = re.compile(r"^大[一二三四五六](上|下)$")
SKIP_DIRECTORIES = {
    ".git",
    ".github",
    ".vscode",
    ".obsidian",
    "__pycache__",
    "node_modules",
    "dist",
    "site",
    "scripts",
}
SKIP_FILES = {
    "README.md",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
}
CATEGORY_ALIASES = {
    "期末考试题及解答": "往年真题",
    "南开大学往年真题": "往年真题",
    "真题": "往年真题",
    "真题和资料": "往年真题",
    "考试资料和真题": "往年真题",
    "线代期末（扫描）": "往年真题",
    "课件PPT": "课程课件",
    "PPT": "课程课件",
    "复习资料": "复习笔记",
    "复习": "复习笔记",
}
PREVIEW_TYPES = {
    "pdf": "pdf",
    "png": "image",
    "jpg": "image",
    "jpeg": "image",
    "webp": "image",
    "gif": "image",
    "svg": "image",
    "txt": "text",
    "md": "text",
    "doc": "office",
    "docx": "office",
    "ppt": "office",
    "pptx": "office",
    "xls": "office",
    "xlsx": "office",
    "mp4": "media",
    "webm": "media",
    "zip": "archive",
    "rar": "archive",
    "7z": "archive",
}
MIME_GROUPS = {
    "pdf": "document",
    "doc": "document",
    "docx": "document",
    "ppt": "presentation",
    "pptx": "presentation",
    "xls": "spreadsheet",
    "xlsx": "spreadsheet",
    "txt": "text",
    "md": "text",
    "png": "image",
    "jpg": "image",
    "jpeg": "image",
    "webp": "image",
    "gif": "image",
    "svg": "image",
    "zip": "archive",
    "rar": "archive",
    "7z": "archive",
    "mp4": "media",
    "webm": "media",
}


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def encode_path(path: str) -> str:
    return "/".join(quote(part, safe="") for part in Path(path).parts)


def size_text(size: int) -> str:
    units = ("B", "KB", "MB", "GB")
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{int(value)} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024
    return f"{size} B"


def git_timestamps(repo_root: Path) -> dict[str, str]:
    command = [
        "git",
        "-c",
        "core.quotepath=false",
        "log",
        "--format=@@NKAI_COMMIT@@%cI",
        "--name-only",
        "--diff-filter=AM",
        "--no-renames",
        "--",
    ]
    try:
        result = subprocess.run(
            command,
            cwd=repo_root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.CalledProcessError):
        return {}

    timestamps: dict[str, str] = {}
    current_timestamp = ""
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("@@NKAI_COMMIT@@"):
            current_timestamp = line.removeprefix("@@NKAI_COMMIT@@")
            continue
        normalized = line.replace("\\", "/")
        if current_timestamp and normalized not in timestamps:
            timestamps[normalized] = current_timestamp
    return timestamps


def fallback_timestamp(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()


def discover_resources(repo_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    timestamps = git_timestamps(repo_root)
    resources: list[dict[str, Any]] = []
    warnings: list[str] = []
    names_by_course: defaultdict[tuple[str, str], Counter[str]] = defaultdict(Counter)

    semester_dirs = sorted(
        (entry for entry in repo_root.iterdir() if entry.is_dir() and SEMESTER_RE.match(entry.name)),
        key=lambda item: item.name,
    )
    for semester_dir in semester_dirs:
        course_dirs = sorted((entry for entry in semester_dir.iterdir() if entry.is_dir()), key=lambda item: item.name)
        for course_dir in course_dirs:
            matched_file = False
            for file_path in sorted(course_dir.rglob("*"), key=lambda item: item.as_posix()):
                if not file_path.is_file():
                    continue
                relative = file_path.relative_to(repo_root)
                if any(part in SKIP_DIRECTORIES or part.startswith(".") for part in relative.parts):
                    continue
                if file_path.name in SKIP_FILES or file_path.name.startswith("~$"):
                    continue

                matched_file = True
                relative_posix = relative.as_posix()
                category_parts = list(relative.parts[2:-1])
                raw_category = category_parts[0] if category_parts else "未分类"
                category = CATEGORY_ALIASES.get(raw_category, raw_category)
                sub_category = " / ".join(category_parts[1:])
                extension = file_path.suffix.lower().lstrip(".") or "file"
                encoded_path = encode_path(relative_posix)
                updated_at = timestamps.get(relative_posix, fallback_timestamp(file_path))
                resource = {
                    "id": hashlib.sha1(relative_posix.encode("utf-8")).hexdigest()[:16],
                    "semester": semester_dir.name,
                    "course": course_dir.name,
                    "category": category,
                    "rawCategory": raw_category,
                    "subCategory": sub_category,
                    "name": file_path.name,
                    "extension": extension,
                    "mimeGroup": MIME_GROUPS.get(extension, "other"),
                    "size": file_path.stat().st_size,
                    "sizeText": size_text(file_path.stat().st_size),
                    "relativePath": relative_posix,
                    "githubUrl": f"https://github.com/{REPOSITORY}/blob/{BRANCH}/{encoded_path}",
                    "rawUrl": f"https://raw.githubusercontent.com/{REPOSITORY}/{BRANCH}/{encoded_path}",
                    "previewType": PREVIEW_TYPES.get(extension, "download"),
                    "updatedAt": updated_at,
                }
                resources.append(resource)
                names_by_course[(semester_dir.name, course_dir.name)][file_path.name.casefold()] += 1

            if not matched_file:
                warnings.append(f"空课程目录：{course_dir.relative_to(repo_root).as_posix()}")

    for (semester, course), names in names_by_course.items():
        for name, count in names.items():
            if count > 1:
                warnings.append(f"重复文件名：{semester}/{course}/{name}（{count} 个）")

    resources.sort(key=lambda item: (item["semester"], item["course"], item["category"], item["name"]))
    return resources, sorted(warnings)


def build_indexes(repo_root: Path) -> dict[str, Any]:
    resources, warnings = discover_resources(repo_root)
    grouped: defaultdict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for resource in resources:
        grouped[(resource["semester"], resource["course"])].append(resource)

    courses: list[dict[str, Any]] = []
    for (semester, course), course_resources in sorted(grouped.items()):
        categories = Counter(item["category"] for item in course_resources)
        extensions = Counter(item["extension"] for item in course_resources)
        courses.append(
            {
                "semester": semester,
                "name": course,
                "slug": quote(course, safe=""),
                "resourceCount": len(course_resources),
                "categories": [
                    {"name": name, "count": count} for name, count in sorted(categories.items())
                ],
                "extensions": dict(sorted(extensions.items())),
                "latestUpdatedAt": max(item["updatedAt"] for item in course_resources),
            }
        )

    semester_counts = Counter(item["semester"] for item in resources)
    latest_timestamp = max((item["updatedAt"] for item in resources), default="")
    recent_resources = sorted(resources, key=lambda item: item["updatedAt"], reverse=True)[:12]
    statistics = {
        "semesterCount": len(semester_counts),
        "courseCount": len(courses),
        "resourceCount": len(resources),
        "totalSize": sum(item["size"] for item in resources),
        "totalSizeText": size_text(sum(item["size"] for item in resources)),
        "semesterResourceCounts": dict(sorted(semester_counts.items())),
        "latestUpdatedAt": latest_timestamp,
        "recentResourceIds": [item["id"] for item in recent_resources],
        "warningCount": len(warnings),
        "warnings": warnings,
    }
    return {"resources.json": resources, "courses.json": courses, "statistics.json": statistics}


def write_or_check(indexes: dict[str, Any], output_dir: Path, check: bool) -> bool:
    output_dir.mkdir(parents=True, exist_ok=True)
    current = True
    for name, data in indexes.items():
        target = output_dir / name
        expected = json_text(data)
        if check:
            actual = target.read_text(encoding="utf-8") if target.exists() else ""
            if actual != expected:
                print(f"索引过期：{target}", file=sys.stderr)
                current = False
        else:
            target.write_text(expected, encoding="utf-8", newline="\n")
            print(f"已生成 {target.relative_to(output_dir.parent.parent.parent)}")
    return current


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true", help="Check committed indexes without writing files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    indexes = build_indexes(repo_root)
    output_dir = repo_root / "site" / "src" / "data"
    is_current = write_or_check(indexes, output_dir, args.check)
    statistics = indexes["statistics.json"]
    print(
        f"索引统计：{statistics['semesterCount']} 学期，"
        f"{statistics['courseCount']} 门课程，{statistics['resourceCount']} 份资料"
    )
    return 0 if is_current else 1


if __name__ == "__main__":
    raise SystemExit(main())
