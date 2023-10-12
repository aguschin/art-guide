# Image Croper Module

This module is in charge of cropping and adjust the image to the object of interest, in this case it is a painting. In case there is no image, it returns the original image.
The legacy cropper description based on component con be found [here](CCROPER.md)



For this, it is first preferable to use an image where the artwork is the center, as it will be used to select it.
A [huggingface segmenter](https://huggingface.co/nvidia/segformer-b0-finetuned-ade-512-512) was used to separate the objects:


<table>
  <tr>
  <td>Rotated</td> <td>In Perspective</td> <td>Normal</td>
  </tr>
  <tr>
    <td><img src="images/d1.jpg" alt="Image 1"></td>
    <td><img src="images/d6.jpg" alt="Image 2"></td>
    <td><img src="images/d11.jpg" alt="Image 3"></td>
  </tr>
  <tr>
    Segmentation with NN
  </tr>
  <tr>
    <td><img src="images/d2.jpg" alt="Image 6"></td>
    <td><img src="images/d7.jpg" alt="Image 7"></td>
    <td><img src="images/d12.jpg" alt="Image 8"></td>
  </tr>
  <tr>
    Contour
  </tr>
  <tr>
    <td><img src="images/d3.jpg" alt="Image 11"></td>
    <td><img src="images/d8.jpg" alt="Image 12"></td>
    <td><img src="images/d13.jpg" alt="Image 13"></td>
  </tr>
  <tr>
    Fiting a 4-side poligon
  </tr>
  <tr>
    <td><img src="images/d4.jpg" alt="Image 11"></td>
    <td><img src="images/d9.jpg" alt="Image 12"></td>
    <td><img src="images/d14.jpg" alt="Image 13"></td>
  </tr>
  <tr>
    Apply distortion/angle/size transformation
  </tr>
  <tr>
    <td><img src="images/d5.jpg" alt="Image 11"></td>
    <td><img src="images/d10.jpg" alt="Image 12"></td>
    <td><img src="images/d15.jpg" alt="Image 13"></td>
  </tr>
</table>



## Technical details

It was used opencv and huggingface modules to archive the current results.
An erosion operation was used to separate the components before the centroids calculations but in some cases the results are not good.


### Future steps and improvements

The segmentation module will need to be improved in the future. The current one does not detect some objects in the dataset such as vessels.

