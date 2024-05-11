from typing import Any


def keras_onnx(model_name: str,
               weight_name: str,
               timesteps: int = None,
               batch_size: int = None,
               output_dir: str = None) -> None:
    """Load a Keras model, convert it to ONNX, and save the resulting ONNX model.
    """
    from os.path import basename
    from os.path import dirname
    from os.path import join
    from os.path import splitext

    import h5py
    import keras_tuner as kt

    from sonusai import logger
    from sonusai.utils import import_module

    if output_dir is None:
        output_dir = dirname(model_name)

    with h5py.File(weight_name, 'r') as f:
        feature = f.attrs['sonusai_feature']
        num_classes = int(f.attrs['sonusai_num_classes'])

    model = import_module(model_name)
    model_base = basename(model_name)
    model_root, _ = splitext(model_base)
    base_name = join(output_dir, model_root)

    # Build default model to check overrides
    timesteps = check_keras_overrides(model, feature, num_classes, timesteps, batch_size)

    try:
        hypermodel = model.MyHyperModel(feature=feature,
                                        num_classes=num_classes,
                                        timesteps=timesteps,
                                        batch_size=batch_size)
        built_model = hypermodel.build_model(kt.HyperParameters())
    except Exception as e:
        logger.exception(f'Error: build_model() in {model_base} failed: {e}.')
        raise SystemExit(1)

    print('')
    print(f'timesteps               {timesteps}')
    print(f'batch_size              {batch_size}')
    print(f'hypermodel.timesteps    {hypermodel.timesteps}')
    print(f'hypermodel.batch_size   {hypermodel.batch_size}')
    print('')

    # Create and save ONNX model with specified batch and timestep sizes
    onnx_name = base_name + '.onnx'
    try:
        create_onnx_from_keras(keras_model=built_model,
                               is_flattened=hypermodel.flatten,
                               has_timestep=(hypermodel.timesteps > 0),
                               has_channel=hypermodel.add1ch,
                               is_mutex=hypermodel.truth_mutex,
                               feature=feature,
                               filename=onnx_name)
    except Exception as e:
        logger.warning(f'Failed to create ONNX model, no file saved: {e}.')
    logger.info(f'Wrote ONNX model to {onnx_name}')

    # Create and save onnx model with timesteps, batch = 1
    timesteps = hypermodel.timesteps
    if timesteps > 0:
        # only set to 1 if nonzero (exists)
        timesteps = 1
    hypermodel = model.MyHyperModel(feature=feature,
                                    num_classes=num_classes,
                                    timesteps=timesteps,
                                    batch_size=1)
    built_model = hypermodel.build_model(kt.HyperParameters())
    # load weights from previously saved HDF5
    built_model.load_weights(weight_name)
    # save a prediction version of model to base_name-pred-onnx
    onnx_name = base_name + '-b1.onnx'
    create_onnx_from_keras(keras_model=built_model,
                           is_flattened=hypermodel.flatten,
                           has_timestep=(hypermodel.timesteps > 0),
                           has_channel=hypermodel.add1ch,
                           is_mutex=hypermodel.truth_mutex,
                           feature=feature,
                           filename=onnx_name)
    logger.info(f'Wrote inference ONNX model to {onnx_name}')


def check_keras_overrides(model: Any,
                          feature: str,
                          num_classes: int,
                          timesteps: int = None,
                          batch_size: int = None) -> int:
    from sonusai import logger

    try:
        hypermodel = model.MyHyperModel()
    except Exception as e:
        logger.exception(f'Error: build_model() failed: {e}.')
        raise SystemExit(1)

    if hypermodel.feature != feature:
        logger.warning(f'Overriding feature: default = {hypermodel.feature}; specified = {feature}.')

    if hypermodel.num_classes != num_classes:
        logger.warning(
            f'Overriding num_classes: default = {hypermodel.num_classes}; specified = {num_classes}.')

    if timesteps is not None:
        if hypermodel.timesteps == 0 and timesteps != 0:
            logger.warning(f'Model does not contain timesteps; ignoring override.')
            timesteps = 0

        if hypermodel.timesteps != 0 and timesteps == 0:
            logger.warning(f'Model contains timesteps; ignoring override.')
            timesteps = hypermodel.timesteps

        if hypermodel.timesteps != timesteps:
            logger.info(f'Overriding timesteps: default = {hypermodel.timesteps}; specified = {timesteps}.')

    if batch_size is not None and hypermodel.batch_size != batch_size:
        logger.info(f'Overriding batch_size: default = {hypermodel.batch_size}; specified = {batch_size}.')

    return timesteps


