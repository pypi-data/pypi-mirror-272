import numpy as np
import cv2




def annot_color(index:int) -> tuple:

    _clr = [(196, 98, 16), (141, 182, 0), (59, 68, 75), (86, 130, 3), (61, 43, 31), (37, 53, 41), (0, 0, 0), (2, 71, 254),
           (13, 152, 186), (138, 43, 226), (102, 255, 0), (255, 0, 127), (72, 6, 7), (89, 39, 32), (222, 49, 99), (0, 46, 99),
           (255, 56, 0), (184, 134, 11), (1, 50, 32), (72, 60, 50), (115, 79, 150), (85, 107, 47), (135, 38, 87), (72, 60, 50),
           (204, 0, 204), (133, 187, 101), (150, 113, 23), (16, 52, 166), (255, 0, 63), (1, 68, 33), (34, 139, 34), (128, 128, 128),
           (201, 0, 22), (128, 128, 0), (0, 65, 106), (75, 0, 130), (186, 22, 12), (90, 79, 207), (0, 144, 0), (0, 168, 107), (165, 11, 94),
           (148, 87, 235), (255, 247, 0), (26, 17, 16), (25, 89, 5), (193, 154, 107), (255, 0, 255), (255, 130, 67), (0, 0, 205), (0, 250, 154),
           (152, 255, 152), (174, 12, 0), (48, 186, 143), (57, 255, 20), (5, 144, 51), (0, 128, 0), (121, 104, 120), (103, 49, 71), (255, 165, 0),
           (255, 69, 0), (153, 0, 0), (104, 40, 96), (120, 24, 74), (128, 0, 128), (28, 57, 187), (0, 166, 147), (254, 40, 162), (0, 15, 137),
           (142, 69, 133), (255, 143, 0), (159, 0, 197), (105, 53, 156), (81, 72, 79), (227, 11, 93), (130, 102, 68), (255, 0, 0), (82, 45, 128),
           (0, 64, 64), (255, 102, 204), (101, 0, 11), (155, 17, 30), (255, 0, 40), (150, 113, 23), (255, 111, 255), (203, 65, 11), (167, 252, 0),
           (153, 0, 0), (139, 133, 137), (10, 186, 181), (253, 14, 53), (0, 255, 239), (255, 179, 0), (65, 102, 245), (218, 29, 129),
           (159, 0, 255), (254, 254, 51), (255, 174, 66), (154, 205, 50)]
    
    assert index < len(_clr), f"The index value must be less than {len(_clr)}."
    return _clr[index]




def coco_rle2mask(rle:list | np.ndarray, size:list|tuple [int, int],
                  max_val:int=255, mask:bool=True, min_area:int=None) -> np.ndarray|list:

    assert isinstance(rle, list|tuple|np.ndarray), "rle must be in list, tuple or numpy array."
    
    if isinstance(rle, list|tuple):
        if len(rle)%2 != 0:
            rle += (0,)
            rle = np.array(rle)
    else:
        rle = np.concatenate([rle, np.array([0,])])
    
    blank = np.zeros(size[0]*size[1], np.uint8)
    count = 0

    for i, j in zip(rle[::2], rle[1::2]): 
        start = count+i
        end = start+j
        count = end
        blank[start:end] = max_val

    blank = blank.reshape(size[::-1]).T
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    blank = cv2.morphologyEx(blank,cv2.MORPH_CLOSE, kernel, iterations=1)
    blank = cv2.erode(blank, np.ones((3,3), dtype=np.uint8), iterations=1)
   
    if mask:
        return blank
    
    assert min_area is not None, "If mask set to False, min_area must not be None."

    cnt, _ = cv2.findContours(blank, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return [cv2.approxPolyDP(ct, (0.1 * cv2.arcLength(ct, True)), True) for ct in cnt if cv2.contourArea(ct) > min_area]




def annot_bbox(img:str|np.ndarray, bbox:list[int], color:tuple[int], box_thickness:int,
               text:str, text_thickness:int) -> np.ndarray:

    assert len(bbox) == 4, "bbox length must be 4."
    assert len(color) == 3, "color must be in RGB format."

    size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 0.45*text_thickness, text_thickness)

    if isinstance(img, str):
        img = cv2.imread(img)

    cv2.rectangle(img, (bbox[0],bbox[1]), (bbox[2], bbox[3]), color, box_thickness)
    cv2.rectangle(img, (bbox[0], bbox[1]-size[1]*2), (bbox[0]+size[0], bbox[1]), color, -1)
    cv2.putText(img, text, (bbox[0], bbox[1]-size[1]//2), cv2.FONT_HERSHEY_COMPLEX, 0.45*text_thickness, (255,255,255), text_thickness)
    
    return img




def annot_seg(img:str|np.ndarray, seg_list:list[list[int,int]]|np.ndarray,
              color:tuple[int], alpha:float=0.45) -> np.ndarray:
    
    assert len(color) == 3, "color must be in RGB format."
    
    if isinstance(img, str): 
        img = cv2.imread(img)

    if isinstance(seg_list, list):
        seg_list = np.array(seg_list).astype("int")
    
    img_cpy = img.copy()
    cv2.drawContours(img_cpy, [seg_list], -1, color, -1)
    img = cv2.addWeighted(img, alpha, img_cpy, 1-alpha, 0)

    return img