import pandas as pd
from datetime import datetime

def validate_and_prepare_data(df):
    """
    Validates and prepares the input data for forecasting.
    """
    required_columns = ['Date', 'Sales']
    
    # Check if required columns exist
    if not all(col in df.columns for col in required_columns):
        raise ValueError("CSV must contain 'Date' and 'Sales' columns")
    
    # Create a copy of the dataframe
    df = df.copy()
    
    # Convert Date column to datetime
    try:
        df['Date'] = pd.to_datetime(df['Date'])
    except:
        raise ValueError("Invalid date format in Date column")
    
    # Verify Sales column contains numeric values
    try:
        df['Sales'] = pd.to_numeric(df['Sales'])
    except:
        raise ValueError("Sales column must contain numeric values")
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['Date'])
    
    # Rename columns for Prophet
    df = df.rename(columns={'Date': 'ds', 'Sales': 'y'})
    
    return df
