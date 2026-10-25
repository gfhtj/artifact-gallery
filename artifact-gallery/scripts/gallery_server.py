#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地画廊服务：读取 manifest，提供预览 / 回撤接口，并托管 gallery.html。

运行: python gallery_server.py [port]   默认端口 8731
打开: http://localhost:8731  （在 WorkBuddy 用 present_files 传入该 URL 即可在预览面板查看）
"""
import os, sys, json, shutil, http.server, socketserver, urllib.parse, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from register_version import load, save, ART_ROOT  # noqa

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8731

GALLERY_HTML = os.path.join(HERE, "..", "assets", "gallery.html")


def content_type(ext: str) -> str:
    return {
        ".html": "text/html; charset=utf-8",
        ".htm": "text/html; charset=utf-8",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".pdf": "application/pdf",
    }.get(ext.lower(), "application/octet-stream")


def do_revert(art_id: str, v: int):
    m = load()
    art = next((a for a in m["artifacts"] if a["id"] == art_id), None)
    if not art:
        return None, "artifact not found"
    target = next((x for x in art["versions"] if x["v"] == v), None)
    if not target:
        return None, "version not found"
    src = os.path.join(ART_ROOT, target["file"])
    dst = art["current_path"]
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    shutil.copy2(src, dst)
    # 记为一个新的"回撤"版本，保留历史
    ext = os.path.splitext(src)[1].lower()
    vn = len(art["versions"]) + 1
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_dir = os.path.join(ART_ROOT, art_id)
    os.makedirs(snap_dir, exist_ok=True)
    snap = os.path.join(snap_dir, f"v{vn}_{ts}{ext}")
    shutil.copy2(src, snap)
    art["versions"].append({
        "v": vn, "ts": ts, "desc": f"回撤至 v{v}", "file": f"{art_id}/v{vn}_{ts}{ext}",
    })
    art["current"] = vn
    save(m)
    return art, None


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = urllib.parse.urlparse(self.path)
        path = p.path
        q = urllib.parse.parse_qs(p.query)
        if path in ("/", "/index.html"):
            try:
                with open(GALLERY_HTML, encoding="utf-8") as f:
                    html = f.read()
                self._send(200, html, "text/html; charset=utf-8")
            except Exception as e:
                self._send(500, str(e))
            return
        if path == "/api/manifest":
            self._send(200, json.dumps(load(), ensure_ascii=False))
            return
        if path == "/api/preview":
            art_id = q.get("art", [""])[0]
            try:
                v = int(q.get("v", ["0"])[0])
            except ValueError:
                v = 0
            m = load()
            art = next((a for a in m["artifacts"] if a["id"] == art_id), None)
            if not art:
                self._send(404, "not found")
                return
            ver = next((x for x in art["versions"] if x["v"] == v), None)
            if not ver:
                self._send(404, "version not found")
                return
            fp = os.path.join(ART_ROOT, ver["file"])
            if not os.path.exists(fp):
                self._send(404, "snapshot missing")
                return
            ext = os.path.splitext(fp)[1].lower()
            with open(fp, "rb") as f:
                data = f.read()
            self._send(200, data, content_type(ext))
            return
        self._send(404, "not found")

    def do_POST(self):
        p = urllib.parse.urlparse(self.path)
        if p.path == "/api/revert":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                body = json.loads(raw.decode("utf-8"))
                art, err = do_revert(body.get("art"), int(body.get("v", 0)))
                if err:
                    self._send(400, json.dumps({"error": err}, ensure_ascii=False))
                else:
                    self._send(200, json.dumps(art, ensure_ascii=False))
            except Exception as e:
                self._send(500, json.dumps({"error": str(e)}, ensure_ascii=False))
            return
        self._send(404, "not found")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Artifact Gallery running at http://localhost:{PORT}")
        print(f"ART_ROOT = {ART_ROOT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped.")
