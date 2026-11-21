"""从指定 Git 标签的原始文件内容生成可安装 ZIP 和 SHA-256 清单。"""
import argparse
import hashlib
import io
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILL = "artifact-template-thu-ppt"
PREFIX = "skills/" + SKILL + "/"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def package(tag, output_dir):
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", tag) is None:
        raise ValueError("标签名称须可作为单个目录名")
    commit = git("rev-parse", "--verify", f"refs/tags/{tag}^{{commit}}").decode().strip()
    timestamp = int(git("show", "-s", "--format=%ct", commit))
    entries = git("ls-tree", "-r", "-z", commit, "--", PREFIX).split(b"\0")
    file_hashes = {}
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for entry in filter(None, entries):
            meta, path = entry.split(b"\t", 1)
            mode, kind, object_id = meta.decode("ascii").split()
            if kind != "blob" or mode not in {"100644", "100755"}:
                raise ValueError("技能目录中的条目须为常规文件")
            relative = path.decode("utf-8")[len(PREFIX):]
            member = SKILL + "/" + relative
            data = git("cat-file", "blob", object_id)
            file_hashes[member] = hashlib.sha256(data).digest()
            info = zipfile.ZipInfo(member, time.gmtime(timestamp)[:6])
            info.create_system = 3
            info.external_attr = int(mode, 8) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)

    with zipfile.ZipFile(buffer) as archive:
        if not all(f"{SKILL}/{name}" in file_hashes for name in ("SKILL.md", "LICENSE")):
            raise ValueError("标签中的技能缺少入口或许可证")
        for member, expected in file_hashes.items():
            if hashlib.sha256(archive.read(member)).digest() != expected:
                raise ValueError("ZIP 与 Git 对象内容不一致：" + member)

    target = output_dir.resolve() / tag
    target.mkdir(parents=True, exist_ok=True)
    filename = f"{SKILL}-{tag}.zip"
    data = buffer.getvalue()
    checksum = hashlib.sha256(data).hexdigest() + "  " + filename + "\n"
    with tempfile.TemporaryDirectory(dir=target) as temp:
        staging = Path(temp)
        (staging / filename).write_bytes(data)
        (staging / "SHA256SUMS.txt").write_bytes(checksum.encode("ascii"))
        for name in (filename, "SHA256SUMS.txt"):
            os.replace(staging / name, target / name)
    return target / filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", help="仓库中的版本标签，例如 v1.0.1")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist", help="产物按标签存入此目录")
    args = parser.parse_args()
    print(package(args.tag, args.output_dir))
