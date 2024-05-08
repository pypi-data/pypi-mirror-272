# opencv-cam-idx

Find opencv camera index in windows using win32 api

## Installation

You can install the package via pip:

```
pip install opencv-cam-idx
```

## Usage

```python
from opencv_cam_idx.finder import find_cameras

find_cameras()

# Camera(
#     idx=0,
#     friendly_name='USB Video',
#     device_path='\\\\?\\usb#vid_534d&pid_2109&mi_00#7&11fabc89&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\\global',
#     description='',
# )
# Camera(
#     idx=1,
#     friendly_name='Integrated Webcam',
#     device_path='\\\\?\\usb#vid_1bcf&pid_28b0&mi_00#6&3443eee2&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\\global',
#     description='',
# )
```

## License

This project is licensed under the terms of the MIT license.
