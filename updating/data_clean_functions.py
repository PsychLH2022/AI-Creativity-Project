# This file is for data cleaning before inserting into database

import pandas as pd
import numpy as np

# Read data from github of The New Yorker Cartoon Caption Contest
def read_org_data(start_contest_num, end_contest_num):
    if start_contest_num > end_contest_num:
        raise ValueError('Start contest number must be less than or equal to end contest number')
    else:
        cartoons = list(range(start_contest_num, end_contest_num+1))
        df_merged = pd.DataFrame()
        
        for cartoon in cartoons:
            # contest 525 is missing / contest 643 is overlapped with 644, keeping 644 / 646 overlapped 647, keeping 647 / 655 overlapped 656, keeping 656
            if cartoon != 525 and cartoon != 643 and cartoon != 646 and cartoon != 655:   
                if cartoon >= 660:
                    df = pd.read_csv(f'https://nextml.github.io/caption-contest-data/summaries/{cartoon}.csv')
                elif cartoon < 660 and cartoon >= 560:
                    df = pd.read_csv(f'https://nextml.github.io/caption-contest-data/summaries/{cartoon}_lil-KLUCB.csv')
                elif cartoon < 560 and cartoon != 540:
                    df = pd.read_csv(f'https://nextml.github.io/caption-contest-data/summaries/{cartoon}_LilUCB.csv')
                elif cartoon == 540:
                    df = pd.read_csv('https://nextml.github.io/caption-contest-data/summaries/540_Random.csv')
                df.reset_index(inplace=True)
                df['contest_num'] = cartoon
                df.rename(columns = {'index':'ranking'}, inplace=True)
                df_merged = pd.concat([df_merged, df], ignore_index=True)

    return df_merged



# Class for cleaning original data for resutl table
class org_data_cleaner():
    def __init__(self):
        pass

    # Function to drop nan values in the caption column
    def drop_nan(df):
        
        print("Number of nan values in caption column: ", df['caption'].isna().sum())
        print("Number of blank-space values in caption column: ", df['caption'].str.isspace().sum())
        
        # change blank-space values to nan
        df.loc[df['caption'].str.isspace() == True, 'caption'] = pd.NA

        # drop rows whose captions are nan values
        df = df.dropna(subset=['caption'])

        # reset index
        df_merged = pd.DataFrame()
        for i in range(df['contest_num'].min(), df['contest_num'].max()+1):
            df_temp = df[df.contest_num == i]
            df_temp = df_temp.reset_index(drop=True)
            df_temp['ranking'] = df_temp.index
            df_merged = pd.concat([df_merged, df_temp], ignore_index=True)

        return df_merged
    


    # Function to drop duplicate captions in each contest and reset index for each contest
    def drop_dup_each_contest(df):
        df_merged = pd.DataFrame()

        for i in range(df['contest_num'].min(), df['contest_num'].max()+1):
            df_temp = df[df.contest_num == i]
            df_temp.drop_duplicates(subset=['caption'], keep="first", inplace=True)
            df_temp.reset_index(drop=True, inplace=True)
            df_temp['ranking'] = df_temp.index

            df_merged = pd.concat([df_merged, df_temp], ignore_index=True)

        return df_merged
    


    # Function to check the number of duplicate captions in each contest
    def check_num_dup_each_contest(df):
        num = 0
        for i in range(df['contest_num'].min(), df['contest_num'].max()+1):
            df_temp = df[df.contest_num == i]
            df_dup = df_temp[df_temp.duplicated(subset=['caption'], keep=False)]
            num += len(df_dup)
        print("Total number of duplicated captions: ", num)

    

    # Function to drop duplicate captions across contests and reset index for each contest
    def drop_dup_across_contests(df):
        df.drop_duplicates(subset=['caption'], keep="first", inplace=True)

        df_merged = pd.DataFrame()
        for i in range(df['contest_num'].min(), df['contest_num'].max()+1):
            df_temp = df[df.contest_num == i]
            df_temp.reset_index(drop=True, inplace=True)
            df_temp['ranking'] = df_temp.index
            df_merged = pd.concat([df_merged, df_temp], ignore_index=True)

        return df_merged



# Function to create a new dataframe for updating base table
def create_new_content_for_base(df, start_contest_num, end_contest_num):
    # create a new dataframe for base
    df_base = pd.DataFrame(columns=['contest_num', 'num_caption', 'num_resp', 'image_url'])
    df_base['contest_num'] = range(start_contest_num, end_contest_num+1)

    # get the number of captions and responses for each contest
    cartoons = list(range(start_contest_num, end_contest_num+1))  
    for cartoon in cartoons:
        if cartoon >= 510 and cartoon != 525 and cartoon != 643 and cartoon != 646 and cartoon != 655:
            df_temp = df[df['contest_num'] == cartoon]
            df_base.loc[df_base['contest_num'] == cartoon, 'num_caption'] = len(df_temp.index)
            df_base.loc[df_base['contest_num'] == cartoon, 'num_resp'] = df_temp['votes'].sum()

        # get the image url for each contest
        if cartoon < 510 or cartoon == 525 or cartoon == 643 or cartoon == 646 or cartoon == 655:
            pass
        elif cartoon == 644 or cartoon == 647 or cartoon == 656:
            df_base.loc[df_base['contest_num'] == cartoon, 'image_url'] = f'https://nextml.github.io/caption-contest-data/images/{cartoon-1}.jpg'
        else:
            df_base.loc[df_base['contest_num'] == cartoon, 'image_url'] = f'https://nextml.github.io/caption-contest-data/images/{cartoon}.jpg'
    
    return df_base