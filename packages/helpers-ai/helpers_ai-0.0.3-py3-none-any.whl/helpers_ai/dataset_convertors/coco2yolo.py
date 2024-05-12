from pycocotools.coco import COCO
import os
import tqdm

from helpers_ai.utils.util import coco_rle2mask
from helpers_ai.utils.validator import coco_validator, yolo_validator




def __check_corrupt(corrupted):

    if len(corrupted)>0:

        print("\nThere are {} corrupted files.\n".format(len(corrupted)))
    
        for i in corrupted:
            print(i,"data is corrupted.")
            
        print("")
        
        raise ValueError("Corrupted files are present")




def detetcion(json_path:str, image_path:str, destination:str) -> None:
    
    coco = COCO(json_path)

    print("\nAnnotation Validator in progress.....")

    coco_validator(coco,image_path)

    imgid = coco.getImgIds()
    cat = coco.loadCats(coco.getCatIds())
    categ = [ct["name"] for ct in cat]
    corrupted = []

    print("")

    for imid in tqdm.tqdm(imgid):
        image = coco.loadImgs(imid)
        annid = coco.getAnnIds(imgIds=imid)
        annot = coco.loadAnns(annid)
        height, width = image[0]["height"],image[0]["width"]
        out = []
        ps = True
        
        for ann in annot:
            classes = ann["category_id"]
            x, y, w, h = [float(i) for i in ann["bbox"]]
            cx, cy, nw, nh = (x+x+w)/(2*width), (y+y+h)/(2*height), w/width, h/height
            
            if cx>1 or cy>1 or nw>1 or nh>1 :
                corrupted.append(image[0]["file_name"][:-4]+".txt")
                ps = False
                break
            
            out.append(f"{classes} {cx} {cy} {nw} {nh}")

        if ps:
            with open(os.path.join(destination,image[0]["file_name"][:-4]+".txt"),"w+") as f:
                f.writelines("\n".join(out)) 

    __check_corrupt(corrupted)

    print("\nThe conversion is completed.")

    print("\nValidation of converted annotation in progress..........\n")

    yolo_validator(image_path,destination,categ)

    with open(os.path.join(destination,"__classes.txt"),"w+") as f:
            f.writelines("\n".join(categ))

    print("\nThe annotation file is saved at '{}'.\n".format(destination))
   
                


def segmentation(json_path:str, image_path:str, destination:str) -> None:
    
    coco = COCO(json_path)

    print("\nAnnotation Validator in progress.....")

    coco_validator(coco,image_path)
    
    imgid = coco.getImgIds()
    cat = coco.loadCats(coco.getCatIds())
    categ = [ct["name"] for ct in cat]
    corrupted = []

    print("")

    for imid in tqdm.tqdm(imgid):
        image = coco.loadImgs(imid)
        annid = coco.getAnnIds(imgIds=imid)
        annot = coco.loadAnns(annid)
        height, width = image[0]["height"],image[0]["width"]
        out = []
        ps = True

        
        for ann in annot:
            classes = ann["category_id"]
            ann_seg = ann["segmentation"]

            if isinstance(ann_seg,dict):
                seg = coco_rle2mask(ann_seg["counts"], ann_seg["size"], 255, False, 50)

                for i in seg:
                    seg_p = [val/width if idx%2 == 0 else val/height for idx,val in enumerate(i.ravel())]

                    if max(seg_p)>1:
                        corrupted.append(image[0]["file_name"][:-4]+".txt")
                        ps = False
                        break

                    out.append(f"{classes} {' '.join([str(i) for i in seg_p])}")

            else:
                seg = [val/width if idx%2 == 0 else val/height for idx,val in enumerate(ann_seg[0])]

                if max(seg)>1:
                    corrupted.append(image[0]["file_name"][:-4]+".txt")
                    ps = False
                    break
                
                out.append(f"{classes} {' '.join([str(i) for i in seg])}")
            
        if ps:
            with open(os.path.join(destination,image[0]["file_name"][:-4]+".txt"),"w+") as f:
                f.writelines("\n".join(out))
    
    __check_corrupt(corrupted)

    print("\nThe conversion is completed.")

    print("\nValidation of converted annotation in progress..........\n")

    yolo_validator(image_path,destination,categ)

    with open(os.path.join(destination,"__classes.txt"),"w+") as f:
            f.writelines("\n".join(categ))

    print("\nThe conversion is completed.")
    print("\nThe annotation file is saved at '{}'.\n".format(destination))