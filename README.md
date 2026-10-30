# 명화 퍼즐

퍼블릭 도메인 명화 200점으로 즐기는 3D 직소 퍼즐 웹서비스입니다. 36조각을 모두 맞추면 작품에 맞춰 새로 쓴 명언이 나타납니다.

빌드 과정이 없는 정적 사이트라서 폴더를 그대로 올리면 바로 배포됩니다.

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `index.html` | 게임 전체 (Three.js, CDN에서 불러옴) |
| `art/` | 작품 이미지 200장(약 28MB)과 소장품 정보 `meta.json` |
| `data/quotes.json` | 한국어 제목·작가·명언. **명언은 여기서 고칩니다** |
| `data/paintings.json` | 화면이 읽는 최종 데이터 (아래 스크립트로 생성) |
| `tools/collect.py` | 메트로폴리탄 미술관 API에서 작품 수집 |
| `tools/build_data.py` | `meta.json` + `quotes.json` → `paintings.json` |

## 로컬에서 실행

`index.html`을 파일로 바로 열면 데이터를 불러오지 못하므로, 간단한 서버로 띄웁니다.

```bash
python -m http.server 8123
```

브라우저에서 `http://localhost:8123` 을 엽니다. 주소 끝에 `?debug`를 붙이면 콘솔에서 `solveAll()`로 퍼즐을 한 번에 완성해 볼 수 있습니다.

## 명언 수정·작품 추가

1. 명언만 고칠 때: `data/quotes.json`을 수정한 뒤 `python tools/build_data.py`
2. 작품을 늘릴 때: `python tools/collect.py 250` (목표 개수) → 새 작품의 명언을 `data/quotes.json`에 추가 → `python tools/build_data.py`

`build_data.py`는 명언이 빠진 작품이 있으면 목록을 알려 줍니다. 수집 스크립트에는 Pillow가 필요합니다(`pip install pillow`).

## 배포 방법 (무료, 택1)

- **Netlify Drop** — 가장 간단합니다. https://app.netlify.com/drop 에 이 폴더를 끌어다 놓으면 주소가 생깁니다.
- **GitHub Pages** — 저장소에 올린 뒤 Settings → Pages → Branch를 `main` / root로 지정합니다.
- **Cloudflare Pages / Vercel** — 저장소를 연결하고 빌드 명령은 비워 두고, 출력 폴더는 루트(`/`)로 지정합니다.

`tools/` 폴더는 올리지 않아도 됩니다(올려도 문제는 없습니다).

## 저작권

- 작품 이미지: The Metropolitan Museum of Art Open Access, CC0 1.0 (상업적 이용 가능). 작품별 출처 링크는 `data/paintings.json`의 `source`에 있습니다.
- 명언: 이 서비스를 위해 새로 쓴 문구입니다.
- 진행 기록은 각 사용자의 브라우저(localStorage)에만 저장되며 서버로 전송되지 않습니다.
