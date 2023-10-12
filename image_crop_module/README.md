# Image Croper Module

This module is in charge of cropping and adjust the image to the object of interest, in this case it is a painting. In case there is no image, it returns the original image.
The legacy cropper description based on component con be found [here](CCROPER.md)



For this, it is first preferable to use an image where the artwork is the center, as it will be used to select it.
A [huggingface segmenter](https://huggingface.co/nvidia/segformer-b0-finetuned-ade-512-512) was used to separate the objects:

<p align="center">
  <img src="images/i1.png" alt="Imagen de muestra">
</p>


<p align="center">
  <img src="images/i2.png" alt="Imagen de muestra">
</p>


## Technical details

It was used opencv and huggingface modules to archive the current results.
An erosion operation was used to separate the components before the centroids calculations but in some cases the results are not good.


### Future steps and improvements

The segmentation module will need to be improved in the future. The current one does not detect some objects in the dataset such as vessels.

<p align="center">
  <img src="images/i5.png" alt="Imagen de muestra">
  <img src="images/i6.png" alt="Imagen de muestra">
</p>
<p align="center">
  <img src="images/i7.png" alt="Imagen de muestra" width="40%">
  <img src="images/i8.png" alt="Imagen de muestra" width="40%">
</p>
