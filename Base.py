import pandas as pd
import numpy as np
import os
import phonenumbers

os.chdir('C:\\Users\\CSR001\\Documents\\CleanLeads')

xls = pd.ExcelFile('Lead.xlsx')
df = pd.read_excel(xls, 'Sheet2', encoding='utf8')
NCNumbers = df['telephone'].values
SCNumbers = []

df = df.dropna(subset=['telephone'])

for Unclean in NCNumbers:
    try:
        Number = phonenumbers.parse('+' + str(Unclean), None)
        SCNumbers.append(Number)
    except:
        df = df.drop(df[df.telephone == Unclean].index)

for SecondClean in SCNumbers:
    Num = int(str(SecondClean.country_code) + str(SecondClean.national_number))
    if not phonenumbers.is_valid_number(SecondClean):
        df = df.drop(df[df.telephone == Num].index)

df = df.drop(columns=['country'])
df = df.sort_values(by=['email'])

df.to_excel('TEST.xlsx')

