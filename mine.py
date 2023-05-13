
import pandas
import matplotlib.pyplot as plt
import geopandas

def main():
    data = pandas.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")
    headers = list(data.columns.values)
    print(headers)
    data = data[data["location_key"].astype("str").str.startswith('US')]
    data = data[data["location_key"].astype("str").str.len() == 5]
    data = data.drop(columns=['date', 'new_confirmed', 'new_deceased', 'new_recovered', 'new_tested', 'cumulative_deceased', 'cumulative_recovered', 'cumulative_tested'])
    data['location_key'] = data['location_key'].astype("str").str[3:]
    data = data.groupby(['location_key'])['cumulative_confirmed'].max()
    population = pandas.read_csv("StatePop.csv")
    data = pandas.merge(
        left=data,
        right=population,
        left_on='location_key',
        right_on='location_key',
        how='left'
    )
    data["cumulative_percentage"] = data["cumulative_confirmed"]/data["population"]
    data.to_csv("US.csv")
    states = geopandas.read_file('StateShape/cb_2022_us_state_500k.shp')
    print(states['STUSPS'])
    states = pandas.merge(
        left=states,
        right=data,
        left_on='STUSPS',
        right_on='location_key',
        how='left'
    )
    print(states.columns)

    states = states[~states['NAME'].isin(['Alaska','Hawaii','Peurto Rico'])]

    bound = states.boundary.plot(linewidth=0.2)
    bound.set_xlim(-130, -50)
    bound.set_ylim(20, 50)
    states.plot(ax=bound, column='cumulative_percentage', legend=True, cmap='Reds')
    plt.show()
    plt.savefig('map.png')

    # states = 
    # states.head()
    # states = states.to_crs("EPSG:3395")
    # plt.show()


    # pandas.DataFrame(data.location_key.unique()).to_csv("unique.csv")


if __name__ == "__main__":
    main()