import csv, urllib.request, io, os, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ── 설정 ─────────────────────────────────────────────────────────────
W, H     = 1280, 720
FPS      = 30
MAX_Q    = 10
FONT     = "C:/Windows/Fonts/malgun.ttf" if sys.platform == "win32" else "/usr/share/fonts/opentype/unifont/unifont.otf"
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "20251223.mp4")
CSV_URL  = "https://raw.githubusercontent.com/mimmimmimnu/musalt_queue/20251223/words.csv"

# ── 색상 ─────────────────────────────────────────────────────────────
C = dict(
    bg       = (245, 245, 250),
    qbg      = (255, 255, 255),
    qborder  = ( 70, 130, 200),
    grid     = (200, 200, 210),
    title    = ( 50,  80, 180),
    info     = ( 80,  80, 120),
    qname    = (180,  80,  50),
    code_bg  = ( 30,  30,  50),
    enq      = (120, 220, 120),
    deq      = (255, 120, 120),
    frt      = (120, 200, 255),
    emp      = (255, 220,  80),
    clr      = (255, 140, 200),
    dft      = (230, 230, 230),
    slot_num = (190, 190, 210),
    hl_rear  = (200, 255, 200),
    hl_front = (255, 210, 200),
)
CELL_COLORS = [
    (255,220,220),(220,240,255),(220,255,220),(255,255,200),
    (240,220,255),(255,235,210),(210,255,250),(255,215,215),
    (230,230,255),(215,245,215),
]

# ── 레이아웃 ─────────────────────────────────────────────────────────
QL  = 800
QT  = 80
QW  = 390
CHL = 50
QB  = QT + CHL * MAX_Q + 10
CX, CY, CW, CBH = 40, 130, 710, 85

# ── 유틸 ─────────────────────────────────────────────────────────────
def fnt(size):   return ImageFont.truetype(FONT, size)
def to_cv2(img): return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
def rrect(d, xy, r, fill, outline=None, w=2):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)

# ── CSV 로드 ─────────────────────────────────────────────────────────
FALLBACK = [
    {"id":"20251223","name":"이유민","word1":"카푸치노",   "word2":"카페라떼",    "word3":"피넛라떼"},
    {"id":"20251185","name":"김수민","word1":"말차라떼",   "word2":"초코라떼",    "word3":"레몬티"},
    {"id":"20251229","name":"이채영","word1":"자몽티",     "word2":"카페모카",    "word3":"매실티"},
    {"id":"20251209","name":"유지민","word1":"얼그레이티", "word2":"스콘",        "word3":"레몬티"},
    {"id":"20252213","name":"정서하","word1":"레몬티",     "word2":"카푸치노",    "word3":"초코 스콘"},
    {"id":"20252199","name":"이예은","word1":"매실티",     "word2":"페퍼민트티",  "word3":"휘낭시에"},
    {"id":"20251225","name":"이윤서","word1":"딸기라떼",   "word2":"딸기에이드",  "word3":"망고에이드"},
    {"id":"20251267","name":"황다원","word1":"스콘",       "word2":"청포도에이드","word3":"매실티"},
    {"id":"20252185","name":"안예원","word1":"카페라떼",   "word2":"말차라떼",    "word3":"카푸치노"},
    {"id":"20251207","name":"유가현","word1":"캐모마일티", "word2":"초코 스콘",   "word3":"레몬티"},
]

