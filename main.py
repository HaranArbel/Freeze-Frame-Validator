import sys
import os
import shutil
from utils import run_shell_cmd


dir_path = os.path.dirname(os.path.realpath(__file__))
videos_dir = os.path.join(dir_path, 'videos')
freeze_file_path = os.path.join(dir_path, 'freeze.txt') #todo remove that too during init


def create_new_videos_dir():
    """
    removes the content of the videos dir and creates a new dir in case videos dir does not exist
    :return:
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
    :return:
    """
    cmd = "ffmpeg -i {} {}".format(video_url, out_path)
    return_code, stdout, stderr = run_shell_cmd(cmd)
    if return_code != 0:
        raise Exception("Could not download video")


def filter_freeze_frames(video_path):
    """
    detects freezes in the video file and dumps the results into a text file
    :param video_path: path of the video file
    :return:
    """
    cmd = "ffmpeg -i {} -vf \"freezedetect=n=0.003:d=2,metadata=mode=print:file={}\" -map 0:v:0 -f null -".format(video_path, freeze_file_path)
    run_shell_cmd(cmd)


if __name__ == "__main__":
    videos_dir = create_new_videos_dir()
    for i in range(1, len(sys.argv)):
        video_url = sys.argv[i]
        out_path = os.path.join(videos_dir, 'video{}.mp4'.format(str(i)))
        download_video(video_url, out_path)
        filter_freeze_frames(out_path)
