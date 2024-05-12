import xml.etree.ElementTree as et
import tqdm
import cv2
import os

def class_getter(label_path:str) -> list:

    cll = []
    len_ann = []

    for file in os.listdir(label_path):
        if file.endswith(".xml"):
            tree = et.parse(os.path.join(label_path,file))
            
            for child in tree.findall("object"):
                cll.append(child.find("name").text)
        
        elif file.endswith(".txt"):

            with open(os.path.join(label_path,file),"r") as f:
                for sep in f.read().split("\n"):
                    len_ann.append(len(sep.split()))
                    cll.append(sep.split()[0])

    if len(set(len_ann)) == 1 and list(set(len_ann))[0] == 5:
        print("\033[1m\033[4mThe lables are annotated for Detection task.\033[0m\n")
    
    elif len(set(len_ann)) > 1:
        print("\033[1m\033[4mThe lables are annotated for Segmentation task.\033[0m\n")  
    
    return sorted(list(set(cll)))




def coco_validator(coco:object, image_path:str) -> None:
    img_dt = coco.loadImgs(coco.getImgIds())
    ann_dt = coco.loadAnns(coco.getAnnIds())
    cat_dt = coco.loadCats(coco.getCatIds())
    assert len(img_dt) == len(os.listdir(image_path)), "Number of images does not match."
    
    filefmt = [i["file_name"][-4:] for i in img_dt]
    imgfmt = [i[-4:] for i in os.listdir(image_path)]
    assert len(set(filefmt)) == 1 or len(set(imgfmt)) == 1, "All images must be in a single format."
    assert set(filefmt).issubset([".jpg",".png"]) and set(imgfmt).issubset([".jpg",".png"]), "Images must be in jpg or png format."

    filename = [i["file_name"] for i in img_dt]
    assert sorted(filename) == sorted(os.listdir(image_path)), "Image files does not match."

    catinAnn = [i["category_id"] for i in ann_dt]
    assert len(set(catinAnn)) == len(cat_dt), "Categories does not match."

    imginAnn = [i["image_id"] for i in ann_dt]
    assert len(set(imginAnn)) == len(img_dt), "Image id does not match."
    
    print("\nChecking width and height........\n")
    for i in tqdm.tqdm(img_dt):
        img = cv2.imread(os.path.join(image_path,i["file_name"]))
        assert (i["height"], i["width"]) == img.shape[:2], "Image shape does not match."
    
    print("\nChecking data in annotations.......\n")
    for i in tqdm.tqdm(ann_dt):
        assert i["area"]>0, "Area values must be greater than 0."
        assert len(i["bbox"]) % 2 == 0 and len(i["bbox"]) == 4, "Invalid bbox values."
        t_img_dt = coco.loadImgs(i["image_id"])

        if i["segmentation"] != [[]]:
            if isinstance(i["segmentation"],dict):
                assert sorted(list(i["segmentation"].keys())) == sorted(["counts","size"]), "RLE Segmentation is incorrect"
                assert len(i["segmentation"]["size"]) == 2 , "RLE size values are corrupted"
                assert sum(i["segmentation"]["counts"]) == i["segmentation"]["size"][0] * i["segmentation"]["size"][1], "RLE counts values are corrupted."
                continue

            assert len(i["segmentation"][0]) % 2 == 0 and len(i["segmentation"][0]) >= 6, "Invalid segemntation values."
            

            seg_x = i["segmentation"][0][::2]
            seg_y = i["segmentation"][0][1::2]
            

            for x,y in zip(seg_x,seg_y):
                assert x <= t_img_dt[0]["width"], "Segmentation values are corrupted."
                assert y <= t_img_dt[0]["height"], "Segmentation values are corrupted."
        
        for x,y in zip(i["bbox"][::2],i["bbox"][1::2]):
            assert x <= t_img_dt[0]["width"], "Bbox values are corrupted."
            assert y <= t_img_dt[0]["height"], "Bbox values are corrupted."

    print("\nAnnotation Validator is complete.")
    return 




