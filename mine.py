
import pandas
import matplotlib.pyplot as plt
import geopandas

def main():
    houseData()

    

    
def houseData():
    # houseData = pandas.read_csv("HOUSE_precinct_general.tab", sep='\t')
    # houseData.to_csv("test.csv")

    # houseData = pandas.read_csv("test.csv")
    # houseData = houseData.groupby(['state', 'state_po', 'district', 'party_simplified']).sum()
    # print(houseData.columns)
    # houseData = houseData.drop(columns="Unnamed: 0")
    # houseData.to_csv("votes.csv")

    houseData = pandas.read_csv("votes.csv")
    totalVotes = houseData.groupby(['state', 'state_po', 'district']).sum()
    totalVotes = totalVotes.rename(columns={'votes': 'totalVotes'})
    totalVotes = totalVotes.drop(columns=['county_fips', 'jurisdiction_fips', 'year',
       'special', 'writein', 'state_fips', 'state_cen', 'state_ic',
       'readme_check', 'magnitude'])
    houseData = pandas.merge(
        left=houseData,
        right=totalVotes,
        left_on=['state', 'state_po', 'district'],
        right_on=['state', 'state_po', 'district'],
        how='left'
    )


    houseData['votePercentage'] = houseData['votes'] / houseData['totalVotes']

    houseData.to_csv("districtVotesPerc.csv")
    # print(houseData.columns)

    houseStateData = houseData.groupby(['state', 'state_po', 'party_simplified'], as_index=False).sum()
    print(houseStateData.columns)

    houseStateData = houseStateData.drop(columns=['votePercentage', 'district'])
    houseStateDataTemp = houseStateData.groupby(['state', 'state_po']).sum()
    houseStateDataTemp = houseStateDataTemp.rename(columns={'votes': 'totalStateVotes'})
    houseStateDataTemp = houseStateDataTemp.drop(columns=['totalVotes','county_fips', 'jurisdiction_fips', 'year',
       'special', 'writein', 'state_fips', 'state_cen', 'state_ic',
       'readme_check', 'magnitude'])
    houseStateData = pandas.merge(
        left=houseStateData,
        right=houseStateDataTemp,
        left_on=['state', 'state_po'],
        right_on=['state', 'state_po'],
        how='left'
    )

    houseStateData['votePercentage'] = houseStateData['votes'] / houseStateData['totalStateVotes']
    houseStateData.to_csv("stateVotesPerc.csv")

    houseStateData.loc[houseStateData["party_simplified"] == "OTHER", "votePercentage"] = 0
    houseStateData.loc[houseStateData["party_simplified"] == "LIBERTARIAN", "votePercentage"] = 0
    houseStateData.loc[houseStateData["party_simplified"] == "DEMOCRAT", "votePercentage"] *= -1

    houseStateData = houseStateData.groupby(['state', 'state_po']).sum()
    houseStateData = houseStateData.drop(columns=['votes','county_fips','jurisdiction_fips','year','special','writein','state_fips','state_cen','state_ic','readme_check','magnitude','totalVotes','totalStateVotes'])
    houseStateData.to_csv("bias.csv")

    states = geopandas.read_file('StateShape/cb_2022_us_state_500k.shp')
    print(states['STUSPS'])
    states = pandas.merge(
        left=states,
        right=houseStateData,
        left_on='STUSPS',
        right_on='state_po',
        how='left'
    )

    states = states[~states['NAME'].isin(['Alaska','Hawaii','Peurto Rico'])]

    bound = states.boundary.plot(linewidth=0.2)
    bound.set_xlim(-130, -60)
    bound.set_ylim(20, 50)
    # infection percentage graphing

    states.plot(ax=bound, column='votePercentage', legend=True, vmin = -1, vmax =1, cmap='RdBu_r')
    plt.axis('off')
    plt.show()
    plt.savefig('voterBias.png')


    # states = geopandas.read_file('StateShape/cb_2022_us_state_500k.shp')
    # print(states['STUSPS'])
    # states = pandas.merge(
    #     left=states,
    #     right=houseStateData,
    #     left_on='STUSPS',
    #     right_on='state_po',
    #     how='left'
    # )



def covidData():
    data = pandas.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")
    headers = list(data.columns.values)
    print(headers)
    data = data[data["location_key"].astype("str").str.startswith('US')]
    data = data[data["location_key"].astype("str").str.len() == 5]
    data = data.drop(columns=['date', 'new_confirmed', 'new_deceased', 'new_recovered', 'new_tested', 'cumulative_recovered', 'cumulative_tested'])
    data['location_key'] = data['location_key'].astype("str").str[3:]
    data = data.groupby(['location_key'])['cumulative_confirmed', 'cumulative_deceased'].max()
    population = pandas.read_csv("StatePop.csv")
    data = pandas.merge(
        left=data,
        right=population,
        left_on='location_key',
        right_on='location_key',
        how='left'
    )
    data["cumulative_percentage"] = data["cumulative_confirmed"]/data["population"]
    data["dead_percentage"] = data["cumulative_deceased"]/data["population"]
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
    bound.set_xlim(-130, -60)
    bound.set_ylim(20, 50)
    # infection percentage graphing
    states.plot(ax=bound, column='cumulative_percentage', legend=True, cmap='Reds')
    plt.axis('off')
    plt.show()
    plt.savefig('infectedPerc.png')


    # states.plot(ax=bound, column='dead_percentage', legend=True, cmap='Blues')
    # plt.axis('off')
    # plt.show()
    # plt.savefig('deadPerc.png')

    # states = 
    # states.head()
    # states = states.to_crs("EPSG:3395")
    # plt.show()


    # pandas.DataFrame(data.location_key.unique()).to_csv("unique.csv")


if __name__ == "__main__":
    main()