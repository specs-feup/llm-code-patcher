import os
import json
from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv

from error import extract_errors, parse_errors, get_errors_as_str
from utils import has_extension, get_last_path_component, get_files_from_path, get_directories_from_path, remove_first_path_component
from declaration import DeclParser
from evaluation import evaluate_experiment_result
from logger import logger
from llm import build_prompt, prompt_llm

PROJECT_METADATA = "project.json"
JSON_EXTENSION = ".json"

class Workdir:
    def __init__(self, workdir, experiments_path, prompts_path, raw_results_path):
        self.workdir = workdir
        self.experiments_path = experiments_path
        self.prompts_path = prompts_path
        self.raw_results_path = raw_results_path

load_dotenv()


def get_projects(experiments_path):
    projects = {}

    dirs = get_directories_from_path(experiments_path)

    for project_dirname in dirs:
        project_path = os.path.join(experiments_path, project_dirname)

        project_metadata_path = os.path.join(project_path, PROJECT_METADATA)

        if not os.path.exists(project_metadata_path):
            continue
        
        try:
            with open(project_metadata_path, "r") as project_metadata_file:
                project_metadata = json.load(project_metadata_file)
                project_metadata_file.close()
        except Exception:
            logger.error(f"Couldn't open project '{project_dirname}' metadata")
            return None

        # TODO validate project metadata
        project_name = project_metadata["project"]
        org_name = project_metadata["org"]

        logger.info(f"Found project {project_name} from organization {org_name}")

        experiments = {}

        project_experiments_path = os.path.join(project_path, "metadata")

        experiments_filenames = get_files_from_path(project_experiments_path)

        for filename in experiments_filenames:
            if not has_extension(filename, JSON_EXTENSION) or filename == PROJECT_METADATA:
                continue
            
            logger.debug(f"Found experiment '{filename}'")

            experiment_metadata_path = os.path.join(project_experiments_path, filename)

            experiment_name = filename.split(JSON_EXTENSION)[0]

            try:
                with open(experiment_metadata_path) as experiment_metadata_file:
                    experiment_metadata = json.load(experiment_metadata_file)
                    experiments[experiment_name] = experiment_metadata
                    experiment_metadata_file.close()
            except Exception:
                logger.error(f"Couldn't open experiment '{experiment_name}' metadata from project '{project_dirname}'")
                return None
            
        projects[project_dirname] = {
            "metadata": project_metadata,
            "experiments": experiments
        }
    
    return projects

def get_directory_path(workdir, dirname):
    directory_path = os.path.join(workdir, dirname)

    if os.path.exists(directory_path):
        if os.path.isfile(directory_path):
            logger.error(f"Found a '{dirname}' path but it is a file, not a directory. Aborting..")
            return None

        logger.info(f"Found {dirname} directory")
    else:
        logger.info(f"'{dirname}' directory does not exist. Creating one")
        os.mkdir(directory_path)
    
    return directory_path

def get_project_id(project_name, org_name):
    return f"{project_name.lower()}_{org_name.lower()}"

# Selections
def select_experiment_workdir():
    workdir = input("Enter experiment working directory (press enter for default path \"./\"): ")

    workdir = "./" if workdir == "" else workdir

    if not os.path.exists(workdir):
        logger.error("Provided experiments path does not exist")
        return None

    logger.info(f"Selected experiment working directory: {workdir}")


    experiments_path = get_directory_path(workdir, "experiments")

    if experiments_path is None: return None

    prompts_path = get_directory_path(workdir, "prompts")

    if prompts_path is None: return None

    raw_results_path = get_directory_path(workdir, "raw_results")

    if raw_results_path is None: return None

    return Workdir(workdir, experiments_path, prompts_path, raw_results_path)

def select_project(projects):
    project_ids = projects.keys()
    project_ids_str = ', '.join(project_ids)

    while True:
        project_id = input(f"Select project from the list ({project_ids_str}): ")

        if not project_id in project_ids:
            print(f"Invalid project id '{project_id}'. Try again")
        else:
            break
    
    return project_id, projects[project_id]

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

# Handlers
def create_project_metadata(workdir: Workdir):
    project_metadata = {
        "org": input("Enter project organization: "),
        "project": input("Enter project name: "),
        "repository": input("Enter project repository: "),
        "license": input("Enter project license: "),
    }

    project_id = get_project_id(project_metadata["project"], project_metadata["org"])

    project_path = os.path.join(workdir.experiments_path, project_id)

    project_metadata_path = os.path.join(project_path, "project.json")

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
            logger.info("Aborting creation..")
            return ""
        
    try:
        with open(project_metadata_path, 'w') as project_metadata_file:
            project_metadata_file.write(json.dumps(project_metadata, indent=4))
            project_metadata_file.close()
    except Exception:
        logger.error("Couldn't create project metadata file.")
        return None
    
    logger.info("Project metadata created correctly")

