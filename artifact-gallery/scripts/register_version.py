#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""登记一次交付物版本快照，写入 manifest.json 并把文件副本存到 ART_ROOT/<id>/。

用法:
  python register_version.py "<文件绝对路径>" "<本版描述>" [artifact_id] [显示名] [工作文件路径]

- artifact_id 省略时按文件名自动生成 slug（同名产物会累积版本）。
- 工作文件路径 current_path 省略时默认为被登记文件本身；回撤时旧快照会复制回这里。
"""
import sys, os, json, shutil, re, datetime

ART_ROOT = os.environ.get("ART_ROOT", r"D:\intern\.workbuddy\artifacts")
MANIFEST = os.path.join(ART_ROOT, "manifest.json")


def slugify(s: str) -> str:
    """仅剔除文件系统非法字符（保留中文等），用作 artifact_id / 快照目录名。"""
    s = re.sub(r'[\\/:*?"<>|]', '_', s)
    return (s.strip() or "artifact")


def load() -> dict:
    if os.path.exists(MANIFEST):
        with open(MANIFEST, encoding='utf-8') as f:
            return json.load(f)
    return {"artifacts": []}


def save(m: dict):
    os.makedirs(ART_ROOT, exist_ok=True)
    with open(MANIFEST, 'w', encoding='utf-8') as f:
        json.dump(m, f, ensure_ascii=False, indent=2)


def register(file_path: str, desc: str, artifact_id: str = None,
             name: str = None, current_path: str = None):
    file_path = os.path.abspath(file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    ext = os.path.splitext(file_path)[1].lower()
    m = load()
    if not artifact_id:
        artifact_id = slugify(os.path.splitext(os.path.basename(file_path))[0])
    art = next((a for a in m["artifacts"] if a["id"] == artifact_id), None)
    if not art:
        art = {
            "id": artifact_id,
            "name": name or os.path.basename(file_path),
            "type": ("html" if ext in (".html", ".htm")
                     else ("docx" if ext == ".docx"
                           else ("pptx" if ext == ".pptx" else "file"))),
            "current_path": current_path or file_path,
            "created": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            "versions": [],
        }
        m["artifacts"].append(art)
    vn = len(art["versions"]) + 1
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_dir = os.path.join(ART_ROOT, artifact_id)
    os.makedirs(snap_dir, exist_ok=True)
    snap = os.path.join(snap_dir, f"v{vn}_{ts}{ext}")
    shutil.copy2(file_path, snap)
    art["versions"].append({
        "v": vn, "ts": ts, "desc": desc,
        "file": f"{artifact_id}/v{vn}_{ts}{ext}",
    })
    art["current"] = vn
    art["current_path"] = current_path or file_path
    save(m)
    return art, vn


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 2:
        print("Usage: register_version.py <file_path> <desc> [artifact_id] [name] [current_path]")
        sys.exit(1)
    fp, desc = args[0], args[1]
    aid = args[2] if len(args) > 2 else None
    nm = args[3] if len(args) > 3 else None
    cp = args[4] if len(args) > 4 else None
    art, vn = register(fp, desc, aid, nm, cp)
    print(f"Registered [{art['id']}] v{vn} -> {art['versions'][-1]['file']}")
