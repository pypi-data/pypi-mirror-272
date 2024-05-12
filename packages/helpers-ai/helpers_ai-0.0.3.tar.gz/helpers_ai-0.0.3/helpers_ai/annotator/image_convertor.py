import os
import cv2
import tqdm
import natsort
import imageio as iio




def img2vid(images_path:str, destination_path:str, filename:str,
             fps:int, size:tuple[int,int]) -> None:

    assert os.path.isdir(images_path), "image_path must be a directory."
    assert len(size) == 2, "size must contain two integers."
    # assert len(filename.split(".")) == 1, "filename must not contain extensions."

    vid_wr = cv2.VideoWriter(os.path.join(destination_path,filename[:-4]+".mp4"), cv2.VideoWriter.fourcc(*"mp4v"), fps=fps, frameSize=size)

    for file in tqdm.tqdm(natsort.natsorted(os.listdir(images_path))):
        if file.endswith((".jpg",".png",".jpeg")):
            img = cv2.imread(os.path.join(images_path, file))
            img = cv2.resize(img, size)
            vid_wr.write(img)
    
    vid_wr.release()

    print("\nConversion Completed.\n")

    print("The video file is saved at '{}' named '{}'.".format(destination_path, filename[:-4]+".mp4"))




def img2gif(images_path:str, destination_path:str, filename:str, size:tuple[int,int],
            duration_of_frame:int, loop:int) -> None:

    assert os.path.isdir(images_path), "image_path must be a directory."
    # assert filename[-4:] == ".gif", "filename must endswith '.gif' extensions."

    with iio.get_writer(os.path.join(destination_path,filename[:-4]+".gif"), mode="I", duration=duration_of_frame, loop=loop) as writer:
        
        for file in tqdm.tqdm(natsort.natsorted(os.listdir(images_path))):
            if file.endswith((".jpg",".png",".jpeg")):   
                img = cv2.imread(os.path.join(images_path, file))
                img = cv2.resize(img, size)
                writer.append_data(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

    print("\nConversion Completed.\n")

    print("The gif file is saved at '{}' named '{}'.".format(destination_path, filename[:-4]+".gif"))