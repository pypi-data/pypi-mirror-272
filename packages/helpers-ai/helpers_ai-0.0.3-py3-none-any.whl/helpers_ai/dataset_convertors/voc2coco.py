import xml.etree.ElementTree as et
import tqdm
import os
import json
from datetime import datetime
from pycocotools.coco import COCO

from helpers_ai.utils.validator import voc_validator, coco_validator, class_getter



    
def convert(label_path:str, image_path:str, destination:str) -> None:

    print("\nAnnotation Validator in progress.....")

    voc_validator(image_path,label_path)

    info = {"description": "VOC 2 COCO Converted Dataset",
            "Contributer": "code63ReaPer",
            "date_created": datetime.strftime(datetime.today(),"%Y/%m/%d")}
    
    licenses = {}
    categories = []
    s_cls = class_getter(label_path)

    for idx,cls in enumerate(s_cls):
        categories.append({"id":idx,
                           "name":cls})
        
    images = []
    annotations = []
    ann_id = 0
    tot_dt = 0
    img_id = 0
    
    print("\nThere are {} classes are present in the given labels_path.".format(len(s_cls)))
    flg = input("\nContinue[y/n]: ")
    print("")

    if flg == "n" or flg == "N":
        return

    elif flg == "y" or flg =="Y":
        for file in tqdm.tqdm(os.listdir(label_path)):
            if file.endswith(".xml"):
                tree = et.parse(os.path.join(label_path,file))
                filename = tree.find("filename").text
                size = tree.find("size")
                width = int(size.find("width").text)
                height = int(size.find("height").text)

                images.append({"file_name": filename,
                       "width": width,
                       "height": height,
                       "id": img_id})
                
                tot_dt += len(tree.findall("object"))
                    
                for idx,ann in enumerate(tree.findall("object")):
                    classes = ann.find("name").text
                    bbox = ann.find("bndbox")
                    xmin = int(bbox.find("xmin").text)
                    ymin = int(bbox.find("ymin").text)
                    xmax = int(bbox.find("xmax").text)
                    ymax = int(bbox.find("ymax").text)
                    x, y, w, h = xmin, ymin, xmax-xmin, ymax-ymin
                    
                    if ann.find("polygon") is not None:      
                        seg = [float(child.text) for child in ann.find("polygon")]
                        annotations.append({"segmentation":[seg],
                                    "area": w*h,
                                    "iscrowd": 0,
                                    "image_id": img_id,
                                    "bbox": [x, y, w, h],
                                    "category_id": s_cls.index(classes),
                                    "id": ann_id})
                        ann_id += 1
                   
                    else:
                        annotations.append({"segmentation":[[]],
                                    "area": w*h,
                                    "iscrowd": 0,
                                    "image_id": img_id,
                                    "bbox": [x, y, w, h],
                                    "category_id": s_cls.index(classes),
                                    "id": ann_id})
                        ann_id += 1
                
                img_id += 1
            
    ann_data = {"info":info,
                "licenses":licenses,
                "images":images,
                "annotations":annotations,
                "categories":categories}
    
    print("\nSaving the json file...........\n")
    
    with open(os.path.join(destination,"voc2coco.json"),"w+") as f1:
        json.dump(ann_data,f1)
    
    print("Save Completed.")

    print("\nThe conversion is completed.")

    print("\nValidation of converted annotation in progress..........\n")
    
    coco = COCO(os.path.join(destination,"voc2coco.json"))
    catid = coco.getCatIds()
    annid = coco.getAnnIds()
    imgid = coco.getImgIds()

    coco_validator(coco, image_path)
    
    print("\nThere are {} images, {} annotations and {} classes are loaded.".format(img_id,tot_dt,len(s_cls)))

    print("\nIn the saved json file there are {} images, {} annotations and {} categories are present.".format(len(imgid),len(annid),len(catid)))

    print("\nThe annotation file is saved at '{}' as 'voc2coco.json'.\n".format(destination))