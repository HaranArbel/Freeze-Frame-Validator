import os
import unittest
import json
import sys
from freeze_frame_validator import validate_freeze_frame_videos

dir_path = os.path.dirname(os.path.realpath(__file__))
expected_output_a_b_path = os.path.join(dir_path, 'expected_outputs/expected_output_a_b.txt')
expected_output_a_c_path = os.path.join(dir_path, 'expected_outputs/expected_output_a_c.txt')


class Test(unittest.TestCase):

    def test_input_a_input_b_synced_frame_freeze_wise(self):
        input_a = "https://storage.googleapis.com/hiring_process_data/freeze_frame_input_a.mp4"
        input_b = "https://storage.googleapis.com/hiring_process_data/freeze_frame_input_b.mp4"
        output = json.loads(validate_freeze_frame_videos([input_a, input_b]))
        with open(expected_output_a_b_path) as json_file:
            expected_output = json.load(json_file)
        self.assertTrue(output.items() == expected_output.items())

    def test_input_a_input_c_unsynced_frame_freeze_wise(self):
        input_a = "https://storage.googleapis.com/hiring_process_data/freeze_frame_input_a.mp4"
        input_c = "https://storage.googleapis.com/hiring_process_data/freeze_frame_input_c.mp4"
        output = json.loads(validate_freeze_frame_videos([input_a, input_c]))
        with open(expected_output_a_c_path) as json_file:
            expected_output = json.load(json_file)
        self.assertTrue(output.items() == expected_output.items())


if __name__ == "__main__":
    unittest.main()