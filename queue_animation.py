import os

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

class Queue:
    def __init__(self): self.items = []
    def enqueue(self, item): self.items.append(item)
    def dequeue(self): return self.items.pop(0) if not self.isEmpty() else None
    def front(self): return self.items[0] if not self.isEmpty() else None
    def isEmpty(self): return len(self.items) == 0
    def clear(self): self.items = []

# 큐 선언 → isEmpty → enqueue ... → front → clear → isEmpty
# 팀원 단어 30개 전부 1회 이상 사용 / 큐 크기 10 이하 유지
SCENARIO = [
    ("declare",   None),          # ← 큐 선언부터 시작
    ("isEmpty",   None),
    ("enqueue",   "카푸치노1"),
    ("enqueue",   "카페라떼1"),
    ("enqueue",   "피넛라떼"),
    ("enqueue",   "말차라떼1"),
    ("enqueue",   "초코라떼"),
    ("enqueue",   "레몬티1"),
    ("enqueue",   "자몽티"),
    ("enqueue",   "카페모카"),
    ("enqueue",   "매실티1"),    # size=9
    ("front",     None),
    ("dequeue",   None),
    ("enqueue",   "얼그레이티"),
    ("dequeue",   None),
    ("enqueue",   "스콘1"),
    ("dequeue",   None),
    ("enqueue",   "레몬티2"),
    ("dequeue",   None),
    ("enqueue",   "레몬티3"),
    ("dequeue",   None),
    ("enqueue",   "카푸치노2"),
    ("dequeue",   None),
    ("enqueue",   "초코스콘1"),
    ("dequeue",   None),
    ("enqueue",   "매실티2"),
    ("dequeue",   None),
    ("enqueue",   "페퍼민트티"),
    ("dequeue",   None),
    ("enqueue",   "휘낭시에"),
    ("dequeue",   None),
    ("enqueue",   "딸기라떼"),
    ("dequeue",   None),
    ("enqueue",   "딸기에이드"),
    ("dequeue",   None),
    ("enqueue",   "망고에이드"),
    ("dequeue",   None),
    ("enqueue",   "스콘2"),
    ("dequeue",   None),
    ("enqueue",   "청포도에이드"),
    ("dequeue",   None),
    ("enqueue",   "매실티3"),
    ("dequeue",   None),
    ("enqueue",   "카페라떼2"),
    ("dequeue",   None),
    ("enqueue",   "말차라떼2"),
    ("dequeue",   None),
    ("enqueue",   "카푸치노3"),
    ("dequeue",   None),
    ("enqueue",   "캐모마일티"),
    ("dequeue",   None),
    ("enqueue",   "초코스콘2"),
    ("dequeue",   None),
    ("enqueue",   "레몬티4"),
    ("front",     None),
    ("clear",     None),
    ("isEmpty",   None),
]

def draw(q, op, val, result, done, step):
    clear()
    total = len(SCENARIO)
    print("=" * 56)
    print("        ☕  카페무슬트  Queue  애니메이션")
    print("=" * 56)

    if   op == "declare": msg = "카페무슬트 = Queue()  ← 큐 선언"
    elif op == "enqueue": msg = f"enqueue('{val}')"
    elif op == "dequeue": msg = f"dequeue()   →  반환: {result}"
    elif op == "front":   msg = f"front()     →  반환: {result}"
    elif op == "isEmpty": msg = f"isEmpty()   →  반환: {result}"
    elif op == "clear":   msg =  "clear()     →  큐 초기화"
    else:                 msg = op
    print(f"\n  [{step:02d}/{total}] ▶ {msg}\n")

    print("  [큐]  front →                   → rear")
    if q.items:
        boxes = " | ".join(f"{x:^8}" for x in q.items)
        print(f"  [ {boxes} ]")
    else:
        print("  [ (비어있음) ]")
    print(f"  크기: {len(q.items)}/10\n")

    print("  [처리완료]")
    print("  " + (" → ".join(done) if done else "(없음)"))
    print("=" * 56)
    print("  Enter: 다음  |  q+Enter: 종료")

def run():
    q = Queue()
    done = []
    for step, (op, val) in enumerate(SCENARIO, 1):
        result = None
        if   op == "declare": pass             # 큐는 이미 선언됨, 시각적 표시용
        elif op == "enqueue": q.enqueue(val)
        elif op == "dequeue": result = q.dequeue(); (done.append(result) if result else None)
        elif op == "front":   result = q.front()
        elif op == "isEmpty": result = q.isEmpty()
        elif op == "clear":   q.clear(); done.clear()

        draw(q, op, val, result, done, step)
        if input("  > ").strip().lower() == 'q':
            clear(); print("  종료합니다. "); return

    clear()
    print("=" * 56)
    print("  🎉 모든 큐 연산이 완료되었습니다!")
    print("=" * 56)

if __name__ == "__main__":
    run()
