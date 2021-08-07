import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime as dt
import re
import csv
from sklearn.linear_model import LinearRegression,LogisticRegression,Ridge,RidgeCV,Lasso, LassoCV
from sklearn.model_selection import train_test_split,GridSearchCV,cross_val_score,cross_validate
from sklearn import  metrics as mt
from  statsmodels.stats.outliers_influence import variance_inflation_factor
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from decimal import *
from collections import Counter
import category_encoders as ce
import math
from scipy import stats
from scipy.stats.mstats import kruskalwallis
from pandas import read_csv
import os
import xlrd
from os.path import join, dirname, abspath, isfile
filePath = '/Users/jadonzhou/Research Projects/OneDrive/Psychology Science/Xuejin/Bio study Early Child Education/Data/'
file=filePath+"Data.csv"
# author network
Data = pd.read_csv(file)
result=[]
uniqueAuthors=[]
for authorstr in Data['Author Full Names'].values.tolist():
    if ';' in authorstr:
        temp=authorstr.split(";")
        if len(temp)>=2:
            tempres=[]
            for i in range(len(temp)):
                for j in range(i+1,len(temp)):
                    if (temp[i]!=temp[j]):
                        print([temp[i], temp[j]])
                        tempres.append([temp[i], temp[j]])
                        result.append([temp[i], temp[j]])
                        uniqueAuthors=uniqueAuthors+temp
                    else:
                        print("dup")
        else:
            print("Solo")
    else:
        print("Non-author")
result=pd.DataFrame(result)
result.to_csv(filePath+'Author Graph.csv')
uniqueAuthors=pd.DataFrame(np.unique(uniqueAuthors).tolist())
uniqueAuthors.to_csv(filePath+'Author set.csv')


# keywords graph
Data = pd.read_csv(file)
result=[]
uniquekeywords=[]
for authorstr in Data['AuthorKeywords'].values.tolist():
    authorstr=authorstr.lower()
    if ';' in authorstr:
        temp=authorstr.split(";")
        temp=np.unique(temp).tolist()
        if len(temp)>=2:
            tempres=[]
            for i in range(len(temp)):
                for j in range(i+1,len(temp)):
                    if (temp[i]!=temp[j]):
                        print([temp[i], temp[j]])
                        tempres.append([temp[i], temp[j]])
                        result.append([temp[i], temp[j]])
                        uniquekeywords=uniquekeywords+temp
                    else:
                        print("dup")
        else:
            print("Solo")
    else:
        print("Non-author")
result=pd.DataFrame(result)
result.to_csv(filePath+'Keywords Graph.csv')
uniquekeywords=pd.DataFrame(np.unique(uniquekeywords).tolist())
uniquekeywords.to_csv(filePath+'Keywords set.csv')


# institution network
Data = pd.read_csv(file)
result=[]
uniqueInstitutions=[]
for instituteStr in Data['Addresses'].values.tolist():
    if not (instituteStr == '' or (isinstance(instituteStr, float) and  math.isnan(instituteStr))) and ';' in instituteStr:
        temp=instituteStr.split("] ")
        if len(temp)>=3:
            addressList=[]
            for k in range(1,len(temp)):
                addressList.append(temp[k].split("; [")[0].split(',')[0])
            tempAddress=[]
            for i in range(len(addressList)):
                for j in range(i+1,len(addressList)):
                    if (addressList[i]!=addressList[j]):
                        print([addressList[i], addressList[j]])
                        tempAddress.append([addressList[i], addressList[j]])
                        result.append([addressList[i], addressList[j]]) 
                        uniqueInstitutions=uniqueInstitutions+addressList
        else:
            print("Solo")
    else:
        print("Non-author")
result=pd.DataFrame(result)
result.to_csv(filePath+'Institution Graph.csv')
uniqueInstitutions=pd.DataFrame(np.unique(uniqueInstitutions).tolist())
uniqueInstitutions.to_csv(filePath+'Institution set.csv')

