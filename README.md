Develop: [![Build Status](https://travis-ci.org/nagasuga/jsonh.png?branch=develop)](https://travis-ci.org/nagasuga/jsonh)

Master: [![Build Status](https://travis-ci.org/nagasuga/jsonh.png?branch=master)](https://travis-ci.org/nagasuga/jsonh)


# JSONH
JSON Homogeneous Collections Compressor

## What is JSONH

JSONH is one of the most performant, yet safe, cross programming language, way to pack and unpack generic homogenous collections.

This version is a wrapper around the [JSONH](https://github.com/WebReflection/JSONH) that takes any object, not just a list of dictionaries, to pack to a JSONH formatted JSON object.

### Pro

  * Convenience - Any object that can be dumped to JSON to be in JSONH format.
  * Size - Nested list of JSONH packable objects will all be converted into JSONH format.

### Con

  * Speed - Requires to traverse the entire obj to recursively pack every data.

## Installation

```
pip install git+https://github.com/nagasuga/jsonh
```

## Usage

```
import jsonh

data = {
    'status': 'success',
    'data': [
        {
          'name': 'John',
          'age': 12,
        },
        {
          'name': 'Steve',
          'age': 73,
        },
        {
          'name': 'Mickey',
          'age': 39,
        },
    ],
}

dumped = jsonh.dumps(data)
loaded = jsonh.loads(dumped)

```
