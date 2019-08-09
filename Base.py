import numpy as np
import pandas as pd
import phonenumbers as pn
from tqdm import tqdm
import pycountry as pyc
import re
from datetime import date
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
date = date.today()
today = date.strftime("%m/%d/%y")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
path = r'C:\\Users\\CSR001\\Documents\\CleanLeads\\Lead.xlsx'

xls = pd.ExcelFile(path)
df = xls.parse("Sheet2")
df = df.dropna(subset=['telephone'])
RAND = pd.Series([])

TeleNum = df['telephone'].values
Numbers = []
Surname = []
Country = []

df['RAND'] = np.random.randint(0, 999999, size=(len(df),1))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def replace(orignstr):  # removes unwanted string from numbers
    result = re.sub('\D', '', orignstr)
    return result
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def cleanNumbers(number):  # checks number if it is a valid number
    vaild = True
    try:
        num = pn.parse('+' + str(number), None)
        if not pn.is_valid_number(num):
            vaild = False
    except:
        vaild = False
    return vaild
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def country(Number):
    try:
        num = pn.parse('+' + str(Number), None)
        CountryInitial = pn.region_code_for_number(num)
        return pyc.countries.get(alpha_2=CountryInitial).name
    except:
        pass
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def sortAsia(CleanNumbers):
    ASdf = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['HK', 'SG', 'ID', 'JP', 'MO', 'MY', 'KR', 'TW']:
        ASdf = True
    return ASdf


def sortGCC(CleanNumbers):
    GCCdf = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['BH', 'KW', 'QA', 'SA', 'AE', 'LB']:
        GCCdf = True
    return GCCdf


def sortOC(CleanNumbers):
    OCdf = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['NZ', 'AU']:
        OCdf = True
    return OCdf


def sortEU(CleanNumbers):
    EUdf = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['LU', 'LI', 'IE', 'IS', 'NL', 'NO', 'PL', 'SE', 'CH', 'GB', 'DK', 'FI', 'DE', 'BG', 'HR',
                          'CY', 'EE', 'GR', 'HU', 'IM', 'LT', 'MT', 'MC', 'RO', 'CZ', 'PT']:
        EUdf = True
    return EUdf


def sortAF(CleanNumbers):
    AFdf = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['MG', 'ZA']:
        AFdf = True
    return AFdf


def sortNA(CleanNumbers):
    NAdf = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['CA', 'TT', 'BS']:
        NAdf = True
    return NAdf


def sortIT(CleanNumbers):
    ITdf = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['IT']:
        ITdf = True
    return ITdf


def sortES(CleanNumbers):
    ESdf = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['ES']:
        ESdf = True
    return ESdf


def sortBR(CleanNumbers):
    BRdf = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['BR']:
        BRdf = True
    return BRdf
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def sortDay(Daydf):
    Day = {}
    for g, df in Daydf.groupby(np.arange(len(Daydf)) // 5000):
        Day[g] = df
    return Day


def sortNight(Nightdf):
    Night = pd.DataFrame()
    for g, df in Nightdf.groupby(np.arange(len(Nightdf)) // 5000):
        Night[g] = df
    return Night
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# cleaning for any unwanted strings
for UncleanNum in tqdm(TeleNum):
    newnum = replace(str(UncleanNum))  # calling replace function
    Numbers.append(newnum)  # store string back in data frame
else:
    df = df.drop(columns=['telephone'])
    df.insert(1, "telephone", Numbers)
    TeleNum = df['telephone'].values
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Clean Numbers
df = df[df['telephone'].apply(cleanNumbers)]
TeleNum = df['telephone'].values
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# place country name
for UncleanNum in tqdm(TeleNum):
    newdata = country(str(UncleanNum))  # calling replace function
    Country.append(newdata)  # store string back in data frame
else:
    df = df.drop(columns=['country'])
    df['country'] = Country
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Sort Asia Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortAsia(UncleanNum)]
Asia = df[df.telephone.isin(NewData)]
Asia['Lead Name'] = 'Asia M OldM' + str(today)
Asia.to_csv('C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\Asia.csv', index=False)

# Sort GCC Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortGCC(UncleanNum)]
GCC = df[df.telephone.isin(NewData)]
GCC['Lead Name'] = 'GCC M OldM' + str(today)
GCC.to_csv('C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\GCC.csv', index=False)

# Sort OC Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortOC(UncleanNum)]
OC = df[df.telephone.isin(NewData)]
OC['Lead Name'] = 'Oceania M OldM' + str(today)
OC.to_csv('C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\OC.csv', index=False)

# Sort EU Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortEU(UncleanNum)]
EU = df[df.telephone.isin(NewData)]
EU['Lead Name'] = 'Europe M OldM' + str(today)
EU.to_csv('C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\EU.csv', index=False)

# Sort AF Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortAF(UncleanNum)]
AF = df[df.telephone.isin(NewData)]
AF.to_csv('C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\AF.csv', index=False)

# Sort NA Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortNA(UncleanNum)]
NA = df[df.telephone.isin(NewData)]
NA.to_csv('C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\NA.csv', index=False)

# Sort IT Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortIT(UncleanNum)]
IT = df[df.telephone.isin(NewData)]
IT.to_csv('C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\IT.csv', index=False)

# Sort ES Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortES(UncleanNum)]
ES = df[df.telephone.isin(NewData)]
ES.to_csv('C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\ES.csv', index=False)

# Sort BR Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortBR(UncleanNum)]
BR = df[df.telephone.isin(NewData)]
BR.to_csv('C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\BR.csv', index=False)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Day Sort
i = 0
Day = [OC, Asia]
Day = pd.concat(Day)
Day = Day.sort_values(by='RAND')
Day = Day.drop(columns=['RAND'])
NewData = sortDay(Day)
for p in tqdm(NewData):
    n = pd.DataFrame(NewData[i])
    path = 'C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\Day\\' + str(i) + 'Day.csv'
    n.to_csv(path, index=False)
    i += 1

#Night Sort
i = 0
Night = [EU, GCC]
Night = pd.concat(Night)
Night = Night.sort_values(by='RAND')
Night = Night.drop(columns=['RAND'])
NewData = sortDay(Night)
for p in tqdm(NewData):
    n = pd.DataFrame(NewData[i])
    path = 'C:\\Users\\CSR001\\Documents\\CleanLeads\\Test\\Night\\' + str(i) + 'Night.csv'
    n.to_csv(path, index=False)
    i += 1
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
