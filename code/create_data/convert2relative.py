import json

def edit_stored_data(stored_concept_file):
    with open(stored_concept_file,'r') as file:
        concept = json.load(file)
    resolved_objects = {}
    for item in concept:
        resolved_objects[item] = concept[item]

        temp_co_ord   = concept[item]['original_index']
        temp_left     = concept[item]['left']
        temp_right    = concept[item]['right']
        temp_top      = concept[item]['top']
        temp_bottom   = concept[item]['bottom']
        temp_top_left     = concept[item]['top_left']
        temp_top_right    = concept[item]['top_right']
        temp_bottom_left  = concept[item]['bottom_left']
        temp_bottom_right = concept[item]['bottom_right']

        temp_left_cord   = [temp_co_ord[0]-1,temp_co_ord[1],temp_co_ord[2]] if temp_left != None else -1
        temp_right_cord  = [temp_co_ord[0]+1,temp_co_ord[1],temp_co_ord[2]] if temp_right != None else -1
        temp_top_cord    = [temp_co_ord[0],temp_co_ord[1],temp_co_ord[2]+1] if temp_top != None else -1
        temp_bottom_cord = [temp_co_ord[0],temp_co_ord[1],temp_co_ord[2]-1] if temp_bottom != None else -1
        
        temp_top_left_coord     = [temp_co_ord[0]-1,temp_co_ord[1],temp_co_ord[2]+1] if temp_top_left != None else -1
        temp_top_right_coord    = [temp_co_ord[0]+1,temp_co_ord[1],temp_co_ord[2]+1] if temp_top_right != None else -1
        temp_bottom_left_coord  = [temp_co_ord[0]-1,temp_co_ord[1],temp_co_ord[2]-1] if temp_bottom_left != None else -1
        temp_bottom_right_coord = [temp_co_ord[0]+1,temp_co_ord[1],temp_co_ord[2]-1] if temp_bottom_right != None else -1

        for other_item in concept:
            if other_item != item:
                #resolving the left item
                other_cord = concept[other_item]['original_index']
                if temp_left != None:
                    if other_cord == temp_left_cord:
                        resolved_objects[item]['left'] = other_item
                
                if temp_right != None:
                    if other_cord == temp_right_cord:
                        resolved_objects[item]['right'] = other_item
                
                if temp_top != None:
                    if other_cord == temp_top_cord:
                        resolved_objects[item]['top'] = other_item
                
                if temp_bottom != None:
                    if other_cord == temp_bottom_cord:
                        resolved_objects[item]['bottom'] = other_item

                if temp_top_left != None:
                    if other_cord == temp_top_left_coord:
                        resolved_objects[item]['top_left'] = other_item
                
                if temp_top_right != None:
                    if other_cord == temp_top_right_coord:
                        resolved_objects[item]['top_right'] = other_item

                if temp_bottom_left != None:
                    if other_cord == temp_bottom_left_coord:
                        resolved_objects[item]['bottom_left'] = other_item

                if temp_bottom_right != None:
                    if other_cord == temp_bottom_right_coord:
                        resolved_objects[item]['bottom_right'] = other_item
    
    return resolved_objects