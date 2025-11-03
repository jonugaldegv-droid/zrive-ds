import boto3
from dotenv import find_dotenv, load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
import logging

logger = logging.getLogger(__name__)

def download_df(download_filename: str, bucket_name: str, aws_filepath: str):

    # Find .env
    dotenv_path = find_dotenv()
    # Load entries as environment variables
    load_dotenv(dotenv_path)

    # Get .env variables
    ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
    SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')

    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY
)

    s3_client.download_file(Bucket = bucket_name, 
                        Key = aws_filepath,
                        Filename = download_filename+'.csv')
    
def filter_dataframe(
        df: pd.DataFrame, 
        min_products: int=5
        ):
    
    order_size = df.groupby('order_id')['outcome'].sum()
    filtered_orders = order_size[order_size>=min_products].index
    df = df.loc[lambda x: x.order_id.isin(filtered_orders)]
    return (
    df
    .assign(created_at = lambda x: pd.to_datetime(x.created_at))
    .assign(order_date = lambda x: pd.to_datetime(x.order_date))
    )

def time_split_df(
        df: pd.DataFrame, 
        train_threshold_normalised: float = 0.7, 
        val_threshold_normalised: float = 0.9, 
        show: bool = True
        ):

    if val_threshold_normalised<= train_threshold_normalised:
        logger.error('Validation threshold is smaller than testing threshold. This may cause data leakage. Please, select valid thresholds')

    else:
    
        daily_orders = df.groupby('order_date')['order_id'].nunique()
        order_cumsum = daily_orders.cumsum() / daily_orders.sum()

        train_thr   = order_cumsum[order_cumsum <= train_threshold_normalised].idxmax()
        val_thr     = order_cumsum[order_cumsum <= val_threshold_normalised].idxmax()

        train_df    = df[df.order_date <= train_thr]
        val_df      = df[df.order_date.between(train_thr, val_thr, inclusive = 'right')]
        test_df     = df[df.order_date > val_thr]

        logger.info(f'Train from {train_df.order_date.min()} until {train_df.order_date.max()}')
        logger.info(f'Val from {val_df.order_date.min()} up to {val_df.order_date.max()}')
        logger.info(f'Test up to {test_df.order_date.max()}')

        if show:
            print_orders_cumsum(df, train_threshold_percentage = train_threshold_normalised, val_threshold_percentage = val_threshold_normalised)

    return train_df, val_df, test_df

def print_orders_cumsum(
        df: pd.DataFrame, 
        train_threshold_percentage: float | None = None, 
        val_threshold_percentage: float | None = None
        ):
    
    daily_orders = df.groupby('order_date')['order_id'].nunique()
    order_cumsum = daily_orders.cumsum() / daily_orders.sum()

    fig = plt.figure(figsize=(12, 8))

    train_thr   = order_cumsum[order_cumsum <= train_threshold_percentage if train_threshold_percentage else None].idxmax()
    val_thr     = order_cumsum[order_cumsum <= val_threshold_percentage if val_threshold_percentage else None].idxmax()

    order_cumsum.plot(kind = 'line')
    plt.axvline(x = train_thr, color='red', linestyle='-.')
    plt.axvline(x = val_thr, color='red', linestyle='-.')
    plt.show()