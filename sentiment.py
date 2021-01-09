from joblib import load
import re
import string
import os
import secrets

import matplotlib
import matplotlib.pyplot as plt

from lime.lime_text import LimeTextExplainer


matplotlib.use('Agg')
plt.ioff()

punc = string.punctuation
table = str.maketrans('', '', punc)


def remove_html(text):
    return re.sub(r'<.*?>', '', text)


def remove_link(text):
    return re.sub(r'https?://\S*|www\.\S*', '', text)


def replace_hash_at(text):
    text = re.sub(r'@(\w+)', ' constantmention ', text)
    text = re.sub(r'#(\w+)\b', ' constanthash ', text)
    return text


def replace_amp(text):
    return text.replace('&amp', ' and ')


def remove_punc(text):
    return text.translate(table)


def lower(text):
    return text.lower()


def remove_whitespace(text):
    return re.sub(r'[\s]+', ' ', text)


def preprocess_text(text):
    text = remove_html(text)
    text = remove_link(text)
    text = replace_hash_at(text)
    text = replace_amp(text)
    text = remove_punc(text)
    text = lower(text)
    text = remove_whitespace(text)
    return text


image_folder = './static/results/'
lr_model_path = './model/lr_model.joblib'
model = load(lr_model_path)


def explain(text, model):
    explainer = LimeTextExplainer(class_names=['negative', 'positive'])
    exp = explainer.explain_instance(text, model.predict_proba, num_features=6)
    fig = exp.as_pyplot_figure()
    file_name = secrets.token_hex(4) + '.jpg'
    img_path = os.path.join(image_folder, file_name)
    plt.savefig(img_path)
    return file_name


def get_sentiment(text, model=model):
    labels = {0: 'negative', 1: 'positive'}
    text = preprocess_text(text)
    cls_ = labels[model.predict([text])[0]]
    file_name = explain(text, model)
    return text, cls_, file_name

