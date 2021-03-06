# authors: Yuanzhe Marco Ma, Sicheng Sun, Guanshu Tao, Yuan Xiong
# date: 2021-01-23
import pandas as pd
import numpy as np
import altair as alt


"""
Class for data wrangling
"""
class DataManager():

    # retreieve data
    def get_data(self):
        df = pd.read_csv('data/processed/processed_data.csv', index_col=0)
        return df

    # make initial table, land-on page
    def make_table(self, data):
        table = data[['Name', 'Nationality', 'Age', 'Value(€)', 'Overall']]
        table = table.sort_values('Overall', ascending=False)[:15]
        table['Ranking'] = np.arange(table.shape[0]) + 1
        return table

    # make initial charts, land-on page
    def plot_altair(self, data, by='Overall', ascending=False, show_n=10):
        df_nation = data.groupby('Nationality').agg({by: 'mean'}).reset_index()
        df_nation = df_nation.sort_values(by, ascending=ascending)[:show_n]
        nation_chart = alt.Chart(df_nation).mark_bar().encode(
            alt.X('Nationality', sort='-y'),
            alt.Y(by)).properties(
                height=150,
                width=200)

        df_club = data.groupby('Club').agg({by: 'mean'}).reset_index()
        df_club = df_club.sort_values(by, ascending=ascending)[:show_n]
        club_chart = alt.Chart(df_club).mark_bar().encode(
            alt.X('Club', sort='-y'),
            alt.Y(by)).properties(
                height=150,
                width=200)
        return club_chart & nation_chart


    # Updates table from given parameters
    #
    # df : dataframe, processed dataset
    # by : str, column to sort by
    # order : bool, determines ascending or not
    # cols : list(str), columns to include in table
    # filter_natn: str, column to filter Nationality on
    # filter_club: str, column to filter Club on
    #
    # return : dataframe, top ten rows of the sorted dataset
    def update_table(self, data, by, order, cols,
                     filter_cont, filter_club):

        # column conditions
        # 1. by (sort by) column must be present
        # 2. player Name must be present
        if not(by in cols):
            cols.append(by)
        if not('Name' in cols):
            cols.append('Name')

        # update table
        if filter_cont:
            data = data[data['Continent'] == filter_cont]
        if filter_club:
            data = data[data['Club'] == filter_club]
        table = data[cols]
        table = table.sort_values(by=by, ascending=False)
        table['Ranking'] = np.arange(table.shape[0]) + 1
        table = table.sort_values(by='Ranking', ascending=order)[:15]

        # Re-arrange columns
        cols.append('Ranking')
        cols.insert(0, cols.pop(cols.index('Name')))
        cols.insert(0, cols.pop(cols.index('Ranking')))
        table = table[cols]
        return table

