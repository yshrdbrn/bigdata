import matplotlib.pyplot as plt
import pandas as pd


def group_by_time_of_day(df):
    grouped = df.groupby(['TIME_OF_DAY']).size().to_frame('Crimes')
    p = grouped.plot.pie(y='Crimes', labels=['Day', 'Evening', 'Night'])
    p.set_title('Crimes Percentage Grouped By Time of Day')
    plt.savefig('../charts/time_of_day.png')

def group_by_month(df):
    grouped = df.groupby(['MONTH']).size().to_frame('Size')
    grouped['Percentage'] = 100 * grouped['Size'] / len(df)
    grouped = grouped.drop(columns='Size')
    p = grouped.plot.bar()
    p.set_title('Crimes Percentage Grouped By Month')
    p.set_ylabel('Percentage of Crimes')
    p.set_xlabel('Month')
    p.get_legend().remove()
    plt.savefig('../charts/month.png')

def group_by_year(df):
    grouped = df.groupby(['YEAR']).size().to_frame('Crimes')
    p = grouped.plot.pie(y='Crimes')
    p.set_title('Crimes Percentage Grouped By Year')
    plt.savefig('../charts/year.png')

def group_by_territory(df):
    grouped = df.groupby(['PDQ']).size().to_frame('Size')
    grouped['Percentage'] = 100 * grouped['Size'] / len(df)
    grouped = grouped.drop(columns='Size')
    grouped.index = grouped.index.astype(int)
    p = grouped.plot.bar()
    p.set_title('Crimes Percentage Grouped By Territory')
    p.set_ylabel('Percentage of Crimes')
    p.set_xlabel('Territory Number')
    plt.savefig('../charts/territory.png')


if __name__ == '__main__':
    df = pd.read_csv('../data/crimes_dataset_processed_incomplete.csv')
    group_by_territory(df)
    group_by_year(df)
    group_by_month(df)
    group_by_time_of_day(df)
