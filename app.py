import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparative Exam Builder", layout="wide")

st.title("📘 Comparative Reading Exam Builder")

# =====================
# Session State Init
# =====================
if "meta_saved" not in st.session_state:
    st.session_state.meta_saved = False

# =====================
# Exam Metadata
# =====================
with st.form("exam_metadata"):
    st.subheader("🧾 Exam Metadata")

    exam_id = st.number_input("Exam ID", min_value=1, step=1)
    class_name = st.text_input("Class Name", value="Selective")
    subject = st.text_input("Subject", value="Reading Comprehension")
    topic = st.text_input("Topic")
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    total_questions = st.number_input("Total Questions", min_value=1, step=1)
    question_type = st.selectbox(
        "Question Type",
        ["MCQ", "EXTRACT_SELECTION"]
    )

    save_meta = st.form_submit_button("Save Metadata")

if save_meta:
    st.session_state.meta_saved = True
    st.session_state.exam_meta = {
        "exam_id": exam_id,
        "class_name": class_name,
        "subject": subject,
        "topic": topic,
        "difficulty": difficulty,
        "total_questions": total_questions,
        "question_type": question_type
    }

# =====================
# Stop here if metadata not saved
# =====================
if not st.session_state.meta_saved:
    st.info("⬆️ Please save Exam Metadata to continue.")
    st.stop()

meta = st.session_state.exam_meta

# =====================
# Extract Inputs (NOW VISIBLE)
# =====================
st.subheader("📖 Reading Extracts")

extracts = {}

for label in ["A", "B", "C", "D"]:
    with st.expander(f"Extract {label}", expanded=(label in ["A", "B"])):
        title = st.text_input(
            f"Extract {label} Title",
            key=f"extract_{label}_title"
        )
        text = st.text_area(
            f"Extract {label} Text",
            height=220,
            key=f"extract_{label}_text"
        )
        extracts[label] = {
            "title": title.strip(),
            "text": text.strip()
        }

# =====================
# Question Inputs
# =====================
st.subheader("❓ Questions")

questions = []

for i in range(1, meta["total_questions"] + 1):
    with st.expander(f"Question {i}", expanded=(i == 1)):
        q_text = st.text_area(
            "Question Text",
            key=f"q_text_{i}"
        )

        if meta["question_type"] == "MCQ":
            opt_a = st.text_input("Option A", key=f"optA_{i}")
            opt_b = st.text_input("Option B", key=f"optB_{i}")
            opt_c = st.text_input("Option C", key=f"optC_{i}")
            opt_d = st.text_input("Option D", key=f"optD_{i}")
            correct = st.selectbox(
                "Correct Answer",
                ["A", "B", "C", "D"],
                key=f"correct_{i}"
            )
        else:
            opt_a = opt_b = opt_c = opt_d = ""
            correct = st.selectbox(
                "Correct Extract",
                ["A", "B", "C", "D"],
                key=f"correct_{i}"
            )

        questions.append({
            "question_id": i,
            "question_text": q_text,
            "option_A": opt_a,
            "option_B": opt_b,
            "option_C": opt_c,
            "option_D": opt_d,
            "correct_answer": correct
        })

# =====================
# CSV Generation
# =====================
if st.button("📥 Save Question"):
    rows = []

    for q in questions:
        rows.append({
            "exam_id": meta["exam_id"],
            "class_name": meta["class_name"],
            "subject": meta["subject"],
            "topic": meta["topic"],
            "difficulty": meta["difficulty"],
            "total_questions": meta["total_questions"],
            "question_type": meta["question_type"],

            "extract_A_title": extracts["A"]["title"],
            "extract_A_text": extracts["A"]["text"],
            "extract_B_title": extracts["B"]["title"],
            "extract_B_text": extracts["B"]["text"],
            "extract_C_title": extracts["C"]["title"],
            "extract_C_text": extracts["C"]["text"],
            "extract_D_title": extracts["D"]["title"],
            "extract_D_text": extracts["D"]["text"],

            "question_id": q["question_id"],
            "question_text": q["question_text"],
            "option_A": q["option_A"],
            "option_B": q["option_B"],
            "option_C": q["option_C"],
            "option_D": q["option_D"],
            "correct_answer": q["correct_answer"]
        })

    df = pd.DataFrame(rows)

    st.success("✅ CSV generated successfully")

    st.download_button(
        label="⬇️ Download CSV",
        data=df.to_csv(index=False),
        file_name="comparative_exam.csv",
        mime="text/csv"
    )

    st.dataframe(df)
