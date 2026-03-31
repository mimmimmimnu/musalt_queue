import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import matplotlib.animation as animation


FONT_CANDIDATES = [
    'C:/Windows/Fonts/malgun.ttf',
    'C:/Windows/Fonts/NanumGothic.ttf',
]

font_path = None
for fp_candidate in FONT_CANDIDATES:
    try:
        fm.FontProperties(fname=fp_candidate)
        font_path = fp_candidate
        break
    except Exception:
        pass

def make_fp(size, weight='normal'):
    if font_path:
        return fm.FontProperties(fname=font_path, size=size, weight=weight)
    return fm.FontProperties(family='sans-serif', size=size, weight=weight)

FP      = make_fp(13)
FP_SM   = make_fp(10)
FP_LG   = make_fp(17)
FP_BOLD = make_fp(13, 'bold')
FP_CODE = make_fp(12)

# words.csv 내용
MEMBERS = [
    ('이유민',  '20251223', ['카푸치노',   '카페라떼',     '피넛라떼'  ]),
    ('김수민',  '20251185', ['말차라떼',   '초코라떼',     '레몬티'    ]),
    ('이채영',  '20251229', ['자몽티',     '카페모카',     '매실티'    ]),
    ('유지민',  '20251209', ['얼그레이티', '스콘',         '레몬티'    ]),
    ('정서하',  '20252213', ['레몬티',     '카푸치노',     '초코 스콘' ]),
    ('이예은',  '20252199', ['매실티',     '페퍼민트티',   '휘낭시에'  ]),
    ('이윤서',  '20251225', ['딸기라떼',   '딸기에이드',   '망고에이드']),
    ('황다원',  '20251267', ['스콘',       '청포도에이드', '매실티'    ]),
    ('안예원',  '20252185', ['카페라떼',   '말차라떼',     '카푸치노'  ]),
    ('유가현',  '20251207', ['캐모마일티', '초코 스콘',    '레몬티'    ]),
]

all_words = []
seen = set()
for name, _, words in MEMBERS:
    for w in words:
        if w not in seen:
            seen.add(w)
            all_words.append((w, name))

W10 = all_words[:10]   # 최대 10개 사용

# 연산 시나리오
STEPS = []

def add(t, c, d):
    STEPS.append((t, c, d))

# 큐 선언
add('declare', 'Queue<string> 카페무솔트', '큐를 선언합니다.')

# isEmpty -> true
add('isEmpty', '카페무솔트.isEmpty()', '큐가 비어 있는지 확인합니다.')

# enqueue 3개
for i in range(3):
    w, m = W10[i]
    add('enqueue', f'카페무솔트.enqueue("{w}")', f'{m}의 "{w}"를 enqueue')

# front 확인
add('front', '카페무솔트.front()', '맨 앞 원소를 확인합니다.')

# dequeue 2개
add('dequeue', '카페무솔트.dequeue()', '맨 앞 원소를 dequeue합니다.')
add('dequeue', '카페무솔트.dequeue()', '맨 앞 원소를 dequeue합니다.')

# enqueue 4개
for i in range(3, 7):
    w, m = W10[i]
    add('enqueue', f'카페무솔트.enqueue("{w}")', f'{m}의 "{w}"를 enqueue')

# front 확인
add('front', '카페무솔트.front()', '현재 맨 앞 원소를 확인합니다.')

# enqueue 3개
for i in range(7, 10):
    w, m = W10[i]
    add('enqueue', f'카페무솔트.enqueue("{w}")', f'{m}의 "{w}"를 enqueue')

# dequeue 2개
add('dequeue', '카페무솔트.dequeue()', '맨 앞 원소를 dequeue합니다.')
add('dequeue', '카페무솔트.dequeue()', '맨 앞 원소를 dequeue합니다.')

# isEmpty → false
add('isEmpty', '카페무솔트.isEmpty()', '큐가 비어 있는지 확인합니다.')

# clear
add('clear', '카페무솔트.clear()', '모든 원소를 삭제합니다.')

# isEmpty → true
add('isEmpty', '카페무솔트.isEmpty()', 'clear 후 isEmpty를 확인합니다.')

# 큐 상태 사전 계산
_q = []
QUEUE_STATES = [[]]   # 각 스텝 실행 전 큐 상태
RESULTS      = [None] # 각 스텝의 결과 메시지

