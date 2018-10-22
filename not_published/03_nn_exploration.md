% Neuronal Network Dreaming
% Markus Gräb
% 11.4.2018

* TODO
    * Upload experiments to github
    * Use some other neuronal networks
    * Reference Anal Hydrogen
    * Read
      https://research.googleblog.com/2015/06/inceptionism-going-deeper-into-neural.html



This is based on the deep dream work of google[^deepdream].

In this work, trained neuronal networks for recognition of patterns and objects are visualized.

The input data set is an image, which is fed into the neuronal network.


### Basic behaviour

The neuronal network is trained on recognition of an object.
In the "reverse" direction, when an input is fed into the trained network,
it tries to visualize a generic version of the trained object(s), based
on the view of the neuronal network how the object looks.

This process generates dream like images. Similar images are used to describe
hallucinogenic trips, like induced by LSD or Psilocybin. From this observation we can follow that the object recognition in a brain works similarly.

For more information take a look at [pareidolia](https://en.wikipedia.org/wiki/Pareidolia).(The psychological phenomenon where a brain responds to a stimulus/i and perceives a familiar pattern, where none exists.)

### Basic approach

Run the network in reverse and adjust the image to produce a higher confidence.
This will be reiterated multiple times. Note: The weights of the network stay fixed.

For example on an network trained on recognizing cat faces, the image will be modified to be more cat like.

The resulting image has too much noise, because each pixel is judged independently (gradient descent).

__TODO__ improve image by using a prior or regulizer (is it already used?)
https://en.wikipedia.org/wiki/Regularization_(mathematics)

### Implementation details



![Exanmple Video Sequence generated from the ??? Dataset](/static/articles/nn_dreaming.mp4)


[^deepdream]: [The original deep dream code by Google](https://github.com/google/deepdream)