def load_csv(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            raw = r.read()
        for enc in ("utf-8-sig", "utf-8", "euc-kr", "cp949"):
            try:
                content = raw.decode(enc); break
            except UnicodeDecodeError:
                continue
        rows = [{k.strip(): v.strip() for k, v in row.items()}
                for row in csv.DictReader(io.StringIO(content))]
        print(f"✅ CSV 로드 성공 ({url}): {len(rows)}명")
        return rows
    except Exception as e:
        print(f"⚠️  CSV 로드 실패 ({e}) → 하드코딩 데이터 사용")
        return FALLBACK

def unique_words(members):
    seen, out = set(), []
    for m in members:
        for k in ["word1","word2","word3"]:
            w = m[k]
            if w not in seen:
                seen.add(w); out.append((w, m["name"]))
    return out

# ── 연산 시퀀스 생성 ─────────────────────────────────────────────────
# 전략: 단어를 최대 10개씩 묶어서 enqueue → front → dequeue → clear 반복
# 모든 단어 사용, 5가지 연산 모두 포함, 크기 10 이하 유지
def build_ops(members):
    words = unique_words(members)
    ops   = [("declare","",""), ("isEmpty","","")]   # iii. 선언부터, ii. isEmpty

    q           = []
    chunk_size  = MAX_Q   # 한 번에 최대 10개씩 enqueue
    used_ops    = {"enqueue":0,"dequeue":0,"front":0,"isEmpty":1,"clear":0}

    i = 0
    while i < len(words):
        chunk = words[i : i + chunk_size]

        # enqueue
        for word, member in chunk:
            ops.append(("enqueue", word, member))
            q.append(word)
            used_ops["enqueue"] += 1

        # front 연산 (큐가 찼을 때 맨 앞 확인)
        ops.append(("front","",""))
        used_ops["front"] += 1

        # dequeue 1회 (FIFO 확인용)
        if q:
            ops.append(("dequeue","",""))
            q.pop(0)
            used_ops["dequeue"] += 1

        i += chunk_size

        # 마지막 청크가 아니면 clear 후 다음 청크
        if i < len(words):
            ops.append(("clear","",""))
            q.clear()
            used_ops["clear"] += 1
            ops.append(("isEmpty","",""))
            used_ops["isEmpty"] += 1

    # 마지막에 clear + isEmpty로 마무리
    ops.append(("clear","",""))
    q.clear()
    used_ops["clear"] += 1
    ops.append(("isEmpty","",""))
    used_ops["isEmpty"] += 1

    # 검증
    print(f"   연산 수: {len(ops)}")
    print(f"   연산 사용: {used_ops}")
    all_words = set(w for w,_ in words)
    enq_words = set(w for op,w,_ in ops if op=="enqueue")
    missing   = all_words - enq_words
    if missing: print(f"   ❌ 미사용 단어: {missing}")
    else:       print(f"   ✅ 모든 단어 사용됨")

    return ops

MEMBERS    = load_csv(CSV_URL)
WORDS_ALL  = [w for w, _ in unique_words(MEMBERS)]
OPERATIONS = build_ops(MEMBERS)

# ── 프레임 그리기 ────────────────────────────────────────────────────
def draw_frame(queue, op, word, member,
               front_val=None, empty_val=None,
               hl_front=False, hl_rear=False):
    img = Image.new("RGB", (W, H), C["bg"])
    d   = ImageDraw.Draw(img)
    f30, f26, f22, f19, f18, f16 = fnt(30),fnt(26),fnt(22),fnt(19),fnt(18),fnt(16)

    # 타이틀
    d.text((40, 22), "Queue Animation",    font=f30, fill=C["title"])
    d.text((40, 58), "자료구조 큐 시각화", font=f18, fill=C["info"])

    # 큐 이름 헤더
    rrect(d, [QL, QT-48, QL+QW, QT-4], 8, (255,245,235), C["qborder"], 2)
    tw = d.textbbox((0,0),"카페무솔트",font=f26)[2]
    d.text((QL+(QW-tw)//2, QT-40), "카페무솔트", font=f26, fill=C["qname"])

    # 큐 본체 + 격자 + 슬롯 번호
    rrect(d, [QL-4, QT-4, QL+QW+4, QB+4], 10, C["qbg"], C["qborder"], 3)
    for i in range(MAX_Q + 1):
        d.line([(QL, QT+i*CHL),(QL+QW, QT+i*CHL)], fill=C["grid"], width=1)
    for i in range(MAX_Q):
        d.text((QL+5, QT+i*CHL+4), f"[{i}]", font=f16, fill=C["slot_num"])

    # 셀 내용 (index 0 = 맨 위 슬롯)
    for j, item in enumerate(queue):
        x0, y0 = QL, QT + j * CHL
        fill = CELL_COLORS[j % len(CELL_COLORS)]
        if hl_rear  and j == len(queue)-1: fill = C["hl_rear"]
        if hl_front and j == 0:            fill = C["hl_front"]
        d.rectangle([x0+1, y0+1, x0+QW-1, y0+CHL-1], fill=fill)
        bb = d.textbbox((0,0), item, font=f22)
        d.text((x0+(QW-(bb[2]-bb[0]))//2, y0+(CHL-(bb[3]-bb[1]))//2),
               item, font=f22, fill=(40,40,80))

    # size 표시
    d.text((QL, QB+10), f"size: {len(queue)} / {MAX_Q}", font=f18, fill=C["info"])

    # 코드 박스
    rrect(d, [CX, CY, CX+CW, CY+CBH], 10, C["code_bg"])
    code_map = {
        "declare": ("카페무솔트 = Queue()  # 큐 선언",                               C["dft"]),
        "enqueue": (f'카페무솔트.enqueue("{word}")',                                  C["enq"]),
        "dequeue": ("카페무솔트.dequeue()",                                           C["deq"]),
        "front":   (f'카페무솔트.front()  →  "{front_val}"',                         C["frt"]),
        "isEmpty": (f'카페무솔트.isEmpty()  →  {"True" if empty_val else "False"}',  C["emp"]),
        "clear":   ("카페무솔트.clear()",                                             C["clr"]),
    }
    code_str, col = code_map.get(op, ("", C["dft"]))
    tw2 = d.textbbox((0,0), code_str, font=f26)[2]
    d.text((CX+(CW-tw2)//2, CY+28), code_str, font=f26, fill=col)
    if member:
        d.text((CX, CY+CBH+12), f"📌 {member}", font=f19, fill=(100,100,180))

    # 하단 단어 목록
    half = len(WORDS_ALL) // 2
    d.text((40, H-58), "팀원 단어: "+" · ".join(WORDS_ALL[:half]),  font=f18, fill=C["info"])
    d.text((40, H-34), "            "+" · ".join(WORDS_ALL[half:]), font=f18, fill=C["info"])

    return img

# ── 프레임 헬퍼 ──────────────────────────────────────────────────────
def still(queue, op, word, member,
          front_val=None, empty_val=None,
          hl_front=False, hl_rear=False, n=FPS*2):
    return [to_cv2(draw_frame(queue, op, word, member,
                              front_val, empty_val, hl_front, hl_rear))
            for _ in range(n)]

# ── 선언 애니메이션 ───────────────────────────────────────────────────
def declare_frames():
    out = []
    f30, f26, f18, f16 = fnt(30), fnt(26), fnt(18), fnt(16)
    full = [QL-4, QT-4, QL+QW+4, QB+4]
    code = "카페무솔트 = Queue()  # 큐 선언"

    def base():
        img = Image.new("RGB",(W,H),C["bg"]); d = ImageDraw.Draw(img)
        d.text((40,22),"Queue Animation",    font=f30, fill=C["title"])
        d.text((40,58),"자료구조 큐 시각화", font=f18, fill=C["info"])
        return img, d

    def qname(d):
        rrect(d, [QL,QT-48,QL+QW,QT-4], 8, (255,245,235), C["qborder"], 2)
        tw = d.textbbox((0,0),"카페무솔트",font=f26)[2]
        d.text((QL+(QW-tw)//2,QT-40),"카페무솔트",font=f26,fill=C["qname"])

    def grid(d):
        rrect(d, full, 10, C["qbg"], C["qborder"], 3)
        d.text((QL,QB+10), f"size: 0 / {MAX_Q}", font=f18, fill=C["info"])
        for i in range(MAX_Q+1):
            d.line([(QL,QT+i*CHL),(QL+QW,QT+i*CHL)], fill=C["grid"], width=1)
        for i in range(MAX_Q):
            d.text((QL+5,QT+i*CHL+4), f"[{i}]", font=f16, fill=C["slot_num"])

    for _ in range(20):
        img,_ = base(); out.append(to_cv2(img))
    for t in range(15):
        img,d = base()
        if t > 7: qname(d)
        out.append(to_cv2(img))
    total_h = full[3]-full[1]
    for t in range(30):
        frac = (t+1)/30; frac = frac*frac*(3-2*frac)
        img,d = base(); qname(d)
        d.rounded_rectangle([full[0],full[1],full[2],full[1]+max(int(total_h*frac),20)],
                             radius=10, fill=C["qbg"], outline=C["qborder"], width=3)
        out.append(to_cv2(img))
    for i in range(MAX_Q+1):
        for _ in range(2):
            img,d = base(); qname(d)
            rrect(d, full, 10, C["qbg"], C["qborder"], 3)
            d.text((QL,QB+10), f"size: 0 / {MAX_Q}", font=f18, fill=C["info"])
            for j in range(i+1):
                d.line([(QL,QT+j*CHL),(QL+QW,QT+j*CHL)], fill=C["grid"], width=1)
            out.append(to_cv2(img))
    step = max(1, len(code)//20); ci = 0
    while ci <= len(code):
        img,d = base(); qname(d); grid(d)
        rrect(d, [CX,CY,CX+CW,CY+CBH], 10, C["code_bg"])
        if ci: d.text((CX+20,CY+28), code[:ci], font=f26, fill=C["dft"])
        tw = d.textbbox((0,0),code[:ci],font=f26)[2]
        d.rectangle([CX+20+tw+2,CY+28,CX+20+tw+14,CY+56], fill=(180,180,180))
        out.append(to_cv2(img)); ci += step
    for _ in range(45):
        img,d = base(); qname(d); grid(d)
        rrect(d, [CX,CY,CX+CW,CY+CBH], 10, C["code_bg"])
        d.text((CX+20,CY+28), code, font=f26, fill=C["dft"])
        out.append(to_cv2(img))
    return out

# ── clear 애니메이션 ──────────────────────────────────────────────────
def clear_frames(q_before):
    out = []; q = q_before[:]
    while q:
        for _ in range(8):
            out.append(to_cv2(draw_frame(q,"clear","","",hl_front=True)))
        q.pop(0)
        for _ in range(4):
            out.append(to_cv2(draw_frame(q,"clear","","")))
    for _ in range(FPS):
        out.append(to_cv2(draw_frame([],"clear","","")))
    return out

# ── 메인 렌더링 ───────────────────────────────────────────────────────
def render():
    writer = cv2.VideoWriter(OUT_PATH, cv2.VideoWriter_fourcc(*"mp4v"), FPS, (W,H))
    queue  = []

    for op, word, member in OPERATIONS:
        q_prev = queue[:]

        if op == "declare":
            for f in declare_frames(): writer.write(f)

        elif op == "enqueue":
            queue.append(word)
            for f in still(queue,op,word,member,hl_rear=True,  n=14):     writer.write(f)
            for f in still(queue,op,word,member,hl_rear=True,  n=FPS+10): writer.write(f)

        elif op == "dequeue":
            for f in still(queue,op,word,member,hl_front=True, n=12):     writer.write(f)
            queue.pop(0)
            for f in still(queue,op,word,member,               n=FPS+5):  writer.write(f)

        elif op == "front":
            fv = queue[0] if queue else ""
            for f in still(queue,op,word,member,front_val=fv,
                           hl_front=True, n=FPS*2): writer.write(f)

        elif op == "isEmpty":
            for f in still(queue,op,word,member,
                           empty_val=(len(queue)==0), n=FPS*2): writer.write(f)

        elif op == "clear":
            for f in clear_frames(q_prev): writer.write(f)
            queue.clear()

    writer.release()
    path = os.path.abspath(OUT_PATH)
    print(f"✅ 영상 저장 완료: {path}")
    if sys.platform == "win32":
        os.startfile(path)
        import subprocess; subprocess.Popen(f'explorer /select,"{path}"')

if __name__ == "__main__":
    render()