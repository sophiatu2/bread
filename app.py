from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from io import BytesIO
import os
import subprocess

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Mapping user-friendly names to script filenames
SCRIPT_MAP = {
    "Amex": "amex.py",
    "Bilt": "bilt.py",
    "Chase": "chase.py",
    "Capital One": "capitalone.py",
    "Capital One Checking": "capitalonedebit.py",
    "Citi": "citi.py",
}


@app.route("/process", methods=["POST"])
def process_file():
    if "file" not in request.files or "script" not in request.form:
        return jsonify({"error": "File or script not provided"}), 400

    file = request.files["file"]
    user_selection = request.form["script"]

    # Check file compatibility
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # if user_selection == "Amex":
    #     expected_extension = ".xlsx"
    #     if not file.filename.endswith(".xlsx"):
    #         return (
    #             jsonify(
    #                 {
    #                     "error": f"Invalid file type. Expected a .xlsx file for {user_selection}."
    #                 }
    #             ),
    #             400,
    #         )
    if not file.filename.lower().endswith(".csv"):
        return (
            jsonify(
                {
                    "error": f"Invalid file type. Expected a .csv file for {user_selection}."
                }
            ),
            400,
        )
    else:
        expected_extension = ".csv"

    # Check script compatibility
    script_name = SCRIPT_MAP.get(user_selection)
    if not script_name:
        return jsonify({"error": f"Invalid script selection: {user_selection}"}), 400

    script_path = f"scripts/{script_name}"
    if not os.path.exists(script_path):
        return jsonify({"error": f"Script file not found: {script_path}"}), 400

    # Save file in memory
    input_stream = BytesIO(file.read())
    output_stream = BytesIO()

    try:
        # Save the input to a temporary file for the script to read
        input_path = f"/tmp/input{expected_extension}"
        base_name = os.path.splitext(os.path.basename(file.filename))[0]
        output_path = f"/tmp/{base_name}_processed.csv"

        with open(input_path, "wb") as temp_input:
            temp_input.write(input_stream.getvalue())

        # Run the Python script
        subprocess.run(
            ["python3", f"scripts/{script_name}", input_path, output_path], check=True
        )

        # Read the output from the temporary file
        with open(output_path, "rb") as temp_output:
            output_stream.write(temp_output.read())

        # Clean up temporary files
        os.remove(input_path)
        os.remove(output_path)

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Error processing file: {str(e)}"}), 500

    # Before sending the file
    print(f"Saved file as {output_path}")

    # Return the processed file as a download
    output_stream.seek(0)
    return send_file(
        output_stream,
        as_attachment=True,
        download_name=f"{base_name}_processed.csv",
    )


if __name__ == "__main__":
    app.run(debug=True)
