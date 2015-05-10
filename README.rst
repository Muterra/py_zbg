zbg
===

Python library for zbg encoding.

Installation
============

pip install zbg

Use
===

Please see the ZBG standard for details on what objects are supported. The short version is you may serialize anything consisting of only:

+ Lists
+ Dictionaries
+ Arbitrary binary

In this particular implementation, to be correctly interpreted, the corresponding python entities should be compatible with:

+ Mutable sequence (see containers.abc.MutableSequence)
+ Mapping (see containers.abc.Mapping)
+ Bytes-like objects (support the buffer protocol)

``dump(obj)``: serializes the entire ``obj``. Object must be as described above. Returns bytes.

``dumpf(obj, f)``: Serializes the ``obj`` to a standalone file. ``f`` is the *open* file handle to output to. ``dumpf`` will not call close(). ``f`` should be opened with mode ``'w+b'``.

``load(zbg)``: Loads a zbg-serialized bytes-like object into memory. Returns an object corresponding to whatever was contained within ``zbg``.

``loadf(f)``: Loads a standalone zbg-serialized file from ``f``. Returns an object corresponding to whatever was contained within ``zbg``. ``f`` should be opened with mode ``'rb'`` and will not be closed by the load.