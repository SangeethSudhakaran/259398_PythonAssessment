#Importing pandas
import pandas as pd

#Directory of the csv file
CSVFilePath = "TheGiftOfMagi.csv"


#Function to get word count
def WordCounter(CSVFilePath):

    #Read the specified csv file
    CSVFile = open(CSVFilePath, "r", encoding="UTF-8")

    #New dictionay to store unique words and counts
    dict_Uniquewords = {}

    #looping through each lines in the csv file
    for line in CSVFile:

        #Checking for not empty lines
        if line.strip() != "":

            #Removing spaces
            #Spliting sentences to words based on space character
            line = line.strip()
            list_Lines = line.split()

            #Loop through each items/words in line
            for item in list_Lines:
                if item not in dict_Uniquewords:
                    dict_Uniquewords[item] = 1  #if new word then adding to dictionary
                else:
                    dict_Uniquewords[
                        item
                    ] += 1  #if already existing word incrementing count
    CSVFile.close()
    return dict_Uniquewords


#Call function
dictionaryWordCount = WordCounter(CSVFilePath)

#New Dataframe and defining columns
df = pd.DataFrame(list(dictionaryWordCount.items()), columns=["Words", "Count"])
print(df)

#Save the results into a new CSV file
df.to_csv("Output.csv")