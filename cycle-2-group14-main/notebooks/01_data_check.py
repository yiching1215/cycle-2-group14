from pathlib import Path
import pandas as pd
import numpy as np


# =========================
# 1. Path settings
# =========================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "YRBS_2007.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# =========================
# 2. Helper functions
# =========================
def recode_sad_or_hopeless(value):
    if pd.isna(value):
        return np.nan
    if value == 1:
        return 1   # success
    if value == 2:
        return 0   # failure
    return np.nan


def print_section(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


# =========================
# 3. Main workflow
# =========================
def main():
    print_section("Project Cycle 2 Data Preparation")

    print("Project root:", PROJECT_ROOT)
    print("Raw data path:", RAW_DATA_PATH)
    print("Processed dir:", PROCESSED_DIR)

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Cannot find raw data file:\n{RAW_DATA_PATH}\n"
            "Please make sure YRBS_2007.csv is placed in data/raw/."
        )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(RAW_DATA_PATH)

    required_columns = ["SadOrHopeless", "BMIPCT"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns in dataset: {missing_columns}")

    df_selected = df[["SadOrHopeless", "BMIPCT"]].copy()

    df_selected["SadOrHopeless_binary"] = df_selected["SadOrHopeless"].apply(recode_sad_or_hopeless)
    df_selected["BMIPCT_clean"] = pd.to_numeric(df_selected["BMIPCT"], errors="coerce")

    prop_data = df_selected.dropna(subset=["SadOrHopeless_binary"]).copy()
    mean_data = df_selected.dropna(subset=["BMIPCT_clean"]).copy()

    print_section("Original SadOrHopeless Frequency Table")
    print(df_selected["SadOrHopeless"].value_counts(dropna=False).sort_index())

    print_section("Recoded SadOrHopeless Binary Frequency Table")
    print(df_selected["SadOrHopeless_binary"].value_counts(dropna=False).sort_index())

    print_section("BMIPCT Summary Statistics")
    print(df_selected["BMIPCT_clean"].describe())

    print_section("Missing Value Check")
    print("SadOrHopeless missing after recoding:", df_selected["SadOrHopeless_binary"].isna().sum())
    print("BMIPCT missing/non-numeric after cleaning:", df_selected["BMIPCT_clean"].isna().sum())

    print_section("Final Sample Sizes")
    print("Proportion analysis n =", len(prop_data))
    print("Mean analysis n =", len(mean_data))

    selected_output = PROCESSED_DIR / "yrbs_selected_recoded.csv"
    prop_output = PROCESSED_DIR / "yrbs_prop_analysis.csv"
    mean_output = PROCESSED_DIR / "yrbs_mean_analysis.csv"

    df_selected.to_csv(selected_output, index=False)
    prop_data.to_csv(prop_output, index=False)
    mean_data.to_csv(mean_output, index=False)

    print_section("Files Saved Successfully")
    print("Saved:", selected_output)
    print("Saved:", prop_output)
    print("Saved:", mean_output)

    print_section("Done")
    print("Data preparation completed successfully.")


if __name__ == "__main__":
    main()