import pandas as pd

# read 866.csv
data = pd.read_csv('data_of_contest_866/866.csv', encoding='utf-8')

# extract 'caption' and 'mean' columns
data = data[['caption', 'mean']]

# drop rows with missing values
data = data.dropna()

# remove '\n' in 'caption' column
data['caption'] = data['caption'].str.replace('\n', ' ')

# category data by 'mean' score, funny for over 1.5, somewhat funny for between 1.3 and 1.5, not funny for under 1.3
funny = data[data['mean'] > 1.5]
somewhat_funny = data[(data['mean'] >= 1.3) & (data['mean'] <= 1.5)]
not_funny = data[data['mean'] < 1.3]

# add 'label' column to each category
funny['label'] = 'funny'
somewhat_funny['label'] = 'somewhat_funny'
not_funny['label'] = 'not_funny'

# for each category, split data into 3 parts, 80% for training, 20% for testing
funny_train = funny.sample(frac=0.8, random_state=200)
funny_test = funny.drop(funny_train.index)
somewhat_funny_train = somewhat_funny.sample(frac=0.8, random_state=200)
somewhat_funny_test = somewhat_funny.drop(somewhat_funny_train.index)
not_funny_train = not_funny.sample(frac=0.8, random_state=200)
not_funny_test = not_funny.drop(not_funny_train.index)

# combine training data and testing data
train = pd.concat([funny_train, somewhat_funny_train, not_funny_train])
test = pd.concat([funny_test, somewhat_funny_test, not_funny_test])

# write training data and testing data to csv files
train.to_csv('data_of_contest_866/866_train.csv', index=False)
test.to_csv('data_of_contest_866/866_test.csv', index=False)
