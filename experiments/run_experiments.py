import json
import os
import os.path
import time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

CODE_TAG = "<CODE>"
ERRORS_TAG = "<ERRORS>"

load_dotenv()

def get_single_error_type_as_str(data, error_type, error_msg_prefix=""):
    if not error_type in data["errors"]:
        return ""

    errors = data["errors"][error_type]

    error_str = error_msg_prefix + ": "
    
    for i in range(len(errors)):
        error_str += f"\'{errors[i]}\'"

        if i == len(errors) - 1:
            error_str += "."
        else:
            error_str += ", "
     
    return error_str

def get_all_errors_as_str(data):
    errors = [
        get_single_error_type_as_str(data, "unknown_type_name", "    - unknown type name"),
        get_single_error_type_as_str(data, "use_undeclared_identifier", "    - use of undeclared identifier"),
        get_single_error_type_as_str(data, "call_undeclared_function", "    - call to undeclared function"),
        get_single_error_type_as_str(data, "call_undeclared_library_function", "    - call to undeclared library function")]

    errors = filter(lambda x: x != "", errors)

    return "\n".join(errors)

def build_prompt(prompt_template, snippet, errors):
    code_start_index = prompt_template.find(CODE_TAG)
    code_end_index = code_start_index + len(CODE_TAG)
    prompt = prompt_template[0:code_start_index] + snippet + prompt_template[code_end_index:]

    errors_start_index = prompt.find(ERRORS_TAG)
    prompt = prompt[:errors_start_index] + errors

    return prompt

def get_last_path_component(path):
    components = os.path.normpath(path).split(os.path.sep)
    
    # Get the last component
    last_component = components[-1]
    
    return last_component

def has_extension(file_path, target_extension):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == target_extension.lower()

def get_projects(root_path="."):
    projects = {}

    for project_path, _, filenames in os.walk(root_path):
        if "project.json" in filenames:
            project_dirname = get_last_path_component(project_path)
            
            project_metadata_path = os.path.join(project_path, "project.json")

            try:
                with open(project_metadata_path, "r") as project_metadata_file:
                    project_metadata = json.load(project_metadata_file)
                    project_metadata_file.close()
            except Exception:
                print(f"Couldn't open project '{project_dirname}' metadata")
                return None

            experiments = {}

            for filename in filenames:
                if not has_extension(filename, ".json") or filename == "project.json":
                    continue

                experiment_metadata_path = os.path.join(project_path, filename)

                experiment_name = filename.split(".json")[0]

                try:
                    with open(experiment_metadata_path) as experiment_metadata_file:
                        experiment_metadata = json.load(experiment_metadata_file)
                        experiments[experiment_name] = experiment_metadata
                        experiment_metadata_file.close()
                except Exception:
                    print(f"Couldn't open experiment '{experiment_name}' metadata from project '{project_dirname}'")
                    return None

            projects[project_dirname] = {
                "metadata": project_metadata,
                "experiments": experiments
            }

    return projects

def select_metadata_path():
    metadata_path = input("Enter experiment metadata path (press Enter for default path \"./metadata\"): ")

    metadata_path = "./metadata" if metadata_path == "" else metadata_path

    if os.path.exists(metadata_path):
        if os.path.isfile(metadata_path):
            print("Provided metadata path is a file, not a directory")
            return None
    else:
        print("Provided metadata path doesn't exist. Aborting..")
        return None
    
    return metadata_path

def get_files_from_path(directory_path):
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

def select_prompt_template():
    prompts_path = input("Enter prompts path (press Enter for default path \"./prompts\"): ")

    prompts_path = "./prompts" if prompts_path == "" else prompts_path

    if os.path.exists(prompts_path):
        if os.path.isfile(prompts_path):
            print("Provided prompt path is a file, not a directory")
            return None, None
    else:
        print("Provided prompt path doesn't exist. Aborting..")
        return None, None
    
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
    project_dirnames = projects.keys()
    project_dirnames_str = ', '.join(project_dirnames)

    while True:
        dirname = input(f"Select project from the list ({project_dirnames_str}): ")

        if not dirname in project_dirnames:
            print(f"Invalid project '{dirname}'. Try again")
        else:
            break
    
    return projects[dirname], dirname

def select_experiment(project):
    experiment_filenames = project["experiments"].keys()
    experiment_filenames_str = ', '.join(experiment_filenames)

    while True:
        filename = input(f"Select experiment from the list ({experiment_filenames_str}): ")

        if not filename in experiment_filenames:
            print(f"Invalid filename '{filename}'. Try again")
        else:
            break

    return project["experiments"][filename], filename

