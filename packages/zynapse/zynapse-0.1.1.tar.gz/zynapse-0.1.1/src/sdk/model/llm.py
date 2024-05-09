# import torch
from transformers import AutoModelForSequenceClassification

class Model(AutoModelForSequenceClassification):
    def __init__(self, model_name_or_path):
        super(Model, self).__init__(model_name_or_path)