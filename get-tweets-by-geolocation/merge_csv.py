import pandas as pd
import glob

frames = []

input_folder = 'data/'
print('Input files:')

for filename in (glob.glob(input_folder+'/*.csv')):
    print(filename)
    df = pd.read_csv(filename)
    frames.append(df)

merged = pd.concat(frames)
output = 'training_tweets.csv'
merged.to_csv(output, index=False)
print('Output file: ', output)