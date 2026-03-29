import os

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

class Queue:
    def __init__(self): self.items = []
    def enqueue(self, item): self.items.append(item)
    def dequeue(self): return self.items.pop(0) if not self.isEmpty() else None
    def front(self): return self.items[0] if not self.isEmpty() else None
    def isEmpty(self): return len(self.items) == 0
    def clear(self): self.items = []

SCENARIO = [
    ("declare",  None),
    ("isEmpty",  None),
    ("enqueue",  "카푸치노1"),
    ("enqueue",  "카페라떼1"),
    ("enqueue",  "피넛라떼"),
    ("enqueue",  "말차라떼1"),
    ("enqueue",  "초코라떼"),
    ("enqueue",  "레몬티1"),
    ("enqueue",  "자몽티"),
    ("enqueue",  "카페모카"),
    ("enqueue",  "매실티1"),
    ("front",    None),
    ("dequeue",  None),
    ("enqueue",  "얼그레이티"),
    ("dequeue",  None),
    ("enqueue",  "스콘1"),
    ("dequeue",  None),
    ("enqueue",  "레몬티2"),
    ("dequeue",  None),
    ("enqueue",  "레몬티3"),
    ("dequeue",  None),
    ("enqueue",  "카푸치노2"),
    ("dequeue",  None),
    ("enqueue",  "초코스콘1"),
    ("dequeue",  None),
    ("enqueue",  "매실티2"),
    ("dequeue",  None),
    ("enqueue",  "페퍼민트티"),
    ("dequeue",  None),
    ("enqueue",  "휘낭시에"),
    ("dequeue",  None),
    ("enqueue",  "딸기라떼"),
    ("dequeue",  None),
    ("enqueue",  "딸기에이드"),
    ("dequeue",  None),
    ("enqueue",  "망고에이드"),
    ("dequeue",  None),
    ("enqueue",  "스콘2"),
    ("dequeue",  None),
    ("enqueue",  "청포도에이드"),
    ("dequeue",  None),
    ("enqueue",  "매실티3"),
    ("dequeue",  None),
    ("enqueue",  "카페라떼2"),
    ("dequeue",  None),
    ("enqueue",  "말차라떼2"),
    ("dequeue",  None),
    ("enqueue",  "카푸치노3"),
    ("dequeue",  None),
    ("enqueue",  "캐모마일티"),
    ("dequeue",  None),
    ("enqueue",  "초코스콘2"),
    ("dequeue",  None),
    ("enqueue",  "레몬티4"),
    ("front",    None),
    ("clear",    None),
    ("isEmpty",  None),
]

W_LEFT  = 30   # 왼쪽 연산 영역 너비
W_RIGHT = 20   # 오른쪽 큐 박스 너비
SEP     = "│"

def box(text, width):
    inner = width - 2          # 테두리 제외
    t = text.center(inner)[:inner]
    top    = "┌" + "─" * inner + "┐"
    middle = "│" + t           + "│"
    bottom = "└" + "─" * inner + "┘"
    return top, middle, bottom

def draw(q, op, val, result, step):
    clear()
    total = len(SCENARIO)

    # 제목줄 (큐 이름 오른쪽 박스)
    title_top, title_mid, title_bot = box("카페무슬트", W_RIGHT)
    print(" " * W_LEFT + title_top)
    print(" " * W_LEFT + title_mid)
    print(" " * W_LEFT + title_bot)
    print()

    # 왼쪽 연산 문자열
    if   op == "declare": left = "카페무슬트 = Queue()"
    elif op == "enqueue": left = f'카페무슬트.enqueue("{val}")'
    elif op == "dequeue": left = f"카페무슬트.dequeue()  →  {result}"
    elif op == "front":   left = f"카페무슬트.front()    →  {result}"
    elif op == "isEmpty": left = f"카페무슬트.isEmpty()  →  {result}"
    elif op == "clear":   left =  "카페무슬트.clear()"
    else:                 left = op

    # 큐 아이템 박스들 (위→아래 = front→rear)
    items = list(q.items)
    rows = []
    for i, item in enumerate(items):
        t, m, b = box(item, W_RIGHT)
        # 맨 위 아이템만 top 테두리 출력, 이후는 top 생략(이어붙임)
        if i == 0:
            rows.append(t)
        rows.append(m)
        rows.append(b)

    if not items:
        t, m, b = box("(비어있음)", W_RIGHT)
        rows = [t, m, b]

    # 왼쪽 연산 + 오른쪽 큐 박스 나란히 출력
    # 연산 텍스트는 박스들의 중간 행에 배치
    mid_row = len(rows) // 2
    for i, row in enumerate(rows):
        if i == mid_row:
            l = left.ljust(W_LEFT)
        else:
            l = " " * W_LEFT
        print(l + row)

    print()
    print(f"  [{step:02d}/{total}]  크기: {len(q.items)}/10")
    print("─" * (W_LEFT + W_RIGHT))
    print("  Enter: 다음  │  q+Enter: 종료")

def run():
    q = Queue()
    for step, (op, val) in enumerate(SCENARIO, 1):
        result = None
        if   op == "declare": pass
        elif op == "enqueue": q.enqueue(val)
        elif op == "dequeue": result = q.dequeue()
        elif op == "front":   result = q.front()
        elif op == "isEmpty": result = q.isEmpty()
        elif op == "clear":   q.clear()

        draw(q, op, val, result, step)
        if input("  > ").strip().lower() == 'q':
            clear(); print("  종료합니다. 👋"); return

    clear()
    print("=" * (W_LEFT + W_RIGHT))
    print("  🎉 모든 큐 연산이 완료되었습니다!")
    print("=" * (W_LEFT + W_RIGHT))

if __name__ == "__main__":
    run()
