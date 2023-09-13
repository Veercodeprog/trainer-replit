import os
import re
import yaml
import paramiko
from flask import Flask, render_template, jsonify, request
import subprocess  # Import the subprocess module
import mysql.connector
import pandas as pd
import ruamel.yaml
from io import StringIO


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'veer',
    'password': 'veer@945050',
    'database': 'training_app'
}




@app.route('/')
def training_ui():
    return render_template('training_ui.html')

@app.route('/train_from_excel')
def train_from_excel():
    return render_template('train_from_excel.html')

@app.route('/add_training_and_train')
def add_training_and_train():
    return render_template('add_training_data.html')


def generate_stories_yml_from_yml_hindi(domain_file_path):
    stories_data = {"version": "3.1", "stories": []}

    with open(domain_file_path, "r") as domain_file:
        domain_data = yaml.safe_load(domain_file)

    for intent in domain_data.get("intents", []):
        intent_name = intent.strip()
        action_name = f"utter_{intent_name}"

        story = {
            "story": f"{intent_name} hi",
            "steps": [
                {"intent": intent_name, "action": action_name}
            ],
        }

        stories_data["stories"].append(story)

    return stories_data

def generate_stories_yml_from_yml_urdu(domain_file_path):
    stories_data = {"version": "3.1", "stories": []}

    with open(domain_file_path, "r") as domain_file:
        domain_data = yaml.safe_load(domain_file)

    for intent in domain_data.get("intents", []):
        intent_name = intent.strip()
        action_name = f"utter_{intent_name}"

        story = {
            "story": f"{intent_name} ur",
            "steps": [
                {"intent": intent_name, "action": action_name}
            ],
        }

        stories_data["stories"].append(story)

    return stories_data

@app.route('/generate_nlu_english', methods=['POST'])
def generate_nlu_route_english():
    if 'nluFile' not in request.files:
        return "No file part"

    nlu_file = request.files['nluFile']

    if nlu_file.filename == '':
        return "No selected file"

    if nlu_file:
        excel_file_name = os.path.splitext(nlu_file.filename)[0]  # Corrected indentation
        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        nlu_file.save(excel_file_path)

        # Generate NLU content from the uploaded Excel file
        nlu_yml_content = generate_nlu_yml_from_excel_english(excel_file_path)

        # Save the generated nlu.yml content to a file
        nlu_filename = f"{excel_file_name}_nlu_english.yml"
        with open(nlu_filename, "w") as nlu_file:
            nlu_file.write(nlu_yml_content)

        return "NLU File generated!"



@app.route('/generate_nlu_hindi', methods=['POST'])
def generate_nlu_route_hindi():
    if 'nluFile' not in request.files:
        return "No file part"

    nlu_file = request.files['nluFile']

    if nlu_file.filename == '':
        return "No selected file"

    if nlu_file:
        excel_file_name = os.path.splitext(nlu_file.filename)[0]  # Corrected indentation
        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        nlu_file.save(excel_file_path)

        # Generate NLU content from the uploaded Excel file
        nlu_yml_content = generate_nlu_yml_from_excel_hindi(excel_file_path)

        # Save the generated nlu.yml content to a file
        nlu_filename = f"{excel_file_name}_nlu_hindi.yml"
        with open(nlu_filename, "w") as nlu_file:
            nlu_file.write(nlu_yml_content)

        return "NLU File generated!"



@app.route('/generate_nlu_urdu', methods=['POST'])
def generate_nlu_route_urdu():
    if 'nluFile' not in request.files:
        return "No file part"

    nlu_file = request.files['nluFile']

    if nlu_file.filename == '':
        return "No selected file"


    if nlu_file:
        excel_file_name = os.path.splitext(nlu_file.filename)[0]  # Corrected indentation
        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        nlu_file.save(excel_file_path)

        # Generate NLU content from the uploaded Excel file
        nlu_yml_content = generate_nlu_yml_from_excel_urdu(excel_file_path)

        # Save the generated nlu.yml content to a file
        nlu_filename = f"{excel_file_name}_nlu_urdu.yml"
        with open(nlu_filename, "w") as nlu_file:
            nlu_file.write(nlu_yml_content)

        return "NLU File generated!"



@app.route('/generate_domain_english', methods=['POST'])
def generate_domain_route_english():
    if 'domainFile' not in request.files:
        return "No file part"

    domain_file = request.files['domainFile']

    if domain_file.filename == '':
        return "No selected file"

    if domain_file:
        excel_file_name = os.path.splitext(domain_file.filename)[0]

        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        domain_file.save(excel_file_path)

        # Generate Domain content from the uploaded Excel file
        domain_yml_content = generate_domain_yml_from_excel_english(excel_file_path)
        domain_filename = f"{excel_file_name}_domain_english.yml"

        # Save the generated domain.yml content to a file
        with open(domain_filename, "w") as domain_file:
            domain_file.write(domain_yml_content)

        return "Domain English File generated!"


