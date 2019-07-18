import pandas as pd
import glob
 
out_file = 'training_tweets.csv'
first_file = True # needed to write the header only for first file
for fp in (glob.glob('./data/*.csv')):
    print(fp)
    df = pd.read_csv(fp)
    if first_file: 
        df.to_csv(out_file, index=False)
        first_file = False
    else:
        df.to_csv(out_file, index=False, header=False, mode='a')