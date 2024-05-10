# Import libraries
import pandas as pd
from pandas import DataFrame
from typing import List, Union, Dict
import seaborn as sns
import matplotlib.pyplot as plt
import warnings


import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame

import matplotlib.pyplot as plt
import seaborn as sns
from pandas import DataFrame


def create_subplots(data: DataFrame, plot_type: str) -> None:
    """
    Creates subplots for the specified plot type.

    Parameters:
        data (DataFrame): Input DataFrame.
        plot_type (str): Type of plot ('boxplot' or 'histplot').
    """
    numeric_columns = [column for column in data.columns 
                       if data[column].dtypes == 'int64' or data[column].dtypes == 'float64']
    num_plots = len(numeric_columns)
    if num_plots == 0:
        print("No numeric columns found in the DataFrame.")
        return
    
    # Determine the number of rows and columns for subplots
    num_cols = min(2, num_plots)  # Maximum of 3 columns
    num_rows = (num_plots + num_cols - 1) // num_cols
    
    # Create subplots
    if num_cols <= 1:
        raise ValueError('There must be more than one numeric column in the dataframe')
    elif num_cols == 2:
        fig, axes = plt.subplots(num_plots, 1, figsize=(8, num_plots * 5))
    else:
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, num_rows * 5))
        return
        
    # Iterate over numeric columns and create plots
    for i, column in enumerate(numeric_columns):
        if num_cols <= 1:
            print('There must be more than one numeric column in the dataframe.')
            return
        if num_cols == 2:
            ax = axes[i]
        else:
            row = i // num_cols
            col = i % num_cols
            ax = axes[row, col]
        
        if plot_type == 'boxplot':
            sns.boxplot(x=data[column], ax=ax)
        elif plot_type == 'histplot':
            sns.histplot(x=data[column], ax=ax)
        else:
            raise ValueError(f'{plot_type} is not a valid input')

        ax.set_title(f'{column}'.capitalize())
    
    plot_title = "Boxplot" if plot_type == 'boxplot' else "Histogram"
    plt.suptitle(f"{plot_title} Analysis", fontsize=16, y=1.02)
    
    plt.tight_layout()
    plt.show()




def create_heatmap(data: DataFrame) -> None:
    """
    Creates a heatmap of correlation matrix.

    Parameters:
        data (DataFrame): Input DataFrame.
    """
    numeric_columns = [column for column in data.columns 
                       if data[column].dtypes == 'int64' or data[column].dtypes == 'float64']
    numeric_data = data[numeric_columns]
    corr_matrix = numeric_data.corr()
    
    # Set up the heatmap figure
    plt.figure(figsize=(8, 6))
    
    # Customize the appearance of the heatmap
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", linewidths=.5)
    
    # Add title to the heatmap
    plt.title('Correlation Heatmap')
    
    # Adjust layout
    plt.tight_layout()
    
    # Show the heatmap
    plt.show()


def data_input(csv: str) -> pd.DataFrame:
    """
    Read a CSV file and return its contents as a DataFrame.

    Parameters:
        csv (str): The file path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(csv)


def data_describe(data: DataFrame) -> pd.DataFrame:
    """
    Generate descriptive statistics of the DataFrame columns.

    Parameters:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: Descriptive statistics for the DataFrame columns.
    """
    data = data.describe()
    data_transpose = data.T
    data_describe = data_transpose.drop(columns='count')
    return data_describe
    

def data_is_null(data: DataFrame) -> pd.DataFrame:
    """
    Count the number of missing values in each column of the DataFrame.

    Parameters:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the count of missing values for each column.
    """
    result = data.isnull().sum().to_frame()
    data = result.rename(columns={0: 'null_count'})
    return data

def data_type(data: DataFrame) -> pd.Series:
    """
    Get the data types of each column in the DataFrame.

    Parameters:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.Series: A Series containing the data types of each column.
    """
    return data.dtypes
    

def data_count(data: DataFrame) -> dict:
    """
    Count the number of entries in each column of the DataFrame.

    Parameters:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        dict: A dictionary containing the count of entries for each column.
    """
    count_dict = {}
    for column in data.columns:
        count_dict[column] = [data.shape[0]]
    return count_dict
    

def stats_report(csv: str) -> DataFrame:
    """
    Generate an Exploratory Data Analysis (EDA) report for the DataFrame.

    Parameters:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: An EDA report containing descriptive statistics, data types, null counts, and entry counts for each                   column.
    """
    data = data_input(csv)
    df1 = pd.DataFrame(data_count(data)).T.rename(columns={0: 'entry_count'})
    df1['data_type'] = data_type(data)
    df1['null_count'] = data_is_null(data)
    df2 = data_describe(data)
    report = pd.merge(df1, df2, left_index=True, right_index=True, how='left')
    return report


def plot_analysis(csv: str) -> None:
    """
    Perform initial analysis of the data.

    Parameters:
        csv (str): The file path to the CSV file.
    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        pd.set_option('mode.use_inf_as_na', True)
        data = data_input(csv)
        print('\n')
        create_subplots(data, 'boxplot')
        print('\n\n')
        create_subplots(data, 'histplot')
        print('\n\n')
        create_heatmap(data)