# Project Cycle 2 – Confidence Intervals and One-Sample Inference

## Group Information
- Group Number: 14
- Members:
  - 王奕晴
  - 周以心
  - 詹濬誌


---

## Dataset
- Dataset used: YRBS_2007.csv
- Source: Provided for Project Cycle 2

---

## Selected Variables

### 1. Proportion Analysis Variable
- Variable: **SadOrHopeless**
- Description: Whether a student felt sad or hopeless

### 2. Mean Analysis Variable
- Variable: **BMIPCT**
- Description: BMI percentile of students

---

## Benchmark Values

- SadOrHopeless:  
  \( p_0 = 0.30 \)

- BMIPCT:  
  \( \mu_0 = 65.0 \)

---

## Research Questions

1. **Proportion Question**  
   Is the proportion of students who felt sad or hopeless different from 0.30?

2. **Mean Question**  
   Is the mean BMI percentile of students different from 65.0?

---

## Data Processing

### Raw Data
- Stored in: `data/raw/YRBS_2007.csv`
- The original dataset is not modified

### Data Cleaning and Recoding

#### SadOrHopeless
- Original codes:
  - 1 = Yes (felt sad or hopeless)
  - 2 = No
- Recoding:
  - 1 → 1 (success)
  - 2 → 0 (failure)
  - Other values → missing (excluded)

#### BMIPCT
- Converted to numeric format
- Non-numeric values → treated as missing
- Missing values excluded from analysis

### Processed Data Files

- `yrbs_selected_recoded.csv`  
  → Contains selected variables with recoding applied

- `yrbs_prop_analysis.csv`  
  → Clean dataset for proportion analysis (SadOrHopeless)

- `yrbs_mean_analysis.csv`  
  → Clean dataset for mean analysis (BMIPCT)

---

## Project Structure
