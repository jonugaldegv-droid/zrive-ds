from utils import *
from train import *
import logging
import joblib
import datetime as dt

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(level=logging.INFO, encoding='utf-8')
    path = '../Data/'
    df = pd.read_csv(path+'feature_frame.csv')

    df_feature = filter_dataframe(df)

    train_df, val_df, test_df = time_split_df(df_feature, train_threshold_normalised=0.7, val_threshold_normalised=0.9, show = True)

    train_val_df = pd.concat([train_df, val_df])
    logger.info('Starting to train the model')
    model = train_model(train_val_df, val_df)

    stamp = dt.datetime.now().strftime("%Y%m%d-%H")
    model_path = f'models/gb_basic_{stamp}.sav'
    joblib.dump(model, model_path)


if __name__ == "__main__":
    main()
