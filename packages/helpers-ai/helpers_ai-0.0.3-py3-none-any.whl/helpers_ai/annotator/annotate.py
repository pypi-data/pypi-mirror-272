import os
import cv2
import yaml
import tqdm
import imageio as iio
from pycocotools.coco import COCO
import xml.etree.ElementTree as et

from helpers_ai.utils.validator import coco_validator, yolo_validator, voc_validator
from helpers_ai.utils.util import annot_bbox, annot_seg, coco_rle2mask, annot_color




def coco_annotator(image_folder:str, json_path:str, destination_path:str, segmentation:bool,
                   bbox:bool, class_names:tuple[str], file_name:str, size:tuple[int,int],
                   video_out:bool, fps:int, gif_out:bool, duration_of_frame:int, loop:int) -> None:
    
    assert (bbox and segmentation) or bbox or segmentation, "Either segmentation or bbox must be True or both may be True."
    assert json_path.endswith(".json") and os.path.isfile(json_path), "annotation file must be a json file."
    assert os.path.isdir(image_folder), "image_folder must be a folder."
    assert file_name[-4:] in [".mp4",".gif"], "video_name must be in .gif or .mp4 format."

    coco = COCO(json_path)

    print("\nAnnotation Validator in progress.....")

    coco_validator(coco,image_folder)

    print("\nAnnotation in progress...........")
    
    if class_names != ():
        imgid = coco.getImgIds()
        cat_id = coco.getCatIds()
    else:
        cat_id = coco.getCatIds(catNms=class_names)
        imgid = coco.getImgIds(catIds=cat_id)

    if video_out:
        vid_wr = cv2.VideoWriter(os.path.join(destination_path, file_name[:-4]+".mp4"), cv2.VideoWriter.fourcc(*"mp4v"),
                                 fps, size)
    
    elif gif_out:
        gif_wr = iio.get_writer(os.path.join(destination_path,file_name[:-4]+".gif"), mode="I", duration=duration_of_frame, loop=loop) 

    print("")

    for imid in tqdm.tqdm(imgid):
        image = coco.loadImgs(imid)
        annot = coco.loadAnns(coco.getAnnIds(imgIds=imid, catIds=cat_id))
        img = os.path.join(image_folder,image[0]["file_name"])

        for ann in annot:
            classes = int(ann["category_id"])
            ann_seg = ann["segmentation"]
            ann_bbox =  ann["bbox"]

            if segmentation and ann_seg != [[]]:
                if isinstance(ann_seg, dict):
                    continue
                    seg_lst = coco_rle2mask(ann_seg["counts"], ann_seg["size"], 255, False, 50)
                    for k in seg_lst:
                        seg = k.ravel()
                        print(seg)
                        seg_x = seg[0][::2]
                        seg_y = seg[0][1::2]
                        img = annot_seg(img, [[x,y] for x,y in zip(seg_x,seg_y)], annot_color(classes))
                else:
                    seg_x = ann_seg[0][::2]
                    seg_y = ann_seg[0][1::2]
                    img = annot_seg(img, [[x,y] for x,y in zip(seg_x,seg_y)], annot_color(classes))

            if bbox and ann_bbox != []:
                x,y,w,h = [int(i) for i in ann_bbox]
                img = annot_bbox(img, [x, y, x+w, y+h], annot_color(classes), 2, coco.loadCats(classes)[0]["name"], 1)
        
        if video_out:
            img = cv2.resize(img, size)
            vid_wr.write(img)
        
        elif gif_out:
            img = cv2.resize(img, size)
            gif_wr.append_data(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        
        else:
            cv2.imwrite(os.path.join(destination_path, image[0]["file_name"]), img)
    
    if video_out:
        vid_wr.release()
    elif gif_out:
        gif_wr.close()

    print("\nSave Completed.")

    print("\nThe annotation process is Completed.")

    if video_out:
        print("\nThe files are saved at '{}' named '{}'.".format(destination_path, file_name[:-4]+".mp4"))
    elif gif_out:
        print("\nThe files are saved at '{}' named '{}'.".format(destination_path, file_name[:-4]+".gif"))
    else:
        print("\nThe files are saved at '{}'.".format(destination_path))



def yolo_annotator(image_folder:str, labels_folder:str, cls_file_path:str, destination_path:str, segmentation:bool,
                   bbox:bool, class_names:tuple[str], file_name:str, size:tuple[int,int], video_out:bool, fps:int, 
                   gif_out:bool, duration_of_frame:int, loop:int) -> None:
    
    assert (bbox and segmentation) or bbox or segmentation, "Either segmentation or bbox must be True or both may be True."
    assert os.path.isfile(cls_file_path), "cls_file_path must be a class file in txt or yaml format."
    assert os.path.isdir(image_folder) and os.path.isdir(labels_folder), "images_folder and labels_folder must be a directory."
    assert file_name[-4:] in [".mp4",".gif"], "video_name must be in .gif or .mp4 format."

    print("\nAnnotation Validator in progress.....")

    with open(cls_file_path, "r") as f:
        if cls_file_path.endswith(".yaml"):
            cls_name = yaml.safe_load(f)["names"]
        else:
            cls_name = f.readlines()

    yolo_validator(image_folder, labels_folder, list(range(len(cls_name))))

    print("\nAnnotation in progress...........\n")

    
    
    if video_out:
        vid_wr = cv2.VideoWriter(os.path.join(destination_path, file_name[:-4]+".mp4"), cv2.VideoWriter.fourcc(*"mp4v"),
                                 fps, size)
    
    elif gif_out:
        gif_wr = iio.get_writer(os.path.join(destination_path,file_name[:-4]+".gif"), mode="I", duration=duration_of_frame, loop=loop) 

       
    for file in tqdm.tqdm(os.listdir(image_folder)):

        img = cv2.imread(os.path.join(image_folder, file))
        height, width = img.shape[:2]

        with open(os.path.join(labels_folder, file[:-4]+".txt"), "r") as f:
            data = [i.split() for i in f.readlines()]

        for i in data:
            cls = int(i[0])
            
            if class_names != () and cls_name[cls] not in class_names:  
                continue

            ann_data = i[1:]
            seg = [round(float(val)*width,2) if idx%2 == 0 else round(float(val)*height,2) for idx,val in enumerate(ann_data)]
            seg_x = seg[::2]
            seg_y = seg[1::2]

            if segmentation and len(ann_data) > 4:
                img = annot_seg(img, [[x,y] for x,y in zip(seg_x,seg_y)], annot_color(cls))
           
            if bbox and len(ann_data) > 3:
                x, y, x1, y1 = [int(min(seg_x)), int(min(seg_y)), int(max(seg_x)), int(max(seg_y))]
                img = annot_bbox(img, [x, y, x1, y1], annot_color(cls), 2, cls_name[cls], 1)

        if video_out:
            img = cv2.resize(img, size)
            vid_wr.write(img)

        elif gif_out:
            img = cv2.resize(img, size)
            gif_wr.append_data(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

        else:
            cv2.imwrite(os.path.join(destination_path, file), img)
    
    if video_out:
        vid_wr.release()
    elif gif_out:
        gif_wr.close()

    print("\nSave Completed.")

    print("\nThe annotation process is Completed.")

    if video_out:
        print("\nThe files are saved at '{}' named '{}'.".format(destination_path, file_name[:-4]+".mp4"))
    elif gif_out:
        print("\nThe files are saved at '{}' named '{}'.".format(destination_path, file_name[:-4]+".gif"))
    else:
        print("\nThe files are saved at '{}'.".format(destination_path))
            
        


def voc_annotator(image_folder:str, labels_folder:str, destination_path:str, segmentation:bool,
                  bbox:bool, class_names:tuple[str], file_name:str, size:tuple[int,int], video_out:bool, fps:int,
                  gif_out:bool, duration_of_frame:int, loop:int) -> None:
        
    assert (bbox and segmentation) or bbox or segmentation, "Either segmentation or bbox must be True or both may be True."
    assert os.path.isdir(image_folder) and os.path.isdir(labels_folder), "images_folder and labels_folder must be a directory."
    assert file_name[-4:] in [".mp4",".gif"], "video_name must be in .gif or .mp4 format."

    print("\nAnnotation Validator in progress.....")

    cls = voc_validator(image_folder,labels_folder)

    print("\nAnnotation in progress...........\n")

    if video_out:
        vid_wr = cv2.VideoWriter(os.path.join(destination_path, file_name[:-4]+".mp4"), cv2.VideoWriter.fourcc(*"mp4v"),
                                 fps, size)
    
    elif gif_out:
        gif_wr = iio.get_writer(os.path.join(destination_path,file_name[:-4]+".gif"), mode="I", duration=duration_of_frame, loop=loop) 


    for file in tqdm.tqdm(os.listdir(labels_folder)):
        if file.endswith(".xml"):
            tree = et.parse(os.path.join(labels_folder,file))
            f_name = tree.find("filename").text
            img = cv2.imread(os.path.join(image_folder, f_name))
                
            for ann in tree.findall("object"):
                classes = ann.find("name").text

                if class_names != () and classes not in class_names:
                    continue

                if segmentation and ann.find("polygon") is not None:
                    seg = [float(child.text) for child in ann.find("polygon")]
                    seg_x = seg[::2]
                    seg_y = seg[1::2]
                    img = annot_seg(img, [[x,y] for x,y in zip(seg_x,seg_y)], annot_color(cls.index(classes)))

                rd_bbox = ann.find("bndbox")
                if bbox and rd_bbox is not None:
                    xmin = int(rd_bbox.find("xmin").text)
                    ymin = int(rd_bbox.find("ymin").text)
                    xmax = int(rd_bbox.find("xmax").text)
                    ymax = int(rd_bbox.find("ymax").text)
                    img = annot_bbox(img, [xmin, ymin, xmax, ymax], annot_color(cls.index(classes)), 2, classes, 1)

            if video_out:
                img = cv2.resize(img, size)
                vid_wr.write(img)
            
            elif gif_out:
                img = cv2.resize(img, size)
                gif_wr.append_data(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

            else:
                cv2.imwrite(os.path.join(destination_path, f_name), img)
    
    if video_out:
        vid_wr.release()
    elif gif_out:
        gif_wr.close()
    
    print("\nSave Completed.")

    print("\nThe annotation process is Completed.")

    if video_out:
        print("\nThe files are saved at '{}' named '{}'.".format(destination_path, file_name[:-4]+".mp4"))
    elif gif_out:
        print("\nThe files are saved at '{}' named '{}'.".format(destination_path, file_name[:-4]+".gif"))
    else:
        print("\nThe files are saved at '{}'.".format(destination_path))