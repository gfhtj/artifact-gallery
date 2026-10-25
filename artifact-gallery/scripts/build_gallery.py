#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""构建离线版画廊：把 manifest + 各版本快照内联进单个 HTML，无需服务器即可在 WorkBuddy 直接打开。

用法: python build_gallery.py [输出路径]  默认输出 $ART_ROOT/gallery_standalone.html
"""
import os, sys, json, base64

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from register_version import load, ART_ROOT  # noqa

TEMPLATE = os.path.join(HERE, "..", "assets", "gallery_standalone.html")


def build(out_path: str):
    m = load()
    # 内联版本内容
    for a in m["artifacts"]:
        for v in a["versions"]:
            fp = os.path.join(ART_ROOT, v["file"])
            if os.path.exists(fp):
                ext = os.path.splitext(fp)[1].lower()
                with open(fp, "rb") as f:
                    raw = f.read()
                if a["type"] == "html":
                    v["html"] = raw.decode("utf-8", "replace")
                    v["datauri"] = ""
                else:
                    v["html"] = ""
                    v["datauri"] = "data:application/octet-stream;base64," + base64.b64encode(raw).decode()
            else:
                v["html"] = "<p style='padding:20px'>快照文件缺失</p>"
                v["datauri"] = ""
    with open(TEMPLATE, encoding="utf-8") as f:
        tpl = f.read()
    data_json = json.dumps(m, ensure_ascii=False)
    # 防止快照 HTML 内的 </script> 提前闭合 DATA 脚本块
    data_json = data_json.replace("</script>", "<\\/script>")
    out = tpl.replace("__DATA__", data_json)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"Built offline gallery -> {out_path}  ({len(m['artifacts'])} artifacts)")


if __name__ == "__main__":
    default = os.path.join(ART_ROOT, "gallery_standalone.html")
    out = sys.argv[1] if len(sys.argv) > 1 else default
    build(out)
