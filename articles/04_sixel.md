% Matplotlib backend for Sixel Terminals
% Markus Gräb
% 18th April 2018

![Example plot inside a terminal](/static/articles/sixel.png)

[The project repository: https://github.com/koppa/matplotlib-sixel ](https://github.com/koppa/matplotlib-sixel)

A terminal output of plots in full greatness of matplotlib!

Awesome uses:

* Output full blown graphics in your terminal
* Plot over ssh without any X tunnel, even telnet or serial...


Alternative implementations: [PySixel](https://github.com/saitoha/PySixel), especially see their matplotlib example. It does similar things, but is not as easy to use.

## Explanation

Sixel is a bitmap graphics format which is supported by some terminals, f.e. 

* mlterm
* XTerm
* DECterm
* Kermit
* WRQ Reflection
* ZSTEM

For documentation of the protocol, take a look at the [References](#references)

## Implementation

The implementation is basend on the ipython backends.  The figure will first
be generated as image and then _imagemagick_ does the conversion to sixel.  At
last the _curses_ library is used to setup the terminal and print the figure.


## Usage

Make sure the dependencies are met: Python 3.X, Imagemagick and matplotlib.
First install the package with:

    ./setup.py install

Then activate the matplotlib backend in your current terminal session:

    import matplotlib 
    matplotlib.use('module://matplotlib-sixel')

Then plot something:

    from pylab import *
    plt.plot(sin(arange(100) / 10))
    show()

This script can be used as well in nice terminal scripts.
The script should take care of resizing your plots to a correct size of your terminal.


## References
* [Wikipedia - Sixel](https://en.wikipedia.org/wiki/Sixel)
* [Libsixel](https://github.com/saitoha/libsixel)
