import numpy as np, pandas as pd, phonenumbers as pn, pycountry as pyc, re, os
from tqdm import tqdm
from datetime import date
from tkinter import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
date = date.today()
today = date.strftime("%m%d%y")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Choose xlsx file to clean
Tk().withdraw()  # Choose xlsx file
filename = askopenfilename()

Tk().withdraw()  # Choose folder to save in
save_path = filedialog.askdirectory()
try:  # create folders in selected save file
    os.chdir(save_path)
    os.mkdir('Day')
    os.mkdir('Night')
    os.mkdir('Leads')
except FileExistsError:
    pass
except OSError:
    sys.exit()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sheet_Name = input("Enter the Sheet Name: ")
Purchase_Site = input("Enter Purchase Site: ")
xls = pd.ExcelFile(filename)
df = xls.parse(Sheet_Name)  # create pandas DataFrame of selected xlsx file
df = df.dropna(subset=['telephone'])  # remove rows that have no data in their telephone column

TeleNum = df['telephone'].values
Numbers = []
Country = []

df['RAND'] = np.random.randint(0, 999999, size=(len(df), 1))  # sets a random number column(used to randomly sort leads)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def replace(origin_str):  # removes unwanted string from numbers
    result = re.sub('\D', '', origin_str)
    return result


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def cleanNumbers(number):  # checks number if it is a valid number
    vaild = True
    try:
        num = pn.parse('+' + str(number), None)
        if not pn.is_valid_number(num):  # Return true if number is valid
            vaild = False
    except:
        vaild = False
    return vaild


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def country(Number):  # get phone number's country name
    try:
        num = pn.parse('+' + str(Number), None)
        CountryInitial = pn.region_code_for_number(num)  # Get Country Initials
        return pyc.countries.get(alpha_2=CountryInitial).name  # Return Country Name
    except:
        pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def sortAsia(CleanNumbers):  # Find and sort Asia leads
    Asia_DataFrame = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['HK', 'SG', 'ID', 'JP', 'MO', 'MY', 'KR', 'TW']:  # Countries for Asia
        Asia_DataFrame = True
    return Asia_DataFrame


def sortGCC(CleanNumbers):  # Find and sort GCC leads
    GCC_DataFrame = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['BH', 'KW', 'QA', 'SA', 'AE', 'LB']:  # Countries for GCC
        GCC_DataFrame = True
    return GCC_DataFrame


def sortOC(CleanNumbers):  # Find and sort Oceania leads
    Oceania_DataFrame = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['NZ', 'AU']:  # Countries for Oceania
        Oceania_DataFrame = True
    return Oceania_DataFrame


def sortEU(CleanNumbers):  # Find and sort Europe leads
    Europe_DataFrame = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['LU', 'LI', 'IE', 'IS', 'NL', 'NO', 'PL', 'SE', 'CH', 'GB', 'DK', 'FI', 'DE', 'BG', 'HR',
                          'CY', 'EE', 'GR', 'HU', 'IM', 'LT', 'MT', 'MC', 'RO', 'CZ', 'PT']:  # Countries for Europe
        Europe_DataFrame = True
    return Europe_DataFrame


def sortAF(CleanNumbers):  # Find and sort Africa leads
    Africa_DataFrame = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['MG', 'ZA']:  # Countries for Africa
        Africa_DataFrame = True
    return Africa_DataFrame


def sortNA(CleanNumbers):  # Find and sort North Am leads
    NorthAm_DataFrame = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['CA', 'TT', 'BS']:  # Countries for North Am
        NorthAm_DataFrame = True
    return NorthAm_DataFrame


def sortIT(CleanNumbers):  # Find and sort Italy leads
    Italy_DataFrame = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['IT']:  # Sort Italy
        Italy_DataFrame = True
    return Italy_DataFrame


def sortES(CleanNumbers):  # Find and sort Spain leads
    Spain_DataFrame = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['ES']:  # Sort Spain
        Spain_DataFrame = True
    return Spain_DataFrame


