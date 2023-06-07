import datetime
import time

START_TIME_PRECISE = time.perf_counter()
# ha, subtracting here makes it suuuper close the psutil.create_time()
START_TIME_FLOAT = time.time() - START_TIME_PRECISE
START_TIME = int(START_TIME_FLOAT)

START_TIME_DATE = datetime.datetime.now()
START_TIME_PRETTY = datetime.datetime.strftime(START_TIME_DATE, "%Y-%m-%d %H:%M:%S")

BRAND = "Gesture Drawing"


import re
NAME_IS_IMAGE_TYPE_REGEX = re.compile(r".*\.(png|jpg|jpeg|jfif|bmp|tiff|tif|webp)$", re.IGNORECASE)



# image 
IMAGE_JPEG = 100
IMAGE_PNG  = 101
IMAGE_GIF  = 102
IMAGE_BMP  = 103
IMAGE_ICON = 104
IMAGE_WEBP = 105
IMAGE_TIFF = 106