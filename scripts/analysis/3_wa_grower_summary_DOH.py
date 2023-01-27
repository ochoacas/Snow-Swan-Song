import pandas as pd

# Contact Washington State Department of Health for the latest data to include in the inputs folder
infile_approved = r'inputs/Approved Harvest Site Data.xlsx'
infile_inactive = r'inputs/Inactive Harvest Site Data.xlsx'
infile_withdrawn = r'inputs/Withdrawn Harvest Site Data.xlsx'
infiles = [infile_approved, infile_inactive, infile_withdrawn]
# Concatenate the spreadsheets into one data frame
dfs = []
for infile in infiles:
    df = pd.read_excel(infile, sheet_name='HarvestSite')
    dfs.append(df)
df = pd.concat(dfs)
infiles, dfs = [], []
date_fields = ['CertificationDate', 'StatusDate', 'LeaseExpireDate', 'ApplicationReceivedDate']
for date_field in date_fields:
    pd.to_datetime(df[date_field])
    df[date_field].fillna(pd.Timestamp(1700, 1, 1), inplace=True)
    df['year_' + date_field] = [int(d.year) for d in df[date_field]]
    df_company_count_per_year = df.groupby('year_' + date_field).CompanyName.nunique()
    df_growingArea_count_per_year = df.groupby('year_' + date_field).GrowingAreaName.nunique()
    df_waterBody_count_per_year = df.groupby('year_' + date_field).WaterbodyName.nunique()
    df_parcelOwner_count_per_year = df.groupby('year_' + date_field).ParcelOwner.nunique()
    df_ParcelCity_count_per_year = df.groupby('year_' + date_field).ParcelCity.nunique()
    df_ParcelCounty_count_per_year = df.groupby('year_' + date_field).ParcelCounty.nunique()
    df_Acreage_mean_per_year = df.groupby('year_' + date_field).Acreage.mean()
    pd.DataFrame.to_csv(df_company_count_per_year, 'WA_grower_companyCount_DOH_' + date_field + '.csv',
                        sep=',', na_rep='.', index=True)
    pd.DataFrame.to_csv(df_growingArea_count_per_year, 'WA_grower_growingAreaCount_DOH_' + date_field + '.csv',
                        sep=',', na_rep='.', index=True)
    pd.DataFrame.to_csv(df_waterBody_count_per_year, 'WA_grower_waterBodyCount_DOH_' + date_field + '.csv',
                        sep=',', na_rep='.', index=True)
    pd.DataFrame.to_csv(df_parcelOwner_count_per_year, 'WA_grower_parcelOwnerCount_DOH_' + date_field + '.csv',
                        sep=',', na_rep='.', index=True)
    pd.DataFrame.to_csv(df_ParcelCity_count_per_year, 'WA_grower_parcelCityCount_DOH_' + date_field + '.csv',
                        sep=',', na_rep='.', index=True)
    pd.DataFrame.to_csv(df_ParcelCounty_count_per_year, 'WA_grower_parcelCountyCount_DOH_' + date_field + '.csv',
                        sep=',', na_rep='.', index=True)
    pd.DataFrame.to_csv(df_Acreage_mean_per_year, 'WA_grower_acreageMean_DOH_' + date_field + '.csv',
                        sep=',', na_rep='.', index=True)
pd.DataFrame.to_csv(df, 'WA_grower_summary_DOH.csv', sep=',', na_rep='.', index=False)
df_company_summary = df.groupby('CompanyName').Acreage.mean()
pd.DataFrame.to_csv(df_company_summary, 'WA_grower_acreageMeanPerCompany_DOH.csv',
                    sep=',', na_rep='.', index=True)
cols = df.columns
for col in cols:
    print(df[col].value_counts())
