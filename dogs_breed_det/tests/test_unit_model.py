# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - 2019 Karlsruhe Institute of Technology - Steinbuch Centre for Computing
# This code is distributed under the MIT License
# Please, see the LICENSE file
#
"""
Created on Sat Aug 10 08:47:51 2019

@author: vykozlov
"""
import unittest
import numpy as np
import dogs_breed_det.models.model as dog_model

from keras import backend as K

debug = True

class TestModelMethods(unittest.TestCase):
    def test_model_variables(self):
        network = 'Resnet50'
        num_classes = 133

        train_tensor = np.random.normal(size=(2, 1, 1, 2048))
        #train_tensor = np.random.normal(size=(2, 224, 224, 3))  # full ResNet 
        label_tensor = np.random.normal(size=(2, num_classes))

        model = dog_model.build_model(network, num_classes)
        print(model.trainable_weights)

        before = K.get_session().run(model.trainable_weights)
        model.fit(train_tensor,
                  label_tensor,
                  epochs=1,
                  # need batch_size>=2, e.g. for the case of BatchNormalization
                  batch_size=2,
                  verbose=1)
        after = K.get_session().run(model.trainable_weights)

        # Make sure something changed.
        i = 0
        for b, a in zip(before, after):
            if debug:
                print("[DEBUG] {} : ".format(model.trainable_weights[i]))
                i += 1
                if (b != a).any() and debug:
                    print(" * ok, training (values are updated)")
                else:
                    print(" * !!! values didn't change, not training? !!!")
                    print(" * Before: {} : ".format(b))
                    print("")
                    print(" * After: {} : ".format(a))

            # Make sure something changed.
            assert (b != a).any()

#test_model_variables()

if __name__ == '__main__':
    unittest.main()
