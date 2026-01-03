import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd  # 데이터를 표 형태로 다루는 도구

st.title("🎰 AI 바카라 출목표 & 데이터 분석")

st.sidebar.header("설정")
num_games = st.sidebar.slider("생성할 판 수", 30, 100, 72)

if st.sidebar.button("새로운 슈 생성하기"):
    # 1. 데이터 생성
    results_raw = random.choices(['B', 'P', 'T'], weights=[45.8, 44.6, 9.6], k=num_games)
    
    # --- 추가 기능 1: 통계 표시 ---
    b_count = results_raw.count('B')
    p_count = results_raw.count('P')
    t_count = results_raw.count('T')

    # 웹 화면에 보기 좋게 3열로 수치 표시
    col1, col2, col3 = st.columns(3)
    col1.metric("Banker (B)", f"{b_count}회")
    col2.metric("Player (P)", f"{p_count}회")
    col3.metric("Tie (T)", f"{t_count}회")
    st.write(f"**총 진행 판수:** {len(results_raw)}판")

    # 2. 본매 로직 (이전과 동일)
    x_coords, y_coords, colors, types = [], [], [], []
    curr_x, curr_y = 0, 0
    prev_res = None
    for res in results_raw:
        if res == 'T': continue
        if prev_res is None: curr_x, curr_y = 0, 0
        elif res == prev_res:
            curr_y += 1
            if curr_y >= 6: curr_y = 5; curr_x += 1
        else: curr_x += 1; curr_y = 0
        x_coords.append(curr_x); y_coords.append(curr_y)
        colors.append('red' if res == 'B' else 'blue')
        types.append(res); prev_res = res

    # 3. 그래픽 출력
    fig, ax = plt.subplots(figsize=(10, 5))
    for i in range(len(x_coords)):
        circle = plt.Circle((x_coords[i], 5 - y_coords[i]), 0.4, color=colors[i], fill=False, linewidth=2)
        ax.add_patch(circle)
        ax.text(x_coords[i], 5 - y_coords[i], types[i], color=colors[i], ha='center', va='center', fontweight='bold', fontsize=8)
    ax.set_xlim(-1, max(x_coords) + 1 if x_coords else 10)
    ax.set_ylim(-1, 6)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_aspect('equal')
    st.pyplot(fig)

    # --- 추가 기능 2: 엑셀(CSV) 다운로드 ---
    # 데이터를 표(DataFrame)로 만듭니다.
    df = pd.DataFrame({
        'Round': range(1, len(results_raw) + 1),
        'Result': results_raw
    })

    # CSV 형식으로 변환
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📊 게임 결과 엑셀(CSV) 다운로드",
        data=csv,
        file_name='baccarat_results.csv',
        mime='text/csv',
    )
