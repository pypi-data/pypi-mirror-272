from typing import Any


def load_torchl_ckpt_model(model_name: str,
                           ckpt_name: str,
                           batch_size: int = None,
                           timesteps: int = None,
                           training: bool = False) -> Any:
    import torch

    from sonusai import logger
    from sonusai.utils import import_module

    # Load checkpoint first to get hparams if available
    try:
        checkpoint = torch.load(ckpt_name, map_location=lambda storage, loc: storage)
    except Exception as e:
        logger.exception(f'Error: could not load checkpoint from {ckpt_name}: {e}')
        raise SystemExit(1)

    # Import model definition file
    logger.info(f'Importing {model_name}')
    torchl_module = import_module(model_name)

    if 'hyper_parameters' in checkpoint:
        logger.info(f'Found checkpoint file with hyper-parameters')
        hparams = checkpoint['hyper_parameters']
        if batch_size is not None and ['batch_size'] != batch_size:
            if batch_size != 1 and not training:
                batch_size = 1
                logger.warning('Prediction only supports batch_size = 1, forcing to 1')
            logger.info(f'Overriding model default batch_size of {hparams["batch_size"]} with {batch_size}')
            hparams["batch_size"] = batch_size

        if timesteps is not None:
            if hparams['timesteps'] == 0 and timesteps != 0:
                timesteps = 0
                logger.warning(f'Model does not contain timesteps; ignoring override')

            if hparams['timesteps'] != 0 and timesteps == 0:
                timesteps = hparams['timesteps']
                logger.warning(f'Using model default timesteps of {timesteps}')

            if hparams['timesteps'] != timesteps:
                logger.info(f'Overriding model default timesteps of {hparams["timesteps"]} with {timesteps}')
                hparams['timesteps'] = timesteps

        logger.info(f'Building model with hyper-parameters and batch_size={batch_size}, timesteps={timesteps}')
        try:
            model = torchl_module.MyHyperModel(**hparams, training=training)
        except Exception as e:
            logger.exception(f'Error: model build (MyHyperModel) in {model_name} failed: {e}')
            raise SystemExit(1)
    else:
        logger.info(f'Found checkpoint file with no hyper-parameters')
        logger.info(f'Building model with defaults')
        try:
            tmp = torchl_module.MyHyperModel(training=training)
        except Exception as e:
            logger.exception(f'Error: model build (MyHyperModel) in {model_name} failed: {e}')
            raise SystemExit(1)

        if batch_size is not None:
            if tmp.batch_size != batch_size:
                logger.info(f'Overriding model default batch_size of {tmp.batch_size} with {batch_size}')
        else:
            batch_size = tmp.batch_size

        if timesteps is not None:
            if tmp.timesteps == 0 and timesteps != 0:
                logger.warning(f'Model does not contain timesteps; ignoring override')
                timesteps = 0

            if tmp.timesteps != 0 and timesteps == 0:
                logger.warning(f'Using model default timesteps of {timesteps}')
                timesteps = tmp.timesteps

            if tmp.timesteps != timesteps:
                logger.info(f'Overriding model default timesteps of {tmp.timesteps} with {timesteps}.')
        else:
            timesteps = tmp.timesteps

        model = torchl_module.MyHyperModel(timesteps=timesteps, batch_size=batch_size, training=training)

    logger.info(f'Loading weights from {ckpt_name}')

    if training is False:
        # Remove weights that pertain to custom loss or gan models (discriminator) - not needed for prediction
        logger.info('Removing weights that are not needed for inference.')
        for key in checkpoint['state_dict'].copy().keys():
            if key.startswith('per_loss'):
                checkpoint['state_dict'].pop(key)
            elif key.startswith('discr'):
                checkpoint['state_dict'].pop(key)

    model.load_state_dict(checkpoint['state_dict'])
    return model
