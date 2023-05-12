
import pandas

def main():
    data = pandas.read_csv("https://storage.googleapis.com/covid19-open-data/v3/epidemiology.csv")
    headers = list(data.columns.values)
    print(headers)
    data = data[data["location_key"].astype("str").str.startswith('US')]
    data = data[data["location_key"].astype("str").str.len() == 5]
    data.to_csv("US.csv")
    # pandas.DataFrame(data.location_key.unique()).to_csv("unique.csv")


if __name__ == "__main__":
    main()