import sys
import os
import shutil
from utils import run_shell_cmd
import re
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
videos_dir = os.path.join(dir_path, 'videos')
freeze_file_path = os.path.join(dir_path, 'freeze.txt')


def create_new_videos_dir():
    """
    removes the content of the videos dir and creates a new dir in case videos dir does not exist
    :return: videos dir - the directory in which the videos will be saved after download
    """
    try:
        if os.path.exists(videos_dir):
            shutil.rmtree(videos_dir)
        os.makedirs(videos_dir)
    except Exception as e:
        raise Exception(e)
    return videos_dir


def download_video(video_url, out_path):
    """
    downloads a video file from a given url and saves it in a given path
    :param video_url: the video file's url
    :param out_path: the path where the output file will be saved
    :return: None
    """
    cmd = "ffmpeg -i {} {}".format(video_url, out_path)
    return_code, stdout, stderr = run_shell_cmd(cmd)
    if return_code != 0:
        raise Exception("Could not download video")


def filter_freeze_frames(video_path):
    """
    detects freezes in the video file and dumps the results into a text file
    :param video_path: path of the video file
    :return: None
    """
    cmd = "ffmpeg -i {} -vf \"freezedetect=n=0.003:d=2,metadata=mode=print:file={}\" -map 0:v:0 -f null -".format(video_path, freeze_file_path)
    run_shell_cmd(cmd)


def get_video_duration(video_path):
    """
    runs a shell command to get the duration of the video
    :param video_path: the path of the saved video
    :return: duration - duration of the video in seconds
    """
    cmd = "ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 {}".format(video_path)
    return_code, stdout, stderr = run_shell_cmd(cmd)
    if return_code != 0:
        raise Exception("Could not get video duration.")
    duration = round(float(stdout), 2)
    return duration


def get_valid_periods(duration):
    """
    analyzes the freeze.txt file to extract all the valid video periods
    :param duration: the total duration of the video
    :return: a list of the valid periods of the video
    """
    start_regex, end_regex = '.*freeze_start=(.*)\n', '.*freeze_end=(.*)\n'
    valid_periods = []
    valid_start = 0
    is_in_valid_period = True
    with open(freeze_file_path) as file:
        for line in file:
            start = re.search(start_regex, line)
            end = re.search(end_regex, line)
            if start:
                is_in_valid_period = False
                valid_end = round(float(start.group(1)), 2)
                if valid_start != valid_end: # todo: do we want to ignore intervals of length 0?
                    valid_periods.append([valid_start, valid_end])
            elif end:
                is_in_valid_period = True
                valid_start = round(float(end.group(1)), 2)
    if is_in_valid_period and valid_start != duration:
        valid_periods.append([valid_start, duration])

    return valid_periods


def get_total_valid_duration(valid_periods):
    """
    Returns the total valid duration of a video
    :param valid_periods: list of all valid periods of a video
    :return: teh totel valid duration
    """
    total_valid_duration = 0
    for i in range(len(valid_periods)):
        total_valid_duration += valid_periods[i][1] - valid_periods[i][0]
    return total_valid_duration


def get_longest_valid_period(valid_periods):
    """
    returns the longest valid period of all valid periods of a video
    :param valid_periods: list of a video's valid periods
    :return: longest valid period
    """
    longest_valid_period = max(valid_periods, key=lambda interval: interval[1] - interval[0])
    return round(longest_valid_period[1] - longest_valid_period[0], 2)


def get_valid_video_percentage(total_valid_duration, duration):
    """

    :param total_valid_duration: the total duration of valid video periods
    :param duration: the total duration of the video
    :return: the total valid video percentage
    """
    return round(total_valid_duration / duration * 100, 2)


def is_all_videos_synced(videos):
    """
    :param videos_periods: a list containing each video's valid periods list
    :return: returns true if all videos have the same amount of valid periods, and each period's corresponding 'start'
    and 'end' across all videos are no more than 500ms apart
    """
    videos_periods = [video["valid_periods"] for video in videos]
    if not videos_periods:
        return True
    n = len(videos_periods[0])
    for video_periods in videos_periods:
        if len(video_periods) != n:
            return False

    start_times = sorted([video_period[0] for video_period in video_periods])
    end_times = sorted([video_period[1] for video_period in videos_periods])

    for i in range(1, n):
        if start_times[i] - start_times[i - 1] > 0.5 or end_times[i] - end_times[i - 1] > 0.5:
            return False

    return True


def validate_freeze_frame_videos(video_urls):
    """
    validates that the given set of videos is synced frame freeze wise. Returns the results of the analysis in the form
    of a json object
    :param video_urls: a set of video urls to run
    :return:
    """
    res = {}
    videos_dir = create_new_videos_dir()
    for i in range(len(video_urls)):
        video = {}
        out_path = os.path.join(videos_dir, 'video{}.mp4'.format(str(i + 1)))
        download_video(video_urls[i], out_path)
        filter_freeze_frames(out_path)
        duration = get_video_duration(out_path)
        valid_periods = get_valid_periods(duration)
        total_valid_duration = get_total_valid_duration(valid_periods)
        video["longest_valid_period"] = get_longest_valid_period(valid_periods)
        video["valid_video_percentage"] = get_valid_video_percentage(total_valid_duration, duration)
        video["valid_periods"] = valid_periods
        if "videos" in res:
            res["videos"].append(video)
        else:
            res["videos"] = [video]
    res["all_videos_freeze_frame_synced"] = is_all_videos_synced(res["videos"])

    json_object = json.dumps(res, indent=4)
    return json_object


if __name__ == "__main__":
    validate_freeze_frame_videos(sys.argv[1:])