for op, code, _ in STEPS:
    msg = None
    if op == 'enqueue':
        word = code.split('"')[1]
        _q.append(word)
    elif op == 'dequeue':
        if _q:
            msg = f'dequeue → "{_q.pop(0)}"'
    elif op == 'front':
        msg = f'front → "{_q[0]}"' if _q else 'front → null'
    elif op == 'isEmpty':
        msg = f'isEmpty → {str(len(_q) == 0).lower()}'
    elif op == 'clear':
        _q.clear()
        msg = 'clear 완료'
    QUEUE_STATES.append(list(_q))
    RESULTS.append(msg)

# 색상 테마
COLORS = {
    'declare': '#5b8dee',
    'enqueue': '#4caf82',
    'dequeue': '#e07070',
    'front':   '#c8a96e',
    'isEmpty': '#9b7ec8',
    'clear':   '#e07070',
}
BG       = '#f7f4ef'
WHITE    = '#ffffff'
DARK_HDR = '#1a3a4a'
TEAL     = '#2196a0'

fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(0, 13)
ax.set_ylim(0, 7)
ax.axis('off')
fig.tight_layout(pad=0.3)

def draw_static():
    # 외곽 테두리
    ax.add_patch(patches.FancyBboxPatch(
        (0.15, 0.15), 12.7, 6.7,
        boxstyle='round,pad=0.05',
        linewidth=2.5, edgecolor=TEAL, facecolor=WHITE
    ))
    # 좌/우 구분선
    ax.axvline(x=7.5, ymin=0.02, ymax=0.98,
               color='#d0d0d0', linewidth=1, linestyle='--')
    # 우측 상단 타이틀 박스
    ax.add_patch(patches.FancyBboxPatch(
        (8.0, 5.8), 4.8, 0.9,
        boxstyle='round,pad=0.05',
        linewidth=1.5, edgecolor=TEAL, facecolor=DARK_HDR
    ))
    ax.text(10.4, 6.25, '카페무솔트',
            ha='center', va='center', color='white', fontproperties=FP_LG)
    ax.text(0.5, 6.7, '연산',
            ha='left', va='center', color='#888888', fontproperties=FP_SM)

draw_static()

# 동적 요소 관리
dyn_artists = []

def clear_dyn():
    for a in dyn_artists:
        a.remove()
    dyn_artists.clear()

