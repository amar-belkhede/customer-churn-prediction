import pandas as pd
import json
import pickle
from flask import  flash
initial = {"SeniorCitizen": 0,
           "tenure": 0,
           "MonthlyCharges": 0,
           "TotalCharges": 0,
           "gender_Female": 0,
           "gender_Male": 0,
           "Partner_No": 0,
           "Partner_Yes": 0,
           "Dependents_No": 0,
           "Dependents_Yes": 0,
           "PhoneService_No": 0,
           "PhoneService_Yes": 0,
           "MultipleLines_No": 0,
           "MultipleLines_No phone service": 0,
           "MultipleLines_Yes": 0,
           "InternetService_DSL": 0,
           "InternetService_Fiber optic": 0,
           "InternetService_No": 0,
           "OnlineSecurity_No": 0,
           "OnlineSecurity_No internet service": 0,
           "OnlineSecurity_Yes": 0,
           "OnlineBackup_No": 0,
           "OnlineBackup_No internet service": 0,
           "OnlineBackup_Yes": 0,
           "DeviceProtection_No": 0,
           "DeviceProtection_No internet service": 0,
           "DeviceProtection_Yes": 0,
           "TechSupport_No": 0,
           "TechSupport_No internet service": 0,
           "TechSupport_Yes": 0,
           "StreamingTV_No": 0,
           "StreamingTV_No internet service": 0,
           "StreamingTV_Yes": 0,
           "StreamingMovies_No": 0,
           "StreamingMovies_No internet service": 0,
           "StreamingMovies_Yes": 0,
           "Contract_Month-to-month": 0,
           "Contract_One year": 0,
           "Contract_Two year": 0,
           "PaperlessBilling_No": 0,
           "PaperlessBilling_Yes": 0,
           "PaymentMethod_Bank transfer (automatic)": 0,
           "PaymentMethod_Credit card (automatic)": 0,
           "PaymentMethod_Electronic check": 0,
           "PaymentMethod_Mailed check": 0
           }

# input = ([('seniorCitizen', '0'),
#             ('tenure', '1'),
#             ('monthlycharges', '1'),
#             ('totalCharges', '1'),
#             ('gender', 'Female'),
#             ('partner', 'No'),
#             ('dependents', 'No'),
#             ('phoneService', 'No'),
#             ('multipleLines', 'No'),
#             ('internetService', 'DSL'),
#             ('onlineSecurity', 'No'),
#             ('onlineBackup', 'No'),
#             ('deviceProtection', 'No'),
#             ('techSupport', 'No'),
#             ('streamingTV', 'No'),
#             ('streamingMovies', 'No'),
#             ('contract', 'Month-to-month'),
#             ('paperlessBilling', 'No'),
#             ('paymentMethod', 'Bank Transfer (automatic)')])

output = initial


