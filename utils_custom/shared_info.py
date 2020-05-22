import datetime
import json
import os
import time
import numpy as np
from absl import logging
from PIL import Image

from utils_custom.constants_custom import *

class SharedInfo():
    def __init__(self, dataset_path, dump_name):
        """
        The init class.

        Arguments:
            dataset_path (str): the root path of the dataset
            dump_name (str): the name of the directory where the frames and the
                             observation for each frame will be saved
        """
        self._dataset_path = dataset_path
        self._dump_name = dump_name

        self._dump_path = os.path.join(self._dataset_path, self._dump_name)
        os.makedirs(self._dump_path)

        self._frames_path = os.path.join(self._dump_path, 'frames')
        os.makedirs(self._frames_path)

        self._observations_path = os.path.join(self._dump_path, 'observations.json')
        self._observations = {}

        self._frames = []

        self._real_steps = 0

    def _get_observation(self, shared_info):
        observation = {}

        # ball
        observation['ball'] = {}

        observation['ball']['position'] = {}
        observation['ball']['position']['x'] = shared_info.ball_position[0] * X_FIELD_SCALE
        observation['ball']['position']['y'] = shared_info.ball_position[1] * Y_FIELD_SCALE
        observation['ball']['position']['z'] = shared_info.ball_position[2] * Z_FIELD_SCALE

        observation['ball']['position_projected'] = {}
        observation['ball']['position_projected']['x'] = START_X + shared_info.ball_projected_position[0] * X_FIELD_SCALE * EFFECTIVE_X * 0.01
        observation['ball']['position_projected']['y'] = START_Y + shared_info.ball_projected_position[1] * Y_FIELD_SCALE * EFFECTIVE_Y * 0.01

        observation['ball']['direction'] = {}
        observation['ball']['direction']['x'] = shared_info.ball_direction[0] * X_FIELD_SCALE
        observation['ball']['direction']['y'] = shared_info.ball_direction[1] * Y_FIELD_SCALE
        observation['ball']['direction']['z'] = shared_info.ball_direction[2] * Z_FIELD_SCALE

        observation['ball']['owned_team'] = shared_info.ball_owned_team # -1 = ball not owned, 0 = left team, 1 = right team
        observation['ball']['owned_player'] = shared_info.ball_owned_player

        # team
        teams = ['left_team', 'right_team']
        for team in teams:
            observation[team] = {}

            shared_info_team = shared_info.left_team
            shared_info_team_controller = shared_info.left_controllers[0]
            shared_info_team_pressed_action = shared_info.left_team_pressed_action
            if team == 'right_team':
                shared_info_team = shared_info.right_team
                shared_info_team_controller = shared_info.right_controllers[0]
                shared_info_team_pressed_action = shared_info.right_team_pressed_action

            observation[team]['controlled_player'] = shared_info_team_controller.controlled_player
            observation[team]['pressed_action'] = shared_info_team_pressed_action

            for i, player in enumerate(shared_info_team):
                now_player = 'player_{}'.format(i)
                observation[team][now_player] = {}

                observation[team][now_player]['position'] = {}
                observation[team][now_player]['position']['x'] = player.position[0] * X_FIELD_SCALE
                observation[team][now_player]['position']['y'] = player.position[1] * Y_FIELD_SCALE
                observation[team][now_player]['position']['z'] = player.position[2] * Z_FIELD_SCALE

                observation[team][now_player]['position_projected'] = {}
                observation[team][now_player]['position_projected']['x'] = START_X + player.projected_position[0] * X_FIELD_SCALE * EFFECTIVE_X * 0.01
                observation[team][now_player]['position_projected']['y'] = START_Y + player.projected_position[1] * Y_FIELD_SCALE * EFFECTIVE_Y * 0.01

        # general
        observation['frame_name'] = 'frame_{}'.format(len(self._frames) - 1)
        observation['game_mode'] = shared_info.game_mode.name
        observation['is_in_play'] = shared_info.is_in_play
        observation['score'] = (shared_info.left_goals, shared_info.right_goals)

        observation['last_touch_team_id'] = shared_info.last_touch_team_id
        observation['last_touch_player_id'] = shared_info.last_touch_player_id

        observation['player_touch_ball'] = shared_info.player_touch_ball
        observation['team_touch_ball'] = shared_info.team_touch_ball

        observation['is_goal_scored'] = shared_info.is_goal_scored

        return observation

    def save_info(self, info, frame):
        self._frames.append(frame)

        for shared_info in info.shared_info_frames:
            observation = self._get_observation(shared_info)
            self._observations['step_{}'.format(self._real_steps)] = observation

            self._real_steps += 1

        if self._real_steps % 200 == 0:
            logging.info('Save info for frames at step: {}'.format(self._real_steps))

    def save_info_on_disk(self):
        start_time = time.time()
        for i, frame in enumerate(self._frames):
            img = Image.fromarray(frame)
            img.save(os.path.join(self._frames_path, 'frame_{}.png'.format(i)))

            if i % 200 == 0:
                logging.info('Frames: {}/{}'.format(i, len(self._frames)))
        logging.info('Total elapsed time: {} s'.format(time.time() - start_time))

        json.dump(self._observations, open(self._observations_path, 'w'))

def get_shared_info_object(dataset_path, save_info, render):
    shared_info = None
    if save_info:
        if not render:
            logging.error('Please enable game rendering!')
            raise Exception('Render option is false!')

        if not os.path.isdir(dataset_path):
            os.makedirs(dataset_path, exist_ok=True)

        dump_name = 'dump_{}'.format(datetime.datetime.now().strftime('%Y%m%d-%H%M%S%f'))
        shared_info = SharedInfo(dataset_path, dump_name)

    return shared_info