def voc_validator(image_path:str, labels_path:str) -> list:

    assert len(os.listdir(image_path)) == len(os.listdir(labels_path)), "Images and Labels does not match."
    assert sorted([i[:-4] for i in os.listdir(image_path)]) == sorted([i[:-4] for i in os.listdir(labels_path)]), "Images and labels files does not match."

    imgfmt = [i[-4:] for i in os.listdir(image_path)]
    labelfmt = [i[-4:] for i in os.listdir(labels_path)]
    assert len(set(labelfmt)) == 1 and list(set(labelfmt))[0] == ".xml" , "Labels must be in xml format."
    assert len(set(labelfmt)) == 1 or len(set(imgfmt)) == 1, "All images and labels must be in a single format."
    assert set(imgfmt).issubset([".jpg",".png"]), "Images must be in jpg or png format."

    print("\nChecking annotation files.........\n")

    cls = class_getter(labels_path)

    print("Classes present in all the labels : {}\n".format(cls))

    for file in tqdm.tqdm(os.listdir(image_path)):
        tree = et.parse(os.path.join(labels_path,file[:-4]+".xml"))
        filename = tree.find("filename").text
        width = int(tree.find("size").find("width").text)
        height = int(tree.find("size").find("height").text)
        
        assert file == filename, "Filename does not match."

        img = cv2.imread(os.path.join(image_path,filename))
        assert (height, width) == img.shape[:2], "Image shape does not match."

        for ann in tree.findall("object"):
            bbox = ann.find("bndbox")
            assert len(bbox) % 2 == 0 and len(bbox) == 4, "Invalid bbox values."

            xmin = int(bbox.find("xmin").text)
            ymin = int(bbox.find("ymin").text)
            xmax = int(bbox.find("xmax").text)
            ymax = int(bbox.find("ymax").text)

            for x,y in zip([xmin,xmax],[ymin,ymax]):
                assert x <= width, "Bbox values are corrupted."
                assert y <= height, "Bbox values are corrupted."
            
            if ann.find("polygon") is not None:
                seg = [float(child.text) for child in ann.find("polygon")]
                assert len(seg) % 2 == 0 and len(seg) >= 6, "Invalid segemntation values."

                seg_x = seg[::2]
                seg_y = seg[1::2]

                for x,y in zip(seg_x,seg_y):
                    assert x <= width, "Segmentation values are corrupted."
                    assert y <= height, "Segmentation values are corrupted."

    print("\nAnnotation Validator is complete.")
    return cls




def yolo_validator(image_path:str, labels_path:str, n_classes:list[int]) -> None:

    assert len(os.listdir(image_path)) == len(os.listdir(labels_path)), "Images and Labels does not match."
    assert sorted([i[:-4] for i in os.listdir(image_path)]) == sorted([i[:-4] for i in os.listdir(labels_path)]), "Images and labels files does not match."

    imgfmt = [i[-4:] for i in os.listdir(image_path)]
    labelfmt = [i[-4:] for i in os.listdir(labels_path)]
    assert len(set(labelfmt)) == 1 and list(set(labelfmt))[0] == ".txt" , "Labels must be in txt format."
    assert len(set(labelfmt)) == 1 or len(set(imgfmt)) == 1, "All images and labels must be in a single format."
    assert set(imgfmt).issubset([".jpg",".png"]), "Images must be in jpg or png format."

    print("\nChecking annotation files.........\n")

    cls = class_getter(labels_path)

    assert len(n_classes) == len(cls), "Classes does not match."

    print("There are {} classes present in all the labels.\n".format(len(cls)))

    for file in tqdm.tqdm(os.listdir(image_path)):
         img = cv2.imread(os.path.join(image_path,file))
         height, width = img.shape[:2]
         
         with open(os.path.join(labels_path,file[:-4]+".txt"),"r") as f:
                for sep in f.read().split("\n"):
                    data = sep.split()[1:]

                    for i in data:
                        assert float(i) <= 1, "Invalid label content."
                    
                    if len(data) > 4:
                        assert len(data) % 2 == 0 and len(data) >= 6, "Invalid segemntation values."
                        
                        seg = [round(float(val)*width,2) if idx%2 == 0 else round(float(val)*height,2) for idx,val in enumerate(data)]
                        seg_x = seg[::2]
                        seg_y = seg[1::2]

                        for x,y in zip(seg_x,seg_y):
                            assert x <= width, "Segmentation values are corrupted."
                            assert y <= height, "Segmentation values are corrupted."
                    
                    elif len(data) == 4:
                        assert len(data) % 2 == 0, "Invalid bbox values."

                        w, h = float(data[2])*width, float(data[3])*height
                        x, y = round(((float(data[0])*2*width)-w)/2,2), round(((float(data[1])*2*height)-h)/2,2)

                        for x,y in zip([x,x+w],[y,y+h]):
                            assert x <= width, "Bbox values are corrupted."
                            assert y <= height, "Bbox values are corrupted."
    
    print("\nAnnotation Validator is complete.")
    return 