@app.route('/generate_domain_hindi', methods=['POST'])
def generate_domain_route_hindi():
    if 'domainFile' not in request.files:
        return "No file part"

    domain_file = request.files['domainFile']

    if domain_file.filename == '':
        return "No selected file"

    if domain_file:
        excel_file_name = os.path.splitext(domain_file.filename)[0]

        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        domain_file.save(excel_file_path)

        # Generate Domain content from the uploaded Excel file
        domain_yml_content = generate_domain_yml_from_excel_hindi(excel_file_path)
        domain_filename = f"{excel_file_name}_domain_hindi.yml"

        # Save the generated domain.yml content to a file
        with open(domain_filename, "w") as domain_file:
            domain_file.write(domain_yml_content)

        return "Domain Hindi File generated!"

@app.route('/generate_domain_urdu', methods=['POST'])
def generate_domain_route_urdu():
    if 'domainFile' not in request.files:
        return "No file part"

    domain_file = request.files['domainFile']

    if domain_file.filename == '':
        return "No selected file"

    if domain_file:
        excel_file_name = os.path.splitext(domain_file.filename)[0]

        # Save the uploaded Excel file to a temporary location
        excel_file_path = 'temp.xlsx'
        domain_file.save(excel_file_path)

        # Generate Domain content from the uploaded Excel file
        domain_yml_content = generate_domain_yml_from_excel_urdu(excel_file_path)
        domain_filename = f"{excel_file_name}_domain_urdu.yml"

        # Save the generated domain.yml content to a file
        with open(domain_filename, "w") as domain_file:
            domain_file.write(domain_yml_content)

        return "Domain Urdu File generated!"



def generate_stories_yml_from_domainyml(domain_file_path):
    stories_data = {"version": "3.1", "stories": []}

    with open(domain_file_path, "r") as domain_file:
        domain_data = yaml.safe_load(domain_file)

    for intent in domain_data.get("intents", []):
        intent_name_parts = intent.strip().split('_')
        lang_code = intent_name_parts[-1]  # Extract language code
        intent_base = ' '.join(intent_name_parts[:-1])  # Join the intent base

        story = {
            "story": f"{intent_base} {lang_code}"
        }

        # Remove leading or trailing whitespace from intent_base and lang_code
        story["story"] = story["story"].strip()

        intent_name = "_".join(intent_name_parts)  # Reconstruct intent name
        action_name = f"utter_{intent_name}"

        steps = [
            {"intent": intent_name},
            {"action": action_name}
        ]
        story["steps"] = steps

        stories_data["stories"].append(story)

    return stories_data


@app.route('/generate_stories', methods=['POST'])
def generate_stories_route():
    if 'storiesFile' not in request.files:
        return "No file part"

    stories_file = request.files['storiesFile']

    if stories_file.filename == '':
        return "No selected file"

    if stories_file:
        yml_file_name = os.path.splitext(stories_file.filename)[0]

        # Save the uploaded YAML file to a temporary location
        yml_file_path = 'temp.yml'
        stories_file.save(yml_file_path)

        # Generate stories YAML content from the uploaded YAML file
        stories_yml_content = generate_stories_yml_from_domainyml(yml_file_path)
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Create the 'stories.yml' file inside the 'data' directory
        stories_filename = os.path.join(data_dir, "stories.yml")

        # Save the generated stories YAML content to a file
        with open(stories_filename, "w") as stories_file:
            yaml.dump(stories_yml_content, stories_file, default_flow_style=False, sort_keys=False)

        return "Stories English File generated!"
    else:
        return "Invalid file format. Only YAML files are allowed."




@app.route('/train_chatbot_data')
def train_chatbot_data():
    return render_template('train_chatbot.html')



@app.route('/add_training_latest', methods=['POST'])
def add_training_latest():
    try:
        intent = request.form.get('intent')
        examples = request.form.getlist('example[]')
        response_heading = request.form.get('response_heading')
        response_text = request.form.get('response_text')

        # Update nlu.yml
        nlu_path = os.path.join('test_data', 'nlu.yml')
        with open(nlu_path, 'a') as nlu_file:
            nlu_file.write(f'\n- intent: {intent}\n  examples:\n')
            for example in examples:
                nlu_file.write(f'    - {example}\n')

        # Update domain.yml
        domain_path = os.path.join('test_data', 'domain.yml')
        with open(domain_path, 'a') as domain_file:
            domain_file.write(f'\nresponses:\n  utter_{response_heading}_response:\n    - text: "{response_text}"')

        # Update stories.yml
        stories_path = os.path.join('test_data', 'stories.yml')
        with open(stories_path, 'a') as stories_file:
            stories_file.write(f'\n- story: {intent}_story\n  steps:\n    - intent: {intent}\n      user: |-\n')
            for example in examples:
                stories_file.write(f'        {example}\n')

        # Return success message
        return "Training data and intent data added successfully!"
    except Exception as e:
        return f"An error occurred: {e}"


