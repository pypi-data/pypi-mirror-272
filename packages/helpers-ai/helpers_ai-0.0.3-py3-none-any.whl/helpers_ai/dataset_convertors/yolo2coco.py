import tqdm
import cv2
import os
import json
from datetime import datetime
from pycocotools.coco import COCO

from helpers_ai.utils.validator import yolo_validator, coco_validator




def convert(labels_path:str, image_path:str, destination:str, n_classes:list[str]) -> None:

    print("\nAnnotation Validator in progress.....")

    yolo_validator(image_path, labels_path, n_classes)
    
    info = {"description": "YOLO 2 COCO Converted Dataset",
            "Contributer": "code63ReaPer",
            "date_created": datetime.strftime(datetime.today(),"%Y/%m/%d")}
    
    licenses = {}
    categories = []
    
    for idx,cls in enumerate(n_classes):
        categories.append({"id":idx,
                           "name":cls})
        
    images = []
    annotations = []
    ann_id = 0
    tot_dt = 0
    cl = []
    corrupted =[]

    for file in os.listdir(labels_path):
        
        with open(os.path.join(labels_path,file),"r") as lr:
            raw = lr.read()
            data = [sep.split(" ") for sep in raw.split("\n")]

        for ann in data:
            cl.append(ann[0])

            if (len(ann)==5) and (float(ann[1])>1 or float(ann[2])>1 or float(ann[3])>1 or float(ann[4])>1):
                corrupted.append(file)
                break

            elif len(ann)>5 and max([float(i) for i in ann[1:]])>1:
                corrupted.append(file)
                break

    if len(corrupted)>0:
        print("\nThere are {} corrupted files.\n".format(len(corrupted)))
    
        for i in corrupted:
            print(i,"data is corrupted.")
        
        print("")
        raise ValueError("Corrupted files are present")
    
    if len(set(cl)) != len(n_classes):
        raise AssertionError("The number of classes given does not match the classes in annotated file")
    
    print("")
    
    pbar = tqdm.tqdm(total=len(os.listdir(image_path)))
    
    for img_idx,file in enumerate(os.listdir(image_path)):
        img = cv2.imread(os.path.join(image_path,file))
        height,width = img.shape[:2]
        
        with open(os.path.join(labels_path,file[:-4]+".txt"),"r") as f:
            raw = f.read()
            data = [sep.split(" ") for sep in raw.split("\n")]
        
        images.append({"file_name": file,
                       "width": width,
                       "height": height,
                       "id": img_idx})
        tot_dt += len(data)
        
        if len(data[0])==5:
            
            for ann in data:
                classes, cx, cy, nw, nh = ann
                w, h = float(nw)*width, float(nh)*height
                x, y = round(((float(cx)*2*width)-w)/2,2), round(((float(cy)*2*height)-h)/2,2)
                annotations.append({"segmentation":[[]],
                                    "area": w*h,
                                    "iscrowd": 0,
                                    "image_id": img_idx,
                                    "bbox": [x, y, w, h],
                                    "category_id": int(classes),
                                    "id": ann_id})
                ann_id += 1
        
        else:

            for ann in data:
                classes = ann[0]
                seg = [round(float(val)*width,2) if idx%2 == 0 else round(float(val)*height,2) for idx,val in enumerate(ann[1:])]
                seg_x = seg[::2]
                seg_y = seg[1::2]
                x, y, w, h = round(min(seg_x),2), round(min(seg_y),2), round(max(seg_x)-min(seg_x),2), round(max(seg_y)-min(seg_y),2)
                annotations.append({"segmentation":[seg],
                                    "area": w*h,
                                    "iscrowd": 0,
                                    "image_id": img_idx,
                                    "bbox": [x, y, w, h],
                                    "category_id": int(classes),
                                    "id": ann_id})
                ann_id += 1
        
        pbar.update(img_idx+1)
    
    ann_data = {"info":info,
                "licenses":licenses,
                "images":images,
                "annotations":annotations,
                "categories":categories}
    
    print("\n\nSaving the json file...........\n")
    
    with open(os.path.join(destination,"yolo2coco.json"),"w+") as f1:
        json.dump(ann_data,f1)
    
    print("Save Completed.")

    print("\nThe conversion is completed.")

    print("\nValidation of converted annotation in progress..........\n")
    
    coco = COCO(os.path.join(destination,"yolo2coco.json"))
    catid = coco.getCatIds()
    annid = coco.getAnnIds()
    imgid = coco.getImgIds()

    coco_validator(coco, image_path)
    
    print("\nThere are {} images, {} annotations and {} classes are loaded.".format(img_idx+1,tot_dt,len(n_classes)))

    print("\nIn the saved json file there are {} images, {} annotations and {} categories are present.".format(len(imgid),len(annid),len(catid)))

    print("\nThe annotation file is saved at '{}' as 'yolo2coco.json'.\n".format(destination))