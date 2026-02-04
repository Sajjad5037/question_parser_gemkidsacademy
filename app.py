import streamlit as st

st.set_page_config(
    page_title="Reading Exam Builder",
    layout="wide"
)

st.title("📘 Exam Question Builder")

# ============================================================
# Exam Metadata (Single Pass)
# ============================================================
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

st.divider()

# ============================================================
# MCQ – Paragraph Matching UI
# ============================================================
if question_type == "MCQ":

    st.subheader("📖 Reading Material (Paragraphs)")

    paragraphs = {}

    for i in range(1, total_questions + 1):
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

    for i in range(1, total_questions + 1):
        answers[i] = st.selectbox(
            f"Paragraph {i} → Correct Option",
            option_labels,
            key=f"correct_para_{i}"
        )

# ============================================================
# Extract Selection (placeholder for later)
# ============================================================
else:
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
                height=200,
                key=f"extract_{label}_text"
            )

            extracts[label] = {
                "title": title.strip(),
                "text": text.strip()
            }

    st.divider()

    st.subheader("❓ Questions")

    questions = []

    for i in range(1, total_questions + 1):
        with st.expander(f"Question {i}", expanded=(i == 1)):
            q_text = st.text_area(
                "Question Text",
                key=f"extract_q_text_{i}"
            )

            correct = st.selectbox(
                "Correct Extract",
                ["A", "B", "C", "D"],
                key=f"extract_correct_{i}"
            )

            questions.append({
                "question_id": f"Q{i}",
                "question_text": q_text,
                "correct_answer": correct
            })

st.divider()

# ============================================================
# Create Exam (Final Action)
# ============================================================
if st.button("🧠 Create Exam"):

    # ---- Basic validation (minimal, expand later)
    missing_paragraphs = [
        i for i, text in paragraphs.items() if not text.strip()
    ]

    missing_options = [
        k for k, v in options.items() if not v.strip()
    ]

    if missing_paragraphs:
        st.error(f"Missing text for paragraphs: {missing_paragraphs}")
        st.stop()

    if missing_options:
        st.error(f"Missing text for options: {missing_options}")
        st.stop()

    exam_payload = {
        "class_name": class_name.lower(),
        "subject": subject.lower().replace(" ", "_"),
        "topic": topic,
        "difficulty": difficulty.lower(),
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
            for i in range(1, total_questions + 1)
        ]
    }

    st.success("✅ Exam created successfully")
    st.json(exam_payload)
