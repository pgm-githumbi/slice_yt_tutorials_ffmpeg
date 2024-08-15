A powershell script that takes long yt videos (or any videos) and splits it to multiple 
short videos based on a timestamp text file.<br/> <br/>

The timestamp file contains a list of newline separated strings.\
Each string contains a timestamp of the form HH:MM:SS somewhere in it.\
Remainder of the string is used as the video filename.<br/> <br/>
```
py cut.py --input_file "D:\my_video.mp4" --output_folder "D:\test_folder" --timestamps "D:\timestamps2.txt"
```

```
usage: cut.py [-h] --input_file INPUT_FILE --timestamps TIMESTAMPS
              [--output_folder OUTPUT_FOLDER]

cut yt tutorial into segments based on a timestamps text file.

options:
  -h, --help            show this help message and exit
  --input_file INPUT_FILE
                        Path to the video file to be cut into segments     
  --timestamps TIMESTAMPS
                        .txt file containing newline separate strings      
                        containing HH:MM:SS timestamps and a title for each
                        video. The input-file will be split into the number
                        of lines with a valid timestamp in this file (if   
                        enough video is available)
  --output_folder OUTPUT_FOLDER
                        Where to put the cut up videos.
```
Made for windows.
