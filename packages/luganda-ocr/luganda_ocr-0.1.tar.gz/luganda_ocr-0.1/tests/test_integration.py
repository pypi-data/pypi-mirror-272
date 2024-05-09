import os
import unittest
from luganda_ocr.utils import load_pretrained_model, batch_prediction

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.model_path = "luganda_ocr/models/sentenceModel.h5"
        self.image_folder ="/home/beijuka/luganda_ocr/tests/trial" 
    def test_batch_prediction(self):
        model = load_pretrained_model(self.model_path)
        predictions = batch_prediction(model, self.image_folder)

