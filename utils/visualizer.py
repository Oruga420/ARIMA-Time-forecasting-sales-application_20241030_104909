import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_forecast(historical_df, forecast_df):
    """
    Creates an interactive plot showing historical data and forecast.
    """
    fig = go.Figure()

    # Add historical data
    fig.add_trace(
        go.Scatter(
            x=historical_df['ds'],
            y=historical_df['y'],
            name='Historical Sales',
            mode='lines+markers',
            line=dict(color='blue')
        )
    )

    # Add forecast
    fig.add_trace(
        go.Scatter(
            x=forecast_df['ds'],
            y=forecast_df['yhat'],
            name='Forecast',
            mode='lines',
            line=dict(color='red')
        )
    )

    # Add confidence intervals
    fig.add_trace(
        go.Scatter(
            x=forecast_df['ds'].tolist() + forecast_df['ds'].tolist()[::-1],
            y=forecast_df['yhat_upper'].tolist() + forecast_df['yhat_lower'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255,0,0,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Confidence Interval'
        )
    )

    fig.update_layout(
        title='Sales Forecast',
        xaxis_title='Date',
        yaxis_title='Sales',
        hovermode='x unified',
        showlegend=True
    )

    return fig

def plot_components(model):
    """
    Creates a plot showing the forecast components (trend, yearly seasonality, weekly seasonality).
    """
    fig = model.plot_components(model.forecast)
    return fig
