# -*- coding: utf-8 -*-
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

files_to_check = [
    "src/app/plan_5512_builder.py",
    "api/_plan_5512_builder.py",
    "src/app/curated_quizzes.py",
    "api/_curated_quizzes.py",
    "src/app/science_experiments.py",
    "api/_science_experiments.py",
    "src/app/_textbook_renderer.py",
    "api/_textbook_renderer.py",
]

for f in files_to_check:
    if os.path.exists(f):
        with open(f, "r", encoding="utf-8") as fl:
            lines = fl.readlines()
            for i, l in enumerate(lines, 1):
                if any(w in l.lower() for w in ["tân tạo", "tan tao"]):
                    print(f"{f}:{i}: {l.strip()}")
