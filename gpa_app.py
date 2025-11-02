import streamlit as st

grade_to_score = {
    'A+': 4.3, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'F': 0.0
}

st.title("GPA 計算器 v1.0")

subjects = st.text_input("請輸入科目（空格分隔）例如：國文 英文 數學 物理 歷史").split()
grades = st.text_input("請輸入對應成績（空格分隔）例如：A+ B+ A C B-").split()
credits = st.text_input("請輸入對應學分數（空格分隔）例如：3 2 3 2 1").split()

if len(subjects) == len(grades) == len(credits) and len(subjects) > 0:
    try:
        credits = list(map(float, credits))
        gpa_scores = [grade_to_score.get(g, 0) for g in grades]
        weighted_sum = sum(g * c for g, c in zip(gpa_scores, credits))
        total_credits = sum(credits)
        final_gpa = weighted_sum / total_credits
        st.success(f"加權平均 GPA 為：{final_gpa:.2f}")
    except ValueError:
        st.error("學分數輸入錯誤，請確認為數字")
else:
    st.warning("請確保三欄輸入的項目數量相同，且至少一項")


