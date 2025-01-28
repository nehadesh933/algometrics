from flask import Flask, render_template, request, flash, redirect, url_for
import os

app = Flask(__name__)

# Setting the folder where files will be uploaded
app.config['UPLOAD_FOLDER'] = 'uploads'

# Secret key needed to use Flash messages
app.secret_key = 'your_secret_key_here'  # You can change this to any string for security

# Check if the upload folder exists, if not, create it
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Define the main route of the app
@app.route('/', methods=['GET', 'POST'])
def index():
    # When a file is uploaded
    if request.method == 'POST':
        file = request.files['fileInput']  # Get the file from the form
        if file:
            filename = file.filename  # Get the name of the file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save the file
            flash('File successfully uploaded!', 'success')  # Show a success message
            return redirect(url_for('index'))  # Redirect to the same page to show message
        else:
            flash('No file selected!', 'danger')  # Show an error message if no file was selected
            return redirect(url_for('index'))  # Redirect to the same page to show message
    
    # For GET requests (just when the page loads), show the form
    return render_template('index.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
