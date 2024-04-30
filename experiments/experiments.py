import os
import json
import subprocess
import re
import time
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

from error import extract_errors, parse_errors, get_errors_as_str
from utils import has_extension, get_last_path_component, get_files_from_path, remove_first_path_component
from declaration import DeclParser

CODE_TAG = "<CODE>"
ERRORS_TAG = "<ERRORS>"

PROJECT_METADATA = "project.json"
JSON_EXTENSION = ".json"

load_dotenv()

class Paths:
    def __init__(self, experiments_path, metadata_path, snippets_path, prompts_path, raw_results_path):
        self.experiments_path = experiments_path
        self.metadata_path = metadata_path
        self.snippets_path = snippets_path
        self.prompts_path = prompts_path
        self.raw_results_path = raw_results_path

def get_projects(root_path="."):
    projects = {}

    for project_path, _, filenames in os.walk(root_path):
        if PROJECT_METADATA not in filenames:
            continue

        print(f"Found project in {project_path}")
        project_path_id = remove_first_path_component(project_path)
        
        project_metadata_path = os.path.join(project_path, PROJECT_METADATA)

        try:
            with open(project_metadata_path, "r") as project_metadata_file:
                project_metadata = json.load(project_metadata_file)
                project_metadata_file.close()
        except Exception:
            print(f"Couldn't open project '{project_path_id}' metadata")
            return None

        experiments = {}

        for filename in filenames:
            if not has_extension(filename, JSON_EXTENSION) or filename == PROJECT_METADATA:
                continue

            experiment_metadata_path = os.path.join(project_path, filename)

            experiment_name = filename.split(JSON_EXTENSION)[0]

            try:
                with open(experiment_metadata_path) as experiment_metadata_file:
                    experiment_metadata = json.load(experiment_metadata_file)
                    experiments[experiment_name] = experiment_metadata
                    experiment_metadata_file.close()
            except Exception:
                print(f"Couldn't open experiment '{experiment_name}' metadata from project '{project_dirname}'")
                return None

        projects[project_path_id] = {
            "metadata": project_metadata,
            "experiments": experiments
        }

    return projects

def get_directory_path(experiments_path, dirname):
    directory_path = os.path.join(experiments_path, dirname)

    if os.path.exists(directory_path):
        if os.path.isfile(directory_path):
            print(f"Found a {dirname} path but it is a file, not a directory")
            return None

        print(f"Found {dirname} directory")
    else:
        print(f"{dirname} directory does not exist. Creating one")
        os.mkdir(directory_path)
    
    return directory_path

# Selections
def select_experiments_path():
    experiments_path = input("Enter experiments path (press enter for default path \"./\"): ")

    experiments_path = "./" if experiments_path == "" else experiments_path

    if not os.path.exists(experiments_path):
        print("Provided experiments path does not exist")
        return None

    return experiments_path

def select_prompt_template(prompts_path):    
    prompts = get_files_from_path(prompts_path)

    prompt_str = ','.join(prompts)

    while True:
        prompt_template_filename = input(f"Select prompt template from the list ({prompt_str}): ")

        if not prompt_template_filename in prompts:
            print(f"Invalid prompt template '{prompt_template_filename}'. Try again")
        else:
            break
    
    prompt_template_path = os.path.join(prompts_path, prompt_template_filename)

    with open(prompt_template_path, 'r') as file:
        prompt_template = file.read()

    return prompt_template, prompt_template_filename

def select_project(projects):
    project_path_ids = projects.keys()
    project_path_ids_str = ', '.join(project_path_ids)

    while True:
        path_id = input(f"Select project from the list ({project_path_ids_str}): ")

        if not path_id in project_path_ids:
            print(f"Invalid project '{path_id}'. Try again")
        else:
            break
    
    return projects[path_id]

def select_experiment(project):
    experiment_filenames = project["experiments"].keys()
    experiment_filenames_str = ', '.join(experiment_filenames)

    while True:
        filename = input(f"Select experiment from the list ({experiment_filenames_str}): ")

        if not filename in experiment_filenames:
            print(f"Invalid filename '{filename}'. Try again")
        else:
            break

    return project["experiments"][filename]

