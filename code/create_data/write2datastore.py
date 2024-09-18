import os
import json
import configparser
from generate_coordinates import generate_resolve

def create_concept_folders(source_folder_path="",constructs_path=""):
    with open(constructs_path,'r') as file:
        construct_names = json.load(file)
    names = []
    for construct in construct_names:
        names.append(construct['name'])
    for name in names:
        construct_path = os.path.join(source_folder_path,name)
        if not os.path.exists(construct_path):
            os.makedirs(construct_path)

if __name__ == "__main__":
    """
    reading the config file
    """

    config = configparser.ConfigParser()
    config.read('/Users/sbhar/Riju/PhDCode/CoCoApp/faircopy/modularised/config.ini')

    source_folder_path  = config.get('file_paths','concept_folder_path')
    constructs_path     = config.get('file_paths','concept_names_path')
    game_logs           = config.get('file_paths','game_logs_folder')
    concept_folder_path = config.get('file_paths','concept_folder_path')
    concept_names_path  = config.get('file_paths','concept_names_path')

    print("All the config parameters have been read !!")
    create_concept_folders(
        source_folder_path=source_folder_path,
        constructs_path=constructs_path
    )
    generate_resolve(
        game_logs=game_logs,
        concept_folder_path=concept_folder_path,
        concept_names_path=concept_names_path
    )
    print('The concepts have been created for retrieval')