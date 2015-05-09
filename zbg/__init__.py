'''
LICENSING
-------------------------------------------------

zbg: A python library for zbg encodings.
    Copyright (C) 2014-2015 Nicholas Badger
    badg@nickbadger.com
    nickbadger.com

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public
    License along with this library; if not, write to the 
    Free Software Foundation, Inc.,
    51 Franklin Street, 
    Fifth Floor, 
    Boston, MA  02110-1301 USA

------------------------------------------------------
'''

# Core modules
import collections
from math import ceil
# from .encode import *
# from .decode import *

def dump(obj):
    ''' Serializes the object.
    '''
    # In for a penny, in for a pound.
    if isinstance(obj, collections.Mapping):
        # Sort by the big-endian integer representation
        zbg = b'd'
        ordered = sorted(list(obj), key=lambda x: int.from_bytes(x, 'big'))
        for key in ordered:
            zbg += dump(key) + dump(obj[key])
        zbg += b'e'
    elif isinstance(obj, collections.MutableSequence):
        zbg = b'l'
        for value in obj:
            zbg += dump(value)
        zbg += b'e'
    else:
        # Look for the buffer interface to define bytes.
        try:
            memoryview(obj)
            # If that succeeded, it bytes-like, and we can continue
        except TypeError:
            raise TypeError('Object cannot be implicitly converted to a zbg-'
                            'encoded bytestream. Check object typing.')
            
        # How long?
        size = len(obj)
        # Check for 256-bit hash/etc
        if size == 32:
            flag = b'h'
        # Check for 512-bit hash/etc
        elif size == 64:
            flag = b'H'
        # Nope, arbitrary size binary
        else:
            # Start off with the flag
            flag = b':'
            # Figure out how many octets are needed for the object's length
            bytes_for_len = ceil(size.bit_length() / 8)
            # Pack that into the first byte after the flag
            flag += bytes_for_len.to_bytes(1, 'big')
            # Pack the actual length immediately thereafter
            flag += size.to_bytes(bytes_for_len, 'big')
        # Okay, everything has been flagged correctly. Create the serialization
        zbg = flag + obj
        
    # Return.
    return zbg
    
def load(zbg):
    ''' Loads a zbg.
    '''
    # Do a quick check that it's bytes-like
    try:
        memoryview(zbg)
    except TypeError:
        raise TypeError('All zbg blobs must support the buffer protocol.')
    
    