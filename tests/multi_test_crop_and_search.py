# import sys
# from os.path import dirname, abspath
# sys.path.append(dirname(dirname(abspath(__file__))))
# import warnings
# warnings.filterwarnings("ignore")
# from image_crop_module.croper import crop_image
# from reverse_image_search_module.search_image import find_image, find_file_name
# import os
# from PIL import Image
# import statistics
import numpy as np

fil = np.load("../data/embeddings_multi.npy")
print(fil[:5])
