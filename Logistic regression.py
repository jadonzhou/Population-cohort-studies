import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
df= pd.read_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/COVID-19/10. Statins and interactions for COVID 19/LRData.csv")   
print(df.isnull().sum)
from sklearn.preprocessing import LabelEncoder
number=LabelEncoder()
df.iloc[:,0]=number.fit_transform(df.iloc[:,0].astype('str'))
results=pd.DataFrame()
for i in range(df.shape[1]-1):
    df.iloc[:,i+1]=number.fit_transform(df.iloc[:,i+1].astype('str'))
    model=smf.logit(formula=df.columns[0]+'~+'+df.columns[i+1], data=df).fit()
    #print(model.summary())
    model_odds=pd.DataFrame(np.exp(model.params),columns=['OR'])
    model_odds[['2.5%','97.5%']]=np.exp(model.conf_int())
    model_odds['Odds Ratio (95%CI)']=str(round(np.exp(model.params)[1],2))+'['+str(round(np.exp(model.conf_int()).iloc[1,0],2))+','+str(round(np.exp(model.conf_int()).iloc[1,1],2))+']'
    model_odds['P-value']= model.pvalues
    print(model_odds)
    results=results.append(model_odds)
results.to_csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/COVID-19/10. Statins and interactions for COVID 19/Updates/Database antecedent after.csv")   





# multivariate LR
s='';
for i in range(df.shape[1]-2):
    s=s+'+'+df.columns[i+2];
s=df.columns[0]+'~'+df.columns[1]+s;


s='Event~J1TOJ91+J1TOJ92+J1TOJ93+J1TOJ94+J1TOJ95+J1TOJ96+J1TOJ97+J1TOJ98+J1TOJ99';

mModel = smf.logit(formula = s, data = df).fit()  
mModel_odds=pd.DataFrame(np.exp(mModel.params),columns=['OR'])
mModel_odds[['2.5%','97.5%']]=np.exp(mModel.conf_int())
mModel_odds['P-value']= mModel.pvalues
print(mModel_odds)
mModel_oddsNew=[]
for i in range(mModel_odds.shape[0]):
    string=str(round(mModel_odds.iloc[i,0],3))+'['+str(round(mModel_odds.iloc[i,1],3))+','+str(round(mModel_odds.iloc[i,2],3))+']'
    mModel_oddsNew.append([string, mModel_odds.iloc[i,3]])
mModel_oddsNew=pd.DataFrame(mModel_oddsNew)











