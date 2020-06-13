import psycopg2
import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.utils import shuffle
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix,classification_report
from sklearn.model_selection import cross_val_score, GridSearchCV


# connect to db
host = 'localhost'
port = 5432
user = 'postgres'
password = ''
db_name = 'ble_rssi'
conn = psycopg2.connect(host=host, port=port, user=user, password=password, database=db_name)

# execute query on db
query = "select * from rssi_log where (card_x=1 and card_y=1) or (card_x=4.25 and card_y=2.45)"
card_pos = {3131: "1_1", 2292: "4.25_2.45"}
classes = ["1_1", "4.25_2.45"]
data = {"msi-gt70": [], "raspberry-10": [], "erhan-e570": [], "class": []}
with conn.cursor() as cur:
    cur.execute(query)
    i = 0
    for row in cur:
        data[row[2]].append(row[3])
        #data["rssi"].append(row[3])
        if i % 3 == 0:
            data["class"].append(card_pos[row[1]])
        i+=1

conn.commit()


# preprocessing
df = pd.DataFrame(data=data , columns=["msi-gt70", "raspberry-10", "erhan-e570", "class"])

# split dataset into train & test
features = ["msi-gt70", "raspberry-10", "erhan-e570"]
# get features
x = df.loc[:,features].values
# get target
y = df.loc[:,['class']].values

# 80% train, 20% test 
x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.2, random_state=0)

# Dimension of Train and Test set 
print("Dimension of Train set",x_train.shape)
print("Dimension of Test set",x_test.shape,"\n")

# x_train
x_train = pd.DataFrame(data=x_train[0:,0:],
            index=[i for i in range(x_train.shape[0])],
            columns=features)

# y_train
y_train_label = pd.DataFrame(data=y_train[0:,0:],
            index=[i for i in range(y_train.shape[0])],
            columns=['class'])
y_train_label = y_train_label['class'].values.astype(object)

# y_test
y_test_label = pd.DataFrame(data=y_test[0:,0:],
            index=[i for i in range(y_test.shape[0])],
            columns=['class'])
y_test_label = y_test_label['class'].values.astype(object)

# encode labels
# Transforming non numerical labels into numerical labels
from sklearn import preprocessing
encoder = preprocessing.LabelEncoder()

# encoding train labels 
encoder.fit(y_train)
y_train = encoder.transform(y_train_label)

# encoding test labels 
encoder.fit(classes)
y_test = encoder.transform(y_test_label)

#Total Number of Continous and Categorical features in the training set
num_cols = x_train._get_numeric_data().columns
print("Number of numeric features:",num_cols.size)
#list(set(X_train.columns) - set(num_cols))

names_of_predictors = list(x_train.columns.values)

# Scaling the Train and Test feature set 
#from sklearn.preprocessing import StandardScaler
#scaler = StandardScaler()
#x_train_scaled = scaler.fit_transform(x_train)
#x_test_scaled = scaler.transform(x_test)


# hyperparameter tuning
# Create the parameter grid based on the results of random search 
params_grid = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 2, 5, 10]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
# Performing CV to tune parameters for best SVM fit 
svm_model = GridSearchCV(SVC(probability=True), params_grid, cv=5)
svm_model.fit(x_train, y_train)


# confusion matrix and accuracy score
# View the accuracy score
print('Best score for training data:', svm_model.best_score_,"\n") 

# View the best parameters for the model found using grid search
print('Best C:',svm_model.best_estimator_.C,"\n") 
print('Best Kernel:',svm_model.best_estimator_.kernel,"\n")
print('Best Gamma:',svm_model.best_estimator_.gamma,"\n")

final_model = svm_model.best_estimator_
y_pred = final_model.predict(x_test)
y_pred_label = list(encoder.inverse_transform(y_pred))

# Making the Confusion Matrix
print(confusion_matrix(y_test_label, y_pred_label))
print("\n")
print(classification_report(y_test_label, y_pred_label))

print("Training set score for SVM: %f" % final_model.score(x_train, y_train))
print("Testing set score for SVM: %f" % final_model.score(x_test, y_test))

print(svm_model.score)


# single prediction
vals = [-65, -54, -55]
temp = np.array(vals).reshape(1,3)
temp = pd.DataFrame(data=temp,
            index=[i for i in range(temp.shape[0])],
            columns=features)
prob = final_model.predict_proba(temp)
print(prob)


# save the model 
import pickle
filename = 'svm_final_model.sav'
pickle.dump(final_model, open(filename, 'wb'))