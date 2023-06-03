
import seaborn
import matplotlib
import numpy
import spotipy

library_methods = dir(spotipy)
method_count = len([method for method in library_methods if callable(getattr(spotipy, method))])

print("Number of spotipy:", method_count)

library_methods = dir(seaborn)
method_count = len([method for method in library_methods if callable(getattr(seaborn, method))])

print("Number of seaborn:", method_count)


library_methods = dir(matplotlib)
method_count = len([method for method in library_methods if callable(getattr(matplotlib, method))])

print("Number of matplotlib:", method_count)

library_methods = dir(numpy)
method_count = len([method for method in library_methods if callable(getattr(numpy, method))])

print("Number of numpy:", method_count)