def create_experiment_metadata(workdir: Workdir):
    # TODO select project from list
    org = input("Enter project organization: ")
    
    project = input("Enter project name: ")

    project_id = get_project_id(project, org)

    project_path = os.path.join(workdir.experiments_path, project_id)

    project_metadata_path = os.path.join(project_path, "project.json")

    logger.debug(project_metadata_path)

    if not os.path.exists(project_path):
        logger.error("Project path does not exist. Aborting..")
        return None
    
    if not (os.path.exists(project_metadata_path) and os.path.isfile(project_metadata_path)):
        logger.error("Project metadata does not exist. Aborting..")
        return None
    
    try:
        with open(project_metadata_path, "r") as metadata_file:
            project_metadata = json.load(metadata_file)
            metadata_file.close()
    except Exception:
        logger.error("Couldn't open project metadata")
        return None

    logger.info(f"Using project {project} from organization {org}")

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

        logger.error("Invalid language. Please enter a valid language.")

    snippet_name = experiment["snippet"]
    project_snippets_path = os.path.join(project_path, "snippets")

    #declarations_filepath = input("Enter the path to the LLVM declarations file: ")

    declarations_filepath = "./declarations.txt"

    errors_str = extract_errors(snippet_name, project_snippets_path)
    #logger.debug(errors_str)
    
    if not errors_str:
        return
    
    experiment["errors"] = parse_errors(errors_str)

    '''
    try:
        with open(declarations_filepath, 'r') as file:
            declarations_file = file.read()
            #logger.debug(declarations_file)
            tree, _, _ = DeclParser.parse(declarations_file)
            experiment["declarations"] = DeclParser.get_declarations_as_obj(tree)
            file.close()
    except FileNotFoundError:
        logger.error("Declarations file does not exist.")
        return
    '''

    experiment_name = experiment["name"]
    experiment_metadata_path = os.path.join(project_path, "metadata", f"{experiment_name}.json")

    try:
        with open(experiment_metadata_path, 'w') as experiment_file:
            experiment_file.write(json.dumps(experiment, indent=4))
            experiment_file.close()
    except Exception:
        logger.error("Couldn't create experiment file")
        return

    logger.info("Experiment created correctly")
    #logger.debug(json.dumps(experiment, indent=4))

def run_experiments(workdir: Workdir):
    projects = get_projects(workdir.experiments_path)
    if projects == None:
        return

    while True:
        prompt_template, prompt_template_filename = select_prompt_template(workdir.prompts_path)

        if prompt_template == None:
            return
        
        print("\nSelect testing mode:\n   [0] Specific experiment from a project\n   [1] All experiments from a project\n   [2] All projects")

        while True:
            testing_mode = input(">> ")
            if not testing_mode in ["0", "1", "2"]:
                print("Invalid option. Try again:")
            else:
                break

        if testing_mode == "0":
            test_experiment(projects, prompt_template, prompt_template_filename, workdir)
        elif testing_mode == "1":
            test_project(projects, prompt_template, prompt_template_filename, workdir)
        elif testing_mode == "2":
            test_all_projects(projects, prompt_template, prompt_template_filename, workdir)

        while True:
            continue_exec = input("Continue experiments (y/N): ")
            if not continue_exec.lower() in ["y", "yes", "n", "no"]:
                continue_exec = print("Incorrect option. Try again:")
            else:
                break
            
        if continue_exec.lower() in ["n", "no"]:
            break

def evaluate_results(workdir: Workdir):
    logger.info("Evaluating experiment results..")

    raw_results_filenames = get_files_from_path(workdir.raw_results_path)

    projects = get_projects(workdir.experiments_path)

    for raw_result_filename in raw_results_filenames:
        if not has_extension(raw_result_filename, JSON_EXTENSION):
            continue

        logger.info(f"Evaluating result file '{raw_result_filename}'")

        raw_result_path = os.path.join(workdir.raw_results_path, raw_result_filename)

        try:
            with open(raw_result_path, 'r') as raw_result_file:
                raw_result = json.load(raw_result_file)
                
                #logger.debug(raw_result)

                experiment_id = raw_result["experiment"]
                project_name = raw_result["project"]
                org_name = raw_result["org"]

                project_id = get_project_id(project_name, org_name)

                experiment_snippet = projects["experiments"][experiment_id]["snippet"]

                snippet_path = os.path.join(workdir.experiments_path, project_id, "snippets", experiment_snippet)

                with open(snippet_path) as snippet_file:
                    code_snippet = snippet_file.read()
                    logger.debug(code_snippet)
                    snippet_file.close()

                llm_answer = raw_result["llm_answer"]

                #logger.debug(llm_answer)
                
                evaluate_experiment_result(llm_answer, code_snippet)
                
                raw_result_file.close()

        except Exception as e:
            #logger.error(f"Couldn't open result file '{raw_result_filename}'")
            #raise e
            print(e)


