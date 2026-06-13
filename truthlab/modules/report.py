from typing import Dict
from modules.feedback import personalized_tip

def build_final_report(summary: Dict) -> str:
    skill_lines = "\n".join(
        [f"- {skill}: {score}%" for skill, score in summary.get("skill_scores", {}).items()]
    )
    growth = summary.get("growth_area", "Not enough data")
    return f"""
TruthLab Digital Literacy Report

Final Score: {summary.get('percent', 0)}/100
Points: {summary.get('earned', 0)} out of {summary.get('total_possible', 0)}

Skill Breakdown:
{skill_lines}

Strongest Skill: {summary.get('strongest_skill', 'Not enough data')}
Growth Area: {growth}

Personalized Tip:
{personalized_tip(growth)}

Reflection:
Misinformation is not always obvious. The safest digital habits are pausing, checking the source, comparing evidence, and avoiding emotional sharing.
""".strip()
