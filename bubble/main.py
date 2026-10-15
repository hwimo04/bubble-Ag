import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# 외부 호출(GAS 및 브라우저)을 위한 CORS 허용 설정
CORS(app)

def bubble_sort_trace(arr):
    """
    버블 정렬을 수행하면서 각 비교 및 교환 시점의 상태를 단계별로 기록합니다.
    """
    steps = []
    data = list(arr)
    n = len(data)
    
    # 0단계: 초기 상태 저장
    steps.append({
        "step": 0,
        "array": list(data),
        "comparing": [],
        "swapped": False,
        "description": "정렬 시작 전 초기 배열 상태입니다."
    })
    
    step_count = 1
    # 외부 루프: 각 패스마다 가장 큰 원소가 맨 뒤로 이동
    for i in range(n):
        swapped_in_pass = False
        for j in range(0, n - i - 1):
            is_swap = False
            # 인접한 두 원소 비교
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                is_swap = True
                swapped_in_pass = True
            
            # 매 비교/교환 시점의 스냅샷 생성
            steps.append({
                "step": step_count,
                "pass": i + 1,
                "array": list(data),
                "comparing": [j, j + 1],
                "swapped": is_swap,
                "description": f"인덱스 {j}(값: {data[j + 1] if is_swap else data[j]})와 인덱스 {j+1}(값: {data[j] if is_swap else data[j+1]}) 비교 " + 
                               ("후 교환(Swap)되었습니다." if is_swap else "-> 자리 유지")
            })
            step_count += 1
            
        # 패스 내에서 한 번도 교환이 발생하지 않으면 이미 정렬 완료
        if not swapped_in_pass:
            break
            
    # 최종 완료 단계 추가
    steps.append({
        "step": step_count,
        "array": list(data),
        "comparing": [],
        "swapped": False,
        "description": "버블 정렬이 완료되었습니다."
    })
    
    return steps, data

@app.route('/sort', methods=['POST'])
def handle_sort():
    """
    버블 정렬 실행 API 엔드포인트
    Request Body JSON 예시: {"numbers": [64, 34, 25, 12, 22, 11, 90]}
    """
    try:
        content = request.get_json(silent=True)
        if not content or 'numbers' not in content:
            return jsonify({
