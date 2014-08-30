# Reads an input file with directives about where to fast forward.
with open("videos.txt", 'r') as f:
    directives = f.readlines()

outfiles = []
for directive in directives:
    directive = directive.strip()
    # Filename:Starttime,endtime,speed
    # (times are relative to the filename, and in seconds.)
    filename, times = directive.split(":")
    starttime, endtime, speed = times.split(",")
    duration = int(endtime) - int(starttime)
    output = '-'.join((filename, starttime, endtime, speed, ".mp4"))
    outfiles.append(output)

    # For each directive, re-encode the source videos to little snippets, and apply whatever speed directive.
    print("ffmpeg -y -ss {starttime} -i {filename} -t {duration} -q:v 1 -an -vcodec mpeg4 {output}".format(starttime=starttime, filename=filename, duration=duration, speed=speed, output="clip"+output))
    print("ffmpeg -y -i {filename} -filter:v \"setpts={speed}*PTS\" -an {output}".format(starttime=starttime, filename="clip"+output, duration=duration, speed=speed, output=output))
    print("rm clip"+output)

# Optional: Overlay a "FFWD" text in the corner for fun.

# Concatenate them all back together.
with open(".finalvids.txt", 'w') as f:
    for line in outfiles:
        f.write("file '{}'\n".format(line))
print("ffmpeg -y -f concat -i .finalvids.txt -c copy final.mp4")
print("rm .finalvids.txt")

# Clean up
for line in outfiles:
    print("rm "+ line)
