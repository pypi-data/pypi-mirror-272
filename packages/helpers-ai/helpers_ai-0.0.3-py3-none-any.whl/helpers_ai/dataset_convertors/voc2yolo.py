import xml.etree.ElementTree as et
import os
import tqdm

from helpers_ai.utils.validator import voc_validator, yolo_validator, class_getter




def __check_corrupt(corrupted):

    if len(corrupted)>0:

        print("\nThere are {} corrupted files.\n".format(len(corrupted)))

        for i in corrupted:
            print(i,"data is corrupted.")
        
        print("")
        
        raise ValueError("Corrupted files are present")




def detection(label_path:str, image_path:str, destination:str) -> None:

    print("\nAnnotation Validator in progress.....")

    voc_validator(image_path,label_path)

    corrupted = []
    s_cls = class_getter(label_path)

    print("\nThere are {} classes are present in the given labels_path.".format(len(s_cls)))
    flg = input("\nContinue[y/n]: ")
    print("")

    if flg == "y" or flg =="Y":
    
        for file in tqdm.tqdm(os.listdir(label_path)):
            if file.endswith(".xml"):
                tree = et.parse(os.path.join(label_path,file))
                size = tree.find("size")
                width = int(size.find("width").text)
                height = int(size.find("height").text)
                out = []
                ps = True
                    
                for idx,ann in enumerate(tree.findall("object")):
                    classes = ann.find("name").text
                    bbox = ann.find("bndbox")
                    xmin = int(bbox.find("xmin").text)
                    ymin = int(bbox.find("ymin").text)
                    xmax = int(bbox.find("xmax").text)
                    ymax = int(bbox.find("ymax").text)
                    cx, cy, nw, nh =  (xmin+xmax)/(2*width), (ymin+ymax)/(2*height), (xmax-xmin)/width, (ymax-ymin)/height

                    if cx>1 or cy>1 or nw>1 or nh>1 :
                        corrupted.append(file[:-4]+".txt")
                        ps = False
                        break

                    out.append(f"{s_cls.index(classes)} {cx} {cy} {nw} {nh}")

                if ps:
                    with open(os.path.join(destination,file[:-4]+".txt"),"w+") as f:
                        f.writelines("\n".join(out))

        __check_corrupt(corrupted)
        
        print("\nThe conversion is completed.")

        print("\nValidation of converted annotation in progress..........\n")

        yolo_validator(image_path,destination,s_cls)

        with open(os.path.join(destination,"__classes.txt"),"w+") as f:
            f.writelines("\n".join(s_cls))
        
        print("\nThe annotated file is saved at '{}'.\n".format(destination))




def segment(label_path:str, image_path:str, destination:str) -> None:

    print("\nAnnotation Validator in progress.....")

    voc_validator(image_path,label_path)

    corrupted = []
    s_cls = class_getter(label_path)

    print("\nThere are {} classes are present in the given labels_path.".format(len(s_cls)))
    flg = input("\nContinue[y/n]: ")
    print("")

    if flg == "y" or flg =="Y":

        for file in tqdm.tqdm(os.listdir(label_path)):
            if file.endswith(".xml"):
                tree = et.parse(os.path.join(label_path,file))
                size = tree.find("size")
                width = int(size.find("width").text)
                height = int(size.find("height").text)
                out = []
                ps =True
                
                for idx,ann in enumerate(tree.findall("object")):
                    classes = ann.find("name").text
                    seg = [float(child.text)/width if idx%2 == 0 else float(child.text)/height for idx,child in enumerate(ann.find("polygon"))]
            
                    if max(seg)>1:
                        corrupted.append(file[:-4]+".txt")
                        ps = False
                        break
                    
                    out.append(f"{s_cls.index(classes)} {' '.join([str(i) for i in seg])}")

                if ps:
                    with open(os.path.join(destination,file[:-4]+".txt"),"w+") as f:
                        f.writelines("\n".join(out))

        __check_corrupt(corrupted)

        print("\nThe conversion is completed.")

        print("\nValidation of converted annotation in progress..........\n")

        yolo_validator(image_path,destination,s_cls)

        with open(os.path.join(destination,"__classes.txt"),"w+") as f:
            f.writelines("\n".join(s_cls))
        
        print("\nThe annotated file is saved at '{}'.\n".format(destination))