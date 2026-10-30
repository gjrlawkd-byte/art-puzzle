"""art/meta.json(소장품 정보)과 data/quotes.json(한국어 제목·명언)을 합쳐 data/paintings.json 을 만든다.

사용법: python tools/build_data.py
명언을 고치거나 작품을 추가한 뒤 실행하면 화면에 반영된다.
"""
import json, os, sys

ROOT = os.path.join(os.path.dirname(__file__), "..")


def main():
    meta = json.load(open(os.path.join(ROOT, "art", "meta.json"), encoding="utf-8"))
    quotes = json.load(open(os.path.join(ROOT, "data", "quotes.json"), encoding="utf-8"))
    out, missing = [], []
    for m in meta:
        q = quotes.get(str(m["id"]))
        if not q:
            missing.append(f'{m["id"]} {m["title"][:50]}')
            continue
        title, artist, quote = q
        out.append(dict(id=m["id"], title=title, artist=artist, date=m["date"], quote=quote,
                        titleEn=m["title"], artistEn=m["artist"], source=m["source"]))
    json.dump(out, open(os.path.join(ROOT, "data", "paintings.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(out)}점 저장")
    if missing:
        print("명언이 없어 빠진 작품 (data/quotes.json에 추가하세요):", *missing, sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    main()
