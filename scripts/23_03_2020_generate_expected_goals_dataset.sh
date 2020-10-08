rm -rf /tmp/dumps
sleep 2

python -m gfootball.play_game \
	--action_set=full \
	--players="bot:left_players=1;bot:right_players=1" \
	--level=academy_corner \
	--running_time=5760

sleep 2
mv /tmp/dumps /mnt/storage0/football_dataset/academy_corner
sleep 2

python -m gfootball.play_game \
	--action_set=full \
	--players="bot:left_players=1;bot:right_players=1" \
	--level=academy_counterattack_easy \
	--running_time=5760

sleep 2
mv /tmp/dumps /mnt/storage0/football_dataset/academy_counterattack_easy
sleep 2

python -m gfootball.play_game \
	--action_set=full \
	--players="bot:left_players=1;bot:right_players=1" \
	--level=academy_counterattack_hard \
	--running_time=5760

sleep 2
mv /tmp/dumps /mnt/storage0/football_dataset/academy_counterattack_hard
sleep 2

python -m gfootball.play_game \
	--action_set=full \
	--players="bot:left_players=1;bot:right_players=1" \
	--level=11_vs_11_competition \
	--running_time=5760

sleep 2
mv /tmp/dumps /mnt/storage0/football_dataset/11_vs_11_competition
sleep 2

python -m gfootball.play_game \
	--action_set=full \
	--players="ppo2_cnn:left_players=1,policy=gfootball_impala_cnn,checkpoint=/home/ionutc/Downloads/11_vs_11_easy_stochastic_v2;ppo2_cnn:right_players=1,policy=gfootball_impala_cnn,checkpoint=/home/ionutc/Downloads/11_vs_11_easy_stochastic_v2" \
	--level=11_vs_11_easy_stochastic \
	--running_time=5760

sleep 2
mv /tmp/dumps /mnt/storage0/football_dataset/11_vs_11_easy_stochastic
