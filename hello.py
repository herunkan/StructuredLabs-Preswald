from preswald import connect, get_df
from preswald import query
from preswald import table, text
from preswald import plotly
import pandas as pd
import plotly.express as px

#1. Load the dataset
connect()  # Initialize connection to preswald.toml data sources
df = get_df("student_habits_performance.csv")  # Load data
df = pd.read_csv("student_habits_performance.csv")

#2. Query or manipulate the data

sql_find_students = "WITH cte AS (SELECT gender, AVG(exam_score) AS avg_score FROM student_habits_performance WHERE parent_education = 'high school' GROUP BY gender) SELECT s.student_id, s.gender, s.study_hours_per_day, s.exam_score FROM student_habits_performance s JOIN cte a ON cte.gender = 'female' WHERE s.parent_education = 'high school' AND s.exam_score > cte.avg_score;"
filtered_df = query(sql_find_students, "student_habits_performance")
sql_female_average = "SELECT AVG(exam_score) FROM student_habits_performance WHERE gender = 'female' AND parent_education = 'high school'"
female_avg = query(sql_female_average, "student_habits_performance").iloc[0, 0]


#3. Build an interactive UI
text("# A look at Student Habits vs Academic Performance")
text("# This table shows the students whose exam score is higher than the average female student with parents that have a high school degree with their study hours.")
table(filtered_df, title="Result of Students")

#4. Create a visualization
fig = px.scatter(
    filtered_df,
    x = "study_hours_per_day",
    y = "exam_score",
    color = "gender",
    hover_data = ["student_id"],
    title = "Exam scores and study hors (Female with )"
)

fig.add_hline(
    y = female_avg,
    line_dash = "dash",
    line_color = "red",
    annotation_text = f"Female Avg: {female_avg:.1f}",
    annotation_position = "top left"
)

plotly(fig)


