import pickle
import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.model_selection import cross_val_score, GridSearchCV

class fingerprinting:
	def __init__(self, filename, features, classes, probability_threshold):
		self.filename = filename
		self.features = features
		self.classes = classes
		self.probability_threshold =probability_threshold

		# load the model from disk
		self.loaded_model = pickle.load(open(filename, 'rb'))

	def find_highest_class_prob(self, rssi_values):
		temp = np.array(rssi_values).reshape(1,3)
		temp = pd.DataFrame(data=temp,
		            index=[i for i in range(temp.shape[0])],
		            columns=self.features)
		class_probabilities = self.loaded_model.predict_proba(temp)
		
		highest_prob, highest_prob_class = -1, -1
		for i in range(len(self.classes)):
			if (highest_prob < class_probabilities[0][i]):
				highest_prob = class_probabilities[0][i]
				highest_prob_class = i

		return min(self.probability_threshold, highest_prob), self.classes[highest_prob_class]


"""
vals = [-65, -54, -55]
filename = 'svm_final_model.sav'
features = ["msi-gt70", "raspberry-10", "erhan-e570"]
classes = {0: [1,1], 1: [4.25, 2.45]}

f = fingerprinting(filename, features, classes)
highest_prob, highest_prob_class = f.find_highest_class_prob(vals)
print(highest_prob, highest_prob_class)
"""