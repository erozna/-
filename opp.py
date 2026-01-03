import streamlit as st
import random
import matplotlib.pyplot as plt

# 웹 페이지 제목
st.title("🎰 AI 바카라 출목표 생성기")

# 사이드바 설정
st.sidebar.header("설정")
num_games = st.sidebar.slider("생성할 판 수", 30, 100, 72)

if st.sidebar.button("새로운 슈 생성하기"):
    # 1. 데이터 생성
    results_raw = random.choices(['B', 'P', 'T'], weights=[45.8, 44.6, 9.6], k=num_games)
    
    # 2. 본매(Big Road) 좌표 계산 로직
    x_coords, y_coords, colors, types = [], [], [], []
    curr_x, curr_y = 0, 0
    prev_res = None

    for res in results_raw:
        if res == 'T': continue # 타이는 일단 제외
        
        if prev_res is None:
            curr_x, curr_y = 0, 0
        elif res == prev_res:
            curr_y += 1
            if curr_y >= 6: # 6행 넘어가면 옆으로 (간단 로직)
                curr_y = 5
                curr_x += 1
        else:
            curr_x += 1
            curr_y = 0
            
        x_coords.append(curr_x)
        y_coords.append(curr_y)
        colors.append('red' if res == 'B' else 'blue')
        types.append(res)
        prev_res = res

    # 3. 그래픽 그리기 (이 부분이 보강되었습니다!)
    fig, ax = plt.subplots(figsize=(10, 5))
    
    for i in range(len(x_coords)):
        # 원 그리기
        circle = plt.Circle((x_coords[i], 5 - y_coords[i]), 0.4, color=colors[i], fill=False, linewidth=2)
        ax.add_patch(circle)
        # 글자 쓰기 (B 또는 P)
        ax.text(x_coords[i], 5 - y_coords[i], types[i], color=colors[i], 
                ha='center', va='center', fontweight='bold', fontsize=8)

    # 격자 및 축 설정
    ax.set_xlim(-1, max(x_coords) + 1 if x_coords else 10)
    ax.set_ylim(-1, 6)
    ax.set_xticks(range(int(max(x_coords)) + 2 if x_coords else 11))
    ax.set_yticks(range(6))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_aspect('equal')
    
    # Streamlit에 그래프 표시
    st.pyplot(fig)
    st.success(f"총 {num_games}판의 결과가 생성되었습니다!")
