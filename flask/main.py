from flask import Flask, request, render_template, send_file
import os
from handwritingOCR import converter  # Import the updated converter module

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    if file:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Process the uploaded file and extract text
        try:
            output_format = request.form.get("output_format", "text")  # Default to text
            extracted_text, result_path = converter.process_pdf(file_path, output_format=output_format)
            return render_template('preview.html', text=extracted_text, result_path=result_path)
        except Exception as e:
            return f"Error: {str(e)}", 500


@app.route('/download')
def download_file():
    result_path = request.args.get('result_path')
    if not result_path or not os.path.exists(result_path):
        return "File not found", 404
    return send_file(result_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
