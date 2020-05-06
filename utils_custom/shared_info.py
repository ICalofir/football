import datetime
import json
import os
import numpy as np
from absl import logging
from PIL import Image

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
        observation['ball']['x'] = shared_info.ball_position[0]
        observation['ball']['y'] = shared_info.ball_position[1]
        observation['ball']['z'] = shared_info.ball_position[2]

        observation['ball_owned_team'] = shared_info.ball_owned_team # -1 = ball not owned, 0 = left team, 1 = right team
        observation['ball_owned_player'] = shared_info.ball_owned_player

        # team
        teams = ['left_team', 'right_team']
        for team in teams:
            observation[team] = {}
            for i, player in enumerate(shared_info.left_team):
                now_player = 'player_{}'.format(i)
                observation[team][now_player] = {}
                observation[team][now_player]['x'] = player.position[0]
                observation[team][now_player]['y'] = player.position[1]
                observation[team][now_player]['z'] = player.position[2]

        # general
        observation['is_in_play'] = shared_info.is_in_play
        # game_mode: e_GameMode_Normal,
        #            e_GameMode_KickOff,
        #            e_GameMode_GoalKick,
        #            e_GameMode_FreeKick,
        #            e_GameMode_Corner,
        #            e_GameMode_ThrowIn,
        #            e_GameMode_Penalty
        observation['game_mode'] = shared_info.game_mode.name

        return observation

    def save_info(self, info, frame):
        step = info.shared_info_frames[0].step
        self._frames.append(frame)

        dudu_step = [info.shared_info_frames[i].step for i in range(10)]
        print('Step: {}'.format(dudu_step))

        for i, shared_info in enumerate(info.shared_info_frames):
            observation = self._get_observation(shared_info)
            self._observations['step_{}'.format(self._real_steps)] = observation

            self._real_steps += 1

        print(len(self._frames))

        if self._real_steps % 200 == 0:
            logging.info('Save info for frames at step: {}'.format(self._real_steps))

    def save_info_on_disk(self):
        for i, frame in enumerate(self._frames):
            img = Image.fromarray(frame)
            img.save(os.path.join(self._frames_path, 'frame_{}.png'.format(i)))

            if i % 200 == 0:
                logging.info('Frames: {}/{}'.format(i, len(self._frames)))

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