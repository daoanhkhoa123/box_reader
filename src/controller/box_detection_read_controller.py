from queue import Queue
from threading import Thread
from typing import Tuple

from src.domain.image_streamer import Frames
from src.services.box_detect_service import BoxDetectService
from src.services.box_reader_service import BoxReaderService
from src.services.image_reader_service import ImageReaderService
from src.services.box_callback_service import BoxCallBackService

def _reader_worker(queue: Queue, box_reader: BoxReaderService, box_callback: BoxCallBackService):
    while True:
        task = queue.get()

        if task is None:
            break

        frames, image_id = task

        try:
            callback, infer_result = box_reader.read(frames, image_id)
            box_callback.call(callback)
        finally:
            queue.task_done()


def func():
    # [CVCameraStream(0)]
    img_reader = ImageReaderService()  # type: ignore
    box_detect = BoxDetectService()  # type: ignore
    box_reader = BoxReaderService()  # type: ignore
    box_callback = BoxCallBackService()

    queue: Queue[Tuple[Frames, str]] = Queue(maxsize=10)

    worker = Thread(
        target=_reader_worker,
        args=(queue, box_reader, box_callback),
        daemon=True,
    )
    worker.start()

    img_reader.start()

    try:
        for frames in img_reader.frames():
            res_detect, paths = box_detect.detect(frames)

            if res_detect:
                # assuming paths[0] is the image id
                image_id = paths[0]

                try:
                    queue.put_nowait((frames, image_id))
                except:
                    # queue full → drop frame
                    pass

    finally:
        img_reader.stop()

        queue.put(None) # type: ignore
        worker.join()

if __name__ == "__main__":
    from src.config.logging import setup_logging
    setup_logging()
    func()