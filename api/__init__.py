import logging
import os
import sys


logger = logging.getLogger(__name__)

api_path = os.path.join(os.getcwd(), "actions")
if api_path not in sys.path:
    sys.path.append(api_path)
    logger.info("Added api package path to sys.path")
    logger.info(f"Added api path: {api_path}")
