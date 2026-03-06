from queue import Queue
from threading import Thread
from typing import Tuple

from src.domain.image_streamer import Frames
from src.services.box_detect_service import BoxDetectService
from src.services.box_reader_service import BoxReaderService
from src.services.image_reader_service import ImageReaderService


def _reader_worker(queue: Queue, box_reader: BoxReaderService):
    while True:
        task = queue.get()

        if task is None:
            break

        frames, image_id = task

        try:
            box_info, infer_result = box_reader.read(frames, image_id)
        finally:
            queue.task_done()


def func():
    img_reader = ImageReaderService()  # type: ignore
    box_detect = BoxDetectService()  # type: ignore
    box_reader = BoxReaderService()  # type: ignore

    queue: Queue[Tuple[Frames, str]] = Queue(maxsize=10)

    worker = Thread(
        target=_reader_worker,
        args=(queue, box_reader),
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