import json
import numpy as np
from sklearn.model_selection import train_test_split




def file_read(json_path:str, train_size:float, test_size:float, shuffle:bool) -> tuple[list,list]:

    assert train_size is not None or test_size is not None, "Either train_size or test_size may be None but not both."

    if train_size is not None and test_size is None:   
        assert isinstance(train_size, float) and train_size <= 1, "train_size must be float within [0-1]."
        test_size = round(abs(1-train_size), 2)

    elif test_size is not None and train_size is None:  
        assert isinstance(train_size, float) and train_size < 1, "test_size must be float and less than 1."
        train_size = round(abs(1-test_size), 2)

    assert (isinstance(train_size, float) and isinstance(test_size, float)) and ((train_size <= 1) and (test_size < 1)), "train_size must be within [0-1] and test_size less than 1 and both are must be in float."
    
    if (train_size+test_size) != 1:
        test_size = round(abs(1-train_size), 2) 

    with open(json_path, "r") as f:
        dt = json.load(f)

    train, test = train_test_split(dt, train_size=train_size, test_size=test_size, shuffle=shuffle)

    return (train, test)




def extractor(v, resize:bool, s_width:int, s_height:int) -> dict:
    img_name=v["ocr"].split("/")[-1]
    ann = v["poly"]
    text = v["transcription"]
    
    if isinstance(text,str):
        text = [v["transcription"]]
    
    w_scale = 1
    h_scale = 1
    p_lst = []
    b_lst = []

    for i in ann:
        width = i["original_width"]
        height = i["original_height"]

        if resize:
            w_scale = s_width/width
            h_scale = s_height/height
            width = s_width
            height = s_height
        
        poly = np.array(i["points"])
        seg_x =(poly[:,0] * w_scale) / 100 * width
        seg_y =(poly[:,1] * h_scale) / 100 * height

        xmin= int(np.min(seg_x))
        ymin= int(np.min(seg_y))
        xmax= int(np.max(seg_x))
        ymax= int(np.max(seg_y))
        
        poly = np.array([[x,y] for x,y in zip(seg_x,seg_y)]).ravel()
        poly = [int(i) for i in poly]

        p_lst.append(poly)
        b_lst.append([xmin,ymin,xmax,ymax])
    
    return {"p_lst": p_lst,
            "b_lst": b_lst,
            "t_lst": text,
            "image_name": img_name,
            "width": width,
            "height": height,
            "len":len(ann)}