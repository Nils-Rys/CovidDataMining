
import pandas
import matplotlib.pyplot as plt
import geopandas

def main():
    # cleanData()
    covidCountyData()
    # covidData()
    # houseData()
    # houseCountyData()

def cleanData():
    # county pop data from https://www.census.gov/data/tables/time-series/demo/popest/2020s-counties-total.html#v2022
    # grab county fips data for csv from https://github.com/ChuckConnell/articles/blob/master/fips2county.tsv
    
    # states = geopandas.read_file('CountyShape/cb_2021_us_county_500k.shp')
    # print("Test\n\n")
    # print(states.columns)
    # # print(states['STATEFP'])
    # states['STATEFP'] = states['STATEFP'].astype(str)
    # states['COUNTYFP'] = states['COUNTYFP'].astype(str)
    # states['county_fips'] = states['STATEFP'] + states['COUNTYFP']
    # states['county_fips'] = states['county_fips'].astype(float)
    # states = states.sort_values('county_fips')
    # print(states.iloc[310])


    # return
    
    countyFips = pandas.read_csv("fips2county.tsv", sep='\t', converters={'CountyFIPS': str})
    print(countyFips.columns)
    countyFips = countyFips.drop(columns=['StateFIPS', 'CountyFIPS_3'])
    countyFips['CountyName'] = countyFips['CountyName'].str.replace(' Parish', '')
    countyFips['CountyName'] = countyFips['CountyName'].str.replace(' Planning', '')

    countyFips.to_csv("countyFips.csv")

    countyPop = pandas.read_csv("co-est2022-pop.csv")
    countyPop[['county', 'state']] = countyPop['Location'].str.split(',', expand=True)
    countyPop["county"] = countyPop["county"].str[1:-7]
    countyPop["state"] = countyPop["state"].str[1:]
    
    countyPop.to_csv("temp.csv")
    countyPop = pandas.merge(
        left=countyPop,
        right=countyFips,
        left_on=['state', 'county'],
        right_on=['StateName', 'CountyName'],
        how='left'
    )
    countyPop = countyPop.drop(columns=['Location', 'CountyName', 'StateName', 'STATE_COUNTY'])
    countyPop['2020_earlyPop'] = countyPop['2020_earlyPop'].str.replace(',', '')
    countyPop['2020_pop'] = countyPop['2020_pop'].str.replace(',', '')
    countyPop['2021_pop'] = countyPop['2021_pop'].str.replace(',', '')
    countyPop['2022_pop'] = countyPop['2022_pop'].str.replace(',', '')

    countyPop['2020_earlyPop'] = countyPop['2020_earlyPop'].astype(float)
    countyPop['2020_pop'] = countyPop['2020_pop'].astype(float)
    countyPop['2021_pop'] = countyPop['2021_pop'].astype(float)
    countyPop['2022_pop'] = countyPop['2022_pop'].astype(float)
    countyPop.to_csv("countyPop.csv")



    
def houseCountyData():
    houseData = pandas.read_csv("HOUSE_precinct_general.tab", sep='\t')
    # houseData.to_csv("test.csv")

    # houseData = pandas.read_csv("test.csv")
    houseData['county_fips'] = houseData['county_fips'].astype(str)

    houseData = houseData.groupby(['state', 'state_po', 'district', 'county_fips', 'party_simplified'], as_index=False).sum()
    print(houseData.columns)
    houseData = houseData.drop(columns=['jurisdiction_fips','year','special','writein','state_fips','state_cen','state_ic','readme_check','magnitude'])
    houseData.to_csv("countyVotes.csv")

    totalVotes = houseData.groupby(['state', 'state_po', 'district', 'county_fips'], as_index=False).sum()
    print(totalVotes.columns)
    totalVotes = totalVotes.rename(columns={'votes': 'totalVotes'})
    houseData = pandas.merge(
        left=houseData,
        right=totalVotes,
        left_on=['state', 'state_po', 'district', 'county_fips'],
        right_on=['state', 'state_po', 'district', 'county_fips'],
        how='left'
    )


    houseData['votePercentage'] = houseData['votes'] / houseData['totalVotes']

    houseData.to_csv("countyDistrictVotesPerc.csv")
    # print(houseData.columns)

    houseStateData = houseData.groupby(['state', 'state_po', 'county_fips', 'party_simplified'], as_index=False).sum()
    print(houseStateData.columns)

    houseStateData = houseStateData.drop(columns=['votePercentage', 'district'])
    houseStateDataTemp = houseStateData.groupby(['state', 'state_po', 'county_fips']).sum()
    houseStateDataTemp = houseStateDataTemp.rename(columns={'votes': 'totalStateVotes'})
    houseStateData = pandas.merge(
        left=houseStateData,
        right=houseStateDataTemp,
        left_on=['state', 'state_po', 'county_fips'],
        right_on=['state', 'state_po', 'county_fips'],
        how='left'
    )

    houseStateData['votePercentage'] = houseStateData['votes'] / houseStateData['totalStateVotes']
    houseStateData.to_csv("countyVotesPerc.csv")

    houseStateData.loc[houseStateData["party_simplified"] == "OTHER", "votePercentage"] = 0
    houseStateData.loc[houseStateData["party_simplified"] == "LIBERTARIAN", "votePercentage"] = 0
    houseStateData.loc[houseStateData["party_simplified"] == "DEMOCRAT", "votePercentage"] *= -1

    houseStateData = houseStateData.groupby(['state', 'state_po', 'county_fips']).sum()
    houseStateData.to_csv("countyBias.csv")
    houseStateData = pandas.read_csv("countyBias.csv")

    states = geopandas.read_file('CountyShape/cb_2021_us_county_500k.shp')
    print("Test\n\n")
    print(states.columns)
    # print(states['STATEFP'])
    states['STATEFP'] = states['STATEFP'].astype(str)
    states['COUNTYFP'] = states['COUNTYFP'].astype(str)
    states['county_fips'] = states['STATEFP'] + states['COUNTYFP']
    states['county_fips'] = states['county_fips'].astype(float)
    print(houseStateData.columns)
    houseStateData[pandas.to_numeric(houseStateData['county_fips'], errors='coerce').notnull()]

    houseStateData['county_fips'] = houseStateData['county_fips'].astype(float)

    print(states['county_fips'])
    states = pandas.merge(
        left=states,
        right=houseStateData,
        left_on='county_fips',
        right_on='county_fips',
        how='left'
    )

    states = states[~states['NAME'].isin(['Alaska','Hawaii','Peurto Rico'])]

    bound = states.boundary.plot(colors="black", linewidth=0.1)
    bound.set_xlim(-130, -60)
    bound.set_ylim(20, 50)
    
    # infection percentage graphing

    states.plot(ax=bound, column='votePercentage', legend=True, vmin = -1, vmax =1, cmap='RdBu_r')
    plt.axis('off')
    plt.show()
    plt.savefig('countyBias.png', transparent=True)

    
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
    plt.savefig('voterBias.png', transparent=True)


    # states = geopandas.read_file('StateShape/cb_2022_us_state_500k.shp')
    # print(states['STUSPS'])
    # states = pandas.merge(
    #     left=states,
    #     right=houseStateData,
    #     left_on='STUSPS',
    #     right_on='state_po',
    #     how='left'
    # )

