"""The Met Open Access(CC0)에서 퍼블릭 도메인 명화를 모아 art/ 에 저장한다.

사용법: python tools/collect.py [목표 개수=200]
결과: art/<id>.jpg, art/meta.json  (이미 받은 이미지는 건너뜀)
"""
import json, os, sys, time, urllib.request
from PIL import Image

API = "https://collectionapi.metmuseum.org/public/collection"
TARGET = int(sys.argv[1]) if len(sys.argv) > 1 else 200
# 유럽 회화, 미국관, 아시아 미술, 소묘·판화 하이라이트 순서로 채운다
DEPARTMENTS = [11, 1, 6, 9]
OK_CLASS = ("Paintings", "Prints")
SKIP = {39799}  # 45434와 같은 「가나가와 해변의 높은 파도 아래」 다른 판
ASPECT = (0.5, 2.0)  # 너무 길쭉한 두루마리는 퍼즐로 부적합
ROOT = os.path.join(os.path.dirname(__file__), "..", "art")


def get(url, raw=False):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (art-puzzle collector)"})
            data = urllib.request.urlopen(req, timeout=30).read()
            return data if raw else json.loads(data)
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def highlight_ids(dept):
    ids, offset = [], 0
    while True:
        page = get(f"{API}/v1.1/search?departmentId={dept}&isHighlight=true&hasImages=true&q=*&limit=100&offset={offset}")
        ids += page.get("objectIDs") or []
        offset += 100
        if offset >= page.get("total", 0):
            return ids


def main():
    os.makedirs(ROOT, exist_ok=True)
    meta_path = os.path.join(ROOT, "meta.json")
    meta = json.load(open(meta_path, encoding="utf-8")) if os.path.exists(meta_path) else []
    have = {m["id"] for m in meta}
    for dept in DEPARTMENTS:
        for oid in highlight_ids(dept):
            if len(meta) >= TARGET:
                break
            if oid in have or oid in SKIP:
                continue
            try:
                d = get(f"{API}/v1/objects/{oid}")
            except Exception as e:
                print("fail", oid, e)
                continue
            if not d.get("isPublicDomain") or not d.get("primaryImage") or d.get("classification") not in OK_CLASS:
                continue
            img = os.path.join(ROOT, f"{oid}.jpg")
            if not os.path.exists(img):
                url = d.get("primaryImageSmall") or d["primaryImage"]
                open(img, "wb").write(get(url, raw=True))
            w, h = Image.open(img).size
            if not ASPECT[0] <= w / h <= ASPECT[1]:
                os.remove(img)
                SKIP.add(oid)
                continue
            meta.append(dict(id=oid, title=d["title"], artist=d.get("artistDisplayName", ""),
                             date=d.get("objectDate", ""), source=d.get("objectURL", ""),
                             license="CC0 (The Met Open Access)"))
            have.add(oid)
            print(len(meta), oid, d["title"][:60])
            json.dump(meta, open(meta_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            time.sleep(0.1)  # API 부하를 줄이기 위한 간격
    print("total", len(meta))


if __name__ == "__main__":
    main()
