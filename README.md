# integrated_seams

## Setup
```bash
python3 -m venv venv
pip install -r requirements.txt
```

## Run
```bash
python app.py
```
Then go to http://127.0.0.1:5000/ on chrome

## How it works
When you upload an image it seam carves the image to precompute the seams, seams are then stored as pickle files.
The pickle files then can be used for significantly faster content aware image resizing.
Similar approach applied to video, except video is broken down into frames and seam carved per frame.
Note: Video seam carving scripts have been added to the repo but they still need to be integrated into gui

## TODO
- Seam Carving for Videos has been implemented as a python script but does still need work to be integrated into gui

