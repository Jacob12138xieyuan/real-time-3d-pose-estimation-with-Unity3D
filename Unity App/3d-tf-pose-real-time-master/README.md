# Tensorflow  2D and 3D pose estimation

### Main Repository used:https://github.com/ildoonet/tf-pose-estimation

#### Repository used for 3D plotting:https://github.com/pyqtgraph/pyqtgraph

#### Dependencies
    python3
    tensorflow 1.4.1+
    opencv3, protobuf, python3-tk

#### Requiremnets
    argparse
    matplotlib
    scipy
    tqdm
    requests
    fire
    dill
    git+https://github.com/ppwwyyxx/tensorpack.git
    PyQt 4.7+, PySide, or PyQt5
    NumPy
    For 3D graphics: pyopengl and qt-opengl

Now from the main repository we get the following 3D points in this format
     
     17 points of x-coordinates,y-coordinates,z-coordinates in 3 lists...(matplotlib version)

    [[[  -5.04015825 -144.44469312 -181.38417344  -80.66403119  136.93109848
        116.99966118  -11.16919163    2.62527356   -1.05079033   -4.14445959
         -2.09431128  191.76896804  267.20449991  262.0793236  -193.72193764
       -250.90957393 -265.76258367]
      [  86.11631527   95.79752119 -356.94342453 -513.95376014   76.43512815
       -375.77265781 -518.52439623  194.44081889  188.62745907   89.32833065
        152.24195646  178.49202036  175.542326     50.77858199  197.77633214
        205.08800837   79.63985917]
      [-189.40400846 -226.05239806   -5.45200828 -287.15627626 -254.17645491
         -5.88772637 -285.68280011   26.52276139  263.97948822  362.16815799
        461.79813566  243.24526949  -33.83331904 -248.24538611  228.03920304
        -35.04000835 -248.7765299 ]]]

    17 lists containing each point coordinates as a single list...(pyqt format for printing 3d pose)

    [  -5.04015825   86.11631527 -189.40400846]
    [-144.44469312   95.79752119 -226.05239806]
    [-181.38417344 -356.94342453   -5.45200828]
    [ -80.66403119 -513.95376014 -287.15627626]
    [ 136.93109848   76.43512815 -254.17645491]
    [ 116.99966118 -375.77265781   -5.88772637]
    [ -11.16919163 -518.52439623 -285.68280011]
    [  2.62527356 194.44081889  26.52276139]
    [ -1.05079033 188.62745907 263.97948822]
    [ -4.14445959  89.32833065 362.16815799]
    [ -2.09431128 152.24195646 461.79813566]
    [191.76896804 178.49202036 243.24526949]
    [267.20449991 175.542326   -33.83331904]
    [ 262.0793236    50.77858199 -248.24538611]
    [-193.72193764  197.77633214  228.03920304]
    [-250.90957393  205.08800837  -35.04000835]
    [-265.76258367   79.63985917 -248.7765299 ]
    
    Using Pyqt library we plot these points and get the estimated 3D pose.

# Results
We get all the 2D keypoints and those are connected with best possible straight lines.
We also get the heat map, Vectormap-x and Vectormap-y
Finally using these 2D keypoints we estimate the 3D pose
These are some of the test images and their results.

![test](https://user-images.githubusercontent.com/19996897/38697955-0d023c9e-3eb1-11e8-9763-aac961ad3096.jpg) 
![heatmap](https://user-images.githubusercontent.com/19996897/38697953-0cd57da8-3eb1-11e8-84ab-f18c7ab7a361.png) 
![figure_3d](https://user-images.githubusercontent.com/19996897/38697950-0c917022-3eb1-11e8-9e1d-71c3a783f1f5.png)

![golf](https://user-images.githubusercontent.com/19996897/38698497-e54108be-3eb2-11e8-9723-cf188a9e5519.jpg)
![heatmap](https://user-images.githubusercontent.com/19996897/38698500-e5a9fba8-3eb2-11e8-8161-5c790bf9493c.png)
![figure_3d](https://user-images.githubusercontent.com/19996897/38698499-e57b0fdc-3eb2-11e8-96ca-2ed3a7b3465c.png)

Multiple Persons in a single image

![heatmap](https://user-images.githubusercontent.com/19996897/38698883-21c2222c-3eb4-11e8-8784-c733f403fbfa.png)
![person_1_3d](https://user-images.githubusercontent.com/19996897/38698878-20c82b5a-3eb4-11e8-8815-b3be38f19711.png)
![person2_3d](https://user-images.githubusercontent.com/19996897/38698880-213255c0-3eb4-11e8-8725-2fb1aba7510d.png)
![figure_3d](https://user-images.githubusercontent.com/19996897/38698882-218c4972-3eb4-11e8-95f1-6b7910f0273e.png)

Images with no humans - 3D pose can't be detected because there are not enough keypoints for pose estimation.Here is an examle of image of a cat

![cat](https://user-images.githubusercontent.com/19996897/38698854-1273a0ac-3eb4-11e8-88f4-3d5ca9f4467c.jpg)
![heatmap](https://user-images.githubusercontent.com/19996897/38698853-1244d3ee-3eb4-11e8-859e-8f2920c65b5b.png)

For more tested images please look into tested images directory in this folder.

Here is a demo of 2D pose Estimation using Webcam.
https://www.youtube.com/watch?v=XNDlHkFQmIs&list=PLpORSxrB3kQwrQ1IaGNqyRX1RM9kwOxwo

Here is a demo of 3D pose Estimation using Webcam.
https://youtu.be/_E2vrBo9z4o

# Following Improvements can be done 

Sometimes the 3D poses estimated by the model are not accurate but still it almost detecting every common pose of humans.For detecting more complicated images we can train the model on complex images and see whether it is detecting the pose or not.

This model is running on Nvidia Geforce 840M with 4GB memory and we are getting nearly 8 frames per second.For near real time dectection we can use higher graphics memory cards.

Camera used for testing the model is 5MP laptop webcam.We can use higher resolution camerad for filtering out the noise and get a clear image.
