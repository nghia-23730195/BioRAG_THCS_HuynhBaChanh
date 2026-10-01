# -*- coding: utf-8 -*-
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

for p in [".", "..", "../BÁO CÁO", "Claude outputs"]:
    if os.path.exists(p):
        print(f"=== DIR: {p} ===")
        for item in os.listdir(p):
            print(f"  {item}")
