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
    #   ffmpeg -i SOURCE.mp4 -ss STARTTIMEs -t DURATIONs -filter:v "setpts=SPEEDMULTIPLIER*PTS" -acodec copy -vcodec copy OUTPUT.mp4
    #       -ss and -t are either hh:mm:ss.sss or whole seconds.
    #       SPEEDMULTIPLIER is a backwards. 0.5 to speed up, 2.0 to slow down.
    print("ffmpeg -ss {starttime} -i {filename} -t {duration} -filter:v setpts={speed}*PTS -acodec copy -vcodec copy {output}".format(starttime=starttime, filename=filename, duration=duration, speed=speed, output=output))

# Optional: Overlay a "FFWD" text in the corner for fun.

# Concatenate them all back together.
