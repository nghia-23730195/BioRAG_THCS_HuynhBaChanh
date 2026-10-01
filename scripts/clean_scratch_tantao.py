import os

for root, dirs, files in os.walk("scratch"):
    for f in files:
        if f.endswith((".js", ".html", ".py", ".json")):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fl:
                content = fl.read()
            if "TÂN TẠO" in content or "Tân Tạo" in content:
                content = content.replace("TRƯỜNG THCS TÂN TẠO", "TRƯỜNG THCS HUỲNH BÁ CHÁNH")
                content = content.replace("THCS Tân Tạo A", "THCS Huỳnh Bá Chánh")
                content = content.replace("THCS Tân Tạo", "THCS Huỳnh Bá Chánh")
                content = content.replace("Tân Tạo", "Huỳnh Bá Chánh")
                with open(p, "w", encoding="utf-8") as fl:
                    fl.write(content)
                print(f"Updated: {p}")
