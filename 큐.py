import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.font_manager as fm
import csv
import os

# 1. 폰트 및 FFmpeg 설정 (본인 환경에 맞게 경로 확인 필수)
font_path = r'C:\Windows\Fonts\malgun.ttf' 
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['font.family'] = font_name
plt.rcParams['animation.ffmpeg_path'] = r'C:\Users\leemy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe'

# 2. 모든 데이터(30개) 로드
team_words = []
try:
    with open('team_words.csv', 'r', encoding='cp949') as f:
        reader = csv.reader(f)
        for row in reader:
            if row: team_words.extend(row)

except:
    # 파일 읽기 실패 시 테스트용 30개 가상 데이터
    team_words = [f"팀원단어_{i+1}" for i in range(30)]

# 3. 애니메이션 시나리오 구성
frames = []
queue = []
MAX_SIZE = 10

# i. 시작: 큐 선언
frames.append(("Queue()", list(queue), "카페무솔트 큐 생성 (크기 제한: 10)"))

# ii. 30개 단어 순환 처리 (10개씩 넣고 5개씩 빼는 방식 등으로 순환)
word_idx = 0
while word_idx < len(team_words):
    # 큐가 가득 차지 않았으면 데이터 삽입
    if len(queue) < MAX_SIZE:
        current_word = team_words[word_idx]
        queue.append(current_word)
        frames.append((f"enqueue('{current_word}')", list(queue), f"{word_idx+1}번째 단어 입장"))
        word_idx += 1
    
    # 큐가 가득 찼거나, 데이터를 어느 정도 보여줬을 때 front실행 후, dequeue 실행 (순환을 위해)
    if len(queue) == MAX_SIZE:
        frames.append(("front()", list(queue), f"반환값: '{queue[0]}' (데이터 추출)"))
        for _ in range(5): # 5개씩 빼서 자리를 만듦
            removed = queue.pop(0)
            frames.append(("dequeue()", list(queue), f"'{removed}' 처리 완료 (자리 확보)"))

# iii. 남은 데이터 모두 제거 (모든 단어 사용 완료 후)
while queue:
    removed = queue.pop(0)
    frames.append(("dequeue()", list(queue), "남은 데이터 순차 처리 중..."))

# iv. 필수 연산 포함 (isEmpty, clear)
frames.append(("isEmpty()", list(queue), f"모든 단어 처리 완료: {len(queue)==0}"))
frames.append(("clear()", [], "작업 종료 - 큐 초기화"))

# 4. 시각화 함수
fig, ax = plt.subplots(figsize=(12, 7))

def update(i):
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    op_name, current_q, msg = frames[i]
    
    # 이미지 가이드라인 구성
    ax.add_patch(patches.Rectangle((0.1, 0.1), 9.8, 9.8, linewidth=2, edgecolor='#00B0F0', facecolor='white'))
    
    # 왼쪽: 연산 및 진행 정보
    ax.text(0.5, 8, "큐 동작 시뮬레이션 (30개 단어)", fontsize=14, color='gray')
    ax.text(0.5, 7, f"카페무솔트.{op_name}", fontsize=18, fontweight='bold')
    ax.text(0.5, 6.2, f"> {msg}", fontsize=12, color='red')
    
    # 오른쪽: 큐 박스 (위에서 아래로 쌓임)
    ax.add_patch(patches.Rectangle((6, 8.5), 3, 0.8, edgecolor='black', facecolor='#f0f0f0'))
    ax.text(7.5, 8.9, "카페무솔트", ha='center', va='center', fontweight='bold', fontsize=14)
    
    for idx, item in enumerate(current_q):
        y_pos = 7.5 - (idx * 0.75)
        ax.add_patch(patches.Rectangle((6, y_pos), 3, 0.7, edgecolor='black', facecolor='white'))
        # 긴 단어 대응을 위해 폰트 크기 조절
        ax.text(7.5, y_pos + 0.35, item, ha='center', va='center', fontsize=9)

# 5. MP4 저장 및 실행
# 프레임이 많아졌으므로 interval을 조금 줄여 속도를 높였습니다.
anim = animation.FuncAnimation(fig, update, frames=len(frames), interval=1500, repeat=False)

save_path = 'queue_30_words_final.mp4'
try:
    print(f"총 {len(frames)}프레임의 MP4 영상을 제작합니다...")
    # FPS를 2로 설정하여 30개 단어 처리가 너무 지루하지 않게 조절
    writer = animation.FFMpegWriter(fps=2, bitrate=2500)
    anim.save('queue_30_final_result.mp4', writer=writer)
    print("완료! 'queue_30_final_result.mp4' 파일이 저장되었습니다.")
except Exception as e:
    print(f"저장 중 오류 발생: {e}")

# 화면 실행창(plt.show)을 제거했습니다.
plt.close()
plt.show()
