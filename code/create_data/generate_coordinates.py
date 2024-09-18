import json
from tqdm import tqdm
import os
from raw_action_generator import generate_raw_action_file
from store_concept import store_concept
from convert2relative import edit_stored_data

def generate_resolve(game_logs="",concept_folder_path="",concept_names_path=""):
    with open(concept_names_path,'r') as file:
        construct_names = json.load(file)
    names = []
    for construct in construct_names:
        names.append(construct['name'])
    for concept_name in tqdm(names):
        target_folder_path = os.path.join(concept_folder_path,concept_name)
        game_log_file_path = game_logs + '/' + concept_name + '_extracted.json'
        raw_actions = generate_raw_action_file(
            game_log_json=game_log_file_path
        )
        stored_concepts = store_concept(
            raw_actions=raw_actions
        )
        resolvable_action_concept = target_folder_path + '/stored_'+concept_name+'.json'
        with open(resolvable_action_concept,'w') as file:
            json.dump(stored_concepts,file,indent=4)
        
        resolved_objects = edit_stored_data(
            stored_concept_file=resolvable_action_concept
        )
        
        #save this resolved objects 
        resolved_concept_path = target_folder_path + '/resolved_'+concept_name+'.json'
        with open(resolved_concept_path,'w') as file:
            json.dump(resolved_objects,file,indent=4)
        
        os.remove(resolvable_action_concept)
        