def test_experiment(projects, prompt_template, prompt_template_filename, raw_results_path):
    project, dirname = select_project(projects)

    project_name = project["metadata"]["project"]
    project_org = project["metadata"]["org"]

    experiment, filename = select_experiment(project)

    experiment_name = experiment["name"]
    experiment_snippet = experiment["snippet"]
    experiment_function_name = experiment["function_name"]

    print(f"Testing experiment '{experiment_name}': snippet '{experiment_snippet}', function name '{experiment_function_name}' from project '{project_name}' and organization '{project_org}'")
        
    with open(f"./snippets/{dirname}/{experiment_snippet}") as file:
        snippet = file.read()
    
    errors = get_all_errors_as_str(experiment)

    prompt = build_prompt(prompt_template, snippet, errors)

    chat_completion, gen_time = prompt_llm(prompt)

    save_experiment_result(chat_completion, gen_time, raw_results_path, experiment_name, project_name, project_org, prompt_template_filename)

    #print(prompt)

def test_project(projects, prompt_template, prompt_template_filename, raw_results_path):
    project, dirname = select_project(projects)

    project_name = project["metadata"]["project"]
    project_org = project["metadata"]["org"]
    print(f"Testing project '{project_name}' from organization '{project_org}'")

    for experiment in project["experiments"].values():
        experiment_name = experiment["name"]
        experiment_snippet = experiment["snippet"]
        experiment_function_name = experiment["function_name"]

        print(f"Experiment '{experiment_name}': snippet '{experiment_snippet}', function name '{experiment_function_name}'")
        
        with open(f"./snippets/{dirname}/{experiment_snippet}") as file:
            snippet = file.read()
        
        errors = get_all_errors_as_str(experiment)

        prompt = build_prompt(prompt_template, snippet, errors)

        chat_completion, gen_time = prompt_llm(prompt)

        save_experiment_result(chat_completion, gen_time, raw_results_path, experiment_name, project_name, project_org, prompt_template_filename)

        #print(prompt)

def test_all_projects(projects, prompt_template, prompt_template_filename, raw_results_path):
    for dirname, project in projects.items():
        #print(json.dumps(project, indent=2))
        project_name = project["metadata"]["project"]
        project_org = project["metadata"]["org"]
        print(f"Testing project '{project_name}' from organization '{project_org}'")

        for experiment in project["experiments"].values():
            experiment_name = experiment["name"]
            experiment_snippet = experiment["snippet"]
            experiment_function_name = experiment["function_name"]

            print(f"Experiment '{experiment_name}': snippet '{experiment_snippet}', function name '{experiment_function_name}'")
            
            with open(f"./snippets/{dirname}/{experiment_snippet}") as file:
                snippet = file.read()
            
            errors = get_all_errors_as_str(experiment)

            prompt = build_prompt(prompt_template, snippet, errors)

            chat_completion, gen_time = prompt_llm(prompt)

            save_experiment_result(chat_completion, gen_time, raw_results_path, experiment_name, project_name, project_org, prompt_template_filename)
            #print(prompt)

def prompt_llm(prompt):
    client = OpenAI()
    '''chat_completion = {
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
    }'''

    input()
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
    #print(prompt)
    #print(chat_completion)

    return chat_completion, gen_time

def select_raw_results_path():
    raw_results_path = input("Enter experiment raw results path (press Enter for default path \"./raw_results\"): ")

    raw_results_path = "./raw_results" if raw_results_path == "" else raw_results_path

    if os.path.exists(raw_results_path):
        if os.path.isfile(raw_results_path):
            print("Provided raw results path is a file, not a directory")
            return None
    else:
        print("Provided raw results path doesn't exist. Creating one..")
        os.mkdir(raw_results_path, mode=777)
    
    return raw_results_path
    
def save_experiment_result(chat_completion, gen_time, raw_results_path, experiment_name,
                           project_name, org_name, prompt_name):

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
    '''

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

def main():
    metadata_path = select_metadata_path() 
    if metadata_path == None:
        return
    
    raw_results_path = select_raw_results_path()
    if raw_results_path == None:
        return

    projects = get_projects(metadata_path)
    if projects == None:
        return
    
    while True:
        prompt_template, prompt_template_filename = select_prompt_template()

        if prompt_template == None:
            return None
        
        print("Select testing mode:\n   [0] Specific experiment from a project\n   [1] All experiments from a project\n   [2] All projects")

        while True:
            testing_mode = input(">> ")
            if not testing_mode in ["0", "1", "2"]:
                print("Invalid option. Try again:")
            else:
                break

        if testing_mode == "0":
            test_experiment(projects, prompt_template, prompt_template_filename, raw_results_path)
        elif testing_mode == "1":
            test_project(projects, prompt_template, prompt_template_filename, raw_results_path)
        elif testing_mode == "2":
            test_all_projects(projects, prompt_template, prompt_template_filename, raw_results_path)

        while True:
            continue_exec = input("Continue experiments (y/N): ")
            if not continue_exec.lower() in ["y", "yes", "n", "no"]:
                continue_exec = print("Incorrect option. Try again:")
            else:
                break
            
        if continue_exec.lower() in ["n", "no"]:
            break

if __name__ == "__main__":
    main()