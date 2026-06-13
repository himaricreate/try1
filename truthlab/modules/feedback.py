def coach_feedback(user_answer: str, correct_answer: str, explanation: str, red_flags: str) -> str:
    """Generate deterministic AI-coach style feedback without relying on external APIs."""
    user = user_answer.strip().lower()
    correct = correct_answer.strip().lower()

    if user == correct:
        opening = "Correct. Your judgment matched the safest interpretation of this post."
    elif user == "doubt" and correct == "report":
        opening = "You were close. Doubting the post was a good start, but this content has enough risk that it should be reported."
    elif user == "trust" and correct in {"doubt", "report"}:
        opening = "Not quite. This post contains warning signs that should make you slow down before trusting or sharing it."
    elif user == "report" and correct == "doubt":
        opening = "Almost. This post is suspicious, but the best first step is to doubt and verify before reporting."
    else:
        opening = "Not quite. The best response depends on the level of evidence, risk, and potential harm."

    flags = [flag.strip() for flag in str(red_flags).split(";") if flag.strip()]
    flags_text = "\n".join([f"- {flag}" for flag in flags])

    return f"{opening}\n\nWhy this matters:\n{explanation}\n\nSignals to notice:\n{flags_text}"

def personalized_tip(skill: str) -> str:
    tips = {
        "Source Verification": "Before trusting a claim, ask: Who published it? Can I verify it through another credible source?",
        "Scam Awareness": "Be careful with urgent messages that ask for money, passwords, or personal information.",
        "Image Skepticism": "Images and screenshots can be edited, reused, or AI-generated. Check context before sharing.",
        "Emotional Manipulation Detection": "If a post tries to make you feel panic, guilt, or anger, pause before reacting.",
        "Critical Reasoning": "Precise numbers need context: source, sample size, date, and method matter.",
    }
    return tips.get(skill, "Pause, verify, and compare sources before sharing online content.")
