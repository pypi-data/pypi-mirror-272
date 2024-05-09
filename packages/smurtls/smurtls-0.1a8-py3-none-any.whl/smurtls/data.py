import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from lifelines.utils import  concordance_index
from datetime import datetime

class Reader:
    @staticmethod 
    def read_csv(dataSetPath, columns = [], **params):
        df = pd.read_csv(dataSetPath)
        if len(columns) != 0:
            df = df[columns]
        # --------------------
        if "dropna_rows" in params and params["dropna_rows"]:
            na_mask = df.isna().any(axis=1)
            df = df[~na_mask]
            df.reset_index(drop=True, inplace=True)

        if "head" in params and params["head"]:
            num = params["head"]

            if "head_type" in params and params["head_type"] == "frac":
                num = int(df.shape[0] * num)

            if num > df.shape[0]:
                Debug.puts(actor=Reader, status=418, message="Number of rows to display is greater than the number of rows in the dataset. Displaying the entire dataset.")
                num = df.shape[0]
            if num < 0:
                Debug.puts(actor=Reader, status=418, message="Number of rows to display is negative. Displaying the entire dataset.")
                num = df.shape[0]
            
            df = df.head(num)
        # --------------------
        Reader.print_df_stats(df)
        return df

    @staticmethod
    def print_df_stats(df):
        state = "Shape: " + str(df.shape) + "\n"
        state += "NaN rows: " + str(len(df[df.isna().any(axis=1)])) + "\n"
        Debug.puts(actor=Reader, status=101, message=state)


class Scaler:
    data_parameters = {}
    meta_parameters = {}

    def __init__(self, **params):
        if "numerical_cols" in params:
            numerical_cols = params["numerical_cols"]
            self.data_parameters["numerical_cols"] = numerical_cols

        if "binary_cols" in params:
            binary_cols = params["binary_cols"]
            self.data_parameters["binary_cols"] = binary_cols

        if "categorical_cols" in params:
            categorical_cols = params["categorical_cols"]
            self.data_parameters["categorical_cols"] = categorical_cols

        if "ignored_cols" in params:
            ignored_cols = params["ignored_cols"]
            self.data_parameters["ignored_cols"] = ignored_cols
        if "oversample" in params:
            oversample_status = params["oversample"]
            self.meta_parameters["oversample"] = oversample_status


    def call(self, data):
        self.scaling_pipeline = []
        self.raw_data = data
        for data_format, column_names in self.data_parameters.items():
            if data_format != "ignored_cols":
                self.scaling_pipeline.append({data_format:data[column_names]})
        
        res = self._scale()
        del self.raw_data
        del self.scaling_pipeline
        return res
        
    
    def _scale(self):
        bin_res = []
        for scaling_item in self.scaling_pipeline:
            data_format, columns = next(iter(scaling_item.items()))
            if data_format == "categorical_cols":
                bin = self.scaling_functions.get(data_format, self._default)(self, columns)
            else:
                bin = self.scaling_functions.get(data_format, self._default)(columns)
              
            bin_res.append(bin)    
        res = pd.concat(bin_res, axis=1)
        if self.data_parameters['ignored_cols'] != None or len(self.data_parameters['ignored_cols']) != 0:
            for ign_col in self.data_parameters['ignored_cols']:
                res[ign_col] = self.raw_data[ign_col]

        

        res.reset_index(drop=True, inplace=True)
        return res


    # Scaler functions
    @staticmethod      
    def _normalize_numerical_cols(data):
        cols = data.columns
        normalizer = MinMaxScaler()
        res = pd.DataFrame()
        res[cols] = pd.DataFrame(normalizer.fit_transform(data))
        res.reset_index(drop=True, inplace=True)
        return res
    @staticmethod
    def _binary_cols_to_numerical(data):
        cols = data.columns
        data = data.copy()
        for col in cols:
            uniqs = data[col].unique()
            if len(uniqs) == 2:
                if data[col].dtype == bool:
                    data[col] = data[col].astype(float)
                elif data[col].dtype == 'object' and any(value.lower() in {'yes', 'no', 'ja', 'nein'} for value in data[col].unique()):
                    data[col] = data[col].str.lower().replace({"yes": 1.0, "no": 0.0, "ja": 1.0, "nein": 0.0})
                else:
                    data[col] = data[col].map({uniqs[0]: 0.0, uniqs[1]: 1.0})
        
        data.reset_index(drop=True, inplace=True)
        return data

    @staticmethod
    def _one_hot_encode_categorical_cols(data):
        res = pd.get_dummies(data.copy(), drop_first=False)
        return res

    def _process_categorical_cols(self, data):
        res = Scaler._one_hot_encode_categorical_cols(data)
        res = Scaler._binary_cols_to_numerical(res)
        if "ignored_cols" in self.data_parameters:
            res = pd.merge(res, self.raw_data[self.data_parameters["ignored_cols"]], left_index=True, right_index=True)
        res.reset_index(drop=True, inplace=True)
        return res

    @staticmethod   
    def _default(data):
        return ("#default")

    scaling_functions = {
        "numerical_cols": _normalize_numerical_cols,
        "categorical_cols": _process_categorical_cols,
        "binary_cols": _binary_cols_to_numerical
        }


class DebugState:
    INFO = 100
    WARNING = 418
    ERROR = 500
    @staticmethod
    def get(state):
        if state == 100:
            return "INFO"
        elif state == 101:
            return "META INFO"
        elif state == 418:
            return "WARNING"
        elif state == 500:
            return "ERROR"
        else:
            return "UNKNOWN"


class Debug:
    @staticmethod
    def puts(actor, status, message):
        status = DebugState.get(state=status)
        header = actor.__name__ + " " + status + ":"    
        underline = "-" * len(header)
        print(header + "\n" + underline + "\n" + message + "\n")




def categorize_cols(labeled_cols):
    def _categorize(cat, labeled_cols):
        cat_list = [list(col_label.keys())[0] for col_label in labeled_cols if list(col_label.values())[0] == cat]
        return cat_list
    
    res = {}
    for col_label in labeled_cols:
        if 'cat' in col_label.values():
            res['categorical_cols'] = _categorize('cat', labeled_cols)
        if 'bin' in col_label.values():
            res['binary_cols'] = _categorize('bin', labeled_cols)
        if 'nan' in col_label.values():
            res['ignored_cols'] = _categorize('nan', labeled_cols)
    
    return res



class Eval:
    @staticmethod
    def hci(y_pred, labels, breaks, time):
        """
        y_pred: shape (n_samples, n_intervals) -> [Prediction_at_interval_1, ..., Prediction_at_interval_n]
        labels: shape (n_samples, 2) -> [Time_OS, Status_OS]
        breaks: shape (n_intervals+1,) -> [0, ..., n_intervals]
        time: point in time of interest in years
        """
        return concordance_index(labels["Time_OS"], np.cumprod(y_pred[:,0:np.where(breaks>time*365)[0][0]], axis=1)[:,-1], labels["Status_OS"])
        

