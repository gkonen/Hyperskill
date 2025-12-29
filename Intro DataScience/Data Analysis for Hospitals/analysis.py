# write your code here
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

pd.set_option('display.max_columns', 8)
PATH = './test'

def stage_1():
    return [
        pd.read_csv(PATH + '/general.csv'),
        pd.read_csv(PATH + '/prenatal.csv'),
        pd.read_csv(PATH + '/sports.csv')
    ]

def stage_2(general_df, prenatal_df, sports_df):
    prenatal_df.columns = general_df.columns.to_list()
    sports_df.columns = general_df.columns.to_list()
    merge_df = pd.concat([general_df, prenatal_df, sports_df], axis=0, ignore_index=True)
    merge_df.drop(columns=['Unnamed: 0'], inplace=True)
    return merge_df

def stage_3(merge_df):
    # Remove empty rows
    merge_df = merge_df.dropna(how='all')
    # Replace void gender in prenatal
    merge_df.loc[(merge_df['hospital'] == 'prenatal') & merge_df['gender'].isna(), 'gender'] = 'f'
    merge_df.loc[:, 'gender'] = merge_df['gender'].replace({"man": "m", "woman": "f", "male": "m", "female": "f"})
    # Fill missing values
    columnName = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
    merge_df.loc[:, columnName] = merge_df.loc[:, columnName].fillna(0)
    return merge_df

def stage_4(clean_df):
    print("The answer to the 1st question is", clean_df.groupby(['hospital']).count().max(axis='columns').idxmax(axis='index'))
    print("The answer to the 2nd question is", clean_df[clean_df["hospital"] == 'general']["diagnosis"].value_counts(normalize=True)['stomach'].round(3))
    print("The answer to the 3rd question is", clean_df[clean_df["hospital"] == 'sports']['diagnosis'].value_counts(normalize=True)['dislocation'].round(3))
    print("The answer to the 4th question is", clean_df[clean_df["hospital"] == 'general']['age'].median() - clean_df[clean_df["hospital"] == 'sports']['age'].median())
    pivot = pd.pivot_table(clean_df, index=['hospital'], columns=['blood_test'], values='age' ,aggfunc='count', fill_value=0)
    print(f"The answer to the 5th question is {pivot['t'].idxmax()}, {pivot['t'].max()} blood tests")

def stage_5(clean_df):
    clean_df.hist(column='age', bins=[0, 15, 35, 55, 70, 80],  edgecolor='black', figsize=(10, 8))
    plt.show()
    print("The answer to the 1st question: 15-35")
    plt.pie(clean_df['diagnosis'].value_counts(), labels=clean_df['diagnosis'].value_counts().index, autopct='%.2f%%')
    plt.show()
    print("The answer to the 2nd question: pregnancy")
    sns.violinplot(data=clean_df, x='hospital', y='height')
    plt.show()
    # I search to answer the question: Why there are two peaks, which correspond to the relatively small and big values ?
    # Without context of the dataset, I'm not sure how to answer this question.
    print("The answer to the 3rd question: It's because we have a large distribution of people which lead to a normal distribution hence the peaks for minimum and maximum.")


if __name__ == '__main__':
    general_df, prenatal_df, sports_df = stage_1()
    merge_df = stage_2(general_df, prenatal_df, sports_df)
    clean_df = stage_3(merge_df)
    #stage_4(clean_df)
    stage_5(clean_df)
