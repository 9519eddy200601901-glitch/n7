import streamlit as st

st.title("GPA 計算器 v2.0")

# ➤ 1. 科目輸入
subjects_input = st.text_input("請輸入科目（空格分隔）", "國文 英文 數學 物理 歷史")
subjects = subjects_input.split()

grade_options = ["A+", "A", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]

# ➤ 2. 動態生成成績選單
grades = {}
st.subheader("請為每個科目選擇成績")
for subject in subjects:
    grades[subject] = st.selectbox(f"{subject} 成績", grade_options)

# ➤ 3. 學分輸入
credit_input = st.text_input("請輸入對應學分數（空格分隔）", "3 2 3 2 1")
credits = list(map(int, credit_input.split()))

# ➤ GPA 換算表
gpa_map = {
    "A+": 4.3, "A": 4.0,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D": 1.0, "F": 0.0
}

# ➤ 4. GPA 計算
if st.button("計算 GPA"):
    if len(subjects) != len(credits):
        st.error("⚠️ 科目數與學分數量不一致！")
    else:
        total_points = sum(gpa_map[grades[sub]] * credits[i] for i, sub in enumerate(subjects))
        total_credits = sum(credits)
        gpa = total_points / total_credits
        st.success(f"🎓 你的 GPA 是：**{gpa:.2f}**")
