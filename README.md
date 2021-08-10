## Animating the London Underground tube map!

The tube map is an excellent way of explaining pathfinding algorithms. In fact, it is often used in company interviews as a way of testing the candidate's knowledge of graph data structures and shortest path algorithms.

This project aims to visualise algorithms such as BFS, DFS, Dijkstra and A* using the tube map.

[![How do travel planners work? on YouTube by Timothy Langer](https://img.youtube.com/vi/wLNai11U2tI/0.jpg)](https://www.youtube.com/watch?v=wLNai11U2tI)

Press the thumbnail above to view the final video on YouTube, or [click here.](https://www.youtube.com/watch?v=wLNai11U2tI)</small>

### The internals

I converted the [official tube map provided by TfL](https://content.tfl.gov.uk/standard-tube-map.pdf) into an SVG file and removed clutter such as DLR, Trams and Thameslink that do not belong on a map of the London Underground.
Next, I individually selected each station in the SVG in Inkscape and gave it a unique ID. In this case, I based the ID off the three-letter station codes that TfL uses.

In addition, I downloaded the average inter-station travel times from a TfL FOI request provided in XLSX format. This was converted into a CSV for simpler parsing.

[`tube.py`](https://github.com/ZeevoX/animated-london-tube/blob/main/tube.py) is a wrapper for importing the aforementioned SVG and inter-station travel times and provides methods for individually showing / hiding stations on the map as well as changing their opacity.

In [`main.py`](https://github.com/ZeevoX/animated-london-tube/blob/main/tube.py) are the actual pathfinding algorithms. During their execution, they show/hide visited stations and write to an SVG file for every frame.

The SVG files can then be rasterised and formed into an MP4 using `ffmpeg` to create a visualisation of the pathfinding algorithms at work.
