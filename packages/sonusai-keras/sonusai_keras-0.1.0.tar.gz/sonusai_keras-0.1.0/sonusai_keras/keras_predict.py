"""sonusai keras_predict

usage: keras_predict [-hvr] [-i MIXID] (-m MODEL) (-w KMODEL) [-b BATCH] [-t TSTEPS] INPUT ...

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -i MIXID, --mixid MIXID         Mixture ID(s) to generate if input is a mixture database. [default: *].
    -m MODEL, --model MODEL         Python model file.
    -w KMODEL, --weights KMODEL     Keras model weights file.
    -b BATCH, --batch BATCH         Batch size.
    -t TSTEPS, --tsteps TSTEPS      Timesteps.
    -r, --reset                     Reset model between each file.

Run prediction on a trained Keras model defined by a SonusAI Keras Python model file using SonusAI genft or WAV data.

Inputs:
    MODEL       A SonusAI Python model file with build and/or hypermodel functions.
    KMODEL      A Keras model weights file (or model file with weights).
    INPUT       The input data must be one of the following:
                * Single WAV file or glob of WAV files
                  Using the given model, generate feature data and run prediction. A model file must be
                  provided. The MIXID is ignored.

                * directory
                  Using the given SonusAI mixture database directory, generate feature and truth data if not found.
                  Run prediction. The MIXID is required.

Outputs the following to kpredict-<TIMESTAMP> directory:
    <id>.h5
        dataset:    predict
    keras_predict.log

"""
import signal
from typing import Any

from sonusai.mixture import Feature
from sonusai.mixture import Predict


