from typing import Dict, List

POINTS_BY_DIFFICULTY = {
    "Easy": 8,
    "Medium": 10,
    "Hard": 12,
}

def normalize_answer(answer: str) -> str:
    return answer.strip().lower()

def is_correct(user_answer: str, correct_answer: str) -> bool:
    return normalize_answer(user_answer) == normalize_answer(correct_answer)

def points_for_scenario(difficulty: str, correct: bool) -> int:
    if not correct:
        return 0
    return POINTS_BY_DIFFICULTY.get(difficulty, 10)

def summarize_results(responses: List[Dict]) -> Dict:
    total_possible = sum(POINTS_BY_DIFFICULTY.get(r.get("difficulty", "Medium"), 10) for r in responses)
    earned = sum(r.get("points", 0) for r in responses)
    percent = round((earned / total_possible) * 100) if total_possible else 0

    skills = {}
    for r in responses:
        skill = r.get("skill", "General")
        if skill not in skills:
            skills[skill] = {"correct": 0, "total": 0}
        skills[skill]["total"] += 1
        if r.get("correct"):
            skills[skill]["correct"] += 1

    skill_scores = {
        skill: round((values["correct"] / values["total"]) * 100)
        for skill, values in skills.items()
        if values["total"] > 0
    }

    strongest = max(skill_scores, key=skill_scores.get) if skill_scores else "Not enough data"
    weakest = min(skill_scores, key=skill_scores.get) if skill_scores else "Not enough data"

    return {
        "earned": earned,
        "total_possible": total_possible,
        "percent": percent,
        "skill_scores": skill_scores,
        "strongest_skill": strongest,
        "growth_area": weakest,
    }