def create_onnx_from_keras(keras_model,
                           is_flattened: bool = True,
                           has_timestep: bool = True,
                           has_channel: bool = False,
                           is_mutex: bool = True,
                           feature: str = '',
                           filename: str = ''):
    import tf2onnx
    from keras import backend as kb

    from sonusai.utils import add_sonusai_metadata
    from sonusai.utils import replace_stateful_grus

    kb.clear_session()
    onnx_model, _ = tf2onnx.convert.from_keras(keras_model)
    onnx_model = replace_stateful_grus(keras_model=keras_model, onnx_model=onnx_model)
    onnx_model = add_sonusai_metadata(model=onnx_model,
                                      is_flattened=is_flattened,
                                      has_timestep=has_timestep,
                                      has_channel=has_channel,
                                      is_mutex=is_mutex,
                                      feature=feature)
    if filename:
        import onnx
        onnx.save(onnx_model, filename)
    return onnx_model


def import_and_check_keras_model(model_name: str,
                                 weights_name: str,
                                 timesteps: int = None,
                                 batch_size: int = None) -> Any:
    from os.path import basename

    import h5py

    from sonusai import logger
    from sonusai.utils import import_module

    model_base = basename(model_name)

    # Import model definition file
    logger.info(f'Importing {model_base}')
    model = import_module(model_name)
    try:
        hypermodel = model.MyHyperModel(timesteps=timesteps, batch_size=batch_size)
    except Exception as e:
        logger.exception(f'build_model() in {model_base} failed: {e}.')
        raise SystemExit(1)

    with h5py.File(weights_name, 'r') as f:
        if 'sonusai_feature' in f.attrs:
            feature_mode = f.attrs['sonusai_feature']
        else:
            feature_mode = hypermodel.feature
            logger.warn(f'Could not find SonusAI feature in weights file; using hypermodel default.')
        if 'sonusai_num_classes' in f.attrs:
            num_classes = int(f.attrs['sonusai_num_classes'])
        else:
            num_classes = hypermodel.num_classes
            logger.warn(f'Could not find SonusAI num_classes in weights file; using hypermodel default.')

    # Check overrides
    timesteps = check_keras_overrides(model, feature_mode, num_classes, timesteps, batch_size)

    logger.info('Building model')
    try:
        hypermodel = model.MyHyperModel(feature=feature_mode,
                                        num_classes=num_classes,
                                        timesteps=timesteps,
                                        batch_size=batch_size)
    except Exception as e:
        logger.exception(f'build_model() in {model_base} failed: {e}.')
        raise SystemExit(1)

    return hypermodel


def replace_stateful_grus(keras_model, onnx_model):
    """Replace stateful GRUs with custom layers."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        from keras.layers import GRU

    stateful_gru_names = []
    for i in range(len(keras_model.layers)):
        layer = keras_model.layers[i]
        if isinstance(layer, GRU):
            if layer.stateful:
                stateful_gru_names.append(layer.name)

    for node_index in range(len(onnx_model.graph.node)):
        node = onnx_model.graph.node[node_index]
        replace = False
        if node.op_type == 'GRU':
            for i in node.input:
                for n in stateful_gru_names:
                    if n in i:
                        replace = True
        if node.name in stateful_gru_names or replace:
            node.op_type = 'SGRU'

    return onnx_model
