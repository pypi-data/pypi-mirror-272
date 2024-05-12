import json 
import os
import tqdm
import cv2
import shutil

from helpers_ai.utils.jm2mm import extractor, file_read




def detect(json_path:str, image_path:str, destination_path:str, train_size:float=None,
            test_size:float=0.1, resize:bool=False, size:tuple[int,int]=(640,640), shuffle:bool=True) -> None:

    assert len(size) == 2, "size must have a length of 2."
    
    meta_data = {"dataset_type": "OCRDataset",
                "task_name": "textdet",
                "category":{"id":0, "name":"text"}
                }
    
    spt = file_read(json_path, train_size, test_size, shuffle)

    try:
        os.mkdir(os.path.join(destination_path, "detect"))
    except(FileExistsError):
        print("\nFolder detect is already exists.")

    try:
        os.mkdir(os.path.join(destination_path,"detect","annotations"))
    except(FileExistsError):
        print("\nFolder annotations is already exists.")

    for idx, phase in enumerate(spt):
        ann_con = []
        if idx == 0:
            ph = "train"
        elif idx == 1:
            ph = "val"
        try:
            print("\nCreating {} annotations..........".format(ph))
            os.mkdir(os.path.join(destination_path,"detect",ph))
        except(FileExistsError):
            print("\nFolder {} is already exists.".format(ph))
        
        print("")

        for v in tqdm.tqdm(phase):
            b_data = []
            img_name=v["ocr"].split("/")[-1]

            if resize:
                img = cv2.imread(os.path.join(image_path,img_name))
                img = cv2.resize(img, size)
                cv2.imwrite(os.path.join(destination_path,"detect",ph,img_name), img)
            else:
                shutil.copy(os.path.join(image_path,img_name),os.path.join(destination_path,"detect",ph,img_name))

            dt = extractor(v, resize, size[0], size[1])
            
            for poly, bbox, text in zip(dt["p_lst"], dt["b_lst"], dt["t_lst"]):

                b_data.append({"polygon": poly,
                            "bbox": bbox,
                            "bbox_label": 0,
                            "text": text,
                            "ignore": False
                            })
            ann_con.append({"img_path": dt["image_name"],
                        "height": dt["height"],
                        "width": dt["width"],
                        "instances": b_data})
            
        annot = {"metainfo":meta_data,
                    "data_list": ann_con}
        print("\n{} Dataset contains".format(ph), len(annot["data_list"]), "image annotations.")

        with open(os.path.join(destination_path,"detect","annotations","mmocr_detect_"+ph+".json"),"w") as f:
                json.dump(annot, f, indent=2)

    print("\nConversion Successful.\n")




def recog(json_path:str, image_path:str, destination_path:str, train_size:float=None,
            test_size:float=0.1, resize:bool=False, size:tuple[int,int]=(640,640), shuffle:bool=True) -> None:

    assert len(size) == 2, "size must have a length of 2."

    spt = file_read(json_path, train_size, test_size, shuffle)

    try:
        os.mkdir(os.path.join(destination_path,"recog"))
    except(FileExistsError):
        print("\nFolder recog is already exists.")

    try:
        os.mkdir(os.path.join(destination_path,"recog","annotations"))
    except(FileExistsError):
        print("\nFolder annotations is already exists.")

    for idx, phase in enumerate(spt):
        ann_con = []

        if idx == 0:
            ph = "train"
        elif idx == 1:
            ph = "val"

        try:
            print("\nCreating {} annotations..........".format(ph))
            os.mkdir(os.path.join(destination_path,"recog",ph))
        except(FileExistsError):
            print("\nFolder {} is already exists.".format(ph))
        
        print("")
        count = 0
        for v in tqdm.tqdm(phase):

            dt = extractor(v, image_path, destination_path, ph, "recog", resize, size[0], size[1])

            count += dt["len"]
            img = cv2.imread(os.path.join(image_path,dt["image_name"]))
            if resize:
                img = cv2.resize(img, size)

            for idx1, (bbox, text) in enumerate(zip(dt["b_lst"], dt["t_lst"])):

                cr_img = img[bbox[1]:bbox[3],bbox[0]:bbox[2]]
                cv2.imwrite(os.path.join(destination_path,"recog",ph,dt["image_name"][:-4]+"-"+str(idx1+1)+".png"),cr_img)
                ann_con.append(f"{dt['image_name'][:-4]+'-'+str(idx1+1)+'.png'} {text}")
        print(count)        
        with open(os.path.join(destination_path,"recog","annotations","mmocr_recog_"+ph+".txt"),"w") as f:
                f.writelines("\n".join(ann_con))
    
    print("\nConversion Successful.\n")




def kie_closed(json_path:str, image_path:str, destination_path:str, train_size:float=None,
            test_size:float=0.1, resize:bool=False, size:tuple[int,int]=(640,640), shuffle:bool=True) -> None:

    assert len(size) == 2, "size must have a length of 2."

    spt = file_read(json_path, train_size, test_size, shuffle)

    try:
        os.mkdir(os.path.join(destination_path,"kie-closed"))
    except(FileExistsError):
        print("\nFolder kie-closed is already exists.")

    try:
        os.mkdir(os.path.join(destination_path,"kie-closed","annotations"))
    except(FileExistsError):
        print("\nFolder annotations is already exists.")

    label = []
    for phase in spt:
        for v in phase:
            ann = v["label"]
            for idx1,i in enumerate(ann):
                label.append(i["labels"][0])
    cat = sorted(list(set(label)))

    with open(os.path.join(destination_path,"kie-closed","annotations","mmocr_kie_metainfo.txt"),"w") as f:
        for idx2, i in enumerate(cat):
            f.writelines(f"{idx2} {i}\n")

    for idx, phase in enumerate(spt):
        ann_con = []
        label = []

        if idx == 0:
            ph = "train"
        elif idx == 1:
            ph = "val"

        try:
            print("\nCreating {} annotations..........".format(ph))
            os.mkdir(os.path.join(destination_path,"kie-closed",ph))
        except(FileExistsError):
            print("\nFolder {} is already exists.".format(ph))
        
        print("")

        for v in tqdm.tqdm(phase):

            b_data = []
            img_name=v["ocr"].split("/")[-1]

            if resize:
                img = cv2.imread(os.path.join(image_path,img_name))
                img = cv2.resize(img, size)
                cv2.imwrite(os.path.join(destination_path,"kie-closed",ph,img_name), img)
            else:
                shutil.copy(os.path.join(image_path,img_name),os.path.join(destination_path,"kie-closed",ph,img_name))

            dt = extractor(v, resize, size[0], size[1])

            for idx1, (bbox, text) in enumerate(zip(dt["b_lst"], dt["t_lst"])):

                b_data.append({
                            "box": [bbox[0],bbox[1],bbox[0],bbox[3],bbox[2],bbox[3],bbox[2],bbox[1]],
                            "text": text,
                            "label": cat.index(v["label"][idx1]["labels"][0])})
            ann_con.append({"file_name": dt["image_name"],
                        "height": dt["height"],
                        "width": dt["width"],
                        "annotations": b_data})
            
        print("\n{} Dataset contains".format(ph), len(ann_con), "image annotations.")

        with open(os.path.join(destination_path,"kie-closed","annotations","mmocr_kie_"+ph+".json"),"w") as f:
            json.dump(ann_con, f, indent=2)
          
        print("\nConversion Successful.\n")