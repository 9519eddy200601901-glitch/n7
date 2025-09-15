import streamlit as st

grade_to_score = {
    'A+': 4.3, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D': 1.0, 'F': 0.0
}

st.title("GPA 計算器")

subjects = st.text_input("請輸入 5 個科目（空格分隔）", "國文 英文 數學 物理 歷史").split()
grades = st.text_input("請輸入 5 個等第（空格分隔）", "A B+ A- C B").split()
credits = st.text_input("請輸入 5 個學分數（空格分隔）", "3 2 3 2 1").split()

if len(subjects) == len(grades) == len(credits) == 5:
    credits = list(map(float, credits))
    gpa_scores = [grade_to_score.get(g, 0) for g in grades]
    weighted_sum = sum(g * c for g, c in zip(gpa_scores, credits))
    total_credits = sum(credits)
    final_gpa = weighted_sum / total_credits
    st.success(f"加權平均 GPA 為：{final_gpa:.2f}")
else:
    st.warning("請確保每一欄都輸入 5 個項目")
