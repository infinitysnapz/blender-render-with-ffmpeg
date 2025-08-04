# blender-renderwithffmpeg
Creates a PNG image sequence, then converts it to a video via FFmpeg.

Based on https://github.com/Ulf3000/blender-render-to-ffmpeg/

The aim of this extension is to implement support for exporting to novel file formats that Blender doesn't handle - i.e Cineform,
It renders to intermediate .png image sequence in a temp folder and then uses FFmpeg to convert it to a desired format as defined in the extension's 'Input' box
The script assumes that you have FFmpeg in your path variable. Untested on Linux and Mac

## Usage
Basic FFmpeg knowledge is required. the 'Input' box takes FFmpeg output file options - for example:
`-c:v libx264 -crf 23 -vf scale=1280:720` to convert to a 1280x720 H.264 file.
