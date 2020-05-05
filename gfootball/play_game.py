# coding=utf-8
# Copyright 2019 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Script allowing to play the game by multiple players."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags
from absl import logging


from gfootball.env import config
from gfootball.env import football_env

import time

from utils_custom.shared_info import get_shared_info_object

FLAGS = flags.FLAGS

flags.DEFINE_string('players', 'keyboard:left_players=1',
                    'Semicolon separated list of players, single keyboard '
                    'player on the left by default')
flags.DEFINE_string('level', '', 'Level to play')
flags.DEFINE_enum('action_set', 'default', ['default', 'full'], 'Action set')
flags.DEFINE_bool('real_time', False,
                  'If true, environment will slow down so humans can play.')
flags.DEFINE_bool('render', True, 'Whether to do game rendering.')

flags.DEFINE_integer('running_time', -1, 'How long to run play_game.py. If running_time=-1, the game runs until the user stops it.')
flags.DEFINE_bool('save_info', False,
                  'If true, save SharedInfo from the environment for every environment step. (be careful: agent step != environment step)')
flags.DEFINE_string('dataset_path', '/home/ionutc/Documents/Repositories/Dissertation-2020/datasets/raw_dataset',
                    'The path where the frames and their observations will be saved.')


def main(_):
  players = FLAGS.players.split(';') if FLAGS.players else ''
  assert not (any(['agent' in player for player in players])
             ), ('Player type \'agent\' can not be used with play_game.')
  cfg = config.Config({
      'action_set': FLAGS.action_set,
      'dump_full_episodes': True,
      'players': players,
      'real_time': FLAGS.real_time,
  })
  if FLAGS.level:
    cfg['level'] = FLAGS.level
  env = football_env.FootballEnv(cfg)
  if FLAGS.render:
    env.render()
  env.reset()

  shared_info = get_shared_info_object(FLAGS.dataset_path, FLAGS.save_info, FLAGS.render)
  start_time = time.time()
  try:
    while True:
      _, _, done, _ = env.step([], save_info=FLAGS.save_info, shared_info=shared_info)
      if done:
        shared_info.save_info_on_disk()

        shared_info = get_shared_info_object(FLAGS.dataset_path, FLAGS.save_info, FLAGS.render)
        env.reset()

        elapsed_time = time.time() - start_time
        logging.info('Time elapsed: {}'.format(elapsed_time))

        if FLAGS.running_time > -1 and elapsed_time > FLAGS.running_time:
          break
  except KeyboardInterrupt:
    logging.warning('Game stopped, writing dump...')
    env.write_dump('shutdown')
    exit(1)


if __name__ == '__main__':
  app.run(main)
