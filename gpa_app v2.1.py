import streamlit as st

st.title("GPA 計算器 v3.0")

# ➤ GPA 對照表
gpa_map = {
    "A+": 4.3, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D": 1.0, "F": 0.0
}

grade_options = list(gpa_map.keys())
credit_options = [1, 2, 3, 4, 5]

# ➤ Session State 初始化
if "subjects" not in st.session_state:
    st.session_state.subjects = ["國文", "英文"]  # 預設兩科
if "grades" not in st.session_state:
    st.session_state.grades = {}
if "credits" not in st.session_state:
    st.session_state.credits = {}

# ➤ 顯示 GPA 對照表
with st.expander("📘 GPA 等第對照表（點開查看）"):
    for grade, gpa in gpa_map.items():
        st.write(f"**{grade}** = {gpa} 分")

st.write("---")

# ➤ 科目輸入區
st.subheader("科目 / 成績 / 學分")

# 按鈕：新增科目
if st.button("➕ 新增科目"):
    st.session_state.subjects.append(f"科目{len(st.session_state.subjects)+1}")

# 按鈕：刪除最後科目
if len(st.session_state.subjects) > 1 and st.button("➖ 刪除最後科目"):
    st.session_state.subjects.pop()

# ➤ 動態生成欄位
for subject in st.session_state.subjects:
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        new_name = st.text_input(f"科目名稱", subject, key=f"name_{subject}")
        st.session_state.subjects[st.session_state.subjects.index(subject)] = new_name

    with col2:
        st.session_state.grades[new_name] = st.selectbox(
            f"{new_name} 成績", grade_options, key=f"grade_{new_name}"
        )

    with col3:
        st.session_state.credits[new_name] = st.selectbox(
            f"{new_name} 學分", credit_options, key=f"credit_{new_name}"
        )

# ➤ 計算按鈕
if st.button("📊 計算 GPA"):
    total_points = 0
    total_credits = 0

    for subject in st.session_state.subjects:
        grade = st.session_state.grades[subject]
        credit = st.session_state.credits[subject]
        total_points += gpa_map[grade] * credit
        total_credits += credit

    gpa = total_points / total_credits
    st.success(f"🎓 你的 GPA 是：**{gpa:.2f}**")

