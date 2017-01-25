#!/usr/bin/env bash

# Calls TensorFlow demo script for transfer learning on Inception-v3
# Requires large download and pre-processing on first run.
# DEBUG runs only 1000 training steps at 0.003 learning rate
#
# See:
# https://research.googleblog.com/2016/03/train-your-own-image-classifier-with.html
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/examples/image_retraining/retrain.py

cd ~/tensorflow

python3 tensorflow/examples/image_retraining/retrain.py \
--bottleneck_dir=/nvme/stage1_data/transfer_trial/bottlenecks \
--how_many_training_steps 1000 \
--model_dir=/nvme/stage1_data/transfer_trial/inception \
--output_graph=/nvme/stage1_data/transfer_trial/retrained_graph.pb \
--output_labels=/nvme/stage1_data/transfer_trial/retrained_labels.txt \
--learning_rate=0.003 \
--image_dir /nvme/stage1_data/transfer_trial/images
