import numpy as np
import joblib
import pandas as pd
import streamlit as st
from io import BytesIO
# import xlsxwriter


#define UDFs for pipeline
def nulls_to_nan(df):
    """
    This function replaces all the "-" strings that represent null values
    And returns a dataframe with NaNs
    """
    missing_values = ['-', '___']
    df = df.replace(missing_values, np.NaN)
    return df

def grammar(df):
    """
    This function will fix any letter casing issues in the text (Ie. Fixes categories)
    Returns a updated dataframe
    """
    #Fixing SeaState
    df['SeaState'] = df['SeaState'].str.replace('light', 'Light', regex = True)
    df['SeaState'] = df['SeaState'].str.replace(',Wind', 'Wind', regex = True)
    df['SeaState'] = df['SeaState'].str.replace('Light air,  small ripples', 'Light air, small ripples', regex = True)

    #Fixing WindSpeed
    df['WindSpeed'] = df['WindSpeed'].str.replace('5 - 6 kts', '4 - 6 kts', regex = True)
    df['WindSpeed'] = df['WindSpeed'].str.replace('2 - 3 kts', '1 - 3 kts', regex = True)
    df['WindSpeed'] = df['WindSpeed'].str.replace('3 - 3 kts', '1 - 3 kts', regex = True)
    df['WindSpeed'] = df['WindSpeed'].str.replace('18 - 21 kts', '17 - 21 kts', regex = True)

    #Fixing Direction of Travel
    df['Direction of Travel'] = df['Direction of Travel'].str.replace('Uknown', 'Unknown', regex = True)
    df['Direction of Travel'] = df['Direction of Travel'].str.replace('Unknown Travel Direction', 'Unknown', regex = True)

    #Fixing Sighting Platofrm
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('vessel', 'Vessel', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('Verry', 'Ferry', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('Moto Vessel', 'Motor Vessel', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('Motorr', 'Motor', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('feet', 'ft', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('Diving', 'Other', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('Parks Canada', 'Other', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('wter', 'water', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('< 60 ft', '25 - 60 ft', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('> 25 ft', '25 - 60 ft', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('25-60ft', '25 - 60 ft', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('25-60', '25 - 60', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('Vessel  25', 'Vessel 25', regex = True)
    df['SightingPlatform'] = df['SightingPlatform'].str.replace('< 25 - 60', '< 25 ft', regex = True)

    #Fix Experience
    df['Experience'] = df['Experience'].str.replace('Recreational', 'Novice recreational observer', regex = True)
    
    return df

def fill_nans(df):
    """
    As simpleimputer returns an array and loses column names, this function will take it's place.
    Input is the dataframe
    This function will replace all NaNs (mean for numercial and most frequent for categorical)
    Returns a dataframe with no NaNs
    """
    #define your categorical features
    cat_cols = ['Time', 'SpeciesName', 'SeaState', 'Date', 'WindSpeed', 'AnimalCountMeasure',
                'Behaviour', 'Direction of Travel', 'SightingPlatform', 'Experience']

    #Replace NaN with most frequent value for Category columns
    for col in cat_cols:
        most_freq = df[col].mode().values[0]
        df[col].fillna(most_freq, inplace=True)
    
    #Replace missing values for numerical features
    num_cols = ['LatitudeDD', 'LongitudeDD']
    for num in num_cols:
        df[num].fillna(value=df[col].mode().values[0], inplace=True)

    return df

def log_animals(df):
    """
    This function  fills the missing values and applies log to Number of Animals Min
    """
    df['Number of Animals Min'] = np.nan_to_num(np.log(df['Number of Animals Min']), neginf = 0)
    return df

def species_category(df):
    """
    This function uses the SpeciesName column in dataframe
    To create a new feature called Species Category
    Returns updated dataframe with SpeciesName Dropped
    """
    #Lists of Whales and Dolphins/Porpoise Species
    whales = ['Killer whale',"Grey whale", 'Humpback whale', 'Minke whale', 'Fin whale',  'Sperm whale', 
                'False killer whale', "Baird's beaked whale", "Cuvier's beaked whale", 'Sei whale', 
                'Blue whale', 'North Pacific right whale', 'Unidentified whale','Other rare species']

    d_p = ['Harbour porpoise',"Dall's porpoise", 'Pacific white-sided dolphin', "Risso's dolphin",
            'Northern right whale dolphin','Unidentified dolphin or porpoise']

    #Create empty list
    speciescategory = []

    #create for loop and appen to list
    for n in df.SpeciesName:
        if (n in whales) == True:
            speciescategory.append('Whales')
        elif (n in d_p) == True:
            speciescategory.append('Dolphins and Porpoises')
        else:
            speciescategory.append('Sea Turtle')
            
    #define new column
    df['SpeciesCategory'] = speciescategory

    #drop SpeciesName
    df = df.drop(['SpeciesName'], axis = 1)

    return df

def extract_behaviour(df):
    """
    This function takes in the dataframe and extracts unqiue features from the behaviour column
    And One hot encodes each variable
    Returns a dataframe with new behaviour columns and deleted behaviour column
    """
    #Create list if unique Behaviours
    behave = ['Fluking', 'Feeding', 'Porpoising', 'Spy-hopping', 'Slow Moving', 'Diving', 
            'Depredation', 'Travelling quickly', 'Bow-riding', 'Breaching', 'Fast moving']

    #Fix behaviour
    df.Behaviour = df.Behaviour.str.replace(' Fluking', 'Fluking', regex = True)
    df.Behaviour = df.Behaviour.str.replace('slow moving', 'Slow Moving', regex = True)
    df.Behaviour = df.Behaviour.str.replace('Slow moving', 'Slow Moving', regex = True)

    #turn behaviour column into list and split based on comma
    ls = list(df['Behaviour'].str.split(','))

    #create for loop do go through flat list (all unique values)
    for element in behave:
        #create column for each element
        df[element] = 0
        #enumerate through the column turned ls
        for index, l in enumerate(ls):
            #Assign False as 0 and True as 1 if element in ls
            df[element].iloc[index] = int(element in l)
    
    #Drop behaviour column
    df = df.drop(['Behaviour'], axis = 1)

    return df

def date_time(df):
    """
    This function takes in a dataframe and extracts features from date and time
    Features extracted are hour, month and season.
    Returns new dataframe with extracted features and dropped SubDate and SubTime
    """
    #Create Month and Year columns
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month_name().str[:3]
    df['Year'] = df['Date'].dt.year
    df['Year'] = df.Year.astype(str)

    #Create Season Column
    conditions = [(df['Month'] == 'Jan') | (df['Month'] == 'Feb') | (df['Month'] == 'Mar'), #winter
                (df['Month'] == 'Apr') | (df['Month'] == 'May') | (df['Month'] == 'Jun'), #spring
                (df['Month'] == 'Jul') | (df['Month'] == 'Aug') | (df['Month'] == 'Sep'), #summer
                (df['Month'] == 'Oct') | (df['Month'] == 'Nov') | (df['Month'] == 'Dec')] #autumn
    
    seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
    df['Season'] = np.select(conditions, seasons)

    #Create Hour Column
    item = df.Time.apply(lambda x: str(x)[:2])
    df['Hour'] = item

    df = df.drop(['Date', 'Time'], axis = 1)

    return df

def seacategory(df):
    """
    Function takes SeaState Column and categorizes them into a new column SeaCategory
    Returns new dataframe
    """
    crests = ['Wind felt on face;wave crests have glassy appearance', 'Crests begin to break;whitecaps start to form at 10 knots']
    moderate = ['Frequent whitecaps - sea to 3 ft (1 m)', 'Moderate waves form 4-5 ft (1.5-2.5 m);some spray carried']
    rough = ['Large waves 5-7 ft (2-3 m);more spray', 'Swell forms 8-10 ft (3-4 m);foam blown in streaks']
    dangerous = ['Moderately high waves to 16 ft (5 m);crests break into spindrift',
                'High waves to 20 ft (7 m);dense foam, visibility reduced']
    storm = ['Exceptionally high waves to 30 ft (9 m)','Waves to 35 ft (11 m);very limited visibility', 
            'Waves to 50 ft (15m);air filled with foam and spray']

    #Create empty list
    seacategory = []

    #create for loop and append to list
    for n in df.SeaState:
        if (n in crests) == True:
            seacategory.append('Crest')
        elif (n in moderate) == True:
            seacategory.append('Moderate')
        elif (n in rough) == True:
            seacategory.append('Rough')
        elif (n in dangerous) == True:
            seacategory.append('Dangerous')
        elif (n in storm) == True:
            seacategory.append('Storm')
        else:
            seacategory.append('Calm')
            
    #define new column
    df['SeaCategory'] = seacategory

    #drop windspeed
    df = df.drop(['SeaState'], axis = 1)

    return df

def windcategory(df):
    """
    Function takes WindSpeed Column and categorizes them into a new column WindCategory
    Returns new dataframe
    """
    light =['1 - 3 kts (Light Air)', '4 - 6 kts (Light Breeze)', '7 - 10 kts (Gentle Breeze)']
    breeze = ['11 - 16 kts (Moderate Breeze)', '17 - 21 kts (Fresh Breeze)', '22 - 27 kts (Strong Breeze)']
    gale = ['28 - 33 kts (Near Gale)', '34 - 40 kts (Gale)', '41 - 47 kts (Strong Gale)']
    storm = ['48 - 55 kts  (Storm)', '56 - 63 kts (Violent Storm)', '64+ kts (Hurricane)']

    #Create empty list
    windcategory = []

    #create for loop and appen to list
    for n in df.WindSpeed:
        if (n in light) == True:
            windcategory.append('Light')
        elif (n in breeze) == True:
            windcategory.append('Breeze')
        elif (n in gale) == True:
            windcategory.append('Gale')
        elif (n in storm) == True:
            windcategory.append('Storm')
        else:
            windcategory.append('Calm')
            
    #define new column
    df['WindCategory'] = windcategory

    #drop windspeed
    df = df.drop(['WindSpeed'], axis = 1)

    return df

def transform_coord(df):
    """
    This function normalizes latitude and longitude.
    """
    df.LatitudeDD = df.LatitudeDD/100
    df.LongitudeDD = df.LongitudeDD/100

    return df

#define UFD class
class objectTransformer:
    
    def __init__(self, func):
        self.func = func
        
    def fit(self, X, y=None, **fit_params):
        return self
    
    def transform(self, X, **fit_params):
        return self.func(X)

#define function to download new excel file
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def show_predict_page():
    st.title("BCSSN Location Accuracy Prediction")
    st.write("#### Input a document and recieve a document in return for the Location Accuracies.")

    #import model
    classifier = joblib.load('classifier.joblib')

    #upload data
    data_file = st.file_uploader("Input Dataset",type=['csv','xlsx'])
    if data_file is not None:
        # file_details = {"filename":data_file.name, "filetype":data_file.type, "filesize":data_file.size}
        if data_file.type == 'csv':
            df = pd.read_csv(data_file, delimiter=',')
        else:
            df = pd.read_excel(data_file)

    #Create function for prediction
    if st.button('Predict Location Accuracy'):
        prediction=classifier.predict(df)
        result = prediction.tolist()
        df['Location Accuracy'] = result

        #Reformat date
        df['Date'] = df.Date.dt.date

        st.write('##### Location Accuracy Predictions Completed.')
        #st.table(df)

        #Download new dataframe
        df_xlsx = to_excel(df)
        st.download_button(label='📥 Download Current Result', data=df_xlsx ,file_name= 'updated_data.xlsx')


if __name__=='__main__':
    show_predict_page()