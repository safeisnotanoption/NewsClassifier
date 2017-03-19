#!/usr/bin/env python
# -*- coding: utf-8 -*-

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'formatter' : 'simple',
            'class': 'logging.FileHandler',
            'filename': 'access.log',
        },
    },
    'loggers': {
        'access': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
}