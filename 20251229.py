import tkinter as tk
import time
from collections import deque

class Queue:
    def __init__(self, canvas, code_label, queue_rects, queue_texts, info_label):
        self.items = deque()
        self.canvas = canvas
        self.code_label = code_label
        self.queue_rects = queue_rects 
        self.queue_texts = queue_texts
        self.info_label = info_label
        self.max_size = 10
        self.draw_queue_boundary()

    def draw_queue_boundary(self):
        # 상단 제목 및 큐 외곽선
        self.canvas.create_text(350, 40, text="카페무솔트", font=("Malgun Gothic", 15, "bold"))
        x1, y1, x2, y2 = 250, 60, 450, 460
        self.canvas.create_line(x1, y1, x1, y2, width=3, fill="black")
        self.canvas.create_line(x2, y1, x2, y2, width=3, fill="black")
        self.canvas.create_line(x1, y2, x2, y2, width=3, fill="black")
        self.canvas.create_text(350, 480, text="[ Front / Exit ]", font=("Malgun Gothic", 10, "italic"))

    def update_ui(self, code_text, delay=0.8):
        self.code_label.config(text=f'<< Current Code >>\n\n{code_text}')
        size = len(self.items)
        front_item = self.items[0] if self.items else "None"
        self.info_label.config(text=f"Queue Size: {size} / 10 | Front Item: {front_item}")
        self.canvas.update()
        if delay > 0:
            time.sleep(delay)

    def enqueue(self, item):
        if len(self.items) >= self.max_size:
            self.update_ui(f'// Queue Full!\n카페무솔트.enqueue("{item}") // Fail', delay=1.2)
            return

        self.items.append(item)
        idx = len(self.items) - 1 
        
        rect_id = self.queue_rects[idx]
        text_id = self.queue_texts[idx]
        
        self.canvas.itemconfig(rect_id, fill="#FFC0CB") # Enqueue 효과 (분홍)
        self.canvas.itemconfig(text_id, text=item)
        self.update_ui(f'카페무솔트.enqueue("{item}")')
        self.canvas.itemconfig(rect_id, fill="white")

    def dequeue(self):
        if not self.items:
            self.update_ui('// Queue Empty!\n카페무솔트.dequeue()')
            return None
        
        # FIFO 원리: 맨 아래(index 0) 삭제
        rect_id = self.queue_rects[0]
        text_id = self.queue_texts[0]
        item = self.items.popleft() 

        self.canvas.itemconfig(text_id, text="")
        self.canvas.itemconfig(rect_id, fill="#ADD8E6") # Dequeue 효과 (파란색)
        self.update_ui('카페무솔트.dequeue()')
        self.canvas.itemconfig(rect_id, fill="white")

        # 위에 있는 데이터들을 아래로 정렬
        self.refresh_view()
        return item

    def refresh_view(self):
        for i in range(self.max_size):
            text_val = self.items[i] if i < len(self.items) else ""
            self.canvas.itemconfig(self.queue_texts[i], text=text_val)
        self.canvas.update()

    def front(self):
        item = self.items[0] if self.items else "Empty"
        self.update_ui(f'카페무솔트.front()\n// Result: "{item}"')
        return item

    def isEmpty(self):
        result = "true" if not self.items else "false"
        self.update_ui(f'카페무솔트.isEmpty()\n// Result: {result}')
        return not self.items

    def clear(self):
        self.items.clear()
        for t_id in self.queue_texts:
            self.canvas.itemconfig(t_id, text="")
        self.update_ui('카페무솔트.clear()')

def run_animation():
    # 1. 10초 대기 시간
    for i in range(10, 0, -1):
        queue_obj.code_label.config(text=f'<< Recording Preparation >>\n\n{i}초 후 애니메이션이 시작됩니다.\n녹화 버튼을 눌러주세요.')
        root.update()
        time.sleep(1)
    
    queue_obj.update_ui(queue_obj.update_ui('카페무솔트 = Queue()'))

    # 2. 요청하신 시나리오 실행
    queue_obj.enqueue("카푸치노1")
    queue_obj.enqueue("카페라떼1")
    queue_obj.enqueue("피넛라떼")
    queue_obj.enqueue("말차라떼1")
    queue_obj.enqueue("초코라떼")
    queue_obj.enqueue("레몬티1")
    queue_obj.front()

    for _ in range(5): queue_obj.dequeue()

    queue_obj.enqueue("자몽티")
    queue_obj.enqueue("카페모카")
    queue_obj.enqueue("매실티1")
    queue_obj.enqueue("얼그레이티")
    queue_obj.enqueue("스콘1")
    queue_obj.enqueue("레몬티2")

    for _ in range(3): queue_obj.dequeue()

    queue_obj.enqueue("레몬티3")
    queue_obj.enqueue("카푸치노2")
    queue_obj.enqueue("초코 스콘1")
    queue_obj.enqueue("매실티2")
    queue_obj.enqueue("페퍼민트티")
    queue_obj.enqueue("휘낭시에")

    queue_obj.clear()
    queue_obj.isEmpty()

    queue_obj.enqueue("딸기라떼")
    queue_obj.enqueue("딸기에이드")
    queue_obj.enqueue("망고에이드")
    queue_obj.enqueue("스콘2")
    queue_obj.enqueue("청포도에이드")
    queue_obj.enqueue("매실티3")
    queue_obj.enqueue("카페라떼2")
    queue_obj.enqueue("말차라떼2")
    queue_obj.enqueue("카푸치노3")

    for _ in range(3): queue_obj.dequeue()

    queue_obj.enqueue("캐모마일티")
    queue_obj.enqueue("초코 스콘2")
    queue_obj.enqueue("레몬티3")
    
    queue_obj.front()

    queue_obj.code_label.config(text='<< Current Code >>\n\n// All operations finished.\n// Recording can be stopped.')

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cafe Musalt Queue Animation - Final")
    root.geometry("800x600")

    code_frame = tk.Frame(root)
    code_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
    code_label = tk.Label(code_frame, text="", font=("Consolas", 13, "bold"), fg="#2E7D32", bg="white", relief="sunken", bd=2, height=12, justify=tk.LEFT, anchor="nw")
    code_label.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    info_label = tk.Label(code_frame, text="", font=("Malgun Gothic", 11))
    info_label.pack(fill=tk.X)

    canvas = tk.Canvas(root, width=500, height=550, bg="white")
    canvas.pack(side=tk.RIGHT)

    queue_rects, queue_texts = [], []
    for i in range(10):
        y_bottom, y_top = 455 - (i * 38), 420 - (i * 38)
        r = canvas.create_rectangle(260, y_top, 440, y_bottom, fill="white", outline="gray")
        t = canvas.create_text(350, (y_top + y_bottom)/2, text="", font=("Malgun Gothic", 9))
        queue_rects.append(r)
        queue_texts.append(t)

    queue_obj = Queue(canvas, code_label, queue_rects, queue_texts, info_label)
    root.after(100, run_animation)
    root.mainloop()