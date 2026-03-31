import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import platform

# 1. 한글 폰트 깨짐 방지 설정 (운영체제에 맞게 자동 설정)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# 2. 팀원들이 작성한 단어 데이터 (CSV 파일에서 읽어오기)
words = []
try:
    # 한글 깨짐 방지를 위해 cp949 인코딩 사용
    with open('words.CSV', 'r', encoding='cp949') as f:
        reader = csv.DictReader(f)
        for row in reader:
            words.append(row['word1'])
            words.append(row['word2'])
            words.append(row['word3'])
except FileNotFoundError:
    print("words.CSV 파일이 없습니다! 파일을 같은 폴더에 넣어주세요.")
    exit()

# 3. 애니메이션 시나리오 구성 (제약 조건 완벽 충족)
operations = [("init", "queue = Queue()"), ("isEmpty", None)]

q_size = 0
for w in words:
    # 큐 크기가 10에 도달하면 제약 조건을 위해 비우는 과정
    if q_size >= 10:
        operations.append(("front", None)) # 꽉 찼을 때 front(맨 앞) 데이터 확인
        for _ in range(5):
            operations.append(("dequeue", None)) # 공간 확보를 위해 5개 빼기
            q_size -= 1
            
    # 단어 삽입
    operations.append(("enqueue", w))
    q_size += 1

# 남은 데이터 정리 및 모든 연산 시연
operations.append(("clear", None))
operations.append(("isEmpty", None))

# 4. 애니메이션 그리기 설정
fig, ax = plt.subplots(figsize=(10, 6))
queue = []

def update(frame):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14) # 파이프 구조를 위해 y축 높이 확장
    ax.axis('off') # 테두리 숨기기

    op, val = operations[frame]
    code_str = ""

    # 큐 연산 로직 (Queue 상태 업데이트)
    if op == "init":
        queue.clear()
        code_str = "queue = []"
    elif op == "enqueue":
        queue.append(val)
        code_str = f'queue.enqueue("{val}")'
    elif op == "dequeue":
        if queue:
            popped = queue.pop(0) # 큐는 선입선출이므로 맨 앞(0번 인덱스)에서 삭제
            code_str = f'queue.dequeue()\n# 반환: {popped}'
    elif op == "front":
        if queue:
            front_val = queue[0]
            code_str = f'queue.front()\n# 맨 앞: {front_val}'
    elif op == "isEmpty":
        is_empty = len(queue) == 0
        code_str = f'queue.isEmpty()\n# 반환: {is_empty}'
    elif op == "clear":
        queue.clear()
        code_str = "queue.clear()"

    # 화면 좌측: 현재 실행 중인 코드 라인 출력 (기존 디자인 유지)
    ax.text(0.5, 7, code_str, fontsize=18, va='center', ha='left',
            bbox=dict(facecolor='#f0f8ff', edgecolor='#4682b4', boxstyle='round,pad=0.5', lw=2))

    # 화면 우측: 큐 구조 그리기 (위아래가 뚫린 파이프 형태)
    ax.plot([6, 6], [2, 12], color='black', lw=3) # 왼쪽 벽
    ax.plot([9, 9], [2, 12], color='black', lw=3) # 오른쪽 벽

    # 큐 방향 표시 (직관적인 애니메이션 효과)
    ax.text(7.5, 1, "▼ FRONT (출구) ▼", fontsize=14, ha='center', va='center', color='red', fontweight='bold')
    ax.text(7.5, 13, "▲ REAR (입구) ▲", fontsize=14, ha='center', va='center', color='blue', fontweight='bold')

    # 큐 내부의 데이터 그리기 (아래에서부터 위로 쌓이는 시각화)
    for i, item in enumerate(queue):
        rect = patches.Rectangle((6.1, 2.1 + i), 2.8, 0.8, facecolor='#ffe4e1', edgecolor='black')
        ax.add_patch(rect)
        ax.text(7.5, 2.5 + i, item, fontsize=14, ha='center', va='center')

    # 상단에 현재 큐 크기 표시
    ax.text(7.5, 14, f"Queue Size: {len(queue)}/10", fontsize=12, ha='center', va='center', color='gray')

# 애니메이션 객체 생성 (1프레임당 1초 간격)
ani = animation.FuncAnimation(fig, update, frames=len(operations), interval=1000, repeat=False)

# 5. MP4 파일로 저장
print("애니메이션을 렌더링하고 있습니다. 잠시만 기다려주세요... (약 20~30초 소요)")
ani.save('20251267.mp4', writer='ffmpeg', fps=1)
print("저장 완료! '20251267.mp4' 파일을 확인해 보세요.")