# 프레임 그리기
def draw_frame(idx):
    clear_dyn()
    if idx < 0 or idx >= len(STEPS):
        return

    op, code, desc = STEPS[idx]
    oc  = COLORS[op]
    q_b = QUEUE_STATES[idx]       # 이 스텝 실행 전 큐
    q_a = QUEUE_STATES[idx + 1]   # 이 스텝 실행 후 큐
    res = RESULTS[idx + 1]        # 결과 메시지

    # 스텝 카운터
    dyn_artists.append(ax.text(
        6.8, 6.7, f'Step {idx+1} / {len(STEPS)}',
        ha='right', va='center', color='#aaaaaa', fontproperties=FP_SM
    ))

    # 현재 연산 타입 뱃지
    bb = patches.FancyBboxPatch(
        (0.3, 6.3), 2.2, 0.5,
        boxstyle='round,pad=0.05',
        linewidth=1.5, edgecolor=oc, facecolor=oc
    )
    ax.add_patch(bb)
    dyn_artists.append(bb)
    dyn_artists.append(ax.text(
        1.4, 6.55, op + '()',
        ha='center', va='center', color='white', fontproperties=FP_BOLD
    ))

    # 현재 연산 코드 하이라이트 박스
    hl = patches.FancyBboxPatch(
        (0.3, 3.4), 6.8, 1.1,
        boxstyle='round,pad=0.08',
        linewidth=2, edgecolor=oc, facecolor=oc + '22'
    )
    ax.add_patch(hl)
    dyn_artists.append(hl)
    dyn_artists.append(ax.text(
        0.65, 4.0, code,
        ha='left', va='center', color=oc, fontproperties=FP_CODE
    ))

    # 설명 텍스트
    dyn_artists.append(ax.text(
        0.65, 2.9, desc,
        ha='left', va='center', color='#555555', fontproperties=FP_SM
    ))

    # 결과 박스
    if res:
        rb = patches.FancyBboxPatch(
            (0.3, 1.8), 6.8, 0.75,
            boxstyle='round,pad=0.08',
            linewidth=1.5, edgecolor=oc, facecolor=WHITE
        )
        ax.add_patch(rb)
        dyn_artists.append(rb)
        dyn_artists.append(ax.text(
            0.65, 2.18, f'결과:  {res}',
            ha='left', va='center', color=oc, fontproperties=FP_SM
        ))

    # 이전 스텝 로그 (최근 3개)
    for li, pi in enumerate(range(max(0, idx - 3), idx)):
        pt = STEPS[pi][0]
        dyn_artists.append(ax.text(
            0.65, 1.3 - li * 0.35,
            f'  {pi+1:02d}.  {STEPS[pi][1]}',
            ha='left', va='center',
            color=COLORS[pt] + '88', fontproperties=FP_SM
        ))

    # 우측: 큐 시각화
    display_q = list(q_b) if op in ('dequeue', 'front') else list(q_a)

    BW = 4.8      # 박스 너비
    BH = 0.62     # 박스 높이
    BX = 8.0      # 박스 x 시작
    TY = 5.5      # 첫 번째 박스 상단 y

    # front / rear 레이블
    if display_q:
        dyn_artists.append(ax.text(
            7.75, TY - 0.31, 'front ▶',
            ha='right', va='center', color='#c8a96e', fontproperties=FP_SM
        ))
        if len(display_q) > 1:
            dyn_artists.append(ax.text(
                7.75, TY - (len(display_q) - 1) * BH - 0.31, 'rear  ▶',
                ha='right', va='center', color='#5b8dee', fontproperties=FP_SM
            ))

    # 큐 원소 박스
    for i, item in enumerate(display_q):
        by = TY - i * BH - BH

        # 각 상황에 맞는 색상
        if op == 'enqueue' and i == len(display_q) - 1:
            fc2, ec2, lw2 = '#d4f5e9', COLORS['enqueue'], 2.0
        elif op == 'dequeue' and i == 0:
            fc2, ec2, lw2 = '#ffe0e0', COLORS['dequeue'], 2.0
        elif op == 'front' and i == 0:
            fc2, ec2, lw2 = '#fff3d6', COLORS['front'], 2.0
        elif i == 0:
            fc2, ec2, lw2 = '#e8f4f8', TEAL, 1.5
        else:
            fc2, ec2, lw2 = '#f0f0f0', '#bbbbbb', 1.0

        b = patches.FancyBboxPatch(
            (BX, by), BW, BH - 0.05,
            boxstyle='round,pad=0.03',
            linewidth=lw2, edgecolor=ec2, facecolor=fc2
        )
        ax.add_patch(b)
        dyn_artists.append(b)
        dyn_artists.append(ax.text(
            BX + BW / 2, by + BH / 2 - 0.03, item,
            ha='center', va='center', color='#1a1a1a', fontproperties=FP
        ))

    # 큐가 비어 있을 때
    if not display_q:
        eb = patches.FancyBboxPatch(
            (BX, TY - BH), BW, BH - 0.05,
            boxstyle='round,pad=0.03',
            linewidth=1.5, edgecolor='#cccccc', facecolor='#f9f9f9',
            linestyle='--'
        )
        ax.add_patch(eb)
        dyn_artists.append(eb)
        dyn_artists.append(ax.text(
            BX + BW / 2, TY - BH / 2 - 0.03, '(비어 있음)',
            ha='center', va='center', color='#aaaaaa', fontproperties=FP_SM
        ))

    # 큐 크기 표시
    dyn_artists.append(ax.text(
        10.4, 0.5, f'size = {len(display_q)}  /  MAX = 10',
        ha='center', va='center', color='#888888', fontproperties=FP_SM
    ))

# 애니메이션
INTERVAL_MS  = 1800   # 스텝당 간격 (ms). 조절 가능
REPEAT_DELAY = 3000   # 반복 전 대기 시간 (ms)

def animate(frame):
    draw_frame(frame - 1)
    return dyn_artists

ani = animation.FuncAnimation(
    fig,
    animate,
    frames=len(STEPS) + 2,
    interval=INTERVAL_MS,
    blit=False,
    repeat=True,
    repeat_delay=REPEAT_DELAY
)