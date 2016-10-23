# Computer Vision Experiments

For comparing similarities, a picture and video (eg 'wombat.jpg' and 'wombat1.mp4') are needed. The other programs require a webcam.

## Compare similarities of frames

akazevideo: Find two most similar frames using AKAZE and Hamming Distance.
ssimvid: Find similar frames in video using sum of squared differences.

## Object detection

backsub: Background subtraction with default OpenCV function.
histeq: Edge detection after hisogram equalisation.
motion_detector: Improved version of histeq showing edges of a moving object.
hog: Histogram of Oriented Gradients of a video.

## Superpixel detection

posterisekm: Groups pixels into clusters of superpixels (default value = 2)
ragthresh: Groups pixels into superpixels by RAG thresholding

## Export video

vidout: exports "foo.avi" from a webcam