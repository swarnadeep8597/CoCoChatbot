from transformers import AutoTokenizer,AutoModelForSequenceClassification
import torch


"""
Add description text for each of the helper functions to improve their readabilty
"""

#load once statements to reduce system overhead

"""
tokenizer and model for color checking
"""
tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-reranker-large') 
model = AutoModelForSequenceClassification.from_pretrained('BAAI/bge-reranker-large')

def load_task_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def load_function_selector(file_path):
    function_list = ["above", "below", "on_top","underneath","touching","on_the_side","hanging","C12_bridge"] # Replace with your actual function names
    with open(file_path,'r') as file:
        return file.read().format(function_list=function_list)

def color_checker(color):
    model.eval()
    valid_colors = ['red', 'blue', 'yellow', 'green']
    pairs = []
    for valid_color in valid_colors:
        temp = [color,valid_color]
        pairs.append(temp)

    with torch.no_grad():
        inputs = tokenizer(pairs,padding=True,truncation=True,return_tensors='pt',max_length=512)
        scores = model(**inputs,return_dict=True).logits.view(-1,).float()

    return pairs[torch.argmax(scores*-1).item()][1]

def is_valid_output(string):
    splitted = [s.strip()for s in string.split(',')]
    if len(splitted) == 6:
        action_name = splitted[0][1:]
        part_name   = splitted[1]
        part_color  = splitted[2]
        x_cord      = splitted[3]
        y_cord      = splitted[4]
        z_cord      = splitted[5]

        if action_name.lower() == "pick" or action_name.lower() == "remove":
           return True
        else:
           return False
    else:
        return False

def part_name_corrector(part_name):
    #if the model outputs a part name which is a bit convoluted but still can be resolved from the list of the basic parts
    basic_parts = ['washer','screw','nut','h_bridge','v_bridge']
    for i,part in enumerate(basic_parts):
        if part in part_name.lower():
            return basic_parts[i]



