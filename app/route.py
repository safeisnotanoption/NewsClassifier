#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import numpy
from flask import render_template, request, redirect, url_for, session, abort

from app import app

from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

from keras.models import load_model
from sklearn.externals import joblib

LOG = logging.getLogger('access')

cats = ['Авто', 'Бизнес', 'Власть', 'Выборы', 'Город', 'Деньги', 'Доброе дело',
        'ЖКХ', 'Недвижимость', 'Общество', 'Происшествия', 'Работа',
        'Спорт', 'Строительство', 'Технологии', 'Туризм', 'Финансы']


@app.route('/', methods=['GET', 'POST'])
def index():
    LOG.info('Access: %s, %s, %s' % (request.remote_addr, request.args, request.form))

    results = {}

    for k_get, v_get in request.args.items():
        results[k_get] = v_get

    for k_form, v_form in request.form.items():
        t = RegexpTokenizer(r'\w+').tokenize(v_form)
        t = map(lambda z: z.lower(), t)
        t = filter(lambda z: z not in stopwords.words('russian'), t)
        t = filter(lambda z: len(z) > 2, t)
        t = map(SnowballStemmer('russian').stem, t)
        t = map(lambda z: '#' if z.isdigit() else z, t)
        v_form = ' '.join(t)
        print(v_form)
        x = joblib.load('Data_T.pickle').transform([v_form]).todense()
        print(x)
        y = load_model('Data_Z.mdl').predict(x)
        y = joblib.load('Data_LB.pickle').inverse_transform(y)
        results[k_form] = cats[y[0]]

    return render_template('index.html', results=results)
