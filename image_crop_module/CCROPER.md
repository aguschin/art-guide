# Component Cropper approach

For this, it is first preferable to use an image where the artwork is the center, as it will be used to select it:

<p align="center">
  <img src="images/i1.png" alt="Imagen de muestra">
</p>


A [huggingface segmenter](https://huggingface.co/nvidia/segformer-b0-finetuned-ade-512-512) was used to separate the objects:

<p align="center">
  <img src="images/i2.png" alt="Imagen de muestra">
</p>


Then, connected components, their centroids and bounding boxes are calculated. From these, the largest and most centered is chosen.

<p align="center">
  <img src="images/i3.png" alt="Imagen de muestra">
</p>


With the chosen component, the image is cropped and a result is returned:

<p align="center">
  <img src="images/i4.png" alt="Imagen de muestra">
</p>
