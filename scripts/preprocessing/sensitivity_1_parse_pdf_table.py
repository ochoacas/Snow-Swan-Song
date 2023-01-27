from tabula import read_pdf
import pandas as pd
import math

# California-certified shellfish dealers
dfs_ca = read_pdf('CA ONLY Shellfish Shippers List 012020.pdf', pages='1-5', guess=False, multiple_tables=True)
dfs_all_ca = []
columns_ca = ['Name', 'City', 'CertificationType', 'CertificationNumber', 'DealerActivity']

for df in dfs_ca:
    df.columns = columns_ca
    dfs_all_ca.append(df)

new_df_ca = pd.concat(dfs_all_ca)
new_df_ca.to_csv('Shellfishdealers_CA.csv', index=False)

print('California Complete!')

# Oregon-certified shellfish dealers
dfs_or = read_pdf('Shellfishdealers.pdf', pages='1-4', guess=False, multiple_tables=True)
dfs_all_or = []
columns_or = ['NameMailingCityMailingCountyOrCountry', 'DoingBusinessAsLocationCityLocationCounty', 'LicenseDescriptionStatus/Expiration']

addition = []

for i, df in enumerate(dfs_or):
    if i == 0:
        df = df.iloc[9:]
        df.columns = columns_or
        dfs_all_or.append(df)
    elif i == 2:
        df_addition = df.iloc[-1:]
        print(df_addition)
        addition.append(df_addition)
        df = df.iloc[:-1]
    elif i == 3:
        df = df.iloc[:-5]
        print(df.columns)
        # df['WILSONVILLE OR 97070'] = df['WILSONVILLE OR 97070 Active 12/31/2020'].str.split(' Active ', 1).str[0]
        df.columns = columns_or
        dfs_all_or.append(df)
    else:  # i == 4
        df.columns = columns_or
        dfs_all_or.append(df)

new_df_or = pd.concat(dfs_all_or)
new_df_or.to_csv('Shellfishdealers_OR.csv', index=False)

# Reformat Oregon data
df = pd.read_csv('Shellfishdealers_OR.csv')
columns_new = ['Name', 'DoingBusinessAs', 'LicenseDescription', 'MailingCity', 'LocationCity', 'Status/Expiration',
               'MailingCountyOrCountry', 'LocationCounty', 'Certification']
df_new = pd.DataFrame(columns=columns_new)

df1 = df.iloc[::3, :].reset_index(drop=True)  # first row
df2 = df.iloc[1::3, :].reset_index(drop=True)  # second row
df3 = df.iloc[2::3, :].reset_index(drop=True)  # third row
df123 = pd.concat([df1, df2, df3], axis=1)
df123.columns = columns_new
df123.to_csv('Shellfishdealers_OR.csv', index=False)

print('Oregon Complete!')

# WA Part I: Washington-certified shellfish dealers
dfs_wa = read_pdf('332-104.pdf', pages='1-16', guess=False, multiple_tables=True)
licenses_list = []
expirations_list = []
companies_list = []
growing_areas_list = []
lists = [licenses_list, expirations_list, companies_list, growing_areas_list]

# Iterate through each page in the PDF
for i, df in enumerate(dfs_wa):
    # First page has column headings
    if i == 0:
        columns = df.columns
        for k, key in enumerate(df.columns):
            for v in df[key].values:
                lists[k].append(v)
    else:
        for j, k in enumerate(df.columns):
            lists[j].append(k)
            for v in df[k].values:
                try:
                    v = float(v)
                    math.isnan(v)
                    v = ' '
                    lists[j].append(v)
                except:
                    lists[j].append(v)

# Create new data frame to collate lists parsed from PDF
df = pd.DataFrame({'LicenseNo': licenses_list,
                       'Expires': expirations_list,
                       'CompanyName': companies_list,
                       'GrowingAreas': growing_areas_list
                       })

# Save output CSV
df.to_csv('Shellfishdealers_WA.csv', index=False)

# WA Part II: Reformat WA data and handle nan locations
df = pd.read_csv('Shellfishdealers_WA.csv')

licenses_list = []
expirations_list = []
companies_list = []
growing_areas_list = []
count_growing_areas_list = []
wholesale_list = []
growareas = []

for grow_area in df["GrowingAreas"].str.split(";").values:
    try:
        if math.isnan(float(grow_area)):
            continue
    except:
        pass
    for growarea in grow_area:
        growarea = growarea.replace('\r', ' ')
        growareas.append(growarea)

# Summarize grow areas and firms

grow_areas = list(dict.fromkeys(growareas))

growing_area_firms = {key: 0 for key in grow_areas if key != ' '}

growing_areas_per_company = df["GrowingAreas"].str.split(";")
for company, growing_areas in enumerate(list(growing_areas_per_company)):
    # Fill in nan locations for growing areas
    if df['CompanyName'][company] == 'TAYLOR SHELLFISH CO. INC.':
        growing_areas = ['Annas Bay', 'Bay Center', 'Bruceport', 'Burley Lagoon', 'Cedar River', 'Dabob Bay',
                         'Discovery Bay', 'Drayton Passage', 'Eld Inlet', 'Filucy Bay', 'Hammersley Inlet',
                         'Harstine East', 'Henderson Inlet', 'Hood Canal 3', 'Hood Canal 8', 'Nahcotta',
                         'Naselle River', 'Nemah River', 'Nisqually Reach', 'North Bay', 'North River', 'Oakland Bay',
                         'Peale Passage', 'Pickering Passage', 'Rocky Bay', 'Samish Bay', 'Skookum Inlet',
                         'Stony Point', 'Stretch Island', 'Totten Inlet', 'West Key Penninsula']
    elif df['CompanyName'][company] == 'PALIX OYSTER COMPANY':
        growing_areas = ['Bay Center']
    elif df['CompanyName'][company] == 'SOUTH BEND PRODUCTS, LLC':
        growing_areas = ['Bruceport']
    elif df['CompanyName'][company] == 'SHE NAH NAM SEAFOOD GOV. CORP.':
        growing_areas = ['Nisqually Reach']
    elif df['CompanyName'][company] == 'CHETLO HARBOR SHELLFISH':
        growing_areas = ['Naselle River']
    growing_areas = [growing_area.replace('\r', ' ') for growing_area in growing_areas]
    # Identify wholesale firms and summarize growing areas
    if df['GrowingAreas'][company] == 'Wholesale Only':
        count_growing_areas = 0
        wholesale = 1
    else:
        count_growing_areas = len(growing_areas)
        wholesale = 0
    licenses_list.append(df['LicenseNo'][company])
    expirations_list.append(df['Expires'][company])
    companies_list.append(df['CompanyName'][company])
    growing_areas_list.append(';'.join(growing_areas))
    count_growing_areas_list.append(count_growing_areas)
    wholesale_list.append(wholesale)

for growing_area in growing_areas_list:
    for growarea in growing_area.split(';'):
        growing_area_firms[growarea] += 1

df = pd.DataFrame.from_dict(growing_area_firms, orient='index', columns=['firm_ct'])
df.index.name = 'grow_area'
df.to_csv('grow_areas_by_licensed_firms_WA.csv', index=True)

# Create new data frame to collate updated data
df_new = pd.DataFrame({'LicenseNo': licenses_list,
                       'Expires': expirations_list,
                       'CompanyName': companies_list,
                       'GrowingAreas': growing_areas_list,
                       'CountGrowingAreas': count_growing_areas_list,
                       'Wholesale': wholesale_list
                       })

# Output final, reformatted CSV
df_new.to_csv('Shellfishdealers_WA.csv', index=False)

print('Washington Complete!')
