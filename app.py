import streamlit as st
import requests
import os
import pandas as pd

from dotenv import load_dotenv
from sklearn.linear_model import LinearRegression


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Weather Forecasting Dashboard",
    page_icon="🌦️",
    layout="wide"
)


# =====================================
# LOAD API KEY
# =====================================

load_dotenv()

# First try Streamlit Cloud Secrets
try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except:
    # If not deployed, use local .env file
    API_KEY = os.getenv("OPENWEATHER_API_KEY")


# =====================================
# CUSTOM DESIGN
# =====================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================
# DASHBOARD TITLE
# =====================================

st.markdown(
    '<p class="main-title">🌦️ Weather Forecasting Dashboard</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Real-time weather analysis and prediction using Data Science & Machine Learning</p>',
    unsafe_allow_html=True
)


# =====================================
# SIDEBAR
# =====================================

st.sidebar.header("🌍 Weather Search")

city = st.sidebar.text_input(
    "Enter City Name",
    placeholder="Example: Chennai"
)

search_button = st.sidebar.button(
    "🔍 Get Weather",
    use_container_width=True
)


# =====================================
# CHECK API KEY
# =====================================

if not API_KEY:

    st.error(
        "❌ OpenWeather API key not found. "
        "Please configure OPENWEATHER_API_KEY in Streamlit Secrets."
    )


# =====================================
# MAIN APPLICATION
# =====================================

