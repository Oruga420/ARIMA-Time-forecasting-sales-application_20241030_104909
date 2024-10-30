from prophet import Prophet
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

def create_forecast(df, periods):
    """
    Creates forecast using Prophet and returns forecast dataframe and metrics.
    """
    # Initialize and train Prophet model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='multiplicative'
    )
    
    model.fit(df)
    
    # Create future dataframe for forecasting
    future = model.make_future_dataframe(periods=periods, freq='M')
    
    # Generate forecast
    forecast = model.predict(future)
    
    # Calculate metrics using training data
    train_predictions = forecast[forecast['ds'].isin(df['ds'])]['yhat']
    actual_values = df['y']
    
    mae = mean_absolute_error(actual_values, train_predictions)
    rmse = np.sqrt(mean_squared_error(actual_values, train_predictions))
    mape = np.mean(np.abs((actual_values - train_predictions) / actual_values)) * 100
    
    metrics = {
        'mae': mae,
        'rmse': rmse,
        'mape': mape
    }
    
    return forecast, model, metrics