# Handlers
def create_project_metadata(paths: Paths):
    project_path = input("Enter experiment project path (relative to metadata path): ")

    project_path = os.path.join(paths.metadata_path, project_path)

    project_metadata_path = os.path.join(project_path, "project.json")

    project_metadata = {
        "org": input("Enter project organization: "),
        "project": input("Enter project name: "),
        "repository": input("Enter project repository: "),
        "license": input("Enter project license: "),
        "snippets": input("Enter project snippets path (relative to snippets directory): "),
    }

    if not os.path.exists(project_path):
        os.mkdir(project_path)

    if os.path.exists(project_metadata_path) and os.path.isfile(project_metadata_path):
        while True:
            print("Project metadata already exists. Create new project metadata? (y/n)")
            option = input(">> ")

            if not option in ["y", "n"]:
                print("Invalid option. Try again:")
            else:
                break
        
        if option == "n":
            return ""
        
    try:
        with open(project_metadata_path, 'w') as project_metadata_file:
            project_metadata_file.write(json.dumps(project_metadata, indent=4))
            project_metadata_file.close()
    except Exception:
        print("Couldn't create project metadata file.")
        return None

def create_experiment_metadata(paths: Paths):
    project_path = input("Enter experiment project path (relative to metadata path): ")

    project_path = os.path.join(paths.metadata_path, project_path)

    project_metadata_path = os.path.join(project_path, "project.json")

    if not os.path.exists(project_path):
        print("Project path does not exist. Aborting..")
        return None
    
    if not (os.path.exists(project_metadata_path) and os.path.isfile(project_metadata_path)):
        print("Project metadata does not exist. Aborting..")
        return None
    
    try:
        with open(project_metadata_path, "r") as metadata_file:
            project_metadata = json.load(metadata_file)
            metadata_file.close()
    except Exception:
        print("Couldn't open project metadata")
        return None
    
    project = project_metadata["project"]
    org = project_metadata["org"]
    print(f"Using project {project} from organization {org}")

    experiment = {}

    experiment["name"] = input("Enter the experiment name (press enter for same name as the snippet): ")
    experiment["snippet"] = input("Enter the snippet name: ")
    experiment["name"] = experiment["snippet"] if experiment["name"] == "" else experiment["name"]
    experiment["commit_hash"] = input("Enter the commit hash: ")
    experiment["function_name"] = input("Enter the function name: ")
    experiment["function_path"] = input("Enter the function path: ")

    while True:
        experiment["language"] = input("Enter the language (c/cpp): ")

        if experiment["language"] in ["c", "cpp"]:
            break

        print("Invalid language. Please enter a valid language.")

    snippet_name = experiment["snippet"]
    project_snippets_path = project_metadata["snippets"]
    #declarations_filepath = input("Enter the path to the LLVM declarations file: ")

    declarations_filepath = "./declarations.txt"

    errors_str = extract_errors(snippet_name, os.path.join(paths.snippets_path, project_snippets_path))
    #print(errors_str)
    
    if not errors_str:
        return
    
    experiment["errors"] = parse_errors(errors_str)

    try:
        with open(declarations_filepath, 'r') as file:
            declarations_file = file.read()
            #print(declarations_file)
            tree = DeclParser.parse(declarations_file)
            experiment["declarations"] = DeclParser.get_declarations_as_json(tree)
            file.close()
    except FileNotFoundError:
        print("Declarations file does not exist.")
        return

    experiment_name = experiment["name"]
    experiment_metadata_path = os.path.join(project_path, f"{experiment_name}.json")

    try:
        with open(experiment_metadata_path, 'w') as experiment_file:
            experiment_file.write(json.dumps(experiment, indent=4))
            experiment_file.close()
    except Exception:
        print("Couldn't create experiment file")
        return

    print("Experiment created correctly")
    #print(json.dumps(experiment, indent=4))

