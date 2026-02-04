import streamlit as st

st.set_page_config(
    page_title="Reading Exam Builder",
    layout="wide"
)

st.title("📘 Reading Comprehension Exam Builder")

# ============================================================
# Session State Init
# ============================================================
if "meta_saved" not in st.session_state:
    st.session_state.meta_saved = False

# ============================================================
# Exam Metadata
# ============================================================
with st.form("exam_metadata"):
    st.subheader("🧾 Exam Metadata")

    exam_id = st.number_input("Exam ID", min_value=1, step=1)
    class_name = st.text_input("Class Name", value="Selective")
    subject = st.text_input("Subject", value="Reading Comprehension")
    topic = st.text_input("Topic")
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    total_questions = st.number_input(
        "Total Questions",
        min_value=1,
        step=1
    )

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

# ============================================================
# Stop until metadata saved
# ============================================================
if not st.session_state.meta_saved:
    st.info("⬆️ Save Exam Metadata to continue")
    st.stop()

meta = st.session_state.exam_meta

# ============================================================
# MCQ — Paragraph Matching UI
# ============================================================
if meta["question_type"] == "MCQ":

    st.subheader("📖 Reading Material (Paragraphs)")

    paragraphs = {}

    for i in range(1, meta["total_questions"] + 1):
        paragraphs[i] = st.text_area(
            f"Paragraph {i}",
            height=150,
            key=f"paragraph_{i}"
        )

    # --------------------------------------------------------
    # Shared Answer Options
    # --------------------------------------------------------
    st.subheader("🅰️ Answer Options (Shared)")

    options = {}
    option_labels = ["A", "B", "C", "D", "E", "F", "G"]

    cols = st.columns(2)
    for idx, label in enumerate(option_labels):
        with cols[idx % 2]:
            options[label] = st.text_input(
                f"Option {label}",
                key=f"option_{label}"
            )

    # --------------------------------------------------------
    # Correct Answer Mapping
    # --------------------------------------------------------
    st.subheader("✅ Correct Answers")

    answers = {}

    for i in range(1, meta["total_questions"] + 1):
        answers[i] = st.selectbox(
            f"Paragraph {i} → Correct Option",
            option_labels,
            key=f"correct_para_{i}"
        )

    # --------------------------------------------------------
    # Save Exam
    # --------------------------------------------------------
    if st.button("💾 Save Exam"):
        exam_payload = {
            "class_name": meta["class_name"].lower(),
            "subject": meta["subject"].lower().replace(" ", "_"),
            "topic": meta["topic"],
            "difficulty": meta["difficulty"].lower(),
            "question_type": "mcq_paragraph_matching",
            "reading_material": {
                "paragraphs": paragraphs
            },
            "answer_options": options,
            "questions": [
                {
                    "paragraph": i,
                    "correct_answer": answers[i]
                }
                for i in range(1, meta["total_questions"] + 1)
            ]
        }

        st.success("✅ Exam payload ready")

        st.json(exam_payload)

# ============================================================
# Extract Selection (unchanged, placeholder)
# ============================================================
else:
    st.info("EXTRACT_SELECTION UI will render here")
