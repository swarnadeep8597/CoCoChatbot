import json

def generate_raw_action_file(game_log_json):
    with open(game_log_json,'r') as file:
        contents = json.load(file)
    
    data = contents['worldStates']
    for item in data:
        blocks_in_grid = item['blocksInGrid']
        raw_actions = []
        if blocks_in_grid != []:
            for block in blocks_in_grid:
                temp_object = {
                    "shape":block[
                        'shape'
                    ],  
                    "color":block[
                        'color'
                    ],
                    "x":block['position']['x'],
                    "y":block['position']['y'],
                    "z":block['position']['z'],
                }
                raw_actions.append(
                    temp_object
                )
    return raw_actions



