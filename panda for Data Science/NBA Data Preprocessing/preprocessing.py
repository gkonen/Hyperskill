import pandas as pd
import os
import requests
from math import ceil
from itertools import combinations
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# Checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# Download data if it is unavailable.
if 'nba2k-full.csv' not in os.listdir('../Data'):
    print('Train dataset loading.')
    url = "https://www.dropbox.com/s/wmgqf23ugn9sr3b/nba2k-full.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/nba2k-full.csv', 'wb').write(r.content)
    print('Loaded.')

data_path = "../Data/nba2k-full.csv"

def clean_data(data_path):
    df = pd.read_csv(data_path)
    df["b_day"] = pd.to_datetime(df["b_day"], format="%m/%d/%y")
    df["draft_year"] = pd.to_datetime(df["draft_year"], format="%Y")
    df["team"] = df["team"].fillna("No Team")
    df["height"] = df["height"].str.split("/").apply(lambda x: x[1].strip()).astype(float)
    df["weight"] = df["weight"].str.split("/").apply(lambda x: x[1].strip()[:-3]).astype(float)
    df["salary"] = df["salary"].apply(lambda x: x.replace("$", "")).astype(float)
    df["country"] = df["country"].apply(lambda x: x if x == "USA" else "Not-USA")
    df["draft_round"] = df["draft_round"].apply(lambda x: "0" if x == "Undrafted" else x)
    return df

def feature_data(clean_df):
    clean_df["version"] = pd.to_datetime(clean_df["version"].apply(lambda x: 2020 if x[-1] == '0' else 2021), format="%Y")
    clean_df["age"] = ((clean_df["version"] - clean_df["b_day"]).dt.days / 365).apply(ceil)
    clean_df["experience"] = ((clean_df["version"] - clean_df["draft_year"]).dt.days // 365)
    clean_df["bmi"] = clean_df["weight"] / clean_df["height"] ** 2
    clean_df = clean_df.drop(columns=["version", "b_day", "draft_year", "weight", "height"])

    categorical_feature = clean_df.select_dtypes('object').columns.to_list()
    column_to_drop = clean_df[categorical_feature].nunique().loc[clean_df[categorical_feature].nunique() > 50].index.to_list()
    clean_df = clean_df.drop(columns=column_to_drop)
    return clean_df

def multicol_data(feature_df):
    mat_corr = feature_df.corr(method="pearson", numeric_only=True)
    feature = feature_df.drop(columns=["salary"])

    column_to_drop = []
    for pair in combinations(feature.select_dtypes('number').columns.to_list(), 2):
        if (corr := mat_corr.loc[pair[0], pair[1]]) > 0.5 or (corr < -0.5):
            if mat_corr.loc[pair[0], 'salary'] > mat_corr.loc[pair[1], 'salary']:
                column_to_drop.append(pair[1])
            else:
                column_to_drop.append(pair[0])

    return feature_df.drop(columns=column_to_drop)

def transform_data(multicol_df):
    # numerical features
    num_feat = multicol_df.select_dtypes('number')
    target = multicol_df['salary']
    num_feat = num_feat.drop(columns=['salary'])

    scaler = StandardScaler()
    scaler.set_output(transform="pandas")
    num_feat = scaler.fit_transform(num_feat)

    # categorical features
    cat_feat = multicol_df.select_dtypes('object')
    encoder = OneHotEncoder(sparse_output=False,
                            feature_name_combiner=lambda input_feature, category: str(category))
    encoder.set_output(transform="pandas")
    cat_feat = encoder.fit_transform(cat_feat)

    new_df = pd.concat([num_feat, cat_feat], axis=1)

    return new_df, target