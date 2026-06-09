import streamlit as st

st.set_page_config(layout="wide")

# ---------------- STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = "form"

if "result" not in st.session_state:
    st.session_state.result = {}

# ---------------- OPTIONS ----------------
options = {
    "None": 0,
    "Mild": 1,
    "Moderate": 2,
    "Severe": 3,
    "Extreme": 4
}

# ---------------- QUESTIONS ----------------
pain_q = [
    "How much pain do you have when walking on a flat surface?",
    "How much pain do you have when going up or down stairs?",
    "How much pain do you have at night while in bed?",
    "How much pain do you have while sitting or lying down?",
    "How much pain do you have while standing upright?"
]

stiff_q = [
    "How stiff is your knee when you first get up in the morning?",
    "How stiff is your knee later in the day?"
]

func_q = [
    "Descending stairs",
    "Ascending stairs",
    "Rising from sitting",
    "Standing",
    "Bending to floor",
    "Walking on flat surface",
    "Getting in / out of car",
    "Going shopping",
    "Putting on socks",
    "Lying in bed",
    "Taking off socks",
    "Rising from bed",
    "Getting in/out of bath",
    "Sitting",
    "Getting on/off toilet",
    "Heavy domestic duties",
    "Light domestic duties"
]

# ---------------- ASK FUNCTION ----------------
def ask(question, key):
    st.markdown(f"**{question}**")
    return st.radio("", list(options.keys()), horizontal=True, key=key)

# ---------------- FORM PAGE ----------------
def form_page():

    st.title("WOMAC Questionnaire")

    st.info("""
The WOMAC (Western Ontario and McMaster Universities Osteoarthritis Index) is a self-administered questionnaire used to assess three important aspects of knee and hip osteoarthritis: pain, joint stiffness, and physical function.

The questionnaire contains 24 questions and focuses on your experience during the last 48 hours.

Please answer all questions based on your condition over the past 48 hours and choose the option that best reflects your experience.
""")

    st.markdown("""
### Response Scale

For each question, select the option that best describes your condition:

Attention: These explanations are only here to help you choose the option that best matches your condition.

- **0 – None:** No pain, stiffness, or difficulty.
- **1 – Mild:** Slight symptoms that are noticeable but cause little interference.
- **2 – Moderate:** Symptoms are clearly present and cause some difficulty in daily activities.
- **3 – Severe:** Symptoms significantly affect daily activities and are difficult to ignore.
- **4 – Extreme:** Symptoms are very severe and greatly limit normal activities.
""")

    scores = []

    st.markdown("---")

    question_number = 1

    st.subheader("PAIN (1–5 of 24)")
    for q in pain_q:
        ans = ask(f"{question_number}. {q}", f"q{question_number}")
        scores.append(options[ans])
        question_number += 1

    st.subheader("STIFFNESS (6–7 of 24)")
    for q in stiff_q:
        ans = ask(f"{question_number}. {q}", f"q{question_number}")
        scores.append(options[ans])
        question_number += 1

    st.subheader("PHYSICAL FUNCTION (8–24 of 24)")
    for q in func_q:
        ans = ask(f"{question_number}. {q}", f"q{question_number}")
        scores.append(options[ans])
        question_number += 1

    st.markdown("---")

    if st.button("Calculate WOMAC Score"):

        pain_score = sum(scores[:5])
        stiff_score = sum(scores[5:7])
        func_score = sum(scores[7:])
        total = sum(scores)

        st.session_state.result = {
            "pain": pain_score,
            "stiff": stiff_score,
            "func": func_score,
            "total": total
        }

        st.session_state.step = "result"
        st.rerun()

# ---------------- RESULT PAGE ----------------
def result_page():

    r = st.session_state.result

    st.title("Results")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Pain", f"{r['pain']}/20")
    col2.metric("Stiffness", f"{r['stiff']}/8")
    col3.metric("Function", f"{r['func']}/68")
    col4.metric("Total", f"{r['total']}/96")

    if r["total"] == 0:
        level = "No Pain or Functional Limitation"
    elif r["total"] <= 20:
        level = "Mild"
    elif r["total"] <= 40:
        level = "Mild to Moderate"
    elif r["total"] <= 60:
        level = "Moderate"
    elif r["total"] <= 80:
        level = "Severe"
    else:
        level = "Very Severe"

    st.success("Severity: " + level)

    if st.button("Back"):
        st.session_state.step = "form"
        st.rerun()

# ---------------- ROUTER ----------------
if st.session_state.step == "form":
    form_page()
else:
    result_page()