def sortBR(CleanNumbers):  # Find and sort Brazil leads
    Brazil_DataFrame = False
    num = pn.parse('+' + str(CleanNumbers), None)
    CountryInitial = pn.region_code_for_number(num)
    if CountryInitial in ['BR']:  # Sort Brazil
        Brazil_DataFrame = True
    return Brazil_DataFrame


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def sortDay(Daydf):
    Day = {}
    for group, df in Daydf.groupby(np.arange(len(Daydf)) // 5000):
        Day[group] = df
    return Day


def sortNight(Nightdf):
    Night = pd.DataFrame()
    for group, df in Nightdf.groupby(np.arange(len(Nightdf)) // 5000):
        Night[group] = df
    return Night


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
for UncleanNum in tqdm(TeleNum):  # cleaning for any unwanted strings
    newnum = replace(str(UncleanNum))  # calling replace function
    Numbers.append(newnum)  # store string back in data frame
else:
    df = df.drop(columns=['telephone'])
    df.insert(1, "telephone", Numbers)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
df = df[df['telephone'].apply(cleanNumbers)]  # Clean Numbers
TeleNum = df['telephone'].values

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
for UncleanNum in tqdm(TeleNum):  # place country name
    newdata = country(str(UncleanNum))  # calling replace function
    Country.append(newdata)  # store string back in data frame
else:
    df = df.drop(columns=['country'])
    df['country'] = Country

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Sort Asia Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortAsia(UncleanNum)]
Asia = pd.DataFrame(df[df.telephone.isin(NewData)])  # Create a new pandas DataFrame for Asia
Asia['Lead Name'] = 'Asia ' + Purchase_Site + ' ' + str(today)  # Create a column for lead names

# Sort GCC Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortGCC(UncleanNum)]
GCC = pd.DataFrame(df[df.telephone.isin(NewData)])  # Create a new pandas DataFrame for GCC
GCC['Lead Name'] = 'GCC ' + Purchase_Site + ' ' + str(today)  # Create a column for lead names

# Sort OC Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortOC(UncleanNum)]
OC = pd.DataFrame(df[df.telephone.isin(NewData)])  # Create a new pandas DataFrame for Oceania
OC['Lead Name'] = 'Oceania ' + Purchase_Site + ' ' + str(today)  # Create a column for lead names

# Sort EU Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortEU(UncleanNum)]
EU = pd.DataFrame(df[df.telephone.isin(NewData)])  # Create a new pandas DataFrame for Europe
EU['Lead Name'] = 'Europe ' + Purchase_Site + ' ' + str(today)  # Create a column for lead names

# Sort AF Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortAF(UncleanNum)]
AF = pd.DataFrame(df[df.telephone.isin(NewData)])  # Create a new pandas DataFrame for Africa
AF['Lead Name'] = 'Africa ' + Purchase_Site + ' ' + str(today)  # Create a column for lead names

# Sort NA Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortNA(UncleanNum)]
NA = pd.DataFrame(df[df.telephone.isin(NewData)])  # Create a new pandas DataFrame for North Am
NA['Lead Name'] = 'North Am ' + Purchase_Site + ' ' + str(today)  # Create a column for lead names

# Sort IT Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortIT(UncleanNum)]
IT = pd.DataFrame(df[df.telephone.isin(NewData)])  # Create a new pandas DataFrame for Italy
IT['Lead Name'] = 'Italy ' + Purchase_Site + ' ' + str(today)  # Create a column for lead names

# Sort ES Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortES(UncleanNum)]
ES = pd.DataFrame(df[df.telephone.isin(NewData)])  # Create a new pandas DataFrame for Spain
ES['Lead Name'] = 'Spain ' + Purchase_Site + ' ' + str(today)  # Create a column for lead names

# Sort BR Numbers
NewData = [UncleanNum for UncleanNum in tqdm(TeleNum) if sortBR(UncleanNum)]
BR = pd.DataFrame(df[df.telephone.isin(NewData)])  # Create a new pandas DataFrame for Brazil
BR['Lead Name'] = 'Brazil ' + Purchase_Site + ' ' + str(today)  # Create a column for lead names

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Day Sort
Day = [OC, Asia]  # store OC DataFrame and Asia DataFrame
Day = pd.concat(Day)  # combine the DataFrame
Day = Day.sort_values(by='RAND')  # Sort RAND column
Day = Day.drop(columns=['RAND'])  # Drop RAND column
NewData = sortDay(Day)  # Call sortDay
for Array in tqdm(NewData):  # Save DataFrames as individual files
    new_file = pd.DataFrame(NewData[Array])
    path = save_path + '\\Day\\' + str(Array + 1) + ' ' + Purchase_Site + ' Day.csv'
    new_file.to_csv(path, index=False, header=False)

# Night Sort
Night = [EU, GCC]  # store EU DataFrame and GCC DataFrame
Night = pd.concat(Night)  # combine the DataFrame
Night = Night.sort_values(by='RAND')  # Sort RAND column
Night = Night.drop(columns=['RAND'])  # Drop RAND column
NewData = sortDay(Night)  # Call sortNight
for Array in tqdm(NewData):  # Save DataFrames as individual files
    new_file = pd.DataFrame(NewData[Array])
    path = save_path + '\\Night\\' + str(Array + 1) + ' ' + Purchase_Site + ' Night.csv'
    new_file.to_csv(path, index=False, header=False)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if not Asia.empty:
    Asia.to_csv(save_path + '\\Leads\\Asia.csv', index=False, header=False)
if not GCC.empty:
    GCC.to_csv(save_path + '\\Leads\\GCC.csv', index=False, header=False)
if not OC.empty:
    OC.to_csv(save_path + '\\Leads\\OC.csv', index=False, header=False)
if not EU.empty:
    EU.to_csv(save_path + '\\Leads\\EU.csv', index=False, header=False)
if not AF.empty:
    AF.to_csv(save_path + '\\Leads\\AF.csv', index=False, header=False)
if not NA.empty:
    NA.to_csv(save_path + '\\Leads\\NA.csv', index=False, header=False)
if not IT.empty:
    IT.to_csv(save_path + '\\Leads\\IT.csv', index=False, header=False)
if not ES.empty:
    ES.to_csv(save_path + '\\Leads\\ES.csv', index=False, header=False)
if not BR.empty:
    BR.to_csv(save_path + '\\Leads\\BR.csv', index=False, header=False)

myFile = open(save_path + '\\Read me.txt', 'w')
myFile.write("Don't forget to change the decimal to '0'.")
myFile.close()
