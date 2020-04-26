## 1st Phase

# Importing Essential Library
import pandas as pd

# Importing dataset
dataset = pd.read_csv("input/main.csv")
col = dataset.columns

# Creating filteredCountry list
filteredCountry = []
for data in dataset.values:
    if(data[-1].startswith("USA")):
        filteredCountry.append(data)

# Saving into DataFrame
filteredCountry = pd.DataFrame(filteredCountry)

# Saving DataFrame and storing it as .csv file
filteredCountry.to_csv("output/filteredCountry.csv", header = col, index = False)






## 2nd Phase

import pandas as pd
# import string
# string.punctuation
dataset2 = pd.read_csv("output/filteredCountry.csv")

# To remove punctuations from the "PRICE" column
p = ',?$'
def remove_punctuation(txt):
    txt_output = "".join([c for c in txt if c not in p])
    return txt_output

# Converting "PRICE" column into interger value
tempList = []
for i in dataset2[["SKU", "PRICE"]].values:
    i[1] = float(remove_punctuation(i[1]))
    tempList.append([i[0], i[1]])
tempList = pd.DataFrame(tempList, columns = ["SKU", "PRICE"])
dataset2.PRICE = tempList.PRICE

# Finding first smallest price and renaming it to "FIRST_SMALLEST_PRICE"
a = pd.DataFrame(dataset2.groupby("SKU")["PRICE"].nsmallest(2).groupby(level="SKU").first())
a = a.rename(columns = {"PRICE": "FIRST_MINIMUM_PRICE"})

# Finding second smallest price and renaming it to "SECOND_SMALLEST_PRICE"
b = pd.DataFrame(dataset2.groupby("SKU")["PRICE"].nsmallest(2).groupby(level="SKU").last())
b = b.rename(columns = {"PRICE": "SECOND_MINIMUM_PRICE"})

# Concatenating DataFrame a & b into lowestPrice
lowestPrice = pd.concat([a, b], axis = 1)
lowestPrice = lowestPrice.query("FIRST_MINIMUM_PRICE != SECOND_MINIMUM_PRICE")

# Saving lowestPrice into .csv file in /output/ ~directory
lowestPrice.to_csv("output/lowestPrice.csv")