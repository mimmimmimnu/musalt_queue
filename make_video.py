import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import os

# 1. 파일 경로 설정
current_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_path, 'words.csv')

# 2. 데이터 추출 (첫 줄 word1,2,3 무시하고 데이터만 가져오기)
try:
    # skiprows=[0]을 넣어 첫 번째 행(word1, word2, word3)을 아예 읽지 않습니다.
    df = pd.read_csv(csv_path, header=None, skiprows=[0], encoding='cp949')
    
    menu_pool = []
    for _, row in df.iterrows():
        # row[2], row[3], row[4]가 메뉴 데이터입니다.
        menu_pool.extend([str(row[2]).strip(), str(row[3]).strip(), str(row[4]).strip()])
    
    # nan 값 제거
    menu_pool = [m for m in menu_pool if m.lower() != 'nan' and m != '']
except Exception as e:
    print(f"데이터 로드 에러: {e}")
    menu_pool = []

# 3. 큐 시나리오 구성 (과제 요구사항 반영)
queue = deque()
history = []

def record(msg):
    history.append((list(queue), msg))

# [Step 1] isEmpty 연산
record(f"Queue 선언 (isEmpty: {len(queue)==0})")

# [Step 2] enqueue 연산 (모든 메뉴 사용)
for item in menu_pool:
    if len(queue) >= 10:
        removed = queue.popleft()
        record(f"dequeue('{removed}') - 크기 유지")
        
    queue.append(item)
    record(f"enqueue('{item}')")

# [Step 3] front 및 dequeue 연산
if queue:
    record(f"front() 데이터 확인: {queue[0]}")
    val = queue.popleft()
    record(f"dequeue() 수행: {val}")

# [Step 4] clear 연산
queue.clear()
record(f"clear() 수행 완료 (isEmpty: {len(queue)==0})")

# 4. 시각화 설정 (맥북 한글 폰트 적용)
fig, ax = plt.subplots(figsize=(12, 6))
plt.rcParams['font.family'] = 'AppleGothic' 

def update(frame):
    ax.clear()
    curr_q, msg = history[frame]
    ax.set_title(f"카페무솔트 큐 시스템\n{msg}", fontsize=16, pad=20)
    
    for i, txt in enumerate(curr_q):
        ax.text(i, 0.5, txt, ha='center', va='center', fontsize=9,
                bbox=dict(boxstyle="round,pad=0.5", fc="skyblue", ec="navy", lw=1.5))
    
    ax.set_xlim(-0.5, 9.5)
    ax.set_ylim(0, 1)
    ax.set_xticks(range(10))
    ax.set_yticks([])

# 5. 애니메이션 저장
ani = FuncAnimation(fig, update, frames=len(history), repeat=False)
output_file = '20252213.mp4' 
ani.save(output_file, writer='ffmpeg', fps=1)
print(f"애니메이션 생성 완료: {output_file}")