import os
import cv2
import tqdm
import imageio as iio
from dateutil import relativedelta




def vid2img(video_path:str, destination_path:str, size:tuple[int,int]) -> None:

    assert os.path.isfile(video_path), "video_path must be a path to a video file."

    vid = cv2.VideoCapture(video_path)

    total_length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    vid_fps = int(vid.get(cv2.CAP_PROP_FPS))
    vid_time = relativedelta.relativedelta(seconds=(total_length//vid_fps))

    print("\nTotal time of the video : [ {}:{}:{} ]\n".format(vid_time.hours, vid_time.minutes, vid_time.seconds))

    for i in tqdm.tqdm(range(total_length)):
        ret, frame = vid.read()
        if ret:
            if size is not None:
                frame = cv2.resize(frame, size)

            cv2.imwrite(os.path.join(destination_path, f"frame-{i+1}.png"), frame)
    
    vid.release()
    
    print("\nExtraction Successfull.")

    print(f"\nA Total of \033[1m\033[4m{total_length} images\033[0m has been extracted.")

    print("\nThe Extracted images are saved at '{}'.".format(destination_path))




def fps_changer(video_path:str, fps:int, destination_path:str, filename:str,
                size:tuple[int,int], is_fast:bool) -> None:

    assert os.path.isfile(video_path), "video_path must be a path to a video file."

    vid = cv2.VideoCapture(video_path)

    if size is None:
        size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        
    if filename is not None:
        assert filename.endswith(".mp4"), "filename must ends with '.mp4'."
    else:
        filename = video_path.split("/")[-1][:-4]+"-fps_changed.mp4"
    
    total_length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    vid_fps = int(vid.get(cv2.CAP_PROP_FPS))
    vid_time = relativedelta.relativedelta(seconds=(total_length//vid_fps))

    if fps is None:
        fps = vid_fps

    print(f"\nThe video FPS : \033[1m\033[4m{vid_fps} fps\033[0m .")

    assert (not is_fast and fps > vid_fps) or (is_fast and fps <= vid_fps and fps > 0), "'is_fast' must be set to false if 'fps' is greater than video fps."

    vid_wr = cv2.VideoWriter(os.path.join(destination_path, filename), cv2.VideoWriter.fourcc(*"mp4v"), fps, size)

    step = vid_fps//fps

    if is_fast and step > 1:  
        spots = list(range(0,total_length,step))

    print("\nTotal time of the video : [ {}:{}:{} ]\n".format(vid_time.hours, vid_time.minutes, vid_time.seconds))

    for i in tqdm.tqdm(range(total_length)):

        ret, frame = vid.read()
        if ret:
            if size is not None:
                frame = cv2.resize(frame, size)
            
            if is_fast and step > 1:
                if i in spots:
                    vid_wr.write(frame)
                continue
            
            vid_wr.write(frame)
    
    vid_wr.release()
    vid.release()

    print("\nConversion Successfull.")

    print(f"\nA Total of \033[1m\033[4m{total_length//step if is_fast and step > 1 else 0} images\033[0m has been dropped from the video.")

    print("\nThe Converted video is saved at '{}' named '{}'.".format(destination_path, filename))




def vid_cropper(video_path:str, start_time:str, end_time:str, destination_path:str,
                filename:str, fps:int, size:tuple[int,int]) -> None:

    assert os.path.isfile(video_path), "video_path must be a path to a video file."
    assert len(start_time.strip().split(":")) == 3 and len(end_time.strip().split(":")) == 3, "start_time and end_time must be in h:m:s format."

    st_hr, st_mnt, st_sec= start_time.strip().split(":")
    ed_hr, ed_mnt, ed_sec= end_time.strip().split(":")
    test = st_hr+st_mnt+st_sec+ed_hr+ed_mnt+ed_sec
    
    assert test.isdigit(), "start_time and end_time must be in digits."
    assert int(st_mnt) < 60 and int(ed_mnt) < 60 and int(st_sec) < 60 and int(ed_sec) < 60 and int(st_hr) < 24 and int(ed_hr) < 24, "start_time and end_time must be in time format."

    start_second = sum([int(st_hr)*3600, int(st_mnt)*60, int(st_sec)])
    end_second = sum([int(ed_hr)*3600, int(ed_mnt)*60, int(ed_sec)])

    assert end_second > start_second, "start_time must be lower than end_time."

    vid = cv2.VideoCapture(video_path)

    if size is None:
        size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    
    if filename is not None:
        assert filename.endswith(".mp4"), "filename must ends with '.mp4'."
    else:
        filename = video_path.split("/")[-1][:-4]+"-cropped.mp4"
    
    total_length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    vid_fps = int(vid.get(cv2.CAP_PROP_FPS))
    tot_sec = (total_length//vid_fps)
    vid_time = relativedelta.relativedelta(seconds=tot_sec)
    
    if fps is None:
        fps = vid_fps
    
    crp_vid_time = relativedelta.relativedelta(seconds=(end_second - start_second))

    print("\nTotal time of the video : [ {}:{}:{} ]".format(vid_time.hours, vid_time.minutes, vid_time.seconds))

    print(f"\nThe video FPS : \033[1m\033[4m{vid_fps} fps\033[0m .\n")

    assert end_second <= tot_sec and start_second < tot_sec, "The specified time exceeds the video time range."
    assert fps <= vid_fps and fps > 0, "fps must not exceed the video fps"

    vid_wr = cv2.VideoWriter(os.path.join(destination_path, filename), cv2.VideoWriter.fourcc(*"mp4v"), fps, size)

    start_frame = start_second*vid_fps
    end_frame = end_second*vid_fps

    for i in tqdm.tqdm(range(total_length)):
        
        ret, frame = vid.read()
        
        if i >= start_frame and i <= end_frame and ret:
            if size is not None:
                frame = cv2.resize(frame, size)

            vid_wr.write(frame)
        
        elif i == end_frame:
            break
    
    vid_wr.release()
    vid.release()

    print("\nCropping Successfull.")

    print("\nA Total duration of cropped video : [ {}:{}:{} ]".format(crp_vid_time.hours, crp_vid_time.minutes, crp_vid_time.seconds))

    print("\nThe Cropped video is saved at '{}' named '{}'.".format(destination_path, filename))

            


def vid2gif(video_path:str, destination_path:str, filename:str, size:tuple[int,int],
            duration_of_frame:int, loop:int) -> None:
    
    print(size)
    assert os.path.isfile(video_path), "video_path must be a path to a video file."

    if filename is not None:
        assert filename.endswith(".gif"), "filename must ends with '.gif'."
    else:
        filename = video_path.split("/")[-1][:-4]+".gif"

    vid = cv2.VideoCapture(video_path)

    if size is None:
        size = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    total_length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    vid_fps = int(vid.get(cv2.CAP_PROP_FPS))
    tot_sec = (total_length//vid_fps)
    vid_time = relativedelta.relativedelta(seconds=tot_sec)

    print("\nTotal time of the video : [ {}:{}:{} ]\n".format(vid_time.hours, vid_time.minutes, vid_time.seconds))

    with iio.get_writer(os.path.join(destination_path,filename), mode="I", duration=duration_of_frame, loop=loop) as writer:

        for _ in tqdm.tqdm(range(total_length)):

            ret, frame = vid.read()
            if ret:
                if size is not None:
                    frame = cv2.resize(frame, size)

                writer.append_data(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        
    
    print("\nConversion Completed.\n")

    print("The gif file is saved at '{}' named '{}'.".format(destination_path, filename))