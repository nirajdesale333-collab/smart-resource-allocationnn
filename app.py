import streamlit as st
import pandas as pd

st.set_page_config(page_title="Smart Resource Allocation", layout="wide")

# ---------- CUSTOM STYLING ----------
st.markdown("""
<style>
.main {background-color: #f5f7fa;}
h1, h2, h3 {color: #2c3e50;}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
}
.card {
    padding: 15px;
    border-radius: 12px;
    background-color: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🌍 Smart Resource Allocation")
st.subheader("AI-powered Volunteer Coordination for Social Impact")

# ---------- SESSION STATE ----------
if "volunteers" not in st.session_state:
    st.session_state.volunteers = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# ---------- SIDEBAR ----------
st.sidebar.header("➕ Add Volunteer")
v_name = st.sidebar.text_input("Name")
v_skill = st.sidebar.selectbox("Skill", ["Education", "Medical", "Logistics", "Technical"])
v_loc = st.sidebar.text_input("Location")
v_exp = st.sidebar.selectbox("Experience", ["Beginner", "Intermediate", "Expert"])

if st.sidebar.button("Add Volunteer"):
    st.session_state.volunteers.append({
        "Name": v_name,
        "Skill": v_skill,
        "Location": v_loc,
        "Experience": v_exp
    })
    st.sidebar.success("Volunteer Added")

st.sidebar.header("🛠 Add Task")
t_name = st.sidebar.text_input("Task Name")
t_skill = st.sidebar.selectbox("Required Skill", ["Education", "Medical", "Logistics", "Technical"])
t_priority = st.sidebar.selectbox("Priority", ["High", "Medium", "Low"])
t_loc = st.sidebar.text_input("Task Location")

if st.sidebar.button("Add Task"):
    st.session_state.tasks.append({
        "Task": t_name,
        "Skill": t_skill,
        "Priority": t_priority,
        "Location": t_loc
    })
    st.sidebar.success("Task Added")

# ---------- DISPLAY ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👥 Volunteers")
    if st.session_state.volunteers:
        df_v = pd.DataFrame(st.session_state.volunteers)
        st.dataframe(df_v)

with col2:
    st.markdown("### 📋 Tasks")
    if st.session_state.tasks:
        df_t = pd.DataFrame(st.session_state.tasks)
        st.dataframe(df_t)

# ---------- SMART ALLOCATION ----------
st.markdown("## ⚡ Smart Allocation Engine")

def score(vol, task):
    s = 0
    if vol["Skill"] == task["Skill"]:
        s += 5
    if vol["Location"] == task["Location"]:
        s += 3
    if vol["Experience"] == "Expert":
        s += 3
    elif vol["Experience"] == "Intermediate":
        s += 2
    else:
        s += 1
    return s

if st.button("🚀 Run Allocation"):
    allocations = []

    for task in st.session_state.tasks:
        best_vol = None
        best_score = -1

        for vol in st.session_state.volunteers:
            sc = score(vol, task)
            if sc > best_score:
                best_score = sc
                best_vol = vol

        if best_vol:
            allocations.append({
                "Task": task["Task"],
                "Volunteer": best_vol["Name"],
                "Skill": best_vol["Skill"],
                "Score": best_score
            })

    if allocations:
        df_alloc = pd.DataFrame(allocations)
        st.success("✅ Allocation Completed")
        st.dataframe(df_alloc)

        # ---------- CHART ----------
        st.markdown("### 📊 Volunteers per Skill")
        st.bar_chart(df_alloc["Skill"].value_counts())

        # ---------- FAIRNESS CHECK ----------
        counts = df_alloc["Skill"].value_counts()
        if len(counts) > 1 and counts.max() - counts.min() > 2:
            st.error("⚠ Bias Detected (Uneven Skill Distribution)")
        else:
            st.success("🎉 Fair Allocation Achieved")

    else:
        st.warning("No volunteers/tasks available")

# ---------- SUMMARY ----------
st.markdown("## 📈 Summary")
st.info(f"Total Volunteers: {len(st.session_state.volunteers)} | Total Tasks: {len(st.session_state.tasks)}")
