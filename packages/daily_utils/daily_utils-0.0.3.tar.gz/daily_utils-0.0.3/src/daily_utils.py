import json
import multiprocessing
import glob
import os
import tqdm
import requests
import time
import random
import math
import pandas

import itertools
import numpy


def list_dir(parent_folder, pattern):
    files = glob.glob1(parent_folder, pattern)
    files = sorted(files)
    full_paths = [os.path.join(parent_folder, file) for file in files]
    return full_paths


def read_json(path):
    with open(path) as f:
        data = json.load(f)
    return data


def read_jsonl(path):
    print("Loading", path)
    with open(path) as f:
        lines = f.readlines()
    p = multiprocessing.Pool(8)
    data = p.map(json.loads, lines)
    return data


def save_jsonl(data, path):
    p = multiprocessing.Pool(8)
    texts = p.map(json.dumps, data)
    save_textlines(texts, path)


def save_json(data, path):
    print('Saving to ', path)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def read_text(path):
    with open(path) as f:
        text = f.read()
    return text


def read_textlines(path):
    with open(path) as f:
        texts = f.readlines()
    return texts


def save_textlines(lines: list, path):
    print('Saving to ', path)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def save_text(text: str, path):
    print('Saving to ', path)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w') as f:
        f.write(text)

