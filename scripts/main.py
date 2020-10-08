import os

file_path = '01_03_2020_generate_expected_goals_dataset.sh'
dumps_path = '/mnt/storage0/dump_5_01_2020/dumps'

dumps = sorted([dump for dump in os.listdir(dumps_path) if dump[-5:] == '.dump'])

with open(file_path, 'w') as f:
    for i, dump in enumerate(dumps):
        f.write('python -m gfootball.replay --trace_file={}\n'.format(os.path.join(dumps_path, dump)))
        f.write('sleep 5\n')

# import pdb; pdb.set_trace()
