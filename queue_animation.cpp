#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <deque>
#include <thread>
#include <chrono>

using namespace std;

const int DELAY = 700; // 애니메이션 속도 (0.7초)

void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

// UI 출력: 현재 연산, 큐 상태, 진행률(30개 기준) 표시
void drawUI(const string& op, const deque<string>& q, int count) {
    clearScreen();
    cout << "==========================================" << endl;
    cout << "             [ 카페 무솔트 ]              " << endl;
    cout << "      메뉴 데이터 처리: " << count << " / 30" << endl; // 30개로 변경
    cout << "==========================================" << endl;
    cout << "\n  실행 연산: " << op << endl;
    cout << "\n          [ 주문 대기열 ]" << endl;
    cout << "          +-----------------+" << endl;

    if (q.empty()) {
        cout << "          |    (비어 있음)  |" << endl;
        cout << "          +-----------------+" << endl;
    }
    else {
        // Queue 시각화: Rear(최신)가 위, Front(가장 오래된)가 아래
        for (auto it = q.rbegin(); it != q.rend(); ++it) {
            printf("          | %-15s |\n", it->substr(0, 15).c_str());
            cout << "          +-----------------+" << endl;
        }
    }
    cout << "\n==========================================" << endl;
    this_thread::sleep_for(chrono::milliseconds(DELAY));
}

int main() {
    deque<string> cafeQueue;
    vector<string> menuItems;

    // 1. CSV 파일 읽기 (1행 제외, 1~2열 제외 -> 총 30개 메뉴 추출)
    ifstream file("data.csv");
    if (!file.is_open()) {
        cout << "data.csv 파일을 찾을 수 없습니다." << endl;
        return 1;
    }

    string line;
    int rowCount = 0;
    while (getline(file, line) && rowCount < 11) {
        rowCount++;
        if (rowCount == 1) continue; // 1행 전체 제외

        stringstream ss(line);
        string cell;
        int colCount = 0;
        while (getline(ss, cell, ',')) {
            colCount++;
            if (colCount <= 2) continue; // 1열, 2열 전체 제외

            // 3, 4, 5열 데이터만 수집
            if (!cell.empty()) {
                // 개행 문자 및 공백 제거
                cell.erase(cell.find_last_not_of(" \n\r\t") + 1);
                if (!cell.empty()) menuItems.push_back(cell);
            }
        }
    }
    file.close();

    // 데이터가 부족할 경우를 대비해 30개까지만 사용하거나 확인
    if (menuItems.size() > 30) menuItems.resize(30);

    // 2. 애니메이션 시작
    int currentProcessed = 0;

    // [isEmpty] 초기 상태 확인
    drawUI("cafeQueue.isEmpty() -> " + string(cafeQueue.empty() ? "true" : "false"), cafeQueue, 0);

    // [데이터 처리 루프 - 총 30회]
    for (const auto& menu : menuItems) {
        currentProcessed++;

        // 제약조건: 큐 크기를 10 이하로 유지
        if (cafeQueue.size() >= 10) {
            string out = cafeQueue.front();
            cafeQueue.pop_front();
            drawUI("Queue Full! dequeue() -> " + out, cafeQueue, currentProcessed - 1);
        }

        // enqueue 연산
        cafeQueue.push_back(menu);
        drawUI("cafeQueue.enqueue(\"" + menu + "\")", cafeQueue, currentProcessed);

        // 중간중간 front 연산 보여주기 (10개 단위로 수행)
        if (currentProcessed % 10 == 0) {
            drawUI("cafeQueue.front() 확인 -> " + cafeQueue.front(), cafeQueue, currentProcessed);
        }
    }

    // [clear 연산]
    cafeQueue.clear();
    drawUI("cafeQueue.clear() -> 모든 주문 완료", cafeQueue, currentProcessed);

    // [최종 isEmpty]
    drawUI("Final isEmpty() -> " + string(cafeQueue.empty() ? "true" : "false"), cafeQueue, currentProcessed);

    cout << "\n총 " << menuItems.size() << "개의 메뉴 애니메이션이 종료되었습니다." << endl;

    return 0;
}