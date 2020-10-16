import sys
from utils import run_shell_cmd


def download_video(video_url, out_path):
    """
    downloads a video file from a given url and saves it in a given path
    :param video_url: the video file's url
    :param out_path: the path where the output file will be saved
    :return:
    """
    cmd = "ffmpeg -i {} {}".format(video_url, out_path)
    run_shell_cmd(cmd)


if __name__ == "__main__":
    video_url = "https://storage.googleapis.com/hiring_process_data/freeze_frame_input_a.mp4"
    out_path = "video1.mp4"
    download_video(video_url, out_path)