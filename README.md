[![Build Status](https://travis-ci.org/iamlordaubrey/photo-uploader.svg?branch=master)](https://travis-ci.org/iamlordaubrey/photo-uploader)

# photo-uploader
A simple flask app for uploading images. Images are not saved (not locally, not anywhere).


##### To run locally:
```commandline
pip install -r requirements.txt

python image_uploader/app.py
```

##### To run tests:
Without pytest:
```commandline
python -m unittest discover
```

Using pytest:
```commandline
python -m pytest
```

##### Demo:
The app is live and demoed [here](https://img-uploader.herokuapp.com)