def save_experiment_result(workdir: Workdir, chat_completion, gen_time, experiment_name,
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
        "prompt_gen_time": gen_time,
        "llm_answer": chat_completion["choices"][0]["message"]["content"]
    }
    
    created_unix = results["created_unix"]
    experiment_results_path = os.path.join(workdir.raw_results_path,
                f"{experiment_name}_{project_name}_{org_name}_{created_unix}.json")

    try:
        with open(experiment_results_path, 'w') as results_file:
            results_file.write(json.dumps(results, indent=4))
            results_file.close()
    except Exception:
        logger.error("Couldn't create results file")
        return

    logger.info("Experiment results created correctly")

#Tests
def test_experiment(projects, prompt_template, prompt_template_filename, workdir: Workdir):
    project_id, project = select_project(projects)

    project_name = project["metadata"]["project"]
    project_org = project["metadata"]["org"]

    project_snippets_path = os.path.join(workdir.experiments_path, project_id, "snippets")

    experiment = select_experiment(project)

    experiment_name = experiment["name"]
    experiment_snippet = experiment["snippet"]
    experiment_function_name = experiment["function_name"]

    logger.info(f"Testing experiment '{experiment_name}': snippet '{experiment_snippet}', function name '{experiment_function_name}' from project '{project_name}' and organization '{project_org}'")
        
    with open(os.path.join(project_snippets_path, experiment_snippet)) as file:
        snippet = file.read()
    
    errors = get_errors_as_str(experiment)

    prompt = build_prompt(prompt_template, snippet, errors)

    logger.debug(prompt)

    chat_completion, gen_time = prompt_llm(prompt)

    save_experiment_result(workdir, chat_completion, gen_time, experiment_name, project_name, project_org, prompt_template_filename)

def test_project(projects, prompt_template, prompt_template_filename, workdir: Workdir):
    project_id, project = select_project(projects)

    project_name = project["metadata"]["project"]
    project_org = project["metadata"]["org"]

    project_snippets_path = os.path.join(workdir.experiments_path, project_id, "snippets")

    logger.info(f"Testing project '{project_name}' from organization '{project_org}'")

    for experiment in project["experiments"].values():
        experiment_name = experiment["name"]
        experiment_snippet = experiment["snippet"]
        experiment_function_name = experiment["function_name"]

        logger.info(f"Experiment '{experiment_name}': snippet '{experiment_snippet}', function name '{experiment_function_name}'")
        
        with open(os.path.join(project_snippets_path, experiment_snippet)) as file:
            snippet = file.read()
        
        errors = get_errors_as_str(experiment)

        prompt = build_prompt(prompt_template, snippet, errors)

        logger.debug(prompt)

        chat_completion, gen_time = prompt_llm(prompt)

        save_experiment_result(workdir, chat_completion, gen_time, experiment_name, project_name, project_org, prompt_template_filename)

def test_all_projects(projects, prompt_template, prompt_template_filename, workdir: Workdir):
    for project_id, project in projects.items():
        #logger.debug(json.dumps(project, indent=2))
        project_name = project["metadata"]["project"]
        project_org = project["metadata"]["org"]

        project_snippets_path = os.path.join(workdir.experiments_path, project_id, "snippets")

        logger.info(f"Testing project '{project_name}' from organization '{project_org}'")

        for experiment in project["experiments"].values():
            experiment_name = experiment["name"]
            experiment_snippet = experiment["snippet"]
            experiment_function_name = experiment["function_name"]

            logger.info(f"Experiment '{experiment_name}': snippet '{experiment_snippet}', function name '{experiment_function_name}'")
            
            with open(os.path.join(project_snippets_path, experiment_snippet)) as file:
                snippet = file.read()
            
            errors = get_errors_as_str(experiment)

            prompt = build_prompt(prompt_template, snippet, errors)

            logger.debug(prompt)

            chat_completion, gen_time = prompt_llm(prompt)

            save_experiment_result(workdir, chat_completion, gen_time, experiment_name, project_name, project_org, prompt_template_filename)

def main():
    workdir = select_experiment_workdir()

    if workdir is None:
        return

    while True:
        print(
            """\nSelect option:
    [0] Create new project metadata
    [1] Create new code snippet metadata
    [2] Run experiments
    [3] Evaluate experiment results
    [4] Exit
            """
        )       

        while True:
            option = input(">> ")
            if not option in ["0", "1", "2", "3", "4"]:
                print("Invalid option. Try again:")
            else:
                break

        if option == "0":
            create_project_metadata(workdir)
        elif option == "1":
            create_experiment_metadata(workdir)
        elif option == "2":
            run_experiments(workdir)
        elif option == "3":
            evaluate_results(workdir)
        elif option == "4":
            break

if __name__ == "__main__":
    main()