def covidCountyData():
    # data = pandas.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")
    # headers = list(data.columns.values)
    # print(headers)
    # data = data[data["location_key"].astype("str").str.startswith('US')]
    

    # data["county"] = data["location_key"].str[-5:]
    
    # data = data[data["location_key"].astype("str").str.len() == 11]
    # data = data.drop(columns=['date', 'new_confirmed', 'new_deceased', 'new_recovered', 'new_tested', 'cumulative_recovered', 'cumulative_tested'])
    # data['location_key'] = data['location_key'].astype("str").str[3:5]
    # data = data.groupby(['location_key', 'county'])['cumulative_confirmed', 'cumulative_deceased'].max()
    
    # data.to_csv("countyMax.csv")
    


    data = pandas.read_csv("countyMax.csv")
    population = pandas.read_csv("countyPop.csv")
    population = population.drop(columns=['county', 'Unnamed: 0'])
    data = pandas.merge(
        left=data,
        right=population,
        left_on=['location_key', 'county'],
        right_on=['StateAbbr', 'CountyFIPS'],
        how='left'
    )
    data = data.drop(columns=['StateAbbr', 'CountyFIPS', 'StateAbbr'])
    data["cumulative_percentage"] = data["cumulative_confirmed"]/data["2022_pop"]
    data["dead_percentage"] = data["cumulative_deceased"]/data["2022_pop"]
    data.to_csv("countyUS.csv")
    states = geopandas.read_file('CountyShape/cb_2021_us_county_500k.shp')
    states['STATEFP'] = states['STATEFP'].astype(str)
    states['COUNTYFP'] = states['COUNTYFP'].astype(str)
    states['county_fips'] = states['STATEFP'] + states['COUNTYFP']
    states['county_fips'] = states['county_fips'].astype(float)

    states = pandas.merge(
        left=states,
        right=data,
        left_on='county_fips',
        right_on='county',
        how='left'
    )
    print(states.columns)

    states = states[~states['NAME'].isin(['Alaska','Hawaii','Peurto Rico'])]

    bound = states.boundary.plot(linewidth=0.05)
    bound.set_xlim(-130, -60)
    bound.set_ylim(20, 50)
    # infection percentage graphing
    states.plot(ax=bound, column='cumulative_percentage', legend=True, cmap='Reds')
    plt.axis('off')
    plt.show()
    plt.savefig('infectedCountyPerc.png', transparent=True)


    # states.plot(ax=bound, column='dead_percentage', legend=True, cmap='Blues')
    # plt.axis('off')
    # plt.show()
    # plt.savefig('deadCountyPerc.png', transparent=True)

    # states = 
    # states.head()
    # states = states.to_crs("EPSG:3395")
    # plt.show()


    # pandas.DataFrame(data.location_key.unique()).to_csv("unique.csv")
def covidData():
    data = pandas.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")
    headers = list(data.columns.values)
    print(headers)
    data = data[data["location_key"].astype("str").str.startswith('US')]    
    data = data[data["location_key"].astype("str").str.len() == 5]
    data = data.drop(columns=['date', 'new_confirmed', 'new_deceased', 'new_recovered', 'new_tested', 'cumulative_recovered', 'cumulative_tested'])
    data.to_csv("temp.csv")
    return
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
    # states.plot(ax=bound, column='cumulative_percentage', legend=True, cmap='Reds')
    # plt.axis('off')
    # plt.show()
    # plt.savefig('infectedPerc.png', transparent=True)


    states.plot(ax=bound, column='dead_percentage', legend=True, cmap='Blues')
    plt.axis('off')
    plt.show()
    plt.savefig('deadPerc.png', transparent=True)

    # states = 
    # states.head()
    # states = states.to_crs("EPSG:3395")
    # plt.show()


    # pandas.DataFrame(data.location_key.unique()).to_csv("unique.csv")


if __name__ == "__main__":
    main()