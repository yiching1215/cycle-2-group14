from pathlib import Path
import pandas as pd
import numpy as np

# =========================
# 1. Path settings
# =========================
# 假設此腳本位於 notebooks/ 資料夾下，回溯一層到專案根目錄
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
    print_section("Project Cycle 2 Data Preparation (Listwise Deletion Version)")

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f"Cannot find raw data file at: {RAW_DATA_PATH}")

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # 讀取原始資料，新增性別欄位 WhatIsYourSex
    df = pd.read_csv(RAW_DATA_PATH)
    
    required_columns = ["SadOrHopeless", "BMIPCT", "WhatIsYourSex"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns in dataset: {missing_columns}")

    # 1. 選取欄位並進行初步清理
    df_selected = df[required_columns].copy()
    df_selected["SadOrHopeless_binary"] = df_selected["SadOrHopeless"].apply(recode_sad_or_hopeless)
    df_selected["BMIPCT_clean"] = pd.to_numeric(df_selected["BMIPCT"], errors="coerce")

    # 2. 執行全域刪除 (Listwise Deletion)
    # 只要 悲傷、BMI、性別 其中有一個是缺失值，就刪除該樣本
    # 註：WhatIsYourSex 若有缺失也會在此步驟被刪除
    clean_columns = ["SadOrHopeless_binary", "BMIPCT_clean", "WhatIsYourSex"]
    df_final = df_selected.dropna(subset=clean_columns).copy()

    # 3. 準備輸出資料集 (此時所有資料集的樣本數 n 將會完全相同)
    prop_data = df_final.copy()
    mean_data = df_final.copy()

    # 統計報告
    print_section("Data Cleaning Summary")
    print(f"原始選取樣本數: {len(df_selected)}")
    print(f"全域刪除後樣本數 (有效樣本): {len(df_final)}")
    print(f"總共刪除的缺失值個數: {len(df_selected) - len(df_final)}")

    print_section("Final Variable Distribution")
    print("SadOrHopeless_binary 分佈:\n", df_final["SadOrHopeless_binary"].value_counts().sort_index())
    print("\nWhatIsYourSex 分佈:\n", df_final["WhatIsYourSex"].value_counts().sort_index())
    print("\nBMIPCT_clean 描述統計:\n", df_final["BMIPCT_clean"].describe())

    # 4. 存檔
    selected_output = PROCESSED_DIR / "yrbs_selected_recoded.csv"
    prop_output = PROCESSED_DIR / "yrbs_prop_analysis.csv"
    mean_output = PROCESSED_DIR / "yrbs_mean_analysis.csv"

    df_final.to_csv(selected_output, index=False)
    prop_data.to_csv(prop_output, index=False)
    mean_data.to_csv(mean_output, index=False)

    print_section("Files Saved Successfully")
    print(f"已儲存完整樣本至: {PROCESSED_DIR}")
    print("現在後續所有分析（比例、均值、性別對比）將使用完全相同的樣本。")

if __name__ == "__main__":
    main()