from src.services.image_reader_service import ImageReaderService
from src.services.box_detect_service import BoxDetectService
from src.services.box_reader_service import BoxReaderService

def func():
    img_reader = ImageReaderService([])
    box_detect = BoxDetectService(...)
    box_reader = BoxReaderService(...)


    img_reader.start()
    for frames in img_reader.frames():
        res_detect, paths = box_detect.detect(frames)

        if res_detect:
            # this has to be in seperate threadd with a queue
            box_info, infer_result = box_reader.read(frames)    
    
    img_reader.stop()