@app.route('/add_training', methods=['POST'])
def add_training():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        intent = request.form.get('intent')
        examples = request.form.getlist('example[]')
        response_heading = request.form.get('response_heading')
        response_text = request.form.get('response_text')

        # Insert training data into the database
        insert_query = "INSERT INTO training_data (intent, response) VALUES (%s, %s)"
        cursor.execute(insert_query, (intent, response_text))
        connection.commit()

        # Update nlu.yml and domain.yml
        nlu_path = 'data/nlu.yml'
        domain_path = 'domain.yml'
        stories = 'data/stories.yml'

        with open(nlu_path, 'a') as nlu_file:
            nlu_file.write(f'\n- intent: {intent}\n  examples:\n    - {examples[0]}\n    - {examples[1]}\n    - {examples[2]}')

        with open(domain_path, 'a') as domain_file:
            domain_file.write(f'\nresponses:\n  utter_{response_heading}_response:\n    - text: "{response_text}"')


        cursor.close()
        connection.close()

        return "Training data and intent data added successfully!"
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/submit_intent', methods=['POST'])
def submit_intent_data():
    intent_heading = request.form.get('intent_heading')
    examples = request.form.getlist('example')
    response_heading = request.form.get('response_heading')
    response_text = request.form.get('response_text')

    # Update nlu.yml and domain.yml
    nlu_path = 'data/nlu.yml'
    domain_path = 'domain.yml'

    with open(nlu_path, 'a') as nlu_file:
        nlu_file.write(f'\n- intent: {intent_heading}\n  examples:\n    - {examples[0]}\n    - {examples[1]}\n    - {examples[2]}')

    with open(domain_path, 'a') as domain_file:
        domain_file.write(f'\nresponses:\n  utter_{response_heading}_response:\n    - text: "{response_text}"')

    # Train the model
    # subprocess.run(['rasa', 'train'])

    return "Intent data submitted successfully!"



def clean_intent_name(text):
    # Replace special characters '/', '(', ')' with an underscore
    cleaned_text = re.sub(r'[\/\(\)]', '_', text)
    
    # Replace other non-alphanumeric characters with a space
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s_]', ' ', cleaned_text)
    
    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text.strip())
    
    # Replace spaces with underscores
    cleaned_text = cleaned_text.replace(" ", "_")
    
    return cleaned_text




# ... (rest of your code)

def generate_nlu_yml_from_excel_english(excel_file_path):
    df_en = pd.read_excel(excel_file_path, sheet_name='English')
    df_hi = pd.read_excel(excel_file_path, sheet_name='English')

    nlu_content = "nlu:\n"
    for index, row in df_en.iterrows():
        intent_raw = row['Questions_In_English'].split('\n')[0]
        intent_name = clean_intent_name(intent_raw) + '_en'
        examples_en = df_hi.iloc[index]['Questions_In_English']
        nlu_content += f"- intent: {intent_name}\n"
        nlu_content += f"  examples: |\n"
        for line in examples_en.split('\n'):
            nlu_content += f"    - {line}\n"

    return nlu_content


def generate_nlu_yml_from_excel_hindi(excel_file_path):
    df_en = pd.read_excel(excel_file_path, sheet_name='English')
    df_hi = pd.read_excel(excel_file_path, sheet_name='English')

    
    for index, row in df_en.iterrows():
        intent_raw = row['Questions_In_English'].split('\n')[0]
        intent_name = clean_intent_name(intent_raw) + '_hi'
        examples_hi = df_hi.iloc[index]['Questions_In_Hindi']
        nlu_content = f"- intent: {intent_name}\n"
        nlu_content += f"  examples: |\n"
        for line in examples_hi.split('\n'):
            nlu_content += f"    - {line}\n"

    return nlu_content

def generate_nlu_yml_from_excel_urdu(excel_file_path):
    df_en = pd.read_excel(excel_file_path, sheet_name='English')
    df_hi = pd.read_excel(excel_file_path, sheet_name='English')

    
    for index, row in df_en.iterrows():
        intent_raw = row['Questions_In_English'].split('\n')[0]
        intent_name = clean_intent_name(intent_raw) + '_ur'
        examples_ur = df_hi.iloc[index]['Questions_In_Urdu']
        nlu_content = f"- intent: {intent_name}\n"
        nlu_content += f"  examples: |\n"
        for line in examples_ur.split('\n'):
            nlu_content += f"    - {line}\n"

    return nlu_content

def generate_nlu_yml_from_excel(excel_file_path):
    df = pd.read_excel(excel_file_path, sheet_name='English')

    nlu_content = "nlu:\n"
    for index, row in df.iterrows():
        intent_raw = row['Questions_In_English'].split('\n')[0]
        intent_name_en = clean_intent_name(intent_raw) + '_en'
        intent_name_hi = clean_intent_name(intent_raw) + '_hi'
        intent_name_ur = clean_intent_name(intent_raw) + '_ur'

        examples_en = df.iloc[index]['Questions_In_English']
        examples_hi = df.iloc[index]['Questions_In_Hindi']
        examples_ur = df.iloc[index]['Questions_In_Urdu']

        nlu_content += f"- intent: {intent_name_en}\n"
        nlu_content += f"  examples: |\n"
        for line in examples_en.split('\n'):
            nlu_content += f"    - {line}\n"

        nlu_content += f"- intent: {intent_name_hi}\n"
        nlu_content += f"  examples: |\n"
        for line in examples_hi.split('\n'):
            nlu_content += f"    - {line}\n"

        nlu_content += f"- intent: {intent_name_ur}\n"
        nlu_content += f"  examples: |\n"
        for line in examples_ur.split('\n'):
            nlu_content += f"    - {line}\n"

    return nlu_content

