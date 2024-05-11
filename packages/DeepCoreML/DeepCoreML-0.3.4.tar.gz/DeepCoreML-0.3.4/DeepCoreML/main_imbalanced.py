import os
import sys

import numpy as np

import DeepCoreML.eval as evaluation_methods

num_threads = 1
os.environ['OMP_NUM_THREADS'] = str(num_threads)
np.set_printoptions(linewidth=400, threshold=sys.maxsize)

seed = 0

path = '../../../../datasets/soft_defect/'

datasets = {
    'CM1': {'name': 'CM1', 'path': path + 'cm1.csv', 'features_cols': range(0, 21), 'class_col': 21},
    'KC1': {'name': 'KC1', 'path': path + 'kc1.csv', 'features_cols': range(0, 21), 'class_col': 21},
    'KC2': {'name': 'KC2', 'path': path + 'kc2.csv', 'features_cols': range(0, 21), 'class_col': 21},
    'KC3': {'name': 'KC3', 'path': path + 'kc3.csv', 'features_cols': range(0, 39), 'class_col': 39},
    'PC1': {'name': 'PC1', 'path': path + 'pc1.csv', 'features_cols': range(0, 21), 'class_col': 21},
    'PC3': {'name': 'PC3', 'path': path + 'pc3.csv', 'features_cols': range(0, 37), 'class_col': 37},
    'PC4': {'name': 'PC4', 'path': path + 'pc4.csv', 'features_cols': range(0, 37), 'class_col': 37},
    'CAMEL-1.2': {'name': 'CAMEL-1.2', 'path': path + 'camel-1.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'CAMEL-1.4': {'name': 'CAMEL-1.4', 'path': path + 'camel-1.4.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'CAMEL-1.6': {'name': 'CAMEL-1.6', 'path': path + 'camel-1.6.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'IVY-1.1': {'name': 'IVY-1.1', 'path': path + 'ivy-1.1.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'IVY-2.0': {'name': 'IVY-2.0', 'path': path + 'ivy-2.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'JEDIT-4.0': {'name': 'JEDIT-4.0', 'path': path + 'jedit-4.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'JEDIT-4.1': {'name': 'JEDIT-4.1', 'path': path + 'jedit-4.1.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'JEDIT-4.2': {'name': 'JEDIT-4.2', 'path': path + 'jedit-4.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'LOG4J-1.0': {'name': 'LOG4J-1.0', 'path': path + 'log4j-1.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'LOG4J-1.1': {'name': 'LOG4J-1.1', 'path': path + 'log4j-1.1.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'LOG4J-1.2': {'name': 'LOG4J-1.2', 'path': path + 'log4j-1.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'LUCE-2.2': {'name': 'LUCENE-2.2', 'path': path + 'lucene-2.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'LUCE-2.4': {'name': 'LUCENE-2.4', 'path': path + 'lucene-2.4.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'POI-1.5': {'name': 'POI-1.5', 'path': path + 'poi-1.5.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'POI-2.0': {'name': 'POI-2.0', 'path': path + 'poi-2.0.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'VL14': {'name': 'VELOCITY-1.4', 'path': path + 'velocity-1.4.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'VL16': {'name': 'VELOCITY-1.6', 'path': path + 'velocity-1.6.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'XER-1.2': {'name': 'XERCES-1.2', 'path': path + 'xerces-1.2.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'XER-1.3': {'name': 'XERCES-1.3', 'path': path + 'xerces-1.3.csv', 'features_cols': range(0, 20), 'class_col': 20},
    'XER-1.4': {'name': 'XERCES-1.4', 'path': path + 'xerces-1.4.csv', 'features_cols': range(0, 20), 'class_col': 20}
}

evaluation_methods.eval_oversampling_efficacy(datasets, num_threads, seed)

