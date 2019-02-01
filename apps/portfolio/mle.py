import xgboost as xgb
import pandas as pd
from sklearn.externals import joblib


class MachineLearningEngine:
    # TODO: Declare somewhere in a config file
    xgb_params = {'max_depth': 20,
                  'min_child_weight': 0.837870659837664,
                  'gamma': 0.42104203087600217,
                  'eta': 0.3207645224691716,
                  'max_delta_step': 1.0567303998495332,
                  'subsample': 0.8447722656277566,
                  'colsample_bytree': 0.8192733041065964,
                  'colsample_bylevel': 0.9904425844389458,
                  'lambda': 1.1868977513249563,
                  'alpha': 0.09240828211365718,
                  'scale_pos_weight': 1.0541802616596005,
                  'silent': 1,
                  'objective': 'multi:softprob',
                  'num_class': 2}

    # TODO: Hyper parameter configuration and model versioning
    mle_model = joblib.load('/Users/dcamacho/platform_direct_ZTRR_model.joblib')

    def get_ztrr(self, data):
        window_size = 18
        all_df = data.copy()
        future_predictions = pd.DataFrame()
        for i in range(window_size):
            partB = all_df.iloc[:, -114:].values

            all_data = partB

            d = xgb.DMatrix(all_data)
            model_result = self.mle_model.predict(d)
            model_pred = model_result[:, 1]
            model_pred[model_pred >= 0.1] = 1
            model_pred[model_pred < 0.1] = 0

            col = 'fm+' + str(i + 1)
            future_predictions[col] = model_pred

            col_name = 'm' + str(121 + i)
            all_df[col_name] = model_pred

        id_column = data.columns[0]
        return pd.concat([data[[id_column]], future_predictions[['fm+1', 'fm+6', 'fm+12', 'fm+18']]], axis=1)
