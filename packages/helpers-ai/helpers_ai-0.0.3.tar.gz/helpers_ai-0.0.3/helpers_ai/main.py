import argparse
import yaml

from helpers_ai import __version__
from helpers_ai.annotator import annotate, image_convertor, video_convertor
from helpers_ai.dataset_convertors import coco2voc, coco2yolo, yolo2coco, yolo2voc, voc2coco, voc2yolo, jm2mmocr


def cli(): 
    """Main entry point for the Helper."""
    parser = argparse.ArgumentParser(description="Helpers tool which helps in the progress of making models.")
    parser.add_argument('--version', action='version', version=f'Helpers-ai v{__version__}')
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand', description="Available subcommands in Helpers-ai:")

    annot_parser = subparsers.add_parser(
        'annot',
        help='Manage the Annotation Process',
        description='Annotate images with the provided data. The supported annotation formats are "COCO", "YOLO" and "Pascal_VOC" formats.'
    )

    annot_parser.add_argument("format", type=str, choices=['YOLO', 'COCO', 'VOC'], metavar= "Dataset_format",
                            help="Specify the dataset format you want to annotate. Available formats 'YOLO', 'COCO', 'VOC'")
    annot_parser.add_argument("image_path", type=str, metavar= "Image_path", help = 'Local image path directory')
    annot_parser.add_argument("data", nargs="*", metavar= "labels_path", help = 'Local label file path')
    annot_parser.add_argument("-des", "--dest", type=str, metavar= "", help = 'Desination path', default=".")
    annot_parser.add_argument("-bb", "--bbox", type=str, metavar="", help="Perform box annotation process", default=True)
    annot_parser.add_argument("-cls", nargs="*", metavar="", help="Perform annotation for specified classes", default=())
    annot_parser.add_argument("-o", "--out_name", type=str, metavar="", help="Output filename", default="output.mp4")
    annot_parser.add_argument("-lp", "--loop", type=int, metavar="", help="Times of loop for gif image. 0 for infinie loop", default=0)
    annot_parser.add_argument("-vid", "--video", action="store_true", help="Converts the annotated images into video")
    annot_parser.add_argument("--gif", action="store_true", help="Converts the annotated images into a gif file")
    annot_parser.add_argument("-seg", "--segment", action="store_true", help="Perform Segment annotation process")
    annot_parser.add_argument("--resize", type=int, nargs=2, metavar="", help="Resize the image to the specified size", default=(640,640))
    annot_parser.add_argument("--fps", type=int, metavar="", help="Output video fps", default=24)
    annot_parser.add_argument("--frame-dur", type=int, metavar="", help="Frame duration for gif image", default=700)



    img_conv_parser = subparsers.add_parser(
        'image-convert',
        help='Manage the Image conversion Process',
        description='Convert the images into video or gif image'
    )

    img_conv_parser.add_argument("task", type=str, choices=['img2vid', 'img2gif'], metavar="Task",
                                help="Specify the task you want to perform. Available task are 'img2vid', 'img2gif'")
    img_conv_parser.add_argument("image_path", type=str, metavar= "Image_path", help = 'Local image path directory')
    img_conv_parser.add_argument("-des", "--dest", type=str, metavar= "", help = 'Desination path', default=".")
    img_conv_parser.add_argument("-o", "--out_name", type=str, metavar="", help="Output filename", default="output.mp4")
    img_conv_parser.add_argument("--resize",type=int, nargs=2, metavar="", help="Resize the image to the specified size", default=(640,640))
    img_conv_parser.add_argument("--fps", type=int, metavar="", help="Output video fps", default=24)
    img_conv_parser.add_argument("--frame-dur", type=int, metavar="", help="Frame duration for gif image", default=700)
    img_conv_parser.add_argument("-lp", "--loop", type=int, metavar="", help="Times of loop for gif image. 0 for infinie loop", default=0)



    vid_conv_parser = subparsers.add_parser(
        'video-convert',
        help='Manage the video conversion Process',
        description='Convert the video into images, gif or change the fps of the video or crop the video.'
    )

    vid_conv_parser.add_argument("task", type=str, choices= ['vid2img', 'vid2gif', 'change_fps', 'cropper'], metavar="Task",
                    help="Specify the task you want to perform. Available task are 'vid2img', 'vid2gif', 'change_fps', 'cropper'")
    vid_conv_parser.add_argument("video_path", type=str, metavar= "video_path", help = 'Local video file path')
    vid_conv_parser.add_argument("-des", "--dest", type=str, metavar= "", help = 'Desination path', default=".")
    vid_conv_parser.add_argument("-o", "--out_name", type=str, metavar="", help="Output filename", default=None)
    vid_conv_parser.add_argument("--resize", type=int, nargs=2, metavar="", help="Resize the image to the specified size", default=(640,640))
    vid_conv_parser.add_argument("--frame-dur", type=int, metavar="", help="Frame duration for gif image", default=700)
    vid_conv_parser.add_argument("-lp", "--loop", type=int, metavar="", help="Times of loop for gif image. 0 for infinie loop", default=0)
    vid_conv_parser.add_argument("--fps", type=int, metavar="", help="Output video fps", default=24)
    vid_conv_parser.add_argument("--fast", action="store_true", help="Increase the speed of the video playback")
    vid_conv_parser.add_argument("-st", "--start-time", metavar="", help="Start-time of the video to crop. It must be in 'h:m:s' format", default="0:0:0")
    vid_conv_parser.add_argument("-et", "--end-time", metavar="", help="End-time of the video to crop. It must be in 'h:m:s' format", default="0:0:1")



    dat_conv_parser = subparsers.add_parser(
        'dataset-convert',
        help='Manage the Dataset conversion Process',
        description='Convert the dataset from one format to other format like COCO, YOLO, VOC.'
    )

    dat_conv_parser.add_argument("task", type=str, metavar="Task",
                                choices= ['coco2voc', 'coco2yolo', 'voc2coco', 'voc2yolo', 'yolo2coco', 'yolo2voc', 'jm2mmocr'], 
                                help="Specify the task you want to perform. Available task are 'coco2voc', 'coco2yolo', 'voc2coco', 'voc2yolo', 'yolo2coco', 'yolo2voc', 'jm2mmocr'")
    dat_conv_parser.add_argument("image_path", type=str, metavar="Image_path", help ='Local image path directory')
    dat_conv_parser.add_argument("data", nargs="*", metavar= "labels_path", help = 'Local label file path')
    dat_conv_parser.add_argument("-des", "--dest", type=str, metavar= "", help = 'Desination path', default=".")
    dat_conv_parser.add_argument("-m", "--mode", type=str, choices=['detect', 'segment'], metavar="",
                                help="Selection of mode either detect or segment", default="detect")




    args = parser.parse_args()



    if args.subcommand == "annot":

        assert len(args.data) < 3, "Labels_path accepts a max of two arguments only."
        
        if args.format.lower() == "coco":
            annotate.coco_annotator(args.image_path, args.data[0], args.dest, args.segment, eval(args.bbox), args.cls, args.out_name,
                                    args.resize, args.video, args.fps, args.gif, args.frame_dur, args.loop)
        
        elif args.format.lower() == "yolo":
            annotate.yolo_annotator(args.image_path, args.data[0], args.data[1], args.dest, args.segment, eval(args.bbox), args.cls, args.out_name,
                                    args.resize, args.video, args.fps, args.gif, args.frame_dur, args.loop)
        
        elif args.format.lower() == "voc":
            annotate.voc_annotator(args.image_path, args.data[0], args.dest, args.segment, eval(args.bbox), args.cls, args.out_name,
                                args.resize, args.video, args.fps, args.gif, args.frame_dur, args.loop)



    elif args.subcommand == "image-convert":
        if args.task.lower() == "img2vid":
            image_convertor.img2vid(args.image_path, args.dest, args.out_name, args.fps, args.resize)
        
        elif args.task.lower() == "img2gif":
            image_convertor.img2gif(args.image_path, args.dest, args.out_name, args.resize, args.frame_dur, args.loop)



    elif args.subcommand == "video-convert":
        print(args.task.lower())
        if args.task.lower() == "vid2img":
            video_convertor.vid2img(args.video_path, args.dest, args.resize)
        
        elif args.task.lower() == "vid2gif":
            video_convertor.vid2gif(args.video_path, args.dest, args.out_name, args.resize, args.frame_dur, args.loop)
        
        elif args.task.lower() == "change_fps":
            video_convertor.fps_changer(args.video_path, args.fps, args.dest, args.out_name, args.resize, args.fast)

        elif args.task.lower() == "cropper":
            video_convertor.vid_cropper(args.video_path, args.start_time, args.end_time, args.dest, args.out_name, args.fps, args.resize)



    elif args.subcommand == "dataset-convert":
        if args.task.lower() == "coco2voc":
            coco2voc.convert(args.data[0], args.image_path, args.dest)
        
        elif args.task.lower() == "coco2yolo":
            if args.mode == "detect":
                coco2yolo.detetcion(args.data[0], args.image_path, args.dest)
            elif args.mode == "segment":
                coco2yolo.segmentation(args.data[0], args.image_path, args.dest)
        
        elif args.task.lower() == "yolo2coco":
            
            assert len(args.data) == 2, "Provide label directory and class file path in txt or yaml format."

            with open(args.data[1], "r") as f:
                if args.data[1].endswith(".yaml"):
                    cls_name = yaml.safe_load(f)["names"]
                else:
                    cls_name = f.readlines()

            yolo2coco.convert(args.data[0], args.image_path, args.dest, cls_name)
        
        elif args.task.lower() == "yolo2voc":

            assert len(args.data) == 2, "Provide label directory and class file path in txt or yaml format."

            with open(args.data[1], "r") as f:
                if args.data[1].endswith(".yaml"):
                    cls_name = yaml.safe_load(f)["names"]
                else:
                    cls_name = f.readlines()
            
            yolo2voc.convert(args.data[0], args.image_path, args.dest, cls_name)

        elif args.task.lower() == "voc2coco":
            voc2coco.convert(args.data[0], args.image_path, args.dest)
        
        elif args.task.lower() == "voc2yolo":
            if args.mode == "detect":
                voc2yolo.detection(args.data[0], args.image_path, args.dest)
            elif args.mode == "segment":
                voc2yolo.segment(args.data[0], args.image_path, args.dest)


if __name__ == "__main__":
    cli()