@app.route('/generate_nlu', methods=['POST'])
def generate_nlu_route():
    if 'nluFile' not in request.files:
        return "No file part"

    nlu_file = request.files['nluFile']

    if nlu_file.filename == '':
        return "No selected file"

    if nlu_file:
        excel_file_name = os.path.splitext(nlu_file.filename)[0]
        excel_file_path = 'temp.xlsx'
        nlu_file.save(excel_file_path)

        # Generate NLU content from the uploaded Excel file for different languages
        nlu_yml_content = generate_nlu_yml_from_excel(excel_file_path)

        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Create the 'stories.yml' file inside the 'data' directory
        combined_nlu_filename = os.path.join(data_dir, "nlu.yml")
        with open(combined_nlu_filename, "w") as nlu_file:
            nlu_file.write(nlu_yml_content)

        return "Combined NLU File generated!"








@app.route('/generate_domain', methods=['POST'])
def generate_domain_route():
    if 'domainFile' not in request.files:
        return "No file part"

    domain_file = request.files['domainFile']

    if domain_file.filename == '':
        return "No selected file"

    if domain_file:
        excel_file_name = os.path.splitext(domain_file.filename)[0]
        excel_file_path = 'temp.xlsx'
        domain_file.save(excel_file_path)

        # Generate Domain content from the uploaded Excel file for different languages
        domain_yml_content_en = generate_domain_yml_from_excel_english(excel_file_path)
        domain_yml_content_hi = generate_domain_yml_from_excel_hindi(excel_file_path)
        domain_yml_content_ur = generate_domain_yml_from_excel_urdu(excel_file_path)

        # Combine Domain content into a single YAML file
        combined_domain_content = domain_yml_content_en + '\n' + domain_yml_content_hi + '\n' + domain_yml_content_ur

        # Save the combined domain.yml content to a file
        combined_domain_filename = f"{excel_file_name}_domain.yml"
        with open(combined_domain_filename, "w") as domain_file:
            domain_file.write(combined_domain_content)

        return "Combined Domain File generated!"







# @app.route('/submit_intent', methods=['POST'])
# def submit_intent():
#     intent_heading = request.form.get('intent_heading')
#     examples = request.form.get('examples')
#     responses = request.form.get('responses')

#     # Update nlu.yml and domain.yml
#     nlu_path = 'path_to_your_nlu.yml'
#     domain_path = 'path_to_your_domain.yml'

#     with open(nlu_path, 'a') as nlu_file:
#         nlu_file.write(f'\n- intent: {intent_heading}\n  examples: |\n    - {examples}')

#     with open(domain_path, 'a') as domain_file:
#         domain_file.write(f'\nresponses:\n  utter_{intent_heading}_response:\n    - text: "{responses}"')

#     # Train the model
#     # subprocess.run(['rasa', 'train'])

#     return "Intent data submitted successfully!"

# @app.route('/submit_training_chatbot_form', methods=['POST'])
# def submit_intent():
#     intent_heading = request.form.get('intent_heading')
#     examples = request.form.get('examples')
#     responses = request.form.get('responses')

#     # Update nlu.yml and domain.yml
#     nlu_path = 'path_to_your_nlu.yml'
#     domain_path = 'path_to_your_domain.yml'

#     with open(nlu_path, 'a') as nlu_file:
#         nlu_file.write(f'\n- intent: {intent_heading}\n  examples: |\n    - {examples}')

#     with open(domain_path, 'a') as domain_file:
#         domain_file.write(f'\nresponses:\n  utter_{intent_heading}_response:\n    - text: "{responses}"')

#     # Train the model
#     # subprocess.run(['rasa', 'train'])

#     return "Intent data submitted successfully!"


def generate_domain_yml_from_excel_english(excel_file_path):
    df = pd.read_excel(excel_file_path)
    intents_responses = {}
    
    for index, row in df.iterrows():
        intent = row['Questions_In_English'].split('\n')[0]
        intent = clean_intent_name_english(intent)
        response_en = row['Answers_In_English'].split('\n')[0]
        
        intents_responses[intent] = response_en

    domain_yml_content = "intents:\n"
    for intent in intents_responses:
        domain_yml_content += f"  - {intent}\n"
    
    domain_yml_content += "\nresponses:\n"
    for intent, response in intents_responses.items():
        domain_yml_content += f"  utter_{intent}:\n"
        domain_yml_content += f"    - text: |\n"
        lines = response.split('\n')
        for line in lines:
            domain_yml_content += f"        {line}\n"

    return domain_yml_content

def generate_domain_yml_from_excel_hindi(excel_file_path):
    df = pd.read_excel(excel_file_path)
    intents_responses = {}
    
    for index, row in df.iterrows():
        intent = row['Questions_In_English'].split('\n')[0]
        intent = clean_intent_name_hindi(intent)
        print("Row data:", row)
        response_hi = row['Answers_In_Hindi'].split('\n')[0]
        
        intents_responses[intent] = response_hi  # Use response_ur instead of response_hi

    domain_yml_content = "intents:\n"
    for intent in intents_responses:
        domain_yml_content += f"  - {intent}\n"
    
    domain_yml_content += "\nresponses:\n"
    for intent, response in intents_responses.items():
        domain_yml_content += f"  utter_{intent}:\n"
        domain_yml_content += f"    - text: |\n"
        lines = response.split('\n')
        for line in lines:
            domain_yml_content += f"        {line}\n"

    return domain_yml_content


