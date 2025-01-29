from flask import Flask, render_template, request, flash, redirect, url_for # type: ignore
import os

app = Flask(__name__)

# files will be uploaded in this location
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'algometricskey'

# check if folder exists, if not create it
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# main route of the app
@app.route('/', methods=['GET', 'POST'])
def index():
    # file uploaded
    if request.method == 'POST':
        file = request.files['fileInput']  # get the file from the form
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))  # save the file
            flash('file is successfully uploaded.', 'success')  # success message
        else:
            flash('no file was selected.', 'danger')  # error message if no file was selected
        return redirect(url_for('index'))  # redirect to the same page to show message
    
    # for GET requests (just when the page loads), show the form
    return render_template('index.html')

# run the app
if __name__ == '__main__':
    app.run(debug=True)
