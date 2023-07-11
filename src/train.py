from utils import CustomLogging, notebook_wrapper


if __name__ == '__main__':
    logging = CustomLogging()
    logger = logging.get_logger()

    logger.info('Fetching model...')

    FILE_NAME = 'ml_model'
    # Run script
    exec(notebook_wrapper(file_name=FILE_NAME, logger=logger))
    logger.info('Model created and prepared...')