def run_experiments(paths: Paths):
    projects = get_projects(paths.metadata_path)
    if projects == None:
        return

    while True:
        prompt_template, prompt_template_filename = select_prompt_template(paths.prompts_path)

        if prompt_template == None:
            return
        
        print("Select testing mode:\n   [0] Specific experiment from a project\n   [1] All experiments from a project\n   [2] All projects")

        while True:
            testing_mode = input(">> ")
            if not testing_mode in ["0", "1", "2"]:
                print("Invalid option. Try again:")
            else:
                break

        if testing_mode == "0":
            test_experiment(projects, prompt_template, prompt_template_filename, paths.snippets_path, paths.raw_results_path)
        elif testing_mode == "1":
            test_project(projects, prompt_template, prompt_template_filename, paths.snippets_path, paths.raw_results_path)
        elif testing_mode == "2":
            test_all_projects(projects, prompt_template, prompt_template_filename, paths.snippets_path, paths.raw_results_path)

        while True:
            continue_exec = input("Continue experiments (y/N): ")
            if not continue_exec.lower() in ["y", "yes", "n", "no"]:
                continue_exec = print("Incorrect option. Try again:")
            else:
                break
            
        if continue_exec.lower() in ["n", "no"]:
            break

def analyse_experiments(paths: Paths):
    print("Analysing experiments..")

# LLM
def build_prompt(prompt_template, snippet, errors):
    code_start_index = prompt_template.find(CODE_TAG)
    code_end_index = code_start_index + len(CODE_TAG)
    prompt = prompt_template[0:code_start_index] + snippet + prompt_template[code_end_index:]

    errors_start_index = prompt.find(ERRORS_TAG)
    prompt = prompt[:errors_start_index] + errors

    return prompt

def prompt_llm(prompt):
    #client = OpenAI()
    chat_completion = {
        "created": 121214148798,
        "model": "3eheheh",
        "usage": {
            "prompt_tokens": 21,
            "completion_tokens": 2,
            "total_tokens": 23
        },
        "choices": [
            {
                "message": {
                    "content": "hi"
                }
            }
        ]
    }

    #input()
    '''
    start_time = time.time()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4"
    )

    gen_time = time.time() - start_time
    print(f"LLM answered in {gen_time}")
    '''
    gen_time = 2
    print(prompt)
    print(chat_completion)

    return chat_completion, gen_time

def save_experiment_result(chat_completion, gen_time, raw_results_path, experiment_name,
                           project_name, org_name, prompt_name):

    '''
    results = {
        "experiment": experiment_name,
        "project": project_name,
        "org": org_name,
        "created_unix": chat_completion.created,
        "created_iso": datetime.fromtimestamp(chat_completion.created).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prompt": prompt_name,
        "model": chat_completion.model,
        "prompt_tokens": chat_completion.usage.prompt_tokens,
        "answer_tokens": chat_completion.usage.completion_tokens,
        "total_tokens": chat_completion.usage.total_tokens,
        "prompt_gen_time": gen_time,
        "llm_answer": chat_completion.choices[0].message.content
    }
    '''
      
    results = {
        "experiment": experiment_name,
        "project": project_name,
        "org": org_name,
        "created_unix": chat_completion["created"],
        "created_iso": datetime.fromtimestamp(chat_completion["created"]).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prompt": prompt_name,
        "model": chat_completion["model"],
        "prompt_tokens": chat_completion["usage"]["prompt_tokens"],
        "answer_tokens": chat_completion["usage"]["completion_tokens"],
        "total_tokens": chat_completion["usage"]["total_tokens"],
        "llm_answer": chat_completion["choices"][0]["message"]["content"]
    }
    

    created_unix = results["created_unix"]
    experiment_results_path = os.path.join(raw_results_path,
                f"{experiment_name}_{project_name}_{org_name}_{created_unix}.json")

    try:
        with open(experiment_results_path, 'w') as results_file:
            results_file.write(json.dumps(results, indent=4))
            results_file.close()
    except Exception:
        print("Couldn't create results file")
        return

    print("Experiment results created correctly")