# country network
Data = pd.read_csv(file)
result=[]
uniqueCountries=[]
for instituteStr in Data['Addresses'].values.tolist():
    if not (instituteStr == '' or (isinstance(instituteStr, float) and  math.isnan(instituteStr))) and ';' in instituteStr:
        temp=instituteStr.split("] ")
        if len(temp)>=3:
            countries=[]
            for k in range(1,len(temp)):
                address=temp[k].split("; [")[0].split(',')
                conutryCandidate=address[len(address)-1]
                if conutryCandidate[-4:]==" USA":
                    countries.append("USA")
                else:
                    countries.append(conutryCandidate)
            countries=np.unique(countries).tolist()
            if len(countries)>=2:
                for i in range(len(countries)):
                    for j in range(i+1,len(countries)):
                        print([countries[i], countries[j]])
                        result.append([countries[i], countries[j]])
                        uniqueCountries=uniqueCountries+countries
            else:
                result.append([countries[0], countries[0]])
        else:
            print("Solo")
    else:
        print("Non-author")
result=pd.DataFrame(result)
result.to_csv(filePath+'Country Graph.csv')
uniqueCountries=pd.DataFrame(np.unique(uniqueCountries).tolist())
uniqueCountries.to_csv(filePath+'Countries set.csv')



# merge values in a single column
Data = pd.read_csv("/Users/jadonzhou/Research Projects/OneDrive/Psychology Science/Xuejin/BrS bio analysis/Old/Database.csv")
result=[]
for string in Data['AuthorKeywords'].values.tolist():
    if not (string == '' or (isinstance(string, float) and  math.isnan(string))) and ';' in string:
        temp=string.split(";")
        for value in temp:
            result.append(value)
    else:
        print("Empty value")
result=pd.DataFrame(result)
result.to_csv(filePath+'KeywordsFreq.csv')




# author keywords network
Data = pd.read_csv(file)
result=[]
for authorstr in Data['AuthorKeywordsNetwork'].values.tolist():
    #authorstr=authorstr.lower()
    if ';' in authorstr:
        temp=authorstr.split(";")
        temp=np.unique(temp).tolist()
        if len(temp)>=2:
            tempres=[]
            for i in range(len(temp)):
                for j in range(i+1,len(temp)):
                    if (temp[i]!=temp[j]):
                        print([temp[i], temp[j]])
                        tempres.append([temp[i], temp[j]])
                        result.append([temp[i], temp[j]])
                    else:
                        print("dup")
        else:
            print("Solo")
    else:
        print("Non-author")
result=pd.DataFrame(result)
result.to_csv(filePath+'Author keywords Graph.csv')


# institution set by each article
Data = pd.read_csv(file)
result=[]
for instituteStr in Data['Addresses'].values.tolist():
    if '[' in instituteStr:
        temp=instituteStr.split("] ")
        institutions=[]
        for k in range(1,len(temp)):
            institutions.append(temp[k].split("; [")[0].split(',')[0])
        result.append(';'.join(institutions))
    else:
        result.append(';')  
        print("Non-Addresses")
result=pd.DataFrame(result)
result.to_csv(filePath+'Institution set by each article.csv')

# institution keywords network
Data = pd.read_csv(file)
result=[]
for authorstr in Data['InstitutionsKeywordsNetwork'].values.tolist():
    #authorstr=authorstr.lower()
    if ';' in authorstr:
        temp=authorstr.split(";")
        temp=np.unique(temp).tolist()
        if len(temp)>=2:
            tempres=[]
            for i in range(len(temp)):
                for j in range(i+1,len(temp)):
                    if (temp[i]!=temp[j]):
                        print([temp[i], temp[j]])
                        tempres.append([temp[i], temp[j]])
                        result.append([temp[i], temp[j]])
                    else:
                        print("dup")
        else:
            print("Solo")
    else:
        print("Non-author")
result=pd.DataFrame(result)
result.to_csv(filePath+'Institution keywords Graph.csv')


# country set by each article
Data = pd.read_csv(file)
result=[]
for instituteStr in Data['Addresses'].values.tolist():
    if not (instituteStr == '' or (isinstance(instituteStr, float) and  math.isnan(instituteStr))) and '[' in instituteStr:
        temp=instituteStr.split("] ")
        countries=[]
        for k in range(1,len(temp)):
            address=temp[k].split("; [")[0].split(',')
            conutryCandidate=address[len(address)-1]
            if conutryCandidate[-4:]==" USA":
                countries.append("USA")
            else:
                countries.append(conutryCandidate)
        countries=np.unique(countries).tolist()
        result.append(';'.join(countries)) 
    else:
        result.append(';') 
