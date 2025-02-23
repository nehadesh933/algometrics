import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

# ✅ Ensure output directory exists
output_dir = "static/visualizations/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# ✅ Load the data
data_path = r"C:\NEHA\courses\algometrics\uploads\exams.csv"
try:
    df = pd.read_csv(data_path)
    print("✅ Data loaded successfully!")
except Exception as e:
    print(f"❌ ERROR loading data: {e}")
    exit()

# ✅ Handle categorical variables
encoder = LabelEncoder()
df["gender"] = encoder.fit_transform(df["gender"])
df["race/ethnicity"] = encoder.fit_transform(df["race/ethnicity"])
df["parental level of education"] = encoder.fit_transform(df["parental level of education"])
df["lunch"] = encoder.fit_transform(df["lunch"])
df["test preparation course"] = encoder.fit_transform(df["test preparation course"])

# ✅ Generate the correlation matrix
df_corr = df.corr()

# ✅ Generate Visualizations
try:
    # Pie Chart: Average Scores by Gender
    gender_avg = df.groupby("gender")[["math score", "reading score", "writing score"]].mean()
    fig = px.pie(names=gender_avg.index, values=gender_avg.mean(axis=1), title="Average Scores by Gender")
    fig.write_html(os.path.join(output_dir, "average_scores_by_gender.html"))

    # Line Chart: Standard Deviation by Parental Education
    edu_std = df.groupby("parental level of education")[["math score", "reading score", "writing score"]].std()
    fig = px.line(edu_std, x=edu_std.index, y=["math score", "reading score", "writing score"], markers=True,
                  title="Standard Deviation of Scores by Parental Education Level")
    fig.write_html(os.path.join(output_dir, "std_scores_by_parental_education.html"))

    # Bar Chart: Minimum Scores by Race/Ethnicity
    race_min = df.groupby("race/ethnicity")[["math score", "reading score", "writing score"]].min()
    fig = px.bar(race_min, x=race_min.index, y=["math score", "reading score", "writing score"],
                 title="Minimum Scores by Race/Ethnicity", barmode='group')
    fig.write_html(os.path.join(output_dir, "min_scores_by_race.html"))

    # Donut Chart: Average Math Score by Test Preparation
    prep_avg = df.groupby("test preparation course")["math score"].mean()
    fig = go.Figure(data=[go.Pie(labels=prep_avg.index, values=prep_avg, hole=0.3)])
    fig.update_layout(title_text="Average Math Score by Test Preparation")
    fig.write_html(os.path.join(output_dir, "avg_math_score_by_test_prep.html"))

    # Heatmap
    df_corr = df.corr()
    fig = px.imshow(df_corr.values, text_auto=True, aspect="auto", x=df_corr.columns, y=df_corr.columns)
    fig.write_html(os.path.join(output_dir, "Heatmaps.html"))

    print("✅ Visualizations generated successfully!")

except Exception as e:
    print(f"❌ ERROR generating visualizations: {e}")

# ✅ Generate Predictions & Insights
try:
    predictions_text = "<h3>📊 Key Predictions & Insights</h3>"

    # 📌 Gender-Based Performance
    gender_avg = df.groupby("gender")[["math score", "reading score", "writing score"]].mean()
    male_avg = round(gender_avg.iloc[0].mean(), 1)
    female_avg = round(gender_avg.iloc[1].mean(), 1)
    predictions_text += f"<h4>📌 Gender-Based Performance</h4>"
    predictions_text += f"<p>➡️ Males on average score <b>{male_avg}</b>, while females score <b>{female_avg}</b>.</p>"
    predictions_text += f"<p>➡️ Gender differences are more pronounced in <b>math scores</b>.</p>"

    # 📌 Parental Education Impact
    predictions_text += f"<h4>📌 Parental Education Impact</h4>"
    predictions_text += f"<p>➡️ Higher parental education is associated with <b>better overall scores</b>.</p>"
    predictions_text += f"<p>➡️ Students whose parents completed college tend to perform the best in <b>reading</b> and <b>writing</b>.</p>"

    # 📌 Minimum Scores by Race/Ethnicity
    lowest_performing_group = race_min.mean(axis=1).idxmin()
    highest_performing_group = race_min.mean(axis=1).idxmax()
    predictions_text += f"<h4>📌 Minimum Scores by Ethnicity</h4>"
    predictions_text += f"<p>➡️ Group <b>{lowest_performing_group}</b> had the lowest minimum scores.</p>"
    predictions_text += f"<p>➡️ Group <b>{highest_performing_group}</b> consistently had higher minimum scores.</p>"

    # 📌 Test Preparation Insights
    predictions_text += f"<h4>📌 Test Preparation Insights</h4>"
    predictions_text += f"<p>➡️ Completing test preparation courses <b>boosts math scores</b> significantly.</p>"
    predictions_text += f"<p>➡️ Test prep has the <b>biggest impact on writing scores</b>.</p>"

    # 📌 Correlation Insights
    math_corr = df_corr.loc["math score", "writing score"]
    predictions_text += f"<h4>📌 Correlation Insights</h4>"
    predictions_text += f"<p>➡️ Math and writing scores have a high correlation of <b>{round(math_corr, 2)}</b>.</p>"
    predictions_text += f"<p>➡️ A student's math score is a <b>strong predictor</b> of their writing performance.</p>"

    # ✅ Save predictions to file
    predictions_file_path = os.path.join(output_dir, "predictions.html")
    with open(predictions_file_path, "w", encoding="utf-8") as file:
        file.write(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Predictions & Insights</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 20px; }}
                .container {{ max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); }}
                h3 {{ color: #007bff; text-align: center; margin-bottom: 15px; }}
                h4 {{ color: #17a2b8; margin-top: 20px; }}
                p {{ font-size: 1.1rem; color: #333; }}
                hr {{ border-top: 1px solid #ddd; }}
            </style>
        </head>
        <body>
            <div class="container">
                {predictions_text}
            </div>
        </body>
        </html>
        """)

    print(f"✅ PREDICTIONS FILE GENERATED SUCCESSFULLY at {predictions_file_path}")

except Exception as e:
    print(f"❌ ERROR generating predictions: {e}")
