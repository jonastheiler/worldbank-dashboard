import pandas as pd
import plotly.graph_objs as go
from collections import OrderedDict
import requests

# default list of all countries of interest
countries = OrderedDict([('United States', 'USA'),('China', 'CHN'),('Germany', 'DEU'),
                               ('United Kingdom', 'GBR'),('India', 'IND'),('France', 'FRA'),
                               ('Italy', 'ITA'),('Canada', 'CAN')])

def return_figures(countries=countries):
    """Creates plotly visualizations using the World Bank API
    Args:
        country_default (dict): list of countries for filtering the data
    Returns:
        list (dict): list containing the plotly visualizations
    """

    # preparing the country data for the API
    country_filter = list(countries.values())
    country_filter = [x.lower() for x in country_filter]
    country_filter = ';'.join(country_filter)

    # indicator of interest (gdp)
    indicators = ['NY.GDP.MKTP.CD']

    data_frames = []
    urls = []

    # pull data from World Bank API and clean the resulting json
    for indicator in indicators:
        url = 'http://api.worldbank.org/v2/countries/' + country_filter + \
              '/indicators/' + indicator + '?date=1960:2020&per_page=1000&format=json'
        urls.append(url)

        try:
            r = requests.get(url)
            data = r.json()[1]
        except:
            print('could not load data ', indicator)

        for i, value in enumerate(data):
            value['indicator'] = value['indicator']['value']
            value['country'] = value['country']['value']

        data_frames.append(data)

    # creating a line chart
    graph_one = []
    df_one = pd.DataFrame(data_frames[0])

    # creating a country-list
    countrylist = df_one.country.unique().tolist()

    for country in countrylist:
        x_val = df_one[df_one['country'] == country].date.tolist()
        y_val = df_one[df_one['country'] == country].value.tolist()
        graph_one.append(
            go.Scatter(
                x=x_val,
                y=y_val,
                mode='lines',
                name=country
            )
        )

    layout_one = dict(title='Development of GDP from 1960 to 2020',
                      xaxis=dict(title='Year'),
                      yaxis=dict(title='GDP in Trillion USD')
                      )

    # appending the charts to figures
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))

    return figures