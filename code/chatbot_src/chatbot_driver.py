import logging
logging.info('Remain calm!')

from fastapi import FastAPI
from pydantic import BaseModel

import ollama
import configparser
from helper_functions import load_function_selector,is_valid_output,load_task_prompt,part_name_corrector,color_checker
import json
import os
from reconstruct import call_module

"""
Change the part searching function this needs to be finished tonight
this completes our video demonstration
"""
#start the app i.e. activating the api for being called from the UI
app = FastAPI()

config_file_path = "/Users/sbhar/Riju/PhDCode/CoCoApp/modularised_coco/config.ini"
config = configparser.ConfigParser()
config.read(config_file_path)

function_selector_prompt_file = config.get('file_paths','function_selector_prompt_file')
task_description_prompt_file  = config.get('file_paths','task_description_prompt_file')
chat_history_file             = config.get('file_paths','chat_history_file')
blocked_locations_file        = config.get('file_paths','blocked_locations_file')

class TextRequest(BaseModel):
    text:str

def function_selector(instruction):
    function_selector_prompt = load_function_selector(function_selector_prompt_file)
    messages = [
        {
            'role':'system',
            'content':function_selector_prompt
        },
        {
            'role':'user',
            'content':instruction
        }
    ]
    response = ollama.chat(model='llama3.1:8b',messages=messages)
    raw_output = response['message']['content']
    return raw_output

@app.post("/predict")
def predict(request:TextRequest):
    #(PICK, C12Bridge, Blue, 4, 4, 0)
    basic_parts  = ['nut','screw','washer','h_bridge','v_bridge']
    basic_colors = ['red','blue','yellow','green']

    system_prompt = load_task_prompt(task_description_prompt_file)
    messages = [
        {
            'role':'system',
            'content':system_prompt
        }
    ]
    if os.path.exists(chat_history_file):
        with open(chat_history_file,'r') as file:
            chat_history = json.load(file)
    else:
        chat_history = messages
    
    #blocked_locations = []
    if os.path.exists(blocked_locations_file):
        with open(blocked_locations_file,'r') as file:
            blocked_locations = json.load(file)
    else:
        blocked_locations = []
    
    new_message = {
        'role':'user',
        'content':request.text
    }
    chat_history.append(
        new_message
    )
    response = ollama.chat(model='llama3.1:8b',messages=chat_history)
    raw_output = response['message']['content']
    if is_valid_output(raw_output):
        response_tuple = tuple(raw_output.strip("()").split(","))
        action_name = response_tuple[0].strip()
        part_name   = response_tuple[1].strip()
        part_color  = response_tuple[2].strip()
        x_cord      = response_tuple[3].strip()
        y_cord      = response_tuple[4].strip()
        z_cord      = response_tuple[5].strip()

        if action_name == "REMOVE":
            new_instruction = "pick "+str(x_cord)+" "+str(y_cord)+" "+str(z_cord)
        if action_name == "PICK":
            new_action_name = "place"
            if part_name.lower() in basic_parts:
                new_part_name = part_name.lower()
            elif part_name.lower() not in basic_parts:
                #print("Not implemented !!")
                new_part_name = part_name_corrector(part_name.lower())
                #invoke the reuse module and search in the already stored database


            if part_color.lower() not in basic_colors:
                new_color_name = color_checker(part_color.lower())
            else:
                new_color_name = part_color.lower()

            if part_name.lower() not in basic_parts and part_name_corrector(part_name.lower()) not in basic_parts:
                #new_part_name = part_name_corrector(part_name.lower())
                new_part_name = part_name.lower()
                #print("The old part name is:",part_name)
                print("The new part name is:",new_part_name)
                
                success  = call_module(
                    concept_name=new_part_name.lower(),
                    initial_coord=[int(x_cord),int(z_cord)+1,int(y_cord)]
                )
                #all_actions = ""
                if not success:
                    #print("Not able to recreate the module")
                    return ""
                else:
                    new_instruction = success
            #new_instruction = new_action_name+" "+new_part_name+" "+new_color_name+" "+str(x_cord)+" "+str(y_cord)+" "+str(z_cord)
            else:
                new_part_name   = part_name_corrector(part_name.lower()) #this portion can be made better
                new_instruction = new_action_name+" "+new_part_name+" "+new_color_name+" "+str(x_cord)+" "+str(int(z_cord)+1)+" "+str(y_cord)
                location_occupied = {
                    'x':int(x_cord),
                    'y':int(z_cord) + 1,
                    'z': int(y_cord)
                }
                blocked_locations.append(
                    location_occupied
                )
        assistant_move = {
            'role':'assistant',
            'content':raw_output
        }
        chat_history.append(
            assistant_move
        )
        
        #dumping the new chat history to the file
        with open(chat_history_file,'w') as file:
            json.dump(chat_history,file,indent=4)

        with open(blocked_locations_file,'w') as file:
            json.dump(blocked_locations,file,indent=4)
        """
        if os.path.exists(blocked_locations_file):
            with open(blocked_locations_file,'a') as file:
                json.dump(blocked_locations,file,indent=4)
        else:
            with open(blocked_locations_file,'w') as file:
                json.dump(blocked_locations,file,indent=4)
        """
        return new_instruction

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000
    )
