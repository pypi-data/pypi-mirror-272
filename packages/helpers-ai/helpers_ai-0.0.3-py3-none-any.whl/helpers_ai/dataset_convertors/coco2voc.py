from pycocotools.coco import COCO
import os
import tqdm
from xml.dom import minidom

from helpers_ai.utils.voc import element_node, child_node, object_node
from helpers_ai.utils.util import coco_rle2mask
from helpers_ai.utils.validator import coco_validator,voc_validator




def convert(json_path:str, image_path:str, destination:str) -> None:

    assert os.path.isdir(image_path) and os.path.isdir(destination), "image_path and destination must be a directory."
    assert os.path.isfile(json_path) and json_path.endswith(".json"), "json_path must be a path to a json file."

    coco = COCO(json_path)

    print("\nAnnotation Validator in progress.....")

    coco_validator(coco,image_path)

    imgid = coco.getImgIds()
    cat = coco.loadCats(coco.getCatIds())
    categ = [ct["name"] for ct in cat]

    print("")

    for imid in tqdm.tqdm(imgid):
        image = coco.loadImgs(imid)
        annid = coco.getAnnIds(imgIds=imid)
        annot = coco.loadAnns(annid)
        height, width = image[0]["height"],image[0]["width"]

        root = minidom.Document()
        xml = root.createElement("annotation")
        root.appendChild(xml)

        child_node(root,"folder","",xml)
        child_node(root,"filename",image[0]["file_name"],xml)
        child_node(root,"path",image[0]["file_name"],xml)

        source = element_node(root,"source",None)
        xml.appendChild(source)
        child_node(root,"database","",source)

        size = element_node(root,"size",None)
        xml.appendChild(size)
        child_node(root,"width",str(width),size)
        child_node(root,"height",str(height),size)
        child_node(root,"depth","3",size)

        child_node(root,"segmented","0",xml)

        for ann in annot:
            classes = ann["category_id"]
            ann_seg = ann["segmentation"]
            x, y, w, h = [int(i) for i in ann["bbox"]]
            attr = ["Unspecified","0","0","0"]

            if ann_seg == [[]]:  
                obj = object_node(root,attr,[categ[int(classes)],x,y,int(x+w),int(y+h)],None)
                xml.appendChild(obj)
         
            elif isinstance(ann_seg,dict):
                seg = coco_rle2mask(ann_seg["counts"], ann_seg["size"], 255, False, 50)
                
                for i in seg:
                    i = i.ravel()
                    obj = object_node(root,attr,[categ[int(classes)],x,y,int(x+w),int(y+h)],[i[::2], i[1::2]])
                    xml.appendChild(obj)
           
            else:
                seg_x = ann_seg[0][::2]
                seg_y = ann_seg[0][1::2]
                obj = object_node(root,attr,[categ[int(classes)],x,y,int(x+w),int(y+h)],[seg_x,seg_y])
                xml.appendChild(obj)
        
        xml_str = root.toprettyxml(indent ="\t") 

        with open(os.path.join(destination,image[0]["file_name"][:-4]+".xml"),"w+") as f:
            f.write(xml_str[23:])
        
    print("\nThe conversion is completed.")
    
    print("\nValidation of converted annotation in progress..........")

    voc_validator(image_path, destination)

    print("\nThe annotated file is saved at '{}'.\n".format(destination))