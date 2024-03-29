# diet-language-identifier
A language identifier built using DIET classifier offered by Rasa Open Source

---

## About DIET Language Identifier
Often it is required to identify a pre-defined set of languages in some NLP systems, and there should be an intuitive way to fine-tune the model further on new data. 

### Existing Options
Fast-text based language detection models are supervised language detection models that can be used out-of-the-box, however, these models do not provide a way to fine-tune the pre-trained models. Training a state-of-the-art transforer model is another option, however, there is a trade-off between accuracy and compute resource utilization/ latency when it comes to these types of models for production-grade solutions.

### Why DIET?
DIET is also based on transformers architecture, yet it allows to train a classification model with a minimum amount of data with high accuracy. It also allows sparse and dense feature engineering out-of-the-box which prevents developers from having to implement the whole NLP pipeline from scratch. On the otherside, the pipeline is fully customizable in case developers want to implement pipeline components from scratch or customizing existing ones.

### Language Identification
The idea here is to use ISO language code as the `intent` name and provide supervised examples under each intent that we want to detect. The more data provided, the better the model will be. The rasa fallback mechanism can be used to set fallback thresholds for the NLU.

When new data flows in, Rasa `incremental training` can be used to quickly spin up a training session and update the existing model with a minimum effort.

After training the classifier, the `diet_lang_identifier.py` script can be used for inference. Benchmarks are yet to be performed.

## Python Package
The plan is to release the source code as a Python package so anyone can train a model quickly and utilize a self-hosted language detector in their amazing NLP projects.

---

## Contributing
This project is not yet open for contributions, however, the plan is to construct a large language detection dataset that is quite effective and refine the model hyperparameters to unleash its full potential. If you're interested in contributing, stay tuned!

---

## Training locally and perform continous model improvements
### Development environment setup
#### Setting up the pre-commit hooks
1. Install pre-commit using pip install pre-commit
2. create .pre-commit-config.yaml in project root and add required repos
3. run pre-commit install on root to install the hooks
   - run pre-commit uninstall to uninstall hooks
4. run pre-commit hooks
   - run --all-files to manually run the hooks [optional + manual]
   - pre-commit install --hook-type commit-msg [automate]

_Note:_ use conventional commits only, otherwise the commits will fail when pre-commit hooks are enabled

#### Installing dependencies
Install all dev dependencies by executing `pip install -r requirements-dev.txt` at the project root.

#### Running the Rasa NLU server
Simply execute `rasa run --enable-api --cors "*"` to run rasa REST API. Use the following curl request format to infer the language of an input. If DIET fails to categorize the input, the default intent given is `nlu_fallback`. The fallback threshold can be adjusted in the `config.yml`.
```bash
# Request
curl --location 'http://localhost:5005/model/parse/' \
--header 'Content-Type: application/json' \
--data '{
    "text": "hello there!"
}'


# Response
{
    "text": "hello there!",
    "intent": {
        "name": "en",
        "confidence": 1.0
    },
    "entities": [],
    "text_tokens": [
        [
            0,
            5
        ],
        [
            6,
            11
        ]
    ],
    "intent_ranking": [
        {
            "name": "en",
            "confidence": 1.0
        },
        {
            "name": "si",
            "confidence": 3.740343742878632e-19
        },
        {
            "name": "sin",
            "confidence": 1.418158024045691e-20
        }
    ]
}
```
#### Running finetuner web server
_to be updated_
  
### Training Data Format
_to be updated_  

### Model Configurations
_to be updated_

### Training
```bash
rasa data validate  # check if trainng data and configs are in order
rasa train nlu  # training the nlu model
```

### Versioning
_to be updated_

### Fine-tuning
```bash
rasa train nlu --finetune --epoch-fraction 0.2  # or
rasa train nlu --finetune <model_name> --epoch-fraction 0.2  # leave the model name empty to fine-tune the latest model available
```

#### Manual fine-tuning 
_to be updated_

#### Web-based fine-tuning
_to be updated_

## Useful Docs
_to be updated_
