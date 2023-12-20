import pandas as pd
import numpy as np

data = pd.DataFrame()
for i in range(850, 871):
    df = pd.read_csv(f'https://nextml.github.io/caption-contest-data/summaries/{i}.csv')
    
    # get columns 'caption' and 'mean'
    df = df[['caption', 'mean']]

    # if mean>1.5, label='funny'; mean<1.5 and mean>1.3, label='somewhat_funny'; else label = 'not_funny'
    df['label'] = np.where(df['mean'] > 1.5, 'funny', np.where(df['mean'] > 1.3, 'somewhat_funny', 'not_funny'))

    # romeve '\n' in caption
    df['caption'] = df['caption'].str.replace('\n', ' ')

    # drop rows with empty caption
    df = df[df['caption'] != '']

    # concat all dataframes
    data = pd.concat([data, df], ignore_index=True)

# save to csv
data.to_csv('features_model/850_870.csv', index=False)


