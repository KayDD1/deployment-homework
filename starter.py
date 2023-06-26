#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import uuid



year =2022
month = 2
input_file = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-02.parquet'
output_file = 'output/yellow_ride_id_prediction.parquet'
with open('/app/model.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)



def read_data(filename):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    dicts = df[categorical].to_dict(orient='records')
    
    
    return df, dicts



def make_predictions():  
    df, dicts = read_data(input_file)  
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)
    return y_pred





def new_dataframe(year, month):
    df, dicts = read_data(input_file)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')
    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['prediction'] = make_predictions()
    print(df_result.prediction.std())
    df_result.to_parquet(output_file, engine='pyarrow', compression=None, index=False)
    return output_file