def generate_domain_yml_from_excel_urdu(excel_file_path):
    df = pd.read_excel(excel_file_path)
    intents_responses = {}
    
    for index, row in df.iterrows():
        intent = row['Questions_In_English'].split('\n')[0]
        intent = clean_intent_name_urdu(intent)
        response_ur = row['Answers_In_Urdu'].split('\n')[0]
        
        intents_responses[intent] = response_ur

    domain_yml_content = "intents:\n"
    for intent in intents_responses:
        domain_yml_content += f"  - {intent}\n"
    
    domain_yml_content += "\nresponses:\n"
    for intent, response in intents_responses.items():
        domain_yml_content += f"  utter_{intent}:\n"
        domain_yml_content += f"    - text: |\n"
        lines = response.split('\n')
        for line in lines:
            domain_yml_content += f"        {line}\n"

    return domain_yml_content

def generate_combined_content(excel_file_path):
    domain_yml_content_en = yaml.safe_load(generate_domain_yml_from_excel_english(excel_file_path))
    domain_yml_content_hi = yaml.safe_load(generate_domain_yml_from_excel_hindi(excel_file_path))
    domain_yml_content_ur = yaml.safe_load(generate_domain_yml_from_excel_urdu(excel_file_path))

    combined_domain_content = ""
    intents = []
    responses = {}

    # Process English content
    intents.extend(domain_yml_content_en['intents'])
    responses.update(domain_yml_content_en['responses'])

    # Process Hindi content
    intents.extend(domain_yml_content_hi['intents'])
    responses.update(domain_yml_content_hi['responses'])

    # Process Urdu content
    intents.extend(domain_yml_content_ur['intents'])
    responses.update(domain_yml_content_ur['responses'])

    combined_domain_content += "intents:\n"
    for intent in intents:
        combined_domain_content += f"  - {intent}\n"

    combined_domain_content += "responses:\n"
    for intent, response_list in responses.items():
        combined_domain_content += f"  {intent}:\n"
        for response_dict in response_list:
            text_content = response_dict.get('text', '')
            combined_domain_content += f"    - text: |\n        {text_content}\n"

    return combined_domain_content


@app.route('/generate_domain1', methods=['POST'])
def generate_domain_route1():
    if 'domainFile' not in request.files:
        return "No file part"

    domain_file = request.files['domainFile']

    if domain_file.filename == '':
        return "No selected file"

    if domain_file:
        excel_file_name = os.path.splitext(domain_file.filename)[0]
        excel_file_path = 'temp.xlsx'
        domain_file.save(excel_file_path)

        # Generate combined domain content
        combined_domain_content = generate_combined_content(excel_file_path)

        # Save the combined domain.yml content to a file
        combined_domain_filename = f"{excel_file_name}_domain.yml"
        with open(combined_domain_filename, "w") as domain_file:
            domain_file.write(combined_domain_content)

        return "Combined Domain File generated!"






# Define generate_domain_yml_from_excel_hindi2 and generate_domain_yml_from_excel_urdu2 functions similarly



def clean_intent_name(name):
    cleaned_name = re.sub(r'[^a-zA-Z0-9\s]', '', name)  # Remove non-alphanumeric characters
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name)  # Replace multiple spaces with a single space
    cleaned_name = cleaned_name.strip()  # Remove leading and trailing spaces
    cleaned_name = cleaned_name.replace(' ', '_')  # Replace spaces with underscores
    cleaned_name = re.sub(r'_+', '_', cleaned_name)  # Replace multiple underscores with a single underscore


    return cleaned_name

def clean_intent_name_english(name):
    cleaned_name = clean_intent_name(name)
    cleaned_name = cleaned_name + '_en'  # Add language code
    return cleaned_name

def clean_intent_name_hindi(name):
    cleaned_name = clean_intent_name(name)
    cleaned_name = cleaned_name + '_hi'
    return cleaned_name

def clean_intent_name_urdu(name):
    cleaned_name = clean_intent_name(name)
    cleaned_name = cleaned_name + '_ur'
    return cleaned_name

def generate_domain_yml_from_excel_english2(excel_file_path):
    df = pd.read_excel(excel_file_path)
    intents_responses = {}
    
    for index, row in df.iterrows():
        intent = row['Questions_In_English'].split('\n')[0]
        intent = clean_intent_name_english(intent)
        response_en = row['Answers_In_English']

        if intent not in intents_responses:
            intents_responses[intent] = []
        
        intents_responses[intent].append(response_en)

    return intents_responses

def generate_domain_yml_from_excel_hindi2(excel_file_path):
    df = pd.read_excel(excel_file_path)
    intents_responses = {}
    
    for index, row in df.iterrows():
        intent = row['Questions_In_English'].split('\n')[0]  # Change to 'Questions_In_Hindi'
        intent = clean_intent_name_hindi(intent)
        response_hi = row['Answers_In_Hindi']

        if intent not in intents_responses:
            intents_responses[intent] = []
        
        intents_responses[intent].append(response_hi)

    return intents_responses

