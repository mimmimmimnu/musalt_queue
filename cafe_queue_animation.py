import pygame
import pandas as pd
import time
import sys
import ctypes
import os

# 0. 고해상도 및 중앙 배치 설정
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except: pass
os.environ['SDL_VIDEO_CENTERED'] = '1'

# 1. 초기화 및 해상도 (2560x1600)
pygame.init()
INIT_W, INIT_H = 2560, 1600 
screen = pygame.display.set_mode((INIT_W, INIT_H), pygame.RESIZABLE)
pygame.display.set_caption("Cafe Musolt - 33 Words Slow Simulation")

WHITE, BLACK, POINT_BLUE = (255, 255, 255), (0, 0, 0), (0, 51, 153)

def get_fonts(w):
    font_names = ["malgungothic", "nanumgothicbold", "arial"]
    return {
        "code": pygame.font.SysFont(font_names, int(w * 0.032), bold=True),
        "menu": pygame.font.SysFont(font_names, int(w * 0.018), bold=True),
        "title": pygame.font.SysFont(font_names, int(w * 0.015), bold=True)
    }

# 2. 데이터 로드 (33개 메뉴)
def load_data():
    try:
        df = pd.read_csv('menu_data.csv', encoding='utf-8')
        words = []
        for _, row in df.iterrows():
            words.append(str(row['word1']).strip())
            words.append(str(row['word2']).strip())
            words.append(str(row['word3']).strip())
        return words
    except:
        return ["데이터로드실패"] * 33

menu_list = load_data()

# 3. 큐 시뮬레이터 클래스
class QueueSimulator:
    def __init__(self):
        self.items = []
        self.current_code = "카페무솔트 = Queue()"

    def enqueue(self, item):
        if len(self.items) < 10:
            self.items.append(item)
            self.current_code = f"카페무솔트.enqueue('{item}')"

    def dequeue(self):
        if self.items:
            val = self.items.pop(0)
            self.current_code = f"카페무솔트.dequeue() -> '{val}'"

    def front(self):
        if self.items:
            self.current_code = f"카페무솔트.front() -> '{self.items[0]}'"

    def is_empty(self):
        res = (len(self.items) == 0)
        self.current_code = f"카페무솔트.isEmpty() -> {res}"

    def clear(self):
        self.items = []
        self.current_code = "카페무솔트.clear()"

    def draw(self, w, h):
        screen.fill(WHITE)
        fonts = get_fonts(w)
        # 타이틀
        t_box_w, t_box_h = int(w * 0.25), int(h * 0.07)
        pygame.draw.rect(screen, BLACK, (w * 0.7, h * 0.05, t_box_w, t_box_h), 4)
        title_txt = fonts["title"].render("카 페 무 솔 트", True, BLACK)
        screen.blit(title_txt, title_txt.get_rect(center=(w * 0.7 + t_box_w/2, h * 0.05 + t_box_h/2)))
        
        # 코드 로그 (중앙 배치)
        code_txt = fonts["code"].render(self.current_code, True, POINT_BLUE)
        screen.blit(code_txt, (w * 0.08, h * 0.5))
        
        # 큐 시각화 (박스 레이아웃)
        box_w, box_h = int(w * 0.22), int(h * 0.065)
        for i, menu in enumerate(self.items):
            y_pos = (h * 0.88) - (i * box_h)
            pygame.draw.rect(screen, WHITE, (w * 0.73, y_pos, box_w, box_h))
            pygame.draw.rect(screen, BLACK, (w * 0.73, y_pos, box_w, box_h), 3)
            m_txt = fonts["menu"].render(menu, True, BLACK)
            screen.blit(m_txt, m_txt.get_rect(center=(w * 0.73 + box_w/2, y_pos + box_h/2)))
        pygame.display.flip()

# 4. 메인 시나리오
def main():
    sim = QueueSimulator()
    win_w, win_h = INIT_W, INIT_H
    sim.draw(win_w, win_h)
    time.sleep(2.0)

    scenario = [lambda: sim.is_empty()]

    # 33개 단어를 10개씩 끊어서 처리
    for i in range(0, len(menu_list), 10):
        chunk = menu_list[i : i + 10]
        # 1. enqueue 단계
        for menu in chunk:
            scenario.append(lambda m=menu: sim.enqueue(m))
        
        # 2. 필수 연산 시연 단계
        scenario.append(lambda: sim.front())
        scenario.append(lambda: sim.dequeue())
        
        # 3. clear 및 비우기 단계
        scenario.append(lambda: sim.clear())
        scenario.append(lambda: sim.is_empty())

    step_idx = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.VIDEORESIZE:
                win_w, win_h = event.w, event.h
                sim.draw(win_w, win_h)

        if step_idx < len(scenario):
            scenario[step_idx]()
            step_idx += 1
            sim.draw(win_w, win_h)
            
            # --- 속도 조절 핵심 구간 ---
            msg = sim.current_code
            if "clear" in msg or "isEmpty" in msg or "front" in msg:
                time.sleep(2.5) # 연산이 확인되어야 하는 중요한 시점은 2.5초 대기
            elif "dequeue" in msg:
                time.sleep(1.8) # dequeue 확인도 천천히
            else:
                time.sleep(1.2) # 일반적인 enqueue(단어 쌓기)는 1.2초 대기
        else:
            time.sleep(3.0) # 마지막 종료 전 여유 있게 대기
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()