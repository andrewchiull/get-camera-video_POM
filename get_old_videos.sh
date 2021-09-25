#!/bin/bash
date_str=$(date "+%Y_%m%d_%H%M%S")
echo $date_str
echo 'Run: /home/mie/get-camera-video_POM/get_old_videos.py'

cd /home/mie/get-camera-video_POM
export PATH=/home/mie/get-camera-video_POM:$PATH
source /home/mie/.pyenv/versions/3.8.8/envs/selenium/bin/activate
python3 -V
python3 ./get_old_videos.py >> ./logs/get-camera-video_POM_get_old_videos_$date_str.log 2>&1

date_str=$(date "+%Y_%m%d_%H%M%S")
echo $date_str
echo 'End'
echo ''