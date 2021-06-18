import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier


# Function to load CSV file
def load_CSV(name):
    telecom_cust = pd.read_csv(name)
    return telecom_cust


# Loading the CSV file
telecom_cust = load_CSV('churnprediction/Telco-Customer-Churn.csv')

# Converting Total Charges to a numerical data type.
telecom_cust.TotalCharges = pd.to_numeric(
    telecom_cust.TotalCharges, errors='coerce')
telecom_cust.isnull().sum()


# Removing missing values
telecom_cust.dropna(inplace=True)


# Remove customer IDs from the data set
df2 = telecom_cust.iloc[:, 1:]


# Convertin the predictor variable in a binary numeric variable
df2['Churn'].replace(to_replace='Yes', value=1, inplace=True)
df2['Churn'].replace(to_replace='No',  value=0, inplace=True)

# Let's convert all the categorical variables into dummy variables
df_dummies = pd.get_dummies(df2)
df_dummies.head()

# We will use the data frame where we had created dummy variables
y = df_dummies['Churn'].values
X = df_dummies.drop(columns=['Churn'])


# Create Train & Test Data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=101)


# Logistic Regression model
def logistic_regression(X_train, y_train, X_test, y_test):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    print("Logistic Regression model build successfully")
    return model


# XgBoost model
def xgboost(X_train, y_train, X_test, y_test):
    model = XGBClassifier()
    model.fit(X_train, y_train)
    print("XGBoost Classifier model build successfully")
    return model


# AdaBoost model
def adaboost(X_train, y_train, X_test, y_test):
    model = AdaBoostClassifier()
    model.fit(X_train, y_train)
    print("AdaBoost Classifier model build successfully")
    return model


# Random Forest Classfier model
def random_forest(X_train, y_train, X_test, y_test):
    model = RandomForestClassifier(n_estimators=1000, oob_score=True, n_jobs=-1,
                                   random_state=50, max_features="auto",
                                   max_leaf_nodes=30)
    model.fit(X_train, y_train)
    print("Random Forest Classifier model build successfully")
    return model


# Building different ML models and printing accuracies for the same
model_xg = xgboost(X_train, y_train, X_test, y_test)
model_ada = adaboost(X_train, y_train, X_test, y_test)
model_rf = random_forest(X_train, y_train, X_test, y_test)
model_lr = logistic_regression(X_train, y_train, X_test, y_test)


# Function to dump the Model
def dumpModel(model):
    pickle.dump(model, open('model.pkl', 'wb'))


# Function to load the model (model = pickle.load(open('model.pkl', 'rb'))
def loadModel(name):
    model = pickle.load(open(name, 'rb'))
    return model


# Creating a dump file of the model
dumpModel(model_xg)

# Loading the model
load_model = loadModel('model.pkl')


# Function to Test the model
def testSample():

    resJsonNorm = {
        "SeniorCitizen": 0,
        "tenure": 34,
        "MonthlyCharges": 56.95,
        "TotalCharges": 1889.50,
        "gender_Female": 0,
        "gender_Male": 1,
        "Partner_No": 1,
        "Partner_Yes": 0,
        "Dependents_No": 1,
        "Dependents_Yes": 0,
        "PhoneService_No": 0,
        "PhoneService_Yes": 1,
        "MultipleLines_No": 1,
        "MultipleLines_No phone service": 0,
        "MultipleLines_Yes": 0,
        "InternetService_DSL": 1,
        "InternetService_Fiber optic": 0,
        "InternetService_No": 0,
        "OnlineSecurity_No": 0,
        "OnlineSecurity_No internet service": 0,
        "OnlineSecurity_Yes": 1,
        "OnlineBackup_No": 1,
        "OnlineBackup_No internet service": 0,
        "OnlineBackup_Yes": 0,
        "DeviceProtection_No": 0,
        "DeviceProtection_No internet service": 0,
        "DeviceProtection_Yes": 1,
        "TechSupport_No": 1,
        "TechSupport_No internet service": 0,
        "TechSupport_Yes": 0,
        "StreamingTV_No": 1,
        "StreamingTV_No internet service": 0,
        "StreamingTV_Yes": 0,
        "StreamingMovies_No": 1,
        "StreamingMovies_No internet service": 0,
        "StreamingMovies_Yes": 0,
        "Contract_Month-to-month": 0,
        "Contract_One year": 1,
        "Contract_Two year": 0,
        "PaperlessBilling_No": 1,
        "PaperlessBilling_Yes": 0,
        "PaymentMethod_Bank transfer (automatic)": 0,
        "PaymentMethod_Credit card (automatic)": 0,
        "PaymentMethod_Electronic check": 0,
        "PaymentMethod_Mailed check": 1
    }

    resNorm = pd.DataFrame(resJsonNorm, index=[0])
    # print(load_model.predict(resNorm))

    # Making predictions
    if (load_model.predict(resNorm)[0] == 0):
        print("Customer will not churn")
    else:
        print("Customer will churn")


testSample()
