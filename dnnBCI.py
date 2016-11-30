import tensorflow as tf

import numpy as np
import random
import pandas as pd

random.seed(42)

TRAINING = "bciTrainingSet.csv"
TEST = "bciTestSet.csv"

bciDF = pd.read_csv('AveragedDataset.csv')

print(bciDF.head())
# TODO: Properly partition training set and test set such that the sets
#       do not have any common points

bciDFLength = len(bciDF)
testLength = int(0.2 * bciDFLength)
trainingLength = int(0.8 * bciDFLength)

# Obtain test set
testSetRandomRows = np.random.choice(bciDF.index.values, testLength)
test = bciDF.iloc[testSetRandomRows]
test.to_csv("bciTestSet.csv", index=False, header = False)

trainingSetRandomRows = np.random.choice(bciDF.index.values, trainingLength)
training = bciDF.iloc[trainingSetRandomRows]
training.to_csv("bciTrainingSet.csv", index=False, header=False)


testSet = tf.contrib.learn.datasets.base.load_csv_without_header(
    filename=TEST, target_dtype=np.int, features_dtype=np.float)

trainingSet = tf.contrib.learn.datasets.base.load_csv_without_header(
    filename=TRAINING, target_dtype=np.int, features_dtype=np.float)


featureColumns = [tf.contrib.layers.real_valued_column("", dimension=25)]


# Build a 3 layer DNN with 10, 20, 10 units respectively
classifier = tf.contrib.learn.DNNClassifier(
                n_classes=3,
                feature_columns=featureColumns,
                hidden_units=[10, 10])


# Fit model
classifier.fit(
                x=trainingSet.data,
                y=trainingSet.target,
                steps=2000)


# Evaluate accuracy
accuracyScore = classifier.evaluate(
                x=testSet.data,
                y=testSet.target)["accuracy"]


print('Accuracy: {0:f}'.format(accuracyScore))

# Predict
predictions = classifier.predict(testSet.data)
print('Predictions: {}'.format(str(predictions)))