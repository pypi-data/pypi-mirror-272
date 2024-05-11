from importlib import metadata
from os.path import dirname

__version__ = metadata.version(__package__)
BASEDIR = dirname(__file__)

commands_doc = """
   keras_onnx                   Convert a trained Keras model to ONNX
   keras_predict                Run Keras predict on a trained model
   keras_train                  Train a model using Keras
"""
