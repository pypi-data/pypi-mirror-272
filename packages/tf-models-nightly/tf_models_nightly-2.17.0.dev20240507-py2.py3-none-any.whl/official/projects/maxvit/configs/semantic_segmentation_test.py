# Copyright 2024 The TensorFlow Authors. All Rights Reserved.
#
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


from absl.testing import parameterized
import tensorflow as tf, tf_keras

# pylint: disable=unused-import
from official import vision
from official.core import config_definitions as cfg
from official.core import exp_factory
from official.projects.maxvit.configs import semantic_segmentation as exp_cfg


class ImageSegmentationConfigTest(tf.test.TestCase, parameterized.TestCase):

  @parameterized.parameters(('maxvit_seg_pascal',),
                            ('maxvit_seg_coco',))
  def test_semantic_segmentation_configs(self, config_name):
    config = exp_factory.get_exp_config(config_name)
    self.assertIsInstance(config, cfg.ExperimentConfig)
    self.assertIsInstance(config.task, exp_cfg.SemanticSegmentationTask)
    self.assertIsInstance(config.task.train_data, exp_cfg.DataConfig)
    config.validate()
    config.task.train_data.is_training = None
    with self.assertRaises(KeyError):
      config.validate()


if __name__ == '__main__':
  tf.test.main()
