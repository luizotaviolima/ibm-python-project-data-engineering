# Imports
import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

 
# EXTRACTION

def extractCsv(fileProcess):
    dataFrame = pd.read_csv(fileProcess)
    return dataFrame


def extractJson(fileProcess):
    dataFrame = pd.read_json(fileProcess, lines = True)
    return dataFrame


def extractXml(fileProcess):
    dataFrame = pd.DataFrame(columns=["name", "height", "weight"])
    tree = ET.parse(fileProcess)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)
        dataFrame = dataFrame.append({"name":name, "height":height, "weight":weight}, ignore_index=True)
    return dataFrame

def extract():
    extractedData = pd.DataFrame(columns=['name','height','weight']) # create an empty data frame to hold extracted data
    
    #process all csv files
    for csvFile in glob.glob("./data/raw/*.csv"):
        extractedData = pd.concat([extractedData, extractCsv(csvFile)], ignore_index=True)
        
    #process all json files
    for jsonFile in glob.glob("./data/raw/*.json"):
        extractedData = pd.concat([extractedData, extractJson(jsonFile)], ignore_index=True)
    
    #process all xml files
    for xmlFile in glob.glob("./data/raw/*.xml"):
        extractedData = pd.concat([extractedData, extractXml(xmlFile)], ignore_index=True)
        
    return extractedData


#TRANSFORM


def transform(dataFrame):
    dataFrame['height'] = round(dataFrame.height.astype(float) * 0.0254, 2) # inches to milimeter

    dataFrame['weight'] = round(dataFrame.weight.astype(float) * 0.45359237, 2) # pounds to kilograms

    timestamp_format = "%Y-%m-%d-%H:%M:%S"
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)

    dataFrame['timestamp'] = timestamp

    dataFrame = dataFrame.drop_duplicates()
    dataFrame = dataFrame.reset_index(drop=True)

    return dataFrame


# LOADING


def loading(targetPath, transformedData):
    transformedData.to_csv(targetPath)


