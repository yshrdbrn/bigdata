import matplotlib.pyplot as plt
import pandas as pd


def group_by_category(df):
    grouped = df.groupby(['CATEGORY']).size().to_frame('Crimes')
    labels = ['Trespassing', 'Vehicle theft', 'General Theft',
              'Damage to Property', 'Robbery', 'Homicide']
    p = grouped.plot.pie(y='Crimes', labels=labels, autopct='%1.1f%%')
    p.set_title('Crimes Percentage Grouped By Category')
    p.get_legend().remove()
    plt.savefig('../charts/category.png')

def group_by_time_of_day(df):
    grouped = df.groupby(['TIME_OF_DAY']).size().to_frame('Crimes')
    p = grouped.plot.pie(y='Crimes', labels=['Day', 'Evening', 'Night'], autopct='%1.1f%%')
    p.set_title('Crimes Percentage Grouped By Time of Day')
    p.get_legend().remove()
    plt.savefig('../charts/time_of_day.png')

def group_by_day_of_the_week(df):
    grouped = df.groupby(['DAY_OF_THE_WEEK']).size().to_frame('Crimes')
    labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    p = grouped.plot.pie(y='Crimes', labels=labels, autopct='%1.1f%%')
    p.set_title('Crimes Percentage Grouped By Day of The Week')
    p.get_legend().remove()
    plt.savefig('../charts/day_of_the_week.png')

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
    p = grouped.plot.pie(y='Crimes', autopct='%1.1f%%')
    p.set_title('Crimes Percentage Grouped By Year')
    p.get_legend().remove()
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
    p.get_legend().remove()
    plt.savefig('../charts/territory.png')


if __name__ == '__main__':
    df = pd.read_csv('../data/crimes_dataset_processed_incomplete.csv')
    group_by_territory(df)
    group_by_year(df)
    group_by_month(df)
    group_by_time_of_day(df)
    group_by_day_of_the_week(df)
    group_by_category(df)
