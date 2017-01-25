#!/usr/bin/env bash
cd ~/tensorflow

python3 tensorflow/examples/image_retraining/retrain.py \
--bottleneck_dir=/nvme/stage1_data/transfer_trial/bottlenecks \
--how_many_training_steps 50000 \
--model_dir=/nvme/stage1_data/transfer_trial/inception \
--output_graph=/nvme/stage1_data/transfer_trial/retrained_graph.pb \
--output_labels=/nvme/stage1_data/transfer_trial/retrained_labels.txt \
--learning_rate=0.001 \
--image_dir /nvme/stage1_data/transfer_trial/images