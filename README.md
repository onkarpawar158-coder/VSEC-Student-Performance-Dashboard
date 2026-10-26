# 📊 Student Performance Analysis Using Python

A data analysis, visualization, and interactive web dashboard project that explores student performance in Mathematics, Reading, and Writing using Python.

## 📌 About the Project

Student Performance Analysis is a Python-based project developed for the **Scientific Computing with Python (VSEC)** subject. It analyzes students' examination scores to identify performance patterns, understand relationships between subjects, and compare results based on test preparation course completion.

The project uses **Python, Streamlit, Pandas, NumPy, Matplotlib, and Seaborn** to process the dataset, perform dynamic statistical analysis, and present both static notebook analyses and an interactive web dashboard.

## 🎯 Objectives

- Load and analyze student examination data dynamically.
- Inspect data quality and check for missing or duplicate records.
- Calculate average scores and descriptive statistics across examination subjects.
- Analyze correlations between Mathematics, Reading, and Writing scores.
- Compare the performance of students who completed test preparation courses with those who did not.
- Present results using interactive graphs, charts, and a production-grade Streamlit dashboard.
- Provide a searchable and filterable dataset explorer with data export capabilities.

## 🛠️ Technologies Used

| Technology       | Purpose                              |
| ---------------- | ------------------------------------ |
| Python           | Programming and statistical analysis |
| Streamlit        | Interactive web dashboard UI         |
| Jupyter Notebook | Interactive exploratory environment  |
| Pandas           | Data loading, cleaning, and grouping |
| NumPy            | Numerical and vector calculations    |
| Matplotlib       | Creating charts, plots, and figures  |
| Seaborn          | Statistical data visualization       |

## 📂 Project Structure

```text
Student-Performance-Analysis/
│
├── app.py                            # Streamlit interactive dashboard application
├── requirements.txt                  # Python dependencies for the project
├── student_performance.ipynb         # Exploratory data analysis Jupyter Notebook
├── StudentsPerformance.csv           # Original dataset (1,000 records)
├── cleaned_student_performance.csv   # Cleaned dataset without whitespace
├── README.md                         # Project documentation and guide
└── .gitignore
```

## 📁 Dataset Description

The project uses the **Students Performance in Exams** dataset, which contains 1,000 student records and 8 columns.

| Column                      | Description                        |
| --------------------------- | ---------------------------------- |
| gender                      | Student gender                     |
| race/ethnicity              | Student group category             |
| parental level of education | Parent's education level           |
| lunch                       | Type of lunch program              |
| test preparation course     | Test preparation completion status |
| math score                  | Mathematics examination score      |
| reading score               | Reading examination score          |
| writing score               | Writing examination score          |

## ⚙️ Methodology

1. **Data Loading:** Import the CSV dataset dynamically using Pandas.
2. **Data Inspection:** Examine dataset dimensions, columns, and data types.
3. **Data Quality Check:** Check for missing values and duplicate records.
4. **Statistical Analysis:** Calculate subject averages, standard deviations, and percentiles.
5. **Correlation Analysis:** Examine linear relationships between the three subject scores.
6. **Group Comparison:** Compare average scores grouped by test preparation course completion.
7. **Visualization & Dashboard:** Communicate insights using both notebook plots and the multi-page Streamlit dashboard.

## 📈 Key Findings

- Average Mathematics score: **66.09**
- Average Reading score: **69.17**
- Average Writing score: **68.05**
- Reading and Writing scores have an extremely strong positive correlation of approximately **0.955**.
- Math scores correlate strongly with Reading (**r = 0.818**) and Writing (**r = 0.803**).
- Students who completed the test preparation course had higher average scores in all subjects:
  - **Writing Advantage:** `+9.91 points` (74.42 vs 64.50)
  - **Reading Advantage:** `+7.36 points` (73.89 vs 66.53)
  - **Math Advantage:** `+5.62 points` (69.70 vs 64.08)
  - **Overall Average Advantage:** `+7.63 points` (72.67 vs 65.04)

These findings describe patterns in the dataset and do not establish that test preparation alone caused the differences in scores.

## 🖥️ Interactive Streamlit Dashboard Features

The dashboard (`app.py`) provides a multi-page interactive web interface:

1. **📊 Executive Overview:**
   - Real-time KPI metric cards (Total Students, Math Avg, Reading Avg, Writing Avg, Pass Rate).
   - Subject descriptive statistics table (Count, Mean, Std, Min, 25%, Median, 75%, Max).
   - Academic grade distribution bar chart (A+, A, B, C, D, F).
   - Performance highlights and top centurion statistics.

2. **📈 Exploratory Visual Analysis:**
   - **Average Marks by Subject:** Bar chart comparison with precise value annotations.
   - **Score Distribution:** Histogram with Gaussian KDE density curve and adjustable bin sliders.
   - **Correlation Heatmap:** Seaborn viridis heatmap with annotated Pearson coefficients.
   - **Test Preparation Comparison:** Grouped multi-bar chart and exact point advantage breakdown.
   - **Demographic Factors:** Performance breakdowns by Parental Education, Lunch Program, and Gender.

3. **🗂️ Student Dataset Explorer:**
   - Multi-select filters for Gender, Race/Ethnicity, Parental Education, Lunch, Test Prep, and Pass/Fail status.
   - Slider filter for overall average score range and live keyword search.
   - Interactive searchable table with sortable columns.
   - Instant CSV export of filtered cohorts.

4. **💡 Statistical Insights:**
   - Synthesized analytical takeaways explaining verbal synergy and socioeconomic factors.
   - Actionable strategic recommendations for educational policy and curriculum design.

5. **ℹ️ About & Academic Info:**
   - Institutional context, team member recognition, and technical specifications.

## 🚀 Installation and Usage

### Prerequisites

- Python 3.9+ (tested on Python 3.13)
- pip package manager

### 1. Clone the repository

```bash
git clone https://github.com/onkarpawar158-coder/VSEC-project.git
```

### 2. Open the project directory

```bash
cd VSEC-project
```

### 3. Install dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

*(Alternatively: `pip install streamlit pandas numpy matplotlib seaborn jupyter`)*

### 4. Launch the Streamlit Dashboard

Run the interactive dashboard locally:

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

### 5. Run the Jupyter Notebook (Optional)

To explore the original interactive notebook:

```bash
jupyter notebook
```

Open `student_performance.ipynb` and execute the cells from top to bottom.

## 🎓 Academic Information

- **Project Title:** Student Performance Analysis Using Python
- **Subject:** Scientific Computing with Python (VSEC)
- **Class:** Second Year B.Tech
- **Academic Year:** 2026–2027
- **Team Members:**
  - Onkar Pawar
  - Pratik Shendage

## 🔮 Future Scope

- Deploy the Streamlit dashboard on cloud platforms (Streamlit Community Cloud / Render / AWS).
- Integrate predictive machine learning models (e.g., Random Forest or Linear Regression) to predict student scores based on preparatory and demographic variables.
- Extend analysis across longitudinal multi-semester datasets.

## 📚 Dataset Reference

Kaggle — *Students Performance in Exams*  
[https://www.kaggle.com/datasets/spscientist/students-performance-in-exams](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams)

## 📄 License

This project was developed for educational and academic purposes.

---

**Developed as part of the Scientific Computing with Python (VSEC) course project.**
