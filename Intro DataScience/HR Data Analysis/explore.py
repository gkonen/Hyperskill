import pandas as pd
import requests
import os

# scroll down to the bottom to implement your solution
if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('A_office_data.xml' not in os.listdir('../Data') and
        'B_office_data.xml' not in os.listdir('../Data') and
        'hr_data.xml' not in os.listdir('../Data')):
        print('A_office_data loading.')
        url = "https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/A_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('B_office_data loading.')
        url = "https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/B_office_data.xml', 'wb').write(r.content)
        print('Loaded.')

        print('hr_data loading.')
        url = "https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/hr_data.xml', 'wb').write(r.content)
        print('Loaded.')

        # All data in now loaded to the Data folder.

    pd.options.display.max_columns = None
    pd.options.display.width = 1000

    #region : STAGE 1
    df_A = pd.read_xml('../Data/A_office_data.xml')
    df_B = pd.read_xml('../Data/B_office_data.xml')
    df_hr = pd.read_xml('../Data/hr_data.xml')

    df_A["employee_id"] = 'A' + df_A["employee_office_id"].astype(str)
    df_A = df_A.set_index('employee_id')
    df_A = df_A.drop(columns=['employee_office_id'])

    df_B["employee_id"] = 'B' + df_B["employee_office_id"].astype(str)
    df_B = df_B.set_index('employee_id')
    df_B = df_B.drop(columns=['employee_office_id'])

    df_hr = df_hr.set_index('employee_id')
    #endregion

    #region : STAGE 2
    df_office = pd.concat([df_A, df_B])
    df_merge = df_office.merge(df_hr, left_index=True, right_index=True).sort_index()
    #endregion

    #region STAGE 3
    # print( df_merge.sort_values(by=['average_monthly_hours'], ascending=False).head(10)['Department'].to_list() )
    # print( df_merge[ (df_merge['Department'] == 'IT') & (df_merge['salary'] == 'low') ]['number_project'].sum() )
    # print( list(map(lambda x: list(x), (df_merge.loc[['A4', 'B7064', 'A3033']][["last_evaluation", "satisfaction_level"]].itertuples(index=False, name=None)))))
    #endregion

    #region STAGE 4
    def count_bigger_5(number_project):
        return [ project > 5 for project in number_project ].count(True)

    # print( df_merge.groupby('left').agg( { 'number_project': ['median', count_bigger_5],
    #                        'time_spend_company': [ 'mean', 'median'],
    #                        'Work_accident': 'mean',
    #                        'last_evaluation': ['mean', 'std']
    #                        }).round(2).to_dict())
    #endregion

    #region STAGE 5
    pivot_table_dpt = df_merge.pivot_table(index="Department", columns=["left", "salary"], aggfunc={"average_monthly_hours": 'median'})
    pivot_table_dpt.columns = pivot_table_dpt.columns.droplevel(0)
    print(pivot_table_dpt[(pivot_table_dpt[ (0, 'high')] < pivot_table_dpt[ (0, 'medium')]) | (pivot_table_dpt[ (1, 'low')] < pivot_table_dpt[ (1, 'high')])].to_dict())

    pivot_table_time = df_merge.pivot_table(index="time_spend_company", columns=["promotion_last_5years"], aggfunc={"satisfaction_level" : [ 'min', 'max', 'mean'], "last_evaluation": [ 'min', 'max', 'mean'] })
    pivot_table_time.columns = pivot_table_time.columns.swaplevel(0,1)
    print(pivot_table_time[ pivot_table_time[('mean','last_evaluation', 0) ] > pivot_table_time[('mean','last_evaluation', 1)]].to_dict())
    #endregion

