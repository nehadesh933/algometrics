from flask import Flask, render_template, request, flash, redirect, url_for
import os
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import subprocess

app = Flask(__name__)
app.config["TIMEOUT"] = 900
app.secret_key = 'algometricskey'

# Set up the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create the folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# ✅ Route for Landing Page (This is now the FIRST page!)
@app.route('/')
def landing_page():
    return render_template('landingpage.html')

# ✅ Route for Upload Page (Moves Upload logic here)
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['fileInput']
        if file:
            # Save uploaded file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            flash('File successfully uploaded!', 'success')

            try:
                # Read file based on type
                if file.filename.endswith('.csv'):
                    insights = pd.read_csv(filepath)
                elif file.filename.endswith(('.xls', '.xlsx')):  # Excel files
                    insights = pd.read_excel(filepath)
                else:
                    flash('Invalid file format!', 'danger')
                    return redirect(url_for('upload'))

                # Generate EDA results
                eda_results = {
                    'shape': insights.shape,
                    'columns': insights.columns.tolist(),
                    'missing_values': insights.isnull().sum().to_dict(),
                    'summary': insights.describe().to_html(),
                    'head': insights.head().to_html(),
                    'predictions': model_predictions(insights)
                }

                insights = insights.dropna() # preprocessing
                os.remove(filepath)
                # Run visualization script
                subprocess.run(["python", "visualization.py"])

                return render_template('eda_results.html', insights=eda_results)

            except Exception as e:
                print(f"Error processing file: {e}")
                flash(f"Error in processing the file: {str(e)}", 'danger')
                return redirect(url_for('upload'))

        else:
            flash('No file selected!', 'danger')
            return redirect(url_for('upload'))

    return render_template('index.html')

# ✅ Dashboard Route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

def model_predictions(data):
    encoder = LabelEncoder()
    data["gender"] = encoder.fit_transform(data["gender"])
    data["race/ethnicity"] = encoder.fit_transform(data["race/ethnicity"])
    data["parental level of education"] = encoder.fit_transform(data["parental level of education"])
    data["lunch"] = encoder.fit_transform(data["lunch"])
    print("Called")
    data = data.drop(columns=["test preparation course"])

    pred = {}

    # Math Score Predictions
    clf_l = joblib.load("m_Linear_Regression.pkl")
    clf_r = joblib.load("m_Random_Forest.pkl")
    df = data.drop(columns=["math score"])
    pred_r = clf_r.predict(df)
    pred_l = clf_l.predict(df)
    pred["math score"] = [(pred_r[i] + pred_l[i]) / 2 for i in range(len(pred_r))]

    # Reading Score Predictions
    clf_l = joblib.load("r_Linear_Regression.pkl")
    clf_r = joblib.load("r_Random_Forest.pkl")
    df = data.drop(columns=["reading score"])
    pred_r = clf_r.predict(df)
    pred_l = clf_l.predict(df)
    pred["reading score"] = [(pred_r[i] + pred_l[i]) / 2 for i in range(len(pred_r))]

    # Writing Score Predictions
    clf_l = joblib.load("w_Linear_Regression.pkl")
    clf_r = joblib.load("w_Random_Forest.pkl")
    df = data.drop(columns=["writing score"])
    pred_r = clf_r.predict(df)
    pred_l = clf_l.predict(df)
    pred["writing score"] = [(pred_r[i] + pred_l[i]) / 2 for i in range(len(pred_r))]

    final_pred = pd.DataFrame(pred)
    final_pred[["gender", "race/ethnicity", "parental level of education", "lunch"]] = data[["gender", "race/ethnicity", "parental level of education", "lunch"]]
    final_pred.to_csv("Predictions.csv")

if __name__ == '__main__':
    app.run(debug=True)