def signal_handler(_sig, _frame):
    import sys

    from sonusai import logger

    logger.info('Canceled due to keyboard interrupt')
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def main() -> None:
    import sonusai_keras
    from docopt import docopt
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai_keras.__version__, options_first=True)

    verbose = args['--verbose']
    mixids = args['--mixid']
    model_name = args['--model']
    weights_name = args['--weights']
    batch_size = args['--batch']
    timesteps = args['--tsteps']
    reset = args['--reset']
    input_name = args['INPUT']

    from os import makedirs
    from os.path import basename
    from os.path import isdir
    from os.path import isfile
    from os.path import join
    from os.path import splitext

    import h5py
    import keras_tuner as kt
    import tensorflow as tf
    from keras import backend as kb
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import logger
    from sonusai import update_console_handler
    from sonusai.mixture import MixtureDatabase
    from sonusai.mixture import get_feature_from_audio
    from sonusai.mixture import read_audio
    from sonusai.utils import create_ts_name
    from sonusai.utils import get_frames_per_batch
    from sonusai.utils import reshape_outputs

    from sonusai_keras.data_generator import KerasFromH5
    from sonusai_keras.utils import import_and_check_keras_model

    if batch_size is not None:
        batch_size = int(batch_size)

    if timesteps is not None:
        timesteps = int(timesteps)

    output_dir = create_ts_name('kpredict')
    makedirs(output_dir, exist_ok=True)

    # Setup logging file
    create_file_handler(join(output_dir, 'keras_predict.log'))
    update_console_handler(verbose)
    initial_log_messages('keras_predict', sonusai_keras.__version__)

    logger.info(f'tensorflow    {tf.__version__}')
    logger.info(f'keras         {tf.keras.__version__}')
    logger.info('')

    hypermodel = import_and_check_keras_model(model_name=model_name,
                                              weights_name=weights_name,
                                              timesteps=timesteps,
                                              batch_size=batch_size)
    built_model = hypermodel.build_model(kt.HyperParameters())

    frames_per_batch = get_frames_per_batch(hypermodel.batch_size, hypermodel.timesteps)

    kb.clear_session()
    logger.info('')
    built_model.summary(print_fn=logger.info)
    logger.info('')
    logger.info(f'feature       {hypermodel.feature}')
    logger.info(f'num_classes   {hypermodel.num_classes}')
    logger.info(f'batch_size    {hypermodel.batch_size}')
    logger.info(f'timesteps     {hypermodel.timesteps}')
    logger.info(f'flatten       {hypermodel.flatten}')
    logger.info(f'add1ch        {hypermodel.add1ch}')
    logger.info(f'truth_mutex   {hypermodel.truth_mutex}')
    logger.info(f'input_shape   {hypermodel.input_shape}')
    logger.info('')

    logger.info(f'Loading weights from {weights_name}')
    built_model.load_weights(weights_name)

    logger.info('')
    if len(input_name) == 1 and isdir(input_name[0]):
        input_name = input_name[0]
        logger.info(f'Load mixture database from {input_name}')
        mixdb = MixtureDatabase(input_name)

        if mixdb.feature != hypermodel.feature:
            logger.exception(f'Feature in mixture database does not match feature in model')
            raise SystemExit(1)

        mixids = mixdb.mixids_to_list(mixids)
        if reset:
            # reset mode cycles through each file one at a time
            for mixid in mixids:
                feature, _ = mixdb.mixture_ft(mixid)

                feature, predict = _pad_and_predict(hypermodel=hypermodel,
                                                    built_model=built_model,
                                                    feature=feature,
                                                    frames_per_batch=frames_per_batch)

                output_name = join(output_dir, mixdb.mixtures[mixid].name)
                with h5py.File(output_name, 'a') as f:
                    if 'predict' in f:
                        del f['predict']
                    f.create_dataset(name='predict', data=predict)
        else:
            # Run all data at once using a data generator
            feature = KerasFromH5(mixdb=mixdb,
                                  mixids=mixids,
                                  batch_size=hypermodel.batch_size,
                                  timesteps=hypermodel.timesteps,
                                  flatten=hypermodel.flatten,
                                  add1ch=hypermodel.add1ch)

            predict = built_model.predict(feature, batch_size=hypermodel.batch_size, verbose=1)
            predict, _ = reshape_outputs(predict=predict, timesteps=hypermodel.timesteps)

            # Write data to separate files
            for idx, mixid in enumerate(mixids):
                output_name = join(output_dir, mixdb.mixtures[mixid].name)
                with h5py.File(output_name, 'a') as f:
                    if 'predict' in f:
                        del f['predict']
                    f.create_dataset('predict', data=predict[feature.file_indices[idx]])

        logger.info(f'Saved results to {output_dir}')
        return

    if not all(isfile(file) and splitext(file)[1] == '.wav' for file in input_name):
        logger.exception(f'Do not know how to process input from {input_name}')
        raise SystemExit(1)

    logger.info(f'Run prediction on {len(input_name):,} WAV files')
    for file in input_name:
        # Convert WAV to feature data
        audio = read_audio(file)
        feature = get_feature_from_audio(audio=audio, feature_mode=hypermodel.feature)

        feature, predict = _pad_and_predict(hypermodel=hypermodel,
                                            built_model=built_model,
                                            feature=feature,
                                            frames_per_batch=frames_per_batch)

        output_name = join(output_dir, splitext(basename(file))[0] + '.h5')
        with h5py.File(output_name, 'a') as f:
            if 'feature' in f:
                del f['feature']
            f.create_dataset(name='feature', data=feature)

            if 'predict' in f:
                del f['predict']
            f.create_dataset(name='predict', data=predict)

    logger.info(f'Saved results to {output_dir}')


def _pad_and_predict(hypermodel: Any,
                     built_model: Any,
                     feature: Feature,
                     frames_per_batch: int) -> tuple[Feature, Predict]:
    import numpy as np
    from sonusai.utils import reshape_inputs
    from sonusai.utils import reshape_outputs

    frames = feature.shape[0]
    padding = frames_per_batch - frames % frames_per_batch
    feature = np.pad(array=feature, pad_width=((0, padding), (0, 0), (0, 0)))
    feature, _ = reshape_inputs(feature=feature,
                                batch_size=hypermodel.batch_size,
                                timesteps=hypermodel.timesteps,
                                flatten=hypermodel.flatten,
                                add1ch=hypermodel.add1ch)
    predict = built_model.predict(feature, batch_size=hypermodel.batch_size, verbose=1)
    predict, _ = reshape_outputs(predict=predict, timesteps=hypermodel.timesteps)
    predict = predict[:frames, :]
    return feature, predict


if __name__ == '__main__':
    main()
