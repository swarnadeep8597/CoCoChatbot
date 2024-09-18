import numpy as np

def store_concept(raw_actions):
    class MyObject:
        def __init__(self,color,value,shape) -> None:
            self.color = color
            self.value = value
            self.shape = shape
    matrix = np.empty((9,9,9),dtype=object)
    for action in raw_actions:
        x = action['x']
        y = action['y']
        z = action['z']
        color  = action['color']
        shape  = action['shape']
        matrix[int(x),int(y),int(z)] = MyObject(color=color,value=1,shape=shape)
    
    #save_structure
    structure_dict = {}
    part_id = 1
    for index,element in np.ndenumerate(matrix):
        if matrix[index] != None:
            x        = index[0]
            y        = index[1]
            z        = index[2]
            left     = (x-1,y,z)
            right    = (x+1,y,z)
            top      = (x,y,z+1)
            bottom   = (x,y,z-1)

            top_left     = (x-1,y,z+1)
            top_right    = (x+1,y,z+1)
            bottom_left  = (x-1,y,z-1)
            bottom_right = (x+1,y,z-1)

            make_key = matrix[index].color +'_'+matrix[index].shape + '_'+str(part_id) # might look like this red_screw_1
            
            if matrix[index] is not None:
                structure_dict[make_key] = {
                    'original_color':matrix[index].color,
                    'original_shape':matrix[index].shape,
                    'original_index': index,
                    'left':(matrix[left].color,matrix[left].shape) if matrix[left] is not None else None,
                    'top_left':(matrix[top_left].color,matrix[top_left].shape) if matrix[top_left] is not None else None,
                    'bottom_left':(matrix[bottom_left].color,matrix[bottom_left].shape) if matrix[bottom_left] is not None else None,
                    'right':(matrix[right].color,matrix[right].shape) if matrix[right] is not None else None,
                    'top_right':(matrix[top_right].color,matrix[top_right].shape) if matrix[top_right] is not None else None,
                    'bottom_right':(matrix[bottom_right].color,matrix[bottom_right].shape) if matrix[bottom_right] is not None else None,
                    'top':(matrix[top].color,matrix[top].shape) if matrix[top] is not None else None,
                    'bottom':(matrix[bottom].color,matrix[bottom].shape) if matrix[bottom] is not None else None,

                }

                part_id = part_id + 1
    
    return structure_dict