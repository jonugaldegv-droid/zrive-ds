from utils import *
import logging

logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='main.log',filemode='w', level=logging.INFO, encoding='utf-8')
    path = '../Data/'
    df = pd.read_csv(path+'feature_frame.csv')

    df_feature = filter_dataframe(df)

    train_df, val_df, test_df = time_split_df(df_feature, train_threshold_normalised=0.7, val_threshold_normalised=0.9, show = True)

    


if __name__ == "__main__":
    main()
