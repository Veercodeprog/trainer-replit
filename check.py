

def add_nlu_yml_data_from_excel(excel_file_path, selected_department):
    df = pd.read_excel(excel_file_path, sheet_name='English')

    # Read the existing content of nlu.yml
    nlu_filename = os.path.join("data", "nlu.yml")
    try:
        with open(nlu_filename, "r") as nlu_file:
            existing_content = nlu_file.read()
    except FileNotFoundError:
        existing_content = ""

    appended_data = []  # Initialize a list to store appended data

    with open(nlu_filename, "a") as nlu_file:
        for index, row in df.iterrows():
            intent_raw = row['Questions_In_English'].split('\n')[0]
            intent_name_en = clean_intent_name(intent_raw) + '_en'
            intent_name_hi = clean_intent_name(intent_raw) + '_hi'
            intent_name_ur = clean_intent_name(intent_raw) + '_ur'

            examples_en = df.iloc[index]['Questions_In_English']
            examples_hi = df.iloc[index]['Questions_In_Hindi']
            examples_ur = df.iloc[index]['Questions_In_Urdu']

            if existing_content.strip() == "":
                # If the file is empty, don't add an extra newline
                nlu_file.write(f"- intent: {intent_name_en}\n")
            else:
                nlu_file.write(f"\n- intent: {intent_name_en}\n")

            nlu_file.write("  examples: |\n")
            for line in examples_en.split('\n'):
                nlu_file.write(f"    - {selected_department} {line}\n")
                appended_data.append(f"    - {selected_department} {line}")

            nlu_file.write(f"- intent: {intent_name_hi}\n")
            nlu_file.write("  examples: |\n")
            for line in examples_hi.split('\n'):
                nlu_file.write(f"    - {selected_department} {line}\n")
                appended_data.append(f"    - {selected_department} {line}")

            nlu_file.write(f"- intent: {intent_name_ur}\n")
            nlu_file.write("  examples: |\n")
            for line in examples_ur.split('\n'):
                nlu_file.write(f"    - {selected_department} {line}\n")
                appended_data.append(f"    - {selected_department} {line}")

    # Return the appended data as a single string
    return "\n".join(appended_data)

@app.route('/generate_nlu4', methods=['POST'])
def generate_nlu_route4():
    if 'excelFile' not in request.files:
        return "No file part"

    excel_file = request.files['excelFile']
    selected_department = request.form.get('department')  # Get the selected department from the form

    if excel_file.filename == '':
        return "No selected file"

    if excel_file:
        excel_file_name = os.path.splitext(excel_file.filename)[0]
        excel_file_path = 'temp.xlsx'
        excel_file.save(excel_file_path)

        # Add NLU data from the uploaded Excel file to the existing 'nlu.yml' file
        appended_data = add_nlu_yml_data_from_excel(excel_file_path, selected_department)

        # Return the appended data as a JSON response
        response_data = {
            "status": "success",
            "message": "NLU data added successfully!",
            "appended_data": appended_data
        }
        return jsonify(response_data)
    else:
        return "Invalid file format. Only Excel files are allowed."


