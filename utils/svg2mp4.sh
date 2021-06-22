#!/bin/bash
ffmpeg -r 10 -i out/frames/%05d.svg -vf format=yuv420p out/anim.mp4
