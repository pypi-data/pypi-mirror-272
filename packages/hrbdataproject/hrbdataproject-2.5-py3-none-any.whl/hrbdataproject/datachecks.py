from pyspark.sql.functions import col, stddev, mean, length as col_length

def check_nulls_in_specific_cols(df, specific_cols):
    """
    Check for missing values in specific columns of a DataFrame.
    
    Parameters:
    df (DataFrame): Input DataFrame.
    specific_cols (list): List of column names to check for missing values.
    
    Returns:
    dict: Dictionary containing column names with missing values and the number of missing values.
    """
    missing_columns = {col: df.where(col(col_name).isNull()).count() for col_name in specific_cols}
    return {col_name: count for col_name, count in missing_columns.items() if count > 0}

def check_regex_pattern(df, string_cols, pattern):
    """
    Check if values in string columns match a specified regex pattern.
    
    Parameters:
    df (DataFrame): Input DataFrame.
    string_cols (list): List of string column names to check.
    pattern (str): Regular expression pattern to match.
    
    Returns:
    dict: Dictionary containing column names with values not matching the pattern and their respective counts.
    """
    from pyspark.sql.functions import regexp_extract
    
    pattern_mismatch = {}
    for col_name in string_cols:
        mismatch_count = df.where(~col(col_name).rlike(pattern)).count()
        if mismatch_count > 0:
            pattern_mismatch[col_name] = mismatch_count
    return pattern_mismatch

class DataFrameAnalyzer:
    def __init__(self, df):
        self.df = df

    def check_missing_values(self):
        missing_columns = {col: self.df.where(col(col_name).isNull()).count() for col_name in self.df.columns}
        return {col_name: count for col_name, count in missing_columns.items() if count > 0}

    def check_data_types(self):
        data_types = {col_name: str(data_type) for col_name, data_type in self.df.dtypes}
        return data_types

    def check_duplicates(self, subset=None):
        if subset is None:
            duplicate_rows = self.df.groupBy(self.df.columns).count().where(col("count") > 1)
        else:
            duplicate_rows = self.df.groupBy(subset).count().where(col("count") > 1)
        return duplicate_rows

    def check_outliers(self, numerical_cols, threshold=3):
        outliers = {}
        for col_name in numerical_cols:
            stats = self.df.select(mean(col(col_name)).alias('mean'), stddev(col(col_name)).alias('stddev')).collect()[0]
            mean_val, stddev_val = stats['mean'], stats['stddev']
            lower_bound = mean_val - threshold * stddev_val
            upper_bound = mean_val + threshold * stddev_val
            outlier_count = self.df.where((col(col_name) < lower_bound) | (col(col_name) > upper_bound)).count()
            if outlier_count > 0:
                outliers[col_name] = outlier_count
        return outliers

    def check_unique_values(self, categorical_cols):
        non_unique_values = {}
        for col_name in categorical_cols:
            distinct_count = self.df.select(col_name).distinct().count()
            total_count = self.df.select(col_name).count()
            if distinct_count < total_count:
                non_unique_values[col_name] = total_count - distinct_count
        return non_unique_values

    def check_column_lengths(self, string_cols, max_length):
        long_values = {}
        for col_name in string_cols:
            over_max_length_count = self.df.where(col_length(col(col_name)) > max_length).count()
            if over_max_length_count > 0:
                long_values[col_name] = over_max_length_count
        return long_values

    def check_nullability(self, nullable_cols):
        non_nullable_cols = [col_name for col_name in self.df.columns if col_name not in nullable_cols]
        return non_nullable_cols

    def check_data_range(self, numerical_cols, min_val=None, max_val=None):
        out_of_range_values = {}
        for col_name in numerical_cols:
            if min_val and col_name in min_val:
                min_count = self.df.where(col(col_name) < min_val[col_name]).count()
                if min_count > 0:
                    out_of_range_values[col_name] = {'min': min_val[col_name], 'count': min_count}
            if max_val and col_name in max_val:
                max_count = self.df.where(col(col_name) > max_val[col_name]).count()
                if max_count > 0:
                    if col_name in out_of_range_values:
                        out_of_range_values[col_name]['max'] = max_val[col_name]
                        out_of_range_values[col_name]['count'] += max_count
                    else:
                        out_of_range_values[col_name] = {'max': max_val[col_name], 'count': max_count}
        return out_of_range_values
