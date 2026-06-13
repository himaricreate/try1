import streamlit as st
import pandas as pd
from modules.loader import load_scenarios
from modules.scoring import is_correct, points_for_scenario, summarize_results
from modules.feedback import coach_feedback, personalized_tip
from modules.report import build_final_report

st.set_page_config(
    page_title="TruthLab | Misinformation Simulator",
    page_icon="🧠",
    layout="centered"
)

CUSTOM_CSS = """
<style>
    .main-title {font-size: 2.6rem; font-weight: 800; margin-bottom: 0rem;}
    .subtitle {font-size: 1.1rem; color: #6b7280; margin-bottom: 1.5rem;}
    .post-card {border: 1px solid #e5e7eb; border-radius: 18px; padding: 1.2rem; background: #ffffff; box-shadow: 0 6px 20px rgba(0,0,0,0.04);}
    .platform {font-size: 0.9rem; color: #6b7280; font-weight: 600;}
    .post-title {font-size: 1.35rem; font-weight: 700; margin-top: 0.4rem;}
    .post-text {font-size: 1.05rem; line-height: 1.6; margin-top: 1rem;}
    .small-label {font-size: 0.85rem; color: #6b7280;}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "started" not in st.session_state:
    st.session_state.started = False
if "index" not in st.session_state:
    st.session_state.index = 0
if "responses" not in st.session_state:
    st.session_state.responses = []
if "answered_current" not in st.session_state:
    st.session_state.answered_current = False
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""

@st.cache_data
def get_data():
    return load_scenarios()

scenarios = get_data()

st.markdown('<div class="main-title">TruthLab</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-Guided Misinformation Simulator</div>', unsafe_allow_html=True)

if not st.session_state.started:
    st.write("TruthLab is an interactive web application that trains users to identify fake, AI-generated, manipulative, or misleading online content.")
    st.write("You will review simulated posts, choose how to respond, and receive AI-coach style feedback explaining the reasoning behind each answer.")

    st.subheader("What you will practice")
    st.markdown("""
    - Source verification
    - Scam awareness
    - Image skepticism
    - Emotional manipulation detection
    - Critical reasoning
    """)

    if st.button("Start Simulation", type="primary"):
        st.session_state.started = True
        st.rerun()

else:
    total = len(scenarios)
    idx = st.session_state.index

    if idx < total:
        scenario = scenarios.iloc[idx]
        st.progress((idx) / total)
        st.caption(f"Scenario {idx + 1} of {total}")

        st.markdown("<div class='post-card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='platform'>{scenario['platform']} · {scenario['category']} · {scenario['difficulty']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='post-title'>{scenario['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='post-text'>{scenario['post_text']}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("What would you do?")
        choice = st.radio(
            "Choose your response:",
            ["Trust", "Doubt", "Report"],
            horizontal=True,
            disabled=st.session_state.answered_current
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Answer", type="primary", disabled=st.session_state.answered_current):
                correct = is_correct(choice, scenario["correct_answer"])
                points = points_for_scenario(scenario["difficulty"], correct)
                feedback = coach_feedback(choice, scenario["correct_answer"], scenario["explanation"], scenario["red_flags"])
                st.session_state.responses.append({
                    "id": int(scenario["id"]),
                    "title": scenario["title"],
                    "user_answer": choice,
                    "correct_answer": scenario["correct_answer"],
                    "correct": correct,
                    "points": points,
                    "difficulty": scenario["difficulty"],
                    "skill": scenario["skill"],
                })
                st.session_state.last_feedback = feedback
                st.session_state.answered_current = True
                st.rerun()

        if st.session_state.answered_current:
            latest = st.session_state.responses[-1]
            if latest["correct"]:
                st.success(f"Correct! You earned {latest['points']} points.")
            else:
                st.error(f"Not quite. Correct answer: {latest['correct_answer']}")

            st.subheader("AI Coach Feedback")
            st.write(st.session_state.last_feedback)

            with st.expander("Source / asset note"):
                st.write(scenario["source_note"])

            with col2:
                if st.button("Next Scenario"):
                    st.session_state.index += 1
                    st.session_state.answered_current = False
                    st.session_state.last_feedback = ""
                    st.rerun()

    else:
        summary = summarize_results(st.session_state.responses)
        report = build_final_report(summary)

        st.balloons()
        st.header("Your Digital Literacy Report")
        st.metric("Final Score", f"{summary['percent']}/100")
        st.write(f"Points: {summary['earned']} out of {summary['total_possible']}")

        st.subheader("Skill Breakdown")
        skill_df = pd.DataFrame(
            [{"Skill": skill, "Score": score} for skill, score in summary["skill_scores"].items()]
        )
        st.dataframe(skill_df, hide_index=True, use_container_width=True)

        st.subheader("AI Coach Summary")
        st.write(f"Strongest skill: **{summary['strongest_skill']}**")
        st.write(f"Area to improve: **{summary['growth_area']}**")
        st.info(personalized_tip(summary["growth_area"]))

        st.download_button(
            label="Download Report",
            data=report,
            file_name="truthlab_digital_literacy_report.txt",
            mime="text/plain"
        )

        with st.expander("View full report"):
            st.text(report)

        if st.button("Restart Simulation"):
            st.session_state.started = False
            st.session_state.index = 0
            st.session_state.responses = []
            st.session_state.answered_current = False
            st.session_state.last_feedback = ""
            st.rerun()

st.divider()
st.caption("TruthLab is an educational simulation. It is designed to train critical thinking, not to provide legal, medical, or emergency advice.")