def generate_domain_yml_from_excel_urdu2(excel_file_path):
    df = pd.read_excel(excel_file_path)
    intents_responses = {}
    
    for index, row in df.iterrows():
        intent = row['Questions_In_English'].split('\n')[0]  # Change to 'Questions_In_Urdu'
        intent = clean_intent_name_urdu(intent)
        response_ur = row['Answers_In_Urdu']

        if intent not in intents_responses:
            intents_responses[intent] = []
        
        intents_responses[intent].append(response_ur)

    return intents_responses


# Define generate_domain_yml_from_excel_hindi2 and generate_domain_yml_from_excel_urdu2 functions similarly

def generate_domain_yml2(intent_responses):
    combined_domain_content = "---\nversion: '3.1'\nintents:\n"
    for intent in intent_responses:
        combined_domain_content += f"  - {intent}\n"  # For English
        combined_domain_content += f"  - {intent}\n"  # For Hindi
        combined_domain_content += f"  - {intent}\n"  # For Urdu

    combined_domain_content += "\nresponses:\n"
    for intent, response_list in intent_responses.items():
        for lang_suffix in ["en", "hi", "ur"]:
            combined_domain_content += f"  utter_{intent}:\n"
            combined_domain_content += "    - text: |\n"
            for response in response_list:
                lines = response.split('\n')
                for line in lines:
                    combined_domain_content += f"        {line}\n"

    return combined_domain_content


def generate_combined_content2(excel_file_path):
        intent_responses_en = generate_domain_yml_from_excel_english2(excel_file_path)
        intent_responses_hi = generate_domain_yml_from_excel_hindi2(excel_file_path)
        intent_responses_ur = generate_domain_yml_from_excel_urdu2(excel_file_path)

        # Get the unique set of intent names
        all_intents = set(intent_responses_en.keys()) | set(intent_responses_hi.keys()) | set(intent_responses_ur.keys())

        combined_domain_content = "---\nversion: '3.1'\nintents:\n"
        for intent in all_intents:
            combined_domain_content += f"  - {intent}\n"

        combined_domain_content += "\nresponses:\n"
        for intent in all_intents:
            combined_domain_content += f"  utter_{intent}:\n"
            combined_domain_content += "    - text: |\n"
            for lang_suffix, responses_dict in [("en", intent_responses_en),
                                                ("hi", intent_responses_hi),
                                                ("ur", intent_responses_ur)]:
                response_list = responses_dict.get(intent, [])
                if isinstance(response_list, list):  # Check if response_list is a valid list
                    for response in response_list:
                        if isinstance(response, str):  # Check if response is a valid string
                            lines = response.split('\n')
                            for line in lines:
                                combined_domain_content += f"        {line}\n"

        return combined_domain_content
    # Update the generate_combined_content2 function as shown above

@app.route('/generate_domain2', methods=['POST'])
def generate_domain_route2():
        if 'domainFile' not in request.files:
            return "No file part"

        domain_file = request.files['domainFile']

        if domain_file.filename == '':
            return "No selected file"

        if domain_file:
            excel_file_name = os.path.splitext(domain_file.filename)[0]
            excel_file_path = 'temp.xlsx'
            domain_file.save(excel_file_path)

            # Generate combined domain content
            combined_domain_content = generate_combined_content2(excel_file_path)

            # Save the combined domain.yml content to a file
            combined_domain_filename = "domain.yml"
            with open(combined_domain_filename, "w") as domain_file:
                domain_file.write(combined_domain_content)

            return "Combined Domain File generated!"

