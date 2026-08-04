#!/usr/bin/env python3
"""Validate generated resource metadata and local resource links."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlsplit


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "site" / "src" / "data"
    resources = load_json(data_dir / "resources.json")
    courses = load_json(data_dir / "courses.json")
    statistics = load_json(data_dir / "statistics.json")
    errors: list[str] = []

    ids = [item["id"] for item in resources]
    paths = [item["relativePath"] for item in resources]
    if len(ids) != len(set(ids)):
        errors.append("资源 ID 不唯一")
    if len(paths) != len(set(paths)):
        errors.append("资源路径不唯一")
    if statistics["resourceCount"] != len(resources):
        errors.append("statistics.resourceCount 与 resources.json 不一致")
    if statistics["courseCount"] != len(courses):
        errors.append("statistics.courseCount 与 courses.json 不一致")

    course_keys = {(item["semester"], item["name"]): item for item in courses}
    counted: dict[tuple[str, str], int] = {}
    for resource in resources:
        local_path = repo_root / Path(resource["relativePath"])
        if not local_path.is_file():
            errors.append(f"本地文件不存在：{resource['relativePath']}")
        key = (resource["semester"], resource["course"])
        counted[key] = counted.get(key, 0) + 1
        if key not in course_keys:
            errors.append(f"课程索引缺失：{key[0]}/{key[1]}")
        for field in ("githubUrl", "rawUrl"):
            url = resource[field]
            parsed = urlsplit(url)
            if not parsed.scheme.startswith("http") or " " in url or any(ord(char) > 127 for char in url):
                errors.append(f"URL 未正确编码：{field} -> {resource['relativePath']}")

    for key, course in course_keys.items():
        if course["resourceCount"] != counted.get(key, 0):
            errors.append(f"课程统计不一致：{key[0]}/{key[1]}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"索引校验通过：{len(resources)} 份资料，{len(courses)} 门课程。")
    if statistics.get("warnings"):
        print(f"提示：发现 {len(statistics['warnings'])} 条非阻塞扫描警告。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