# Defining serializerJson to convert Json data into DataFrame to feed into model
def serializerJson(input):

    print(input)

    if input["seniorCitizen"] == '1':
        output["SeniorCitizen"] = 1
    else:
        output["SeniorCitizen"] = 0

    if input["tenure"] == "":
        output["tenure"] = 0
    else:
        output["tenure"] = float(input["tenure"])

    # output["tenure"] = input["tenure")

    # if input["monthlycharges"] == "":
    #     output["MonthlyCharges"] = 0
    # else:
    output["MonthlyCharges"] = float(input["monthlyCharges"])

    # output["MonthlyCharges"] = input["monthlycharges")

    # if input["totalCharges"] == "":
    #     output["TotalCharges"] = 0
    # else:
    output["TotalCharges"] = float(input["totalcharges"])

    # output["TotalCharges"] = input["totalCharges")

    if input["gender"] == "1":
        output["gender_Male"] = 1
    else:
        output["gender_Female"] = 1

    if input["partner"] == "1":
        output["Partner_Yes"] = 1
    else:
        output["Partner_No"] = 1

    if input["dependents"] == "1":
        output["Dependents_Yes"] = 1
    else:
        output["Dependents_No"] = 1

    if input["phoneService"] == "1":
        output["PhoneService_Yes"] = 1
    else:
        output["PhoneService_No"] = 1

    # # multiline
    if input["multipleLines"] == "2":
        output["MultipleLines_Yes"] = 1
    elif input["multipleLines"] == "1":
        output["MultipleLines_No phone service"] = 1
    else:
        output["MultipleLines_No"] = 1

    # internetService
    if input["internetService"] == "0":
        output["InternetService_DSL"] = 1
    elif input["internetService"] == "1":
        output["InternetService_Fiber optic"] = 1
    else:
        output["InternetService_No"] = 1

    # onlineSecurity
    if input["onlineSecurity"] == "2":
        output["OnlineSecurity_Yes"] = 1
    elif input["onlineSecurity"] == "1":
        output["OnlineSecurity_No internet service"] = 1
    else:
        output["OnlineSecurity_No"] = 1

    # onlineBackup
    if input["onlineBackup"] == "2":
        output["OnlineBackup_Yes"] = 1
    elif input["onlineBackup"] == "1":
        output["OnlineBackup_No internet service"] = 1
    else:
        output["OnlineBackup_No"] = 1

    # deviceProtection
    if input["deviceProtection"] == "2":
        output["DeviceProtection_Yes"] = 1
    elif input["deviceProtection"] == "1":
        output["DeviceProtection_No internet service"] = 1
    else:
        output["DeviceProtection_No"] = 1

    # techSupport
    if input["techSupport"] == "2":
        output["TechSupport_Yes"] = 1
    elif input["techSupport"] == "1":
        output["TechSupport_No internet service"] = 1
    else:
        output["TechSupport_No"] = 1

    # streamingTV
    if input["streamingTV"] == "2":
        output["StreamingTV_Yes"] = 1
    elif input["streamingTV"] == "1":
        output["StreamingTV_No internet service"] = 1
    else:
        output["StreamingTV_No"] = 1

    # streamingMovies
    if input["streamingmovies"] == "2":
        output["StreamingMovies_Yes"] = 1
    elif input["streamingmovies"] == "1":
        output["StreamingMovies_No internet service"] = 1
    else:
        output["StreamingMovies_No"] = 1

    # Contract_Month-
    if input["contract"] == "0":
        output["Contract_Month-to-month"] = 1
    elif input["contract"] == "1":
        output["Contract_One year"] = 1
    else:
        output["Contract_Two year"] = 1

    # paperlessBilling
    if input["paperlessBilling"] == "1":
        output["PaperlessBilling_Yes"] = 1
    else:
        output["PaperlessBilling_No"] = 1

    # paymentMethod
    if input["paymentMethod"] == "0":
        output["PaymentMethod_Bank transfer (automatic)"] = 1
    elif input["paymentMethod"] == "1":
        output["PaymentMethod_Credit card (automatic)"] = 1
    elif input["paymentMethod"] == "2":
        output["PaymentMethod_Electronic check"] = 1
    else:
        output["PaymentMethod_Mailed check"] = 1

    model = pickle.load(open('churnprediction/model.pkl', 'rb'))
    print(output)
    resNorm = pd.DataFrame(output, index=[0])
    # resNorm = pd.to_numeric(resNorm, errors='coerce')
    # print(resNorm.dtypes)
    # print(resNorm)
    pred = model.predict(resNorm)
    # print(pred)
    lists = pred.tolist()
    json_pred = json.dumps(lists)
    # json_pred = json.dumps(resNorm)
    prediction = 'Congratulations! The customer will not churn 😀🙅‍♂️'
    if json_pred[1] == '1':
        prediction = 'Oh no! The customer will churn 😞'
        flash('Oh no! The customer will churn 😞', 'warning')
    else:
        prediction = 'Congratulations! The customer will not churn 😀🙅‍♂️'
        flash('Congratulations! The customer will not churn 😀🙅‍♂️', 'success')
    
    return json_pred