@app.route('/train_chatbot', methods=['POST'])
def train_chatbot():
    try:
        # Run the Rasa train command
        subprocess.run(["rasa", "train"])
        return jsonify({"message": "Chatbot trained successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



ssh_host = '10.149.87.53'
ssh_port = 22
ssh_username = 'ubuntu'
ssh_password = 'server@123'
remote_directory = ''


@app.route('/generate_nlu3', methods=['POST'])
def generate_nlu_route3():
    if 'excelFile' not in request.files:
        return "No file part"

    excel_file = request.files['excelFile']

    if excel_file.filename == '':
        return "No selected file"

    if excel_file:
        excel_file_name = os.path.splitext(excel_file.filename)[0]
        excel_file_path = 'temp.xlsx'
        excel_file.save(excel_file_path)

        # Generate NLU content from the uploaded Excel file
        nlu_yml_content = generate_nlu_yml_from_excel(excel_file_path)

        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Create the 'nlu.yml' file inside the 'data' directory
        nlu_filename = os.path.join(data_dir, "nlu.yml")
        with open(nlu_filename, "w") as nlu_file:
            nlu_file.write(nlu_yml_content)

        return "NLU File generated!"
    else:
        return "Invalid file format. Only Excel files are allowed."



@app.route('/generate_domain3', methods=['POST'])
def generate_domain_route3():
    if 'excelFile' not in request.files:
        return "No file part"

    excel_file = request.files['excelFile']

    if excel_file.filename == '':
        return "No selected file"

    if excel_file:
        excel_file_name = os.path.splitext(excel_file.filename)[0]
        excel_file_path = 'temp.xlsx'
        excel_file.save(excel_file_path)

        # Generate combined domain content
        combined_domain_content = generate_combined_content2(excel_file_path)

        # Create the 'domain.yml' file in the current directory
        domain_filename = "domain.yml"
        with open(domain_filename, "w") as domain_file:
            domain_file.write(combined_domain_content)

        return combined_domain_content
    else:
        return "Invalid file format. Only Excel files are allowed."



def generate_stories_yml_from_domain_content(domain_content):
    stories_data = {"version": "3.1", "stories": []}

    domain_data = yaml.safe_load(domain_content)

    for intent in domain_data.get("intents", []):
        intent_name_parts = intent.strip().split('_')
        lang_code = intent_name_parts[-1]  # Extract language code
        intent_base = ' '.join(intent_name_parts[:-1])  # Join the intent base

        story = {
            "story": f"{intent_base} {lang_code}"
        }

        # Remove leading or trailing whitespace from intent_base and lang_code
        story["story"] = story["story"].strip()

        intent_name = "_".join(intent_name_parts)  # Reconstruct intent name
        action_name = f"utter_{intent_name}"

        steps = [
            {"intent": intent_name},
            {"action": action_name}
        ]
        story["steps"] = steps

        stories_data["stories"].append(story)

    return yaml.dump(stories_data, default_flow_style=False, sort_keys=False)


@app.route('/generate_stories3', methods=['POST'])
def generate_stories_route3():
    # Read the content of the 'domain.yml' file in the current directory
    domain_filename = "domain.yml"
    try:
        with open(domain_filename, "r") as domain_file:
            combined_domain_content = domain_file.read()
    except FileNotFoundError:
        return "Domain content not available. Please create the 'domain.yml' file in the current directory."

    # Generate stories YAML content from the combined domain content
    stories_yml_content = generate_stories_yml_from_domain_content(combined_domain_content)

    # Create the 'stories.yml' file in the 'data' directory
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    stories_filename = os.path.join(data_dir, "stories.yml")

    # Save the generated stories YAML content to a file (optional)
    with open(stories_filename, "w") as stories_file:
        stories_file.write(stories_yml_content)

    return stories_yml_content  # You can return the generated stories YAML content if needed

def add_nlu_yml_data_from_excel(excel_file_path, selected_department):
    df = pd.read_excel(excel_file_path, sheet_name='English')

    # Read the existing content of nlu.yml
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    nlu_filename = os.path.join(data_dir, "nlu.yml")
    
    try:
        with open(nlu_filename, "r") as nlu_file:
            existing_content = nlu_file.read()
    except FileNotFoundError:
        existing_content = ""

    appended_data = []  # Initialize a list to store appended data

    # Find the position where intents start
    intents_start = existing_content.find("intents:")

    # Combine the new intents with the existing content
    new_intents_content = ''

    for index, row in df.iterrows():
        intent_raw = row['Questions_In_English'].split('\n')[0]
        intent_name_en = clean_intent_name(intent_raw) + '_en'
        intent_name_hi = clean_intent_name(intent_raw) + '_hi'
        intent_name_ur = clean_intent_name(intent_raw) + '_ur'

        examples_en = df.iloc[index]['Questions_In_English']
        examples_hi = df.iloc[index]['Questions_In_Hindi']
        examples_ur = df.iloc[index]['Questions_In_Urdu']

        new_intents_content += f"- intent: {intent_name_en}\n"
        new_intents_content += "  examples: |\n"

        for line in examples_en.split('\n'):
            new_intents_content += f"    - {selected_department} {line}\n"
            appended_data.append(f"    - {selected_department} {line}")

        new_intents_content += f"- intent: {intent_name_hi}\n"
        new_intents_content += "  examples: |\n"

        for line in examples_hi.split('\n'):
            new_intents_content += f"    - {selected_department} {line}\n"
            appended_data.append(f"    - {selected_department} {line}")

        new_intents_content += f"- intent: {intent_name_ur}\n"
        new_intents_content += "  examples: |\n"

        for line in examples_ur.split('\n'):
            new_intents_content += f"    - {selected_department} {line}\n"
            appended_data.append(f"    - {selected_department} {line}")

    if intents_start != -1:
        # Insert new intents below the existing intents
        combined_nlu_content = existing_content[:intents_start] + new_intents_content + "\n" + existing_content[intents_start:]
    else:
        # If 'intents:' is not found, just append new content at the end
        combined_nlu_content = f"{existing_content}\n{new_intents_content}"

    # Write the combined NLU content back to the nlu.yml file
    with open(nlu_filename, "w") as nlu_file:
        nlu_file.write(combined_nlu_content)

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





# Modify the generate_domain_route4 route to append data to the existing 'domain.yml' file
@app.route('/generate_domain4', methods=['POST'])
def generate_domain_route4():
    if 'excelFile' not in request.files:
        return "No file part"

    excel_file = request.files['excelFile']

    if excel_file.filename == '':
        return "No selected file"

    if excel_file:
        excel_file_name = os.path.splitext(excel_file.filename)[0]
        excel_file_path = 'temp.xlsx'
        excel_file.save(excel_file_path)

        # Generate domain content and append it to the existing 'domain.yml' file
        append_domain_content_from_excel(excel_file_path, "domain.yml")

        return "Domain data added successfully!"
    else:
        return "Invalid file format. Only Excel files are allowed."

# Update the generate_combined_content4 function to generate domain content without resetting the variable
# Update the generate_combined_content4 function to generate domain content without resetting the variable
def generate_combined_content4(excel_file_path):
    intent_responses_en = generate_domain_yml_from_excel_english2(excel_file_path)
    intent_responses_hi = generate_domain_yml_from_excel_hindi2(excel_file_path)
    intent_responses_ur = generate_domain_yml_from_excel_urdu2(excel_file_path)

    # Get the unique set of intent names
    all_intents = set(intent_responses_en.keys()) | set(intent_responses_hi.keys()) | set(intent_responses_ur.keys())

    # Create a list to store intents separately
    intents_content = []

    for intent in all_intents:
        intents_content.append(f"  - {intent}")

    # Create a list to store responses separately
    responses_content = []

    for intent in all_intents:
        responses_content.append(f"  utter_{intent}:")
        responses_content.append("    - text: |")
        for lang_suffix, responses_dict in [("en", intent_responses_en),
                                            ("hi", intent_responses_hi),
                                            ("ur", intent_responses_ur)]:
            response_list = responses_dict.get(intent, [])
            if isinstance(response_list, list):  # Check if response_list is a valid list
                for response in response_list:
                    if isinstance(response, str):  # Check if response is a valid string
                        lines = response.split('\n')
                        for line in lines:
                            responses_content.append(f"        {line}")

    return intents_content, responses_content

# Create a function to append domain content from Excel to an existing domain file
def append_domain_content_from_excel(excel_file_path, domain_file_path):
    intents_content, responses_content = generate_combined_content4(excel_file_path)

    # Read the existing domain content
    existing_domain_content = ""
    try:
        with open(domain_file_path, "r") as domain_file:
            existing_domain_content = domain_file.read()
    except FileNotFoundError:
        pass

    # Find the position where responses start
    responses_start = existing_domain_content.find("responses:")

    # Combine the new intents and responses with the existing content
    new_intents_content = '\n'.join(intents_content)
    new_responses_content = '\n'.join(responses_content)

    if responses_start != -1:
        # Insert new intents below the existing intents
        combined_domain_content = existing_domain_content[:responses_start] + new_intents_content + "\n" + existing_domain_content[responses_start:]
        # Insert new responses below the existing responses
        combined_domain_content = combined_domain_content.replace("responses:", f"responses:\n{new_responses_content}", 1)
    else:
        # If 'responses:' is not found, just append new content at the end
        combined_domain_content = f"{existing_domain_content}\n{new_intents_content}\nresponses:\n{new_responses_content}"

    # Write the combined domain content back to the domain file
    with open(domain_file_path, "w") as domain_file:
        domain_file.write(combined_domain_content)


# Keep your existing generate_combined_content2 and other functions as they are

# You can now use the '/generate_domain4' route to append domain data to the existing 'domain.yml' file.

def generate_stories_yml_from_domain_content4(domain_content, existing_stories_content):
    domain_data = yaml.safe_load(domain_content)
    
    # Load existing stories data
    stories_data = yaml.safe_load(existing_stories_content)

    for intent in domain_data.get("intents", []):
        intent_name_parts = intent.strip().split('_')
        lang_code = intent_name_parts[-1]  # Extract language code
        intent_base = ' '.join(intent_name_parts[:-1])  # Join the intent base

        story = {
            "story": f"{intent_base} {lang_code}"
        }

        # Remove leading or trailing whitespace from intent_base and lang_code
        story["story"] = story["story"].strip()

        intent_name = "_".join(intent_name_parts)  # Reconstruct intent name
        action_name = f"utter_{intent_name}"

        steps = [
            {"intent": intent_name},
            {"action": action_name}
        ]
        story["steps"] = steps

        stories_data["stories"].append(story)

    return yaml.dump(stories_data, default_flow_style=False, sort_keys=False)

# Update the generate_stories_route3 route
@app.route('/generate_stories4', methods=['POST'])
def generate_stories_route4():
    # Read the content of the 'domain.yml' and 'stories.yml' files in the current directory
    domain_filename = "domain.yml"
    stories_filename = os.path.join("data", "stories.yml")

    try:
        with open(domain_filename, "r") as domain_file:
            combined_domain_content = domain_file.read()
    except FileNotFoundError:
        return "Domain content not available. Please create the 'domain.yml' file in the current directory."

    try:
        with open(stories_filename, "r") as stories_file:
            existing_stories_content = stories_file.read()
    except FileNotFoundError:
        existing_stories_content = ""

    # Generate stories YAML content and append it to the existing stories file
    new_stories_content = generate_stories_yml_from_domain_content4(combined_domain_content, existing_stories_content)

    # Write the combined stories content back to the stories file
    with open(stories_filename, "w") as stories_file:
        stories_file.write(new_stories_content)

    return new_stories_content  # You can return the updated stories YAML content if needed


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=59410)
