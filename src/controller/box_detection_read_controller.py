from src.services.image_reader_service import ImageReaderService
from src.services.box_detect_service import BoxDetectService
from src.services.box_reader_service import BoxReaderService

def func():
    img_reader = ImageReaderService([])
    box_detect = BoxDetectService(...)
    box_reader = BoxReaderService(...)
    img_storage = 

    img_reader.start()
    for frames in img_reader.frames():
        res_detect = box_detect.detect(frames)

        if res_detect:
            
            box_information = box_reader.read(frames)    