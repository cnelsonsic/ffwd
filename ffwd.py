# Reads an input file with directives about where to fast forward.
import json
directives = json.loads(open("videos.json", 'r').read())

outfiles = []
starttime = 0
endtime = 0
speed = 1
for directive in directives:
    filename = directive.get('file')
    # (times are relative to the filename, and in seconds.)
    # Check if key is present, if not, use any previous setting.
    # If start is missing, use previous end.
    if "start" in directive:
        starttime = directive['start']
    else:
        starttime = endtime

    if "end" in directive:
        endtime = directive['end']
    if "speed" in directive:
        speed = directive['speed']

    duration = int(endtime) - int(starttime)
    output = '-'.join((filename, str(starttime), str(endtime), str(speed), ".mp4"))
    outfiles.append(output)

    # For each directive, re-encode the source videos to little snippets, and apply whatever speed directive.
    print("ffmpeg -y -ss {starttime} -i {filename} -t {duration} -q:v 1 -an -vcodec mpeg4 {output}".format(starttime=starttime, filename=filename, duration=duration, speed=speed, output="clip"+output))
    print("ffmpeg -y -i {filename} -filter:v \"setpts={speed}*PTS\" -an {output}".format(starttime=starttime, filename="clip"+output, duration=duration, speed=speed, output=output))
    print("rm clip"+output)

# Optional: Overlay a "FFWD" text in the corner for fun.
# TODO: If there's a gap, it should ramp up linearly.

# Concatenate them all back together.
with open(".finalvids.txt", 'w') as f:
    for line in outfiles:
        f.write("file '{}'\n".format(line))
print("ffmpeg -y -f concat -i .finalvids.txt -c copy final.mp4")
print("rm .finalvids.txt")

# Clean up
for line in outfiles:
    print("rm "+ line)
