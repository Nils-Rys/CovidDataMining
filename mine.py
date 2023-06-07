
import pandas
import matplotlib.pyplot as plt
from scipy import stats
from ChiMerge import *
import geopandas
import seaborn as sns

def main():
    # cleanData()
    # covidCountyData()
    # covidData()
    # houseData()
    # houseCountyData()
    dataAnalysis()

def dataAnalysis():
    covidCounty = pandas.read_csv('countyUS.csv')
    houseCounty = pandas.read_csv('countyBias.csv')
    megaData = pandas.merge(
        left=covidCounty,
        right=houseCounty,
        left_on=['location_key', 'county'],
        right_on=['state_po', 'county_fips'],
        how='left'
    )
    megaData = megaData.drop(columns="Unnamed: 0")
    megaData = megaData[megaData['cumulative_percentage'] != 3.843137254901961]
    print(megaData['cumulative_percentage'].max())

    # print(megaData.columns)

    megaData['vote_classification'] = ''
    megaData['infec_classification'] = ''
    megaData['death_classification'] = ''
    
    megaData['vote_classification'].mask(megaData['votePercentage'] < -0.75, "-1 | -0.75", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= -0.75) & (megaData["votePercentage"].astype(float) < -0.5),"-0.75 | -0.5", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= -0.5) & (megaData["votePercentage"].astype(float) < -0.3), "-0.5 | -0.3", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= -0.3) & (megaData["votePercentage"].astype(float) < -0.2), "-0.3 | -0.2", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= -0.2) & (megaData["votePercentage"].astype(float) < -0.1), "-0.2 | -0.1", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= -0.1) & (megaData["votePercentage"].astype(float) < -0.05), "-0.1 | -0.05", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= -0.05) & (megaData["votePercentage"].astype(float) < 0.05), "-0.05 | 0.05", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= 0.05) & (megaData["votePercentage"].astype(float) < 0.1), "0.05 | 0.1", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= 0.1) & (megaData["votePercentage"].astype(float) < 0.2), "0.1 | 0.2", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= 0.2) & (megaData["votePercentage"].astype(float) < 0.3), "0.2 | 0.3", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= 0.3) & (megaData["votePercentage"].astype(float) < 0.5), "0.3 | 0.5", inplace=True)
    megaData['vote_classification'].mask((megaData["votePercentage"].astype(float) >= 0.5) & (megaData["votePercentage"].astype(float) < 0.75), "0.5 | 0.75", inplace=True)
    megaData['vote_classification'].mask(megaData["votePercentage"].astype(float) >= 0.75, "0.75 | 1", inplace=True)


    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.0121951219512195) & (megaData["cumulative_percentage"].astype(float) <= 0.1705864840726406),"0.0121951219512195, 0.1705864840726406", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.1707016364043936) & (megaData["cumulative_percentage"].astype(float) <= 0.1709621993127147), "0.1707016364043936, 0.1709621993127147", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.1711065273283606) & (megaData["cumulative_percentage"].astype(float) <= 0.2074110263444699), "0.1711065273283606, 0.2074110263444699", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.207440866482102) & (megaData["cumulative_percentage"].astype(float) <= 0.2075535896563456), "0.207440866482102, 0.2075535896563456", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.2075841927534909) & (megaData["cumulative_percentage"].astype(float) <= 0.2395193940185451), "0.2075841927534909, 0.2395193940185451", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.2396599264705882) & (megaData["cumulative_percentage"].astype(float) <= 0.2396930040342418), "0.2396599264705882, 0.2396930040342418", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.2397075798383993) & (megaData["cumulative_percentage"].astype(float) <= 0.2557263411693791), "0.2397075798383993, 0.2557263411693791", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.255734852080367) & (megaData["cumulative_percentage"].astype(float) <= 0.2558938184518284), "0.255734852080367, 0.2558938184518284", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.2558942200184726) & (megaData["cumulative_percentage"].astype(float) <= 0.2687941086222767), "0.2558942200184726, 0.2687941086222767", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.2688036345280161) & (megaData["cumulative_percentage"].astype(float) <= 0.2688271495144249), "0.2688036345280161, 0.2688271495144249", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.2688500549920567) & (megaData["cumulative_percentage"].astype(float) <= 0.2862528799832437), "0.2688500549920567, 0.2862528799832437", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.2863283187303687) & (megaData["cumulative_percentage"].astype(float) <= 0.2864547339322736), "0.2863283187303687, 0.2864547339322736", inplace=True)
    megaData['infec_classification'].mask((megaData["cumulative_percentage"].astype(float) >= 0.2864564987671715) & (megaData["cumulative_percentage"].astype(float) <= 0.8488490758589409), "0.2864564987671715, 0.8488490758589409", inplace=True)


    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0) & (megaData["dead_percentage"].astype(float) <= 0.0008773448773448),"0.0, 0.0008773448773448", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0008873114463176) & (megaData["dead_percentage"].astype(float) <= 0.0009784735812133), "0.0008873114463176, 0.0009784735812133", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0009823182711198) & (megaData["dead_percentage"].astype(float) <= 0.0009823182711198), "0.0009823182711198, 0.0009823182711198", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0009851269852711) & (megaData["dead_percentage"].astype(float) <= 0.0019893371528606), "0.0009851269852711, 0.0019893371528606", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0019914368216668) & (megaData["dead_percentage"].astype(float) <= 0.0019925280199252), "0.0019914368216668, 0.0019925280199252", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0019941054268831) & (megaData["dead_percentage"].astype(float) <= 0.002333346743372), "0.0019941054268831, 0.002333346743372", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0023341113704568) & (megaData["dead_percentage"].astype(float) <= 0.0023344651952461), "0.0023341113704568, 0.0023344651952461", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0023374021444737) & (megaData["dead_percentage"].astype(float) <= 0.002909796314258), "0.0023374021444737, 0.002909796314258", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0029110664767247) & (megaData["dead_percentage"].astype(float) <= 0.0029118136439267), "0.0029110664767247, 0.0029118136439267", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0029146268994595) & (megaData["dead_percentage"].astype(float) <= 0.0034330877983909), "0.0029146268994595, 0.0034330877983909", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0034330920217926) & (megaData["dead_percentage"].astype(float) <= 0.0034331489605187), "0.0034330920217926, 0.0034331489605187", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.0034364261168384) & (megaData["dead_percentage"].astype(float) <= 0.0049032163635698), "0.0034364261168384, 0.0049032163635698", inplace=True)
    megaData['death_classification'].mask((megaData["dead_percentage"].astype(float) >= 0.004904146232724) & (megaData["dead_percentage"].astype(float) <= 0.0196078431372549), "0.004904146232724, 0.0196078431372549", inplace=True)

    megaData = megaData[megaData['votePercentage'].notna()]
    megaData = megaData[megaData['cumulative_percentage'].notna()]
    print(megaData.loc[megaData['infec_classification'] == ''])
    # -1 -0.75
    # -0.75 -0.5
    # -0.5 -0.3
    # -0.3 -0.2
    # -0.2 -0.1
    # -0.1 -0.05
    # -0.05 0.05
    megaData['vote_classification'] = pd.Categorical(megaData['vote_classification'], ["-1 | -0.75", "-0.75 | -0.5", "-0.5 | -0.3", "-0.3 | -0.2", "-0.2 | -0.1", "-0.1 | -0.05", "-0.05 | 0.05", "0.05 | 0.1", "0.1 | 0.2", "0.2 | 0.3", "0.3 | 0.5", "0.5 | 0.75", "0.75 | 1"])


    infectionCross = pandas.crosstab(megaData['infec_classification'], megaData['vote_classification'], normalize='columns')
    plt.figure(figsize=(13,13))
    ax = sns.heatmap(infectionCross, annot=True)
    ax.figure.tight_layout()

    fig = ax.get_figure()
    fig.savefig("infecHeatmap.png", transparent=True) 
    
    infectionTotalCross = pandas.crosstab(megaData['infec_classification'], megaData['vote_classification'], normalize='all')
    plt.figure(figsize=(13,13))
    ax = sns.heatmap(infectionTotalCross, annot=True)
    ax.figure.tight_layout()

    fig = ax.get_figure()
    fig.savefig("infecSupportHeatmap.png", transparent=True) 

    deathCross = pandas.crosstab(megaData['death_classification'], megaData['vote_classification'], normalize='columns')
    plt.figure(figsize=(13,13))
    ax = sns.heatmap(deathCross, annot=True)
    ax.figure.tight_layout()

    fig = ax.get_figure()
    fig.savefig("deathHeatmap.png", transparent=True) 
    
    deathTotalCross = pandas.crosstab(megaData['death_classification'], megaData['vote_classification'], normalize='all')
    plt.figure(figsize=(13,13))
    ax = sns.heatmap(deathTotalCross, annot=True)
    ax.figure.tight_layout()

    fig = ax.get_figure()
    fig.savefig("deathSupportHeatmap.png", transparent=True) 


    # print(infectionTotalCross)

    # supportInfec = infectionTotalCross
    # xcount = 0
    # ycount = 0
    # temp = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    # xlen = len(supportInfec)
    # for x in supportInfec:
    #     temp[xcount] = supportInfec[x]
    #     ycount=0
    #     print(x)
    #     for y in supportInfec[x]:
    #         ylen = len(supportInfec[x])
    #         print(supportInfec[x][ycount].astype(float) / supportInfec["All"][ylen-1].astype(float))
    #         temp[xcount][ycount]= supportInfec[x][ycount].astype(float) / supportInfec["All"][ylen-1].astype(float)
    #         ycount+=1
    #     xcount+=1 

    # print(temp)



    # infecContingency = pandas.crosstab(megaData['cumulative_percentage'], megaData['vote_classification'])
    # infecContingency.to_csv("infecContingency.csv")
    # temp = pandas.read_csv("infecContingency.csv")
    # start(temp)

    # deadContingency = pandas.crosstab(megaData['dead_percentage'], megaData['vote_classification'])
    # deadContingency.to_csv("deadContingency.csv")
    # temp = pandas.read_csv("deadContingency.csv")
    # start(temp)


    # infecVoteContingency = pandas.crosstab(megaData['votePercentage'], megaData['cumulative_percentage'])
    # deadContingency = pandas.crosstab(megaData['dead_percentage'], megaData['votePercentage'])
    # deadVoteContingency = pandas.crosstab(megaData['votePercentage'], megaData['dead_percentage'])
    # print(infecContingency)

    # infecContingency.plot()
    # plt.show()


    # print(stats.chi2_contingency(infecContingency))
    # stats.chi2_contingency(deadContingency)


    # fig = plt.figure()
    # ax = plt.subplot(111)
    # # megaData.plot.scatter(x='votePercentage', ax=ax, y='cumulative_percentage', c='Blue')
    # megaData.plot.scatter(x='votePercentage', ax=ax, y='dead_percentage', c='Blue')
    # # ax.set_ylim(0,0.5)
    # # plt.savefig('infectedScatter.png', transparent=True)
    # plt.savefig('deadScatter.png', transparent=True)

    # plt.show()


    


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
    # plt.show()
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

    bound = states.boundary.plot(linewidth=0.005)
    bound.set_xlim(-130, -60)
    bound.set_ylim(20, 50)
    # infection percentage graphing
    # states.plot(ax=bound, column='cumulative_percentage', legend=True,vmax =1, cmap='Reds')
    # plt.axis('off')
    # plt.show()
    # plt.savefig('infectedCountyPerc.png', transparent=True)


    states.plot(ax=bound, column='dead_percentage', legend=True, cmap='Blues')
    plt.axis('off')
    plt.show()
    plt.savefig('deadCountyPerc.png', transparent=True)

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