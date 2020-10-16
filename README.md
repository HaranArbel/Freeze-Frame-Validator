# Freeze-Frame-Validator
This program downloads a set of video files from a given set of urls, runs a filter on each one and exposes its output into a useful format for consumption by other APIs.


## Development Setup

Our code uses Python 3.7.

To run the program please do the following:

- Make sure you have fmpeg CLI tool installed. For more information: https://ffmpeg.org/
- Cd into the project's folder.
- Run freeze_frame_validator.py with the videos urls as arguments, for example:
  ```
  $ python3 freeze_frame_validator.py "https://storage.googleapis.com/hiring_process_data/freeze_frame_input_a.mp4" "https://storage.googleapis.com/hiring_process_data/freeze_frame_input_b.mp4"
  ```
  - 
  
## Testing

Our code currently has two tests, one that runs freeze_frame_validator.py on inputs a and b and one that runs freeze_frame_validator.py on inputs a and c.
The tests validate that the output json objects from freeze_frame_validator.py are the same as the expected outputs. 

To run the tests run:
```
  $ python3 test.py
  ```
