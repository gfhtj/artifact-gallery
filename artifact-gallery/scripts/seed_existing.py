import os, glob, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from register_version import register

SRC = r"D:\intern\面试"
files = sorted(glob.glob(os.path.join(SRC, "*.html")))
n = 0
for fp in files:
    name = os.path.basename(fp)
    try:
        register(fp, "初始版本（从历史交付物导入）")
        n += 1
        print("seeded:", name)
    except Exception as e:
        print("skip", name, e)
print(f"\nDone. {n} artifacts seeded.")
