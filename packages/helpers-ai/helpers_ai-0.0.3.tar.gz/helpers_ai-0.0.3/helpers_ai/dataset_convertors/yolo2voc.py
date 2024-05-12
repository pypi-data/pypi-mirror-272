from xml.dom import minidom
import os
import cv2
import tqdm

from helpers_ai.utils.validator import yolo_validator, voc_validator
from helpers_ai.utils.voc import element_node, child_node, object_node




def convert(labels_path:str, image_path:str, destination:str, n_classes:list[str]) -> None:

    print("\nAnnotation Validator in progress.....")

    yolo_validator(image_path, labels_path, n_classes)

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
    
    for file in tqdm.tqdm(os.listdir(image_path)):
        
        img = cv2.imread(os.path.join(image_path,file))
        height,width,depth = img.shape

        with open(os.path.join(labels_path,file[:-4]+".txt"),"r") as f:
            raw = f.read()
            data = [sep.split(" ") for sep in raw.split("\n")]
        
        root = minidom.Document()
        xml = root.createElement("annotation")
        root.appendChild(xml)

        child_node(root,"folder","",xml)
        child_node(root,"filename",file,xml)
        child_node(root,"path",file,xml)

        source = element_node(root,"source",None)
        xml.appendChild(source)
        child_node(root,"database","",source)

        size = element_node(root,"size",None)
        xml.appendChild(size)
        child_node(root,"width",str(width),size)
        child_node(root,"height",str(height),size)
        child_node(root,"depth",str(depth),size)

        child_node(root,"segmented","0",xml)

        if len(data[0])==5:

            for ann in data:
                classes, cx, cy, nw, nh = ann
                w, h = float(nw)*width, float(nh)*height
                x, y = int(((float(cx)*2*width)-w)/2), int(((float(cy)*2*height)-h)/2)
                attr = ["Unspecified","0","0","0"]
                obj = object_node(root,attr,[n_classes[int(classes)],x,y,int(x+w),int(y+h)],None)
                xml.appendChild(obj)

        else:

            for ann in data:
                classes = int(ann[0])
                seg = [round(float(val)*width,2) if idx%2 == 0 else round(float(val)*height,2) for idx,val in enumerate(ann[1:])]
                seg_x = seg[::2]
                seg_y = seg[1::2]
                x1, y1, x2, y2 = int(min(seg_x)), int(min(seg_y)), int(max(seg_x)), int(max(seg_y))
                attr = ["Unspecified","0","0","0"]
                obj = object_node(root,attr,[n_classes[classes],x1,y1,x2,y2],[seg_x,seg_y])
                xml.appendChild(obj)

        xml_str = root.toprettyxml(indent ="\t") 

        with open(os.path.join(destination,file[:-4]+".xml"),"w+") as f:
            f.write(xml_str[23:])
        
    print("\nThe conversion is completed.")

    print("\nValidation of converted annotation in progress..........")

    voc_validator(image_path, destination)

    print("\nThe annotated file is saved at '{}'.\n".format(destination))