result=pd.DataFrame(result)
result.to_csv(filePath+'Country set by each article.csv')


# countries keywords network
Data = pd.read_csv(file)
result=[]
for authorstr in Data['CountryKeywordsNetwork'].values.tolist():
    #authorstr=authorstr.lower()
    if ';' in authorstr:
        temp=authorstr.split(";")
        temp=np.unique(temp).tolist()
        if len(temp)>=2:
            tempres=[]
            for i in range(len(temp)):
                for j in range(i+1,len(temp)):
                    if (temp[i]!=temp[j]):
                        print([temp[i], temp[j]])
                        tempres.append([temp[i], temp[j]])
                        result.append([temp[i], temp[j]])
                    else:
                        print("dup")
        else:
            print("Solo")
    else:
        print("Non-author")
result=pd.DataFrame(result)
result.to_csv(filePath+'Country keywords Graph.csv')





# author-country
Data = pd.read_csv(file)
result=[]
for instituteStr in Data['Addresses'].values.tolist():
    if ';' in instituteStr:
        temp=instituteStr.split("; [")
        if len(temp)>=1:
            addressList=[]
            for k in range(1,len(temp)):
                atemp=temp[k].split("] ")[0].split(';')
                ctemp=temp[k].split("] ")[1].split(',')
                country=ctemp[len(ctemp)-1]
                if (len(atemp)==1):
                    author=atemp[0]
                    result.append([author, country])
                else:
                    for i in range(len(atemp)):
                        author=atemp[i]
                        result.append([author, country])
        else:
            print("Solo")
    else:
        print("Non-author")
result=pd.DataFrame(result)
result.to_csv(filePath+'Author country.csv')




















filePath = '/Users/jadonzhou/Research Projects/OneDrive/Psychology Science/Xuejin/Left-behind bio study/'
filepaths=os.listdir(filePath)
if '.DS_Store' in filepaths:
    filepaths.remove('.DS_Store')
Data=[]
for path in filepaths:
    if isfile(filePath+path):
        print ('File exist: ', path)
        raw = xlrd.open_workbook(filePath+path)
        xl_sheet = raw.sheet_by_index(0)
        for row_idx in range(0, xl_sheet.nrows):    # Iterate through rows
            row = xl_sheet.row_values(row_idx)
            Data.append(row)
Data=pd.DataFrame(Data)            
variables=['Publication Type',
 'Authors',
 'Book Authors',
 'Book Editors',
 'Book Group Authors',
 'Author Full Names',
 'Book Author Full Names',
 'Group Authors',
 'Article Title',
 'Source Title',
 'Book Series Title',
 'Book Series Subtitle',
 'Language',
 'Document Type',
 'Conference Title',
 'Conference Date',
 'Conference Location',
 'Conference Sponsor',
 'Conference Host',
 'Author Keywords',
 'Keywords Plus',
 'Abstract',
 'Addresses',
 'Reprint Addresses',
 'Email Addresses',
 'Researcher Ids',
 'ORCIDs',
 'Funding Orgs',
 'Funding Text',
 'Cited References',
 'Cited Reference Count',
 'Times Cited, WoS Core',
 'Times Cited, All Databases',
 '180 Day Usage Count',
 'Since 2013 Usage Count',
 'Publisher',
 'Publisher City',
 'Publisher Address',
 'ISSN',
 'eISSN',
 'ISBN',
 'Journal Abbreviation',
 'Journal ISO Abbreviation',
 'Publication Date',
 'Publication Year',
 'Volume',
 'Issue',
 'Part Number',
 'Supplement',
 'Special Issue',
 'Meeting Abstract',
 'Start Page',
 'End Page',
 'Article Number',
 'DOI',
 'Book DOI',
 'Early Access Date',
 'Number of Pages',
 'WoS Categories',
 'Research Areas',
 'IDS Number',
 'UT (Unique WOS ID)',
 'Pubmed Id',
 'Open Access Designations',
 'Highly Cited Status',
 'Hot Paper Status',
 'Date of Export',
 '']
Data.columns=variables
Data=Data.drop_duplicates()
Data.to_csv(filePath+'Data.csv')









