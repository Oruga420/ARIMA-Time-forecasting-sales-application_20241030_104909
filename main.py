import streamlit as st
import pandas as pd
from utils.data_processor import validate_and_prepare_data
from utils.forecaster import create_forecast
from utils.visualizer import plot_forecast, plot_components
import io

st.set_page_config(
    page_title="Sales Forecasting App",
    page_icon="📈",
    layout="wide"
)

def main():
    st.title("📈 Sales Forecasting Application")
    st.write("Upload your sales data and get accurate forecasts using advanced time series analysis.")

    # File upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Data validation and preparation
            df = pd.read_csv(uploaded_file)
            valid_df = validate_and_prepare_data(df)
            
            if valid_df is not None:
                st.success("Data validated successfully!")
                
                # Display sample of the data
                st.subheader("Sample of your data")
                st.dataframe(valid_df.head())
                
                # Forecast parameters
                st.subheader("Forecast Parameters")
                forecast_periods = st.slider("Number of months to forecast", 
                                          min_value=1, 
                                          max_value=24, 
                                          value=12)
                
                # Create forecast
                if st.button("Generate Forecast"):
                    with st.spinner("Generating forecast..."):
                        forecast_df, model, metrics = create_forecast(valid_df, forecast_periods)
                        
                        # Display metrics
                        st.subheader("Forecast Accuracy Metrics")
                        col1, col2, col3 = st.columns(3)
                        col1.metric("MAE", f"{metrics['mae']:.2f}")
                        col2.metric("RMSE", f"{metrics['rmse']:.2f}")
                        col3.metric("MAPE", f"{metrics['mape']:.2f}%")
                        
                        # Display plots
                        st.subheader("Forecast Visualization")
                        fig_forecast = plot_forecast(valid_df, forecast_df)
                        st.plotly_chart(fig_forecast, use_container_width=True)
                        
                        st.subheader("Forecast Components")
                        fig_components = plot_components(model)
                        st.plotly_chart(fig_components, use_container_width=True)
                        
                        # Download forecast results
                        forecast_csv = forecast_df.to_csv(index=False)
                        st.download_button(
                            label="Download Forecast Results",
                            data=forecast_csv,
                            file_name="sales_forecast.csv",
                            mime="text/csv"
                        )
                        
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Please ensure your CSV file contains 'Date' and 'Sales' columns.")

if __name__ == "__main__":
    main()
