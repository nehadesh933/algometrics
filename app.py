from flask import Flask, render_template, request, flash, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = 'algometricskey'

# Set up the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create the folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # File upload
        file = request.files['fileInput']
        if file:
            # Save the uploaded file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            flash('File successfully uploaded!', 'success')
            
            # Perform EDA (read and process the file)
            try:
                # Check if file is .csv or .xls
                if file.filename.endswith('.csv'):
                    insights = pd.read_csv(filepath)
                elif file.filename.endswith(('.xls', '.xlsx')):  # Check for Excel files
                    insights = pd.read_excel(filepath)
                else:
                    flash('Invalid file format!', 'danger')
                    return redirect(url_for('index'))
                
                # Prepare EDA results
                eda_results = {
                    'shape': insights.shape,
                    'columns': insights.columns.tolist(),
                    'missing_values': insights.isnull().sum(),
                    'summary': insights.describe().to_html(),
                    'head': insights.head().to_html()
                }

                # Redirect to the results page with the insights data
                return render_template('eda_results.html', insights=eda_results)

            except Exception as e:
                flash(f"Error in processing the file: {str(e)}", 'danger')
                return redirect(url_for('index'))

        else:
            flash('No file selected!', 'danger')
            return redirect(url_for('index'))

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
