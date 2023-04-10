# Foobar

Foobar is a Python library for dealing with word pluralization.

## Installation

Follow installation tutorial here for inference:
https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md



```bash
sudo apt-get install cmake python3-dev python3-setuptools
sudo apt-get install libxml2-dev libxslt-dev python-dev
 
pip install cython
pip install dronekit 
```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
