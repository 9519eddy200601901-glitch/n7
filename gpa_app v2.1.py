# GPA calculator app - v2.2 with dropdown credits
import streamlit as st
from math import isclose

st.set_page_config(page_title="GPA 計算器 v2.1", layout="wide")

st.title("GPA 計算器 v2.1")

# GPA 對照表
gpa_map = {
    "A+": 4.3, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D": 1.0, "F": 0.0
}

grade_options = list(gpa_map.keys())

# 學分選項 (改為下拉式選單)
credit_options = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6]

# 百分制 → 等第
def percent_to_grade(p):
    p = float(p)
    if p >= 97: return "A+"
    if p >= 93: return "A"
    if p >= 90: return "A-"
    if p >= 87: return "B+"
    if p >= 83: return "B"
    if p >= 80: return "B-"
    if p >= 77: return "C+"
    if p >= 73: return "C"
    if p >= 70: return "C-"
    if p >= 60: return "D"
    return "F"

# Session State
if "subjects" not in st.session_state:
    st.session_state.subjects = ["國文", "英文"]
if "grades" not in st.session_state:
    st.session_state.grades = {}
if "credits" not in st.session_state:
    st.session_state.credits = {}
if "input_mode" not in st.session_state:
    st.session_state.input_mode = "grade"

for s in st.session_state.subjects:
    if s not in st.session_state.grades:
        st.session_state.grades[s] = "A"
    if s not in st.session_state.credits:
        st.session_state.credits[s] = 3

with st.expander("📘 GPA 等第對照表（點開查看）"):
    for g,v in gpa_map.items():
        st.write(f"**{g}** = {v}")

st.write("---")

# 設定區
left, right = st.columns([1,2])
with left:
    st.subheader("設定")
    mode = st.radio("成績輸入模式", ("等第", "百分制"))
    st.session_state.input_mode = "grade" if mode == "等第" else "percent"

    if st.button("➕ 新增科目"):
        name = f"科目{len(st.session_state.subjects)+1}"
        st.session_state.subjects.append(name)
        st.session_state.grades[name] = "A"
        st.session_state.credits[name] = 3
        st.experimental_rerun()

    if len(st.session_state.subjects) > 1 and st.button("➖ 刪除最後科目"):
        last = st.session_state.subjects.pop()
        st.session_state.grades.pop(last)
        st.session_state.credits.pop(last)
        st.experimental_rerun()

# 科目輸入
def add_subject_after(idx):
    new = f"科目{len(st.session_state.subjects)+1}"
    st.session_state.subjects.insert(idx+1, new)
    st.session_state.grades[new] = "A"
    st.session_state.credits[new] = 3
    st.experimental_rerun()

with right:
    st.subheader("科目 / 成績 / 學分")
    remove_list = []

    for idx, subj in enumerate(st.session_state.subjects):
        row = st.columns([3,3,2,1])

        with row[0]:
            new = st.text_input("科目名稱", value=subj, key=f"name_{idx}")
            if new != subj:
                st.session_state.subjects[idx] = new
                st.session_state.grades[new] = st.session_state.grades.pop(subj)
                st.session_state.credits[new] = st.session_state.credits.pop(subj)
                subj = new

        with row[1]:
            if st.session_state.input_mode == "grade":
                st.session_state.grades[subj] = st.radio("成績", grade_options, key=f"g{idx}")
            else:
                p = st.number_input("百分制", 0.0, 100.0, 90.0, step=0.5, key=f"p{idx}")
                st.session_state.grades[subj] = p
                st.caption(f"→ {percent_to_grade(p)}")

        with row[2]:
            st.session_state.credits[subj] = st.selectbox("學分", credit_options, key=f"c{idx}")

        with row[3]:
            if st.button("＋", key=f"add{idx}"):
                add_subject_after(idx)
            if len(st.session_state.subjects)>1 and st.button("－", key=f"rm{idx}"):
                remove_list.append(subj)

        st.divider()

    for r in remove_list:
        st.session_state.subjects.remove(r)
        st.session_state.grades.pop(r)
        st.session_state.credits.pop(r)
        st.experimental_rerun()

st.write("---")
st.subheader("計算結果")

if st.button("📊 計算 GPA"):
    total_p = 0
    total_c = 0
    for s in st.session_state.subjects:
        c = float(st.session_state.credits[s])
        if c == 0: continue
        g = st.session_state.grades[s]
        g = percent_to_grade(g) if st.session_state.input_mode == "percent" else g
        total_p += gpa_map[g] * c
        total_c += c
    if total_c == 0:
        st.warning("沒有可計算的學分")
    else:
        st.success(f"🎓 GPA = **{total_p/total_c:.2f}** (總學分 {total_c})")