elif search_button:

    if not city.strip():

        st.warning("⚠️ Please enter a city name.")

    else:

        try:

            # =====================================
            # CURRENT WEATHER API
            # =====================================

            current_weather_url = (
                "https://api.openweathermap.org/data/2.5/weather"
            )

            current_weather_params = {
                "q": city.strip(),
                "appid": API_KEY,
                "units": "metric"
            }

            current_response = requests.get(
                current_weather_url,
                params=current_weather_params,
                timeout=15
            )

            current_data = current_response.json()


            # =====================================
            # SUCCESSFUL WEATHER RESPONSE
            # =====================================

            if current_response.status_code == 200:

                city_name = current_data["name"]
                country = current_data["sys"]["country"]

                st.success(
                    f"📍 Showing weather data for "
                    f"{city_name}, {country}"
                )


                # =====================================
                # CURRENT WEATHER
                # =====================================

                st.header("🌤️ Current Weather")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "🌡️ Temperature",
                        f"{current_data['main']['temp']} °C"
                    )

                with col2:
                    st.metric(
                        "💧 Humidity",
                        f"{current_data['main']['humidity']} %"
                    )

                with col3:
                    st.metric(
                        "💨 Wind Speed",
                        f"{current_data['wind']['speed']} m/s"
                    )

                with col4:
                    st.metric(
                        "🔽 Pressure",
                        f"{current_data['main']['pressure']} hPa"
                    )


                # =====================================
                # WEATHER DETAILS
                # =====================================

                condition = (
                    current_data["weather"][0]["description"].title()
                )

                feels_like = (
                    current_data["main"]["feels_like"]
                )

                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.info(
                        f"🌦️ **Condition:** {condition}"
                    )

                with detail_col2:
                    st.info(
                        f"🤗 **Feels Like:** {feels_like} °C"
                    )


                # =====================================
                # FORECAST API
                # =====================================

                st.divider()

                st.header("📅 5-Day Weather Forecast")

                forecast_url = (
                    "https://api.openweathermap.org/data/2.5/forecast"
                )

                forecast_params = {
                    "q": city.strip(),
                    "appid": API_KEY,
                    "units": "metric"
                }

                forecast_response = requests.get(
                    forecast_url,
                    params=forecast_params,
                    timeout=15
                )

                forecast_data = forecast_response.json()


                # =====================================
                # FORECAST SUCCESS
                # =====================================

                if forecast_response.status_code == 200:

                    forecast_list = []

                    for item in forecast_data["list"]:

                        forecast_list.append({

                            "Date & Time": item["dt_txt"],

                            "Temperature (°C)": (
                                item["main"]["temp"]
                            ),

                            "Humidity (%)": (
                                item["main"]["humidity"]
                            ),

                            "Pressure (hPa)": (
                                item["main"]["pressure"]
                            ),

                            "Weather": (
                                item["weather"][0]["description"]
                            ),

                            "Wind Speed (m/s)": (
                                item["wind"]["speed"]
                            )
                        })


                    # =====================================
                    # CREATE DATAFRAME
                    # =====================================

                    forecast_df = pd.DataFrame(
                        forecast_list
                    )

                    forecast_df["Date & Time"] = pd.to_datetime(
                        forecast_df["Date & Time"]
                    )


                    # =====================================
                    # TEMPERATURE FORECAST
                    # =====================================

                    st.subheader(
                        "📈 Temperature Forecast Trend"
                    )

                    st.line_chart(
                        forecast_df.set_index(
                            "Date & Time"
                        )["Temperature (°C)"]
                    )


                    # =====================================
                    # DATA SCIENCE ANALYSIS
                    # =====================================

                    st.divider()

                    st.header("📊 Data Science Analysis")

                    min_temp = (
                        forecast_df[
                            "Temperature (°C)"
                        ].min()
                    )

                    max_temp = (
                        forecast_df[
                            "Temperature (°C)"
                        ].max()
                    )

                    avg_temp = (
                        forecast_df[
                            "Temperature (°C)"
                        ].mean()
                    )

                    avg_humidity = (
                        forecast_df[
                            "Humidity (%)"
                        ].mean()
                    )


                    stat1, stat2, stat3, stat4 = st.columns(4)

                    with stat1:
                        st.metric(
                            "Minimum Temperature",
                            f"{min_temp:.1f} °C"
                        )

                    with stat2:
                        st.metric(
                            "Maximum Temperature",
                            f"{max_temp:.1f} °C"
                        )

                    with stat3:
                        st.metric(
                            "Average Temperature",
                            f"{avg_temp:.1f} °C"
                        )

                    with stat4:
                        st.metric(
                            "Average Humidity",
                            f"{avg_humidity:.1f} %"
                        )


                    # =====================================
                    # WEATHER TREND ANALYSIS
                    # =====================================

                    st.subheader(
                        "📈 Weather Trend Insight"
                    )

                    first_temp = (
                        forecast_df[
                            "Temperature (°C)"
                        ].iloc[0]
                    )

                    last_temp = (
                        forecast_df[
                            "Temperature (°C)"
                        ].iloc[-1]
                    )

                    temp_difference = (
                        last_temp - first_temp
                    )


                    if temp_difference > 1:

                        st.success(
                            f"📈 Temperature is expected to increase "
                            f"by approximately "
                            f"{temp_difference:.1f} °C."
                        )

                    elif temp_difference < -1:

                        st.info(
                            f"📉 Temperature is expected to decrease "
                            f"by approximately "
                            f"{abs(temp_difference):.1f} °C."
                        )

                    else:

                        st.warning(
                            "➡️ Temperature is expected to remain relatively stable."
                        )


                    # =====================================
                    # HUMIDITY CHART
                    # =====================================

                    st.subheader(
                        "💧 Humidity Forecast Trend"
                    )

                    st.line_chart(
                        forecast_df.set_index(
                            "Date & Time"
                        )["Humidity (%)"]
                    )


                    # =====================================
                    # MACHINE LEARNING
                    # =====================================

                    st.divider()

                    st.header(
                        "🤖 Machine Learning Temperature Prediction"
                    )

                    st.write(
                        "Linear Regression analyzes the temperature trend "
                        "and estimates future temperature values."
                    )


                    # Create numerical time feature

                    forecast_df["Time_Index"] = range(
                        len(forecast_df)
                    )

                    X = forecast_df[
                        ["Time_Index"]
                    ]

                    y = forecast_df[
                        "Temperature (°C)"
                    ]


                    # Train model

                    model = LinearRegression()

                    model.fit(X, y)


                    # =====================================
                    # NEXT TEMPERATURE PREDICTION
                    # =====================================

                    next_time = pd.DataFrame(
                        {
                            "Time_Index": [
                                len(forecast_df)
                            ]
                        }
                    )

                    predicted_temperature = (
                        model.predict(next_time)[0]
                    )


                    pred1, pred2 = st.columns(2)

                    with pred1:
                        st.metric(
                            "🔮 Predicted Next Temperature",
                            f"{predicted_temperature:.2f} °C"
                        )

                    with pred2:
                        st.metric(
                            "🤖 Model",
                            "Linear Regression"
                        )


                    # =====================================
                    # FUTURE PREDICTIONS
                    # =====================================

                    future_indices = pd.DataFrame(
                        {
                            "Time_Index": range(
                                len(forecast_df),
                                len(forecast_df) + 8
                            )
                        }
                    )

                    future_predictions = (
                        model.predict(
                            future_indices
                        )
                    )


                    last_date = (
                        forecast_df[
                            "Date & Time"
                        ].iloc[-1]
                    )


                    future_dates = pd.date_range(
                        start=last_date + pd.Timedelta(
                            hours=3
                        ),
                        periods=8,
                        freq="3h"
                    )


                    prediction_df = pd.DataFrame({

                        "Date & Time": future_dates,

                        "Predicted Temperature (°C)":
                        future_predictions
                    })


                    # =====================================
                    # ML PREDICTION CHART
                    # =====================================

                    st.subheader(
                        "🔮 Predicted Temperature Trend"
                    )

                    combined_chart_df = pd.DataFrame({

                        "Date & Time":
                        list(
                            forecast_df[
                                "Date & Time"
                            ]
                        )
                        +
                        list(
                            prediction_df[
                                "Date & Time"
                            ]
                        ),

                        "Forecast Temperature":
                        list(
                            forecast_df[
                                "Temperature (°C)"
                            ]
                        )
                        +
                        [None] * len(
                            prediction_df
                        ),

                        "ML Prediction":
                        [None] * len(
                            forecast_df
                        )
                        +
                        list(
                            prediction_df[
                                "Predicted Temperature (°C)"
                            ]
                        )
                    })


                    st.line_chart(
                        combined_chart_df.set_index(
                            "Date & Time"
                        )
                    )


                    # =====================================
                    # DETAILED FORECAST DATA
                    # =====================================

                    st.divider()

                    st.subheader(
                        "📋 Detailed Forecast Data"
                    )

                    display_df = forecast_df.drop(
                        columns=["Time_Index"]
                    )

                    st.dataframe(
                        display_df,
                        use_container_width=True
                    )


                # =====================================
                # FORECAST API ERROR
                # =====================================

                else:

                    error_message = (
                        forecast_data.get(
                            "message",
                            "Unknown forecast API error"
                        )
                    )

                    st.error(
                        f"❌ Forecast API Error: {error_message}"
                    )


            # =====================================
            # CURRENT WEATHER API ERROR
            # =====================================

            else:

                error_message = (
                    current_data.get(
                        "message",
                        "Unknown API error"
                    )
                )

                st.error(
                    f"❌ Weather API Error: {error_message}"
                )


        # =====================================
        # INTERNET / API CONNECTION ERROR
        # =====================================

        except requests.exceptions.RequestException as error:

            st.error(
                f"❌ Unable to connect to the weather service: {error}"
            )


# =====================================
# DEFAULT MESSAGE
# =====================================

else:

    st.info(
        "👈 Enter a city name in the sidebar and click "
        "'Get Weather' to view real-time weather data "
        "and predictions."
    )