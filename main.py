#
# auto-project-structure
# This tool automatically creates a basic folder structure for your next Python project.
#
# Version: 0.1.0 (May 19 2024)
# Author: William Pettit
# License: MIT
#

import datetime
import glob
import itertools
import os
import sys

from typing import NoReturn

try:
  from termcolor import colored as col
except ImportError:
  print("Warning: The termcolor module is not installed. Consider installing it using 'pip install termcolor'.")
  
  def col(text: str, **_) -> str:
    return text


def exit_with_error(message: str) -> NoReturn:
  print(col(message, color="red"))
  sys.exit(1)


def print_done() -> None:
  print(col("done.", color="green"))


def get_formatted_current_date() -> str:
  return datetime.datetime.now().strftime("%B %d, %Y")


def get_formatted_current_year() -> str:
  return datetime.datetime.now().strftime("%Y")


def validate_project_name(project_name: str) -> NoReturn | None:
  if not project_name:
    exit_with_error("Error: The project name was empty.")

  if project_name == ".":
    exit_with_error("Error: The project name cannot be '.'.")

  if project_name.startswith("-") or project_name.endswith("-"):
    exit_with_error("Error: The project name cannot start or end with a hyphen.")
  
  for c in project_name:
    if not c.isalnum() and c not in ["-", "_"]:
      exit_with_error("Error: The project name can only contain alphanumeric characters, hyphens, and underscores.")


def create_project_directory(project_name: str) -> None:
  # check if the project directory already exists
  if os.path.exists(project_name):
    exit_with_error(f"Error: The directory \"{project_name}\" already exists.")

  # create the project directory
  os.makedirs(project_name)

  # change to the project directory
  os.chdir(project_name)

  # create the project directory structure
  os.makedirs("data")
  os.makedirs("docs")
  os.makedirs("tests")
  os.makedirs("src")


def create_and_activate_virtual_env() -> None:
  # create the virtual environment
  print("Creating Python virtual environment...", end="")
  os.system("python -m venv .venv")
  print_done()

  # activate the virtual environment
  print("Activating Python virtual environment...", end="")
  if sys.platform == "win32":
    os.system(".venv/Scripts/activate")
  else:
    os.system("source .venv/bin/activate")
  print_done()


def create_basic_files(project_name: str) -> list[str]:
  # define the replacements
  replacements = {
    "project_name": project_name,
    "date": get_formatted_current_date(),
    "year": get_formatted_current_year(),
    "fullname": "",
  }

  # get path to the data directory, even if the current working directory has changed
  data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

  # create glob pattern for the template files by joining the data directory with the pattern
  template_files = itertools.chain(
    glob.glob(os.path.join(data_dir, "*.template")),
    glob.glob(os.path.join(data_dir, ".*.template")),
  )

  # create the basic files
  print("Creating basic files...")
  created_files: list[str] = []
  for template_filename in template_files:
    # get the filename of the new file
    filename = os.path.basename(template_filename).replace(".template", "")
    
    # open the template file and the new file
    with open(template_filename) as template_file, open(filename, "w") as file:
      # read the content of the template file
      template_file_content = template_file.read()

      # replace the placeholders in the template file content
      for key, value in replacements.items():
        template_file_content = template_file_content.replace(f"[{key}]", value)

      # write the content to the file
      file.write(template_file_content)
    
    # add the filename to the list of created files
    created_files.append(filename)

    # print the success message
    print(f"\t> Created file: \"{filename}\"")
  
  # print the success message
  print("Basic files created successfully.")

  # return the list of created files
  return created_files


def initialize_git_repository(project_name: str, created_files: list[str]) -> None:
  # initialize the git repository
  print("Initializing Git repository...", end="")
  os.system("git init")
  print_done()

  # track the created files with git
  print(f"Tracking {len(created_files)} created files with Git...", end="")
  for file in created_files:
    os.system(f"git add {file}")
  print_done()
  

def main() -> None:
  # get the project name from the command line arguments
  project_name = sys.argv[1]
  validate_project_name(project_name)

  # create the project directory
  create_project_directory(project_name)

  # create the virtual environment
  create_and_activate_virtual_env()

  # create the basic files
  created_files = create_basic_files(project_name)

  # create a local git repository and begin tracking the created files
  initialize_git_repository(project_name, created_files)

  # print the success message
  print(f"Project \"{project_name}\" created successfully.")


if __name__ == "__main__":
  main()