#Tests
def test_experiment(projects, prompt_template, prompt_template_filename, snippets_path, raw_results_path):
    project = select_project(projects)

    project_name = project["metadata"]["project"]
    project_org = project["metadata"]["org"]
    project_snippets_path = project["metadata"]["snippets"]

    experiment = select_experiment(project)

    experiment_name = experiment["name"]
    experiment_snippet = experiment["snippet"]
    experiment_function_name = experiment["function_name"]

    print(f"Testing experiment '{experiment_name}': snippet '{experiment_snippet}', function name '{experiment_function_name}' from project '{project_name}' and organization '{project_org}'")
        
    with open(os.path.join(snippets_path, project_snippets_path, experiment_snippet)) as file:
        snippet = file.read()
    
    errors = get_errors_as_str(experiment)

    prompt = build_prompt(prompt_template, snippet, errors)

    chat_completion, gen_time = prompt_llm(prompt)

    save_experiment_result(chat_completion, gen_time, raw_results_path, experiment_name, project_name, project_org, prompt_template_filename)

    #print(prompt)

def test_project(projects, prompt_template, prompt_template_filename, snippets_path, raw_results_path):
    project = select_project(projects)

    project_name = project["metadata"]["project"]
    project_org = project["metadata"]["org"]
    project_snippets_path = project["metadata"]["snippets"]

    print(f"Testing project '{project_name}' from organization '{project_org}'")

    for experiment in project["experiments"].values():
        experiment_name = experiment["name"]
        experiment_snippet = experiment["snippet"]
        experiment_function_name = experiment["function_name"]

        print(f"Experiment '{experiment_name}': snippet '{experiment_snippet}', function name '{experiment_function_name}'")
        
        with open(os.path.join(snippets_path, project_snippets_path, experiment_snippet)) as file:
            snippet = file.read()
        
        errors = get_errors_as_str(experiment)

        prompt = build_prompt(prompt_template, snippet, errors)

        chat_completion, gen_time = prompt_llm(prompt)

        save_experiment_result(chat_completion, gen_time, raw_results_path, experiment_name, project_name, project_org, prompt_template_filename)

        #print(prompt)

def test_all_projects(projects, prompt_template, prompt_template_filename, snippets_path, raw_results_path):
    for dirname, project in projects.items():
        #print(json.dumps(project, indent=2))
        project_name = project["metadata"]["project"]
        project_org = project["metadata"]["org"]
        project_snippets_path = project["metadata"]["snippets"]

        print(f"Testing project '{project_name}' from organization '{project_org}'")

        for experiment in project["experiments"].values():
            experiment_name = experiment["name"]
            experiment_snippet = experiment["snippet"]
            experiment_function_name = experiment["function_name"]

            print(f"Experiment '{experiment_name}': snippet '{experiment_snippet}', function name '{experiment_function_name}'")
            
            with open(os.path.join(snippets_path, project_snippets_path, experiment_snippet)) as file:
                snippet = file.read()
            
            errors = get_errors_as_str(experiment)

            prompt = build_prompt(prompt_template, snippet, errors)

            chat_completion, gen_time = prompt_llm(prompt)

            save_experiment_result(chat_completion, gen_time, raw_results_path, experiment_name, project_name, project_org, prompt_template_filename)
            #print(prompt)

def main():
    experiments_path = select_experiments_path()

    if experiments_path is None:
        return

    print(f"Selected experiments path: {experiments_path}")

    metadata_path = get_directory_path(experiments_path, "metadata")

    if metadata_path is None: return

    snippets_path = get_directory_path(experiments_path, "snippets")

    if snippets_path is None: return

    prompts_path = get_directory_path(experiments_path, "prompts")

    if prompts_path is None: return

    raw_results_path = get_directory_path(experiments_path, "raw_results")

    if raw_results_path is None: return

    paths = Paths(experiments_path, metadata_path, snippets_path, prompts_path, raw_results_path)

    while True:
        print(
            """Select option:
    [0] Create new project metadata
    [1] Create new code snippet metadata
    [2] Run experiments
    [3] Analyse experiments
    [4] Exit
            """
        )       
        #print("Select option:\n   [1] Create new code snippet metadata\n   [2] Run experiments\n   [3] Analyse experiments\n   [4] Exit\n")

        while True:
            option = input(">> ")
            if not option in ["0", "1", "2", "3", "4"]:
                print("Invalid option. Try again:")
            else:
                break

        if option == "0":
            create_project_metadata(paths)
        elif option == "1":
            create_experiment_metadata(paths)
        elif option == "2":
            run_experiments(paths)
        elif option == "3":
            analyse_experiments(paths)
        elif option == "4":
            break

if __name__ == "__main__":
    main()