import logging
import os
import re
import shutil
import tarfile
from typing import Text, Optional, Dict

from rasa.nlu.model import Interpreter

logger = logging.getLogger(__name__)


class LanguageIdentifier:
    def __init__(
        self, model_path: Text, model_prefix: Text = "lang-identifier"
    ) -> None:
        if not model_path:
            model_path = "/custom/extensions/components/nlu/classifiers/lang_identifier/assets/"

        self._model_prefix = model_prefix
        self._model_path = model_path

        # for debugging purposes
        logger.debug(f"Loading the language detection model at {self._model_path}")

        # validate model path or zipped model directly
        model_is_valid, model_name = self._validate_model_path()
        if not model_is_valid or model_name is None:
            raise ValueError(
                f"Model is invalid. Make sure you have a valid model in the assets dir"
            )

        # for debugging purposes
        self._model_name = model_name
        logger.debug(f"Latest model detected: {self._model_name}")

        extracted_model_path = self._extract_model()
        self._interpreter = Interpreter.load(
            model_dir=extracted_model_path, skip_validation=True
        )

    def _validate_model_path(self):
        if os.path.isdir(self._model_path):
            for file_name in os.listdir(self._model_path):
                if file_name.startswith(self._model_prefix) and file_name.endswith(
                    ".tar.gz"
                ):
                    version_match = re.match(
                        rf"{self._model_prefix}-v(\d+\.\d+\.\d+)\.tar\.gz", file_name
                    )
                    if version_match:
                        return True, os.path.join(
                            self._model_path, self._get_latest_model()
                        )

        elif os.path.isfile(self._model_path):
            if self._model_path.startswith(
                self._model_prefix
            ) and self._model_path.endswith(".tar.gz"):
                file_name = os.path.basename(self._model_path)
                version_match = re.match(
                    rf"{self._model_prefix}-v(\d+\.\d+\.\d+)\.tar\.gz", file_name
                )
                if version_match:
                    return True, self._model_path

        else:
            raise ValueError(f"Invalid model path: {self._model_path}")

        return False, None

    def _get_latest_model(self):
        latest_file_name = None
        latest_version = "0.0.0"

        for file_name in os.listdir(self._model_path):
            if file_name.startswith(self._model_prefix) and file_name.endswith(
                ".tar.gz"
            ):
                version_match = re.match(
                    rf"{self._model_prefix}-v(\d+\.\d+\.\d+)\.tar\.gz", file_name
                )
                if version_match:
                    version = version_match.group(1)
                    if latest_version is None or version > latest_version:
                        latest_version = version
                        latest_file_name = file_name

        return latest_file_name

    def _extract_model(self) -> Optional[Text]:
        path_to_extract = os.path.join(os.path.dirname(self._model_path), "extracted")
        logger.debug(
            f"Language identification model is being extracted to {path_to_extract}"
        )

        # Create the extract directory if it doesn't exist
        if not os.path.exists(path_to_extract):
            os.makedirs(path_to_extract)

        # Clear the extract directory if it exists and is not empty
        for file_name in os.listdir(path_to_extract):
            file_path = os.path.join(path_to_extract, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

        # Extract the contents of the tar file to the extract directory
        with tarfile.open(self._model_name, "r:gz") as tar:
            tar.extractall(path_to_extract)

        return os.path.join(path_to_extract, "nlu")

    def identify(self, text: Text) -> Optional[Dict]:
        try:
            parsed_ = self._interpreter.parse(text=text)
            return parsed_
        except Exception as e:
            logger.exception(f"Error occurred while parsing the incoming query. {e}")
            return None


if __name__ == "__main__":
    language_identifier = LanguageIdentifier(
        model_path="assets/"
    )
    res = language_identifier.identify(text="hi, how are you?")
    print(f"detected lang: {res}")
    print("terminating test...")
