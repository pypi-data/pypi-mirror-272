"""
-----------------------------------------------------------------------------------------
DSPTools
-----------------------------------------------------------------------------------------
Digital Signal Processing Tools is a Python package to provide easy to use tools to learn
and teach digital signal processing with Python.

Version: 2024.05.08

### Modules:
* graph: Provides functionality to easily visualise signals. `plot_signal()` is already 
         available by direct import.
* operations: Provides basic operations on the independent variable of signals.
* frequency: Provides frequency analysis tools.
* ztransform: Provides tools for working with z-transform.

### Installation and usage:

Please install this package using PiP by typing:

`pip install USJ_dsptools`

Import this module as:

`import dsptools as dsp`

### Author:
Alejandro Alcaine, Ph.D\\
CoMBA research group\\
MESC Working Group on e-Cardiology\\
MESC European Association of Cardiovascular Imaging (EACVI)\\
lalcaine@usj.es

Faculty of Health Sciences\\
University San Jorge\\
Villanueva de Gállego (Zaragoza)\\
Spain
"""

__version__ = "2024.05.08"

from dsptools.graph import plot_signal

import dsptools.operations
import dsptools.graph
import dsptools.frequency
import dsptools.ztransform