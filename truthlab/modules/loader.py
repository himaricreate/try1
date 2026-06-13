import pandas as pd

REQUIRED_COLUMNS = [
    "id", "title", "platform", "post_text", "category", "correct_answer",
    "difficulty", "skill", "red_flags", "explanation", "source_note"
]

def load_scenarios(path: str = "data/scenarios.csv") -> pd.DataFrame:
    """Load and validate simulation scenarios."""
    df = pd.read_csv(path)
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required scenario columns: {missing}")
    return df
