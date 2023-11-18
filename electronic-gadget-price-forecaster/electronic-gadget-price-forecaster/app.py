import streamlit as st
import pickle
import numpy as np
import requests

# Load the models and datasets for Laptops, Smartwatches, and Graphic Cards
pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

smartwatch_pipe = pickle.load(open('watch-pipe.pkl', 'rb'))
smartwatch_df = pickle.load(open('watch.pkl', 'rb'))

graphics_card_pipe = pickle.load(open('Graphic-pipe.pkl', 'rb'))
graphics_card_df = pickle.load(open('Graphic.pkl', 'rb'))

st.title("Electronic Gadget Price ForeCaster")

# Choose the product category
product_category = st.selectbox('Select Your Gadget Here', ['Laptop', 'Graphic Card', 'Smartwatch'])

if product_category == 'Laptop':
    st.title("Laptop Price Forecaster")
    
    # You can replace these with the actual column names from your laptop dataset
    company = st.selectbox('Brand',df['Company'].unique())
    type = st.selectbox('Type',df['TypeName'].unique())
    ram = st.selectbox('RAM(in GB)',[2,4,6,8,12,16,24,32,64])
    weight = st.number_input('Weight of the Laptop')
    touchscreen = st.selectbox('Touchscreen',['No','Yes'])
    ips = st.selectbox('IPS',['No','Yes'])
    screen_size = st.number_input('Screen Size')
    resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])
    cpu = st.selectbox('CPU',df['Cpu brand'].unique())
    hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])
    ssd = st.selectbox('SSD(in GB)',[0,8,128,256,512,1024])
    gpu = st.selectbox('GPU',df['Gpu brand'].unique())
    os = st.selectbox('OS',df['os'].unique())

    if st.button('Predict Price - Laptop'):

        # Query
        ppi = None
        if touchscreen == 'Yes':
            touchscreen = 1
        else:
            touchscreen = 0

        if ips == 'Yes':
            ips = 1
        else:
            ips = 0

        X_res = int(resolution.split('x')[0])
        Y_res = int(resolution.split('x')[1])
        ppi = ((X_res**2) + (Y_res**2))**0.5/screen_size
        query = np.array([company,type,ram,weight,touchscreen,ips,ppi,cpu,hdd,ssd,gpu,os])

        query = np.array(query).reshape(1, 12)
        # Fetch the latest exchange rate from Fixer.io
        api_key = '38fc2a5b06739e89673c4b66a141deee'  # Replace with your Fixer.io API key
        base_currency = 'PKR'
        target_currency = 'USD'

        # Construct the API URL
        api_url = f'http://data.fixer.io/api/latest?access_key=38fc2a5b06739e89673c4b66a141deee'
        headers = {
            'apikey': api_key  # Add your API key as a header
        }

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                st.error(f"Error fetching exchange rate: {data['error']['info']}")
            else:
                exchange_rate = data['rates'][target_currency]

                # Convert the predicted price from PKR to USD
                predicted_price_pkr = np.exp(pipe.predict(query)[0])
                predicted_price_usd = predicted_price_pkr / exchange_rate
                st.title(f"The predicted price of this configuration is Rs {predicted_price_usd:.2f}")
        else:
            st.error("Unable to fetch exchange rate data. Please check your API key and try again.")

elif product_category == 'Graphic Card':
    st.title("Graphic Card Price Predictor")

    # You can replace these with the actual column names from your graphics card dataset
    brand_graphic = st.selectbox('Brand', graphics_card_df['Brand'].unique())
    comp = st.selectbox('Company', graphics_card_df['Company'])
    model = st.selectbox('Model', graphics_card_df['Model'])
    chipset = st.selectbox('Chipset', graphics_card_df['Chipset'])
    memory = st.selectbox('Memory', graphics_card_df['Memory'])
    coreclock = st.selectbox('Core Clock', graphics_card_df['CoreClock'])
    boostclock = st.selectbox('BoostClock', graphics_card_df['BoostClock'])
    # Add more select boxes for other features
    
    if st.button('Predict Price - Graphic Card'):
        # Collect user inputs and preprocess them
        # Replace the column names accordingly
        query_graphic = np.array([brand_graphic, comp, model, chipset, memory, coreclock, boostclock])

        query_graphic = np.array(query_graphic).reshape(1, 7)  # Add other features as needed

        # Fetch the latest exchange rate from Fixer.io
        api_key = '38fc2a5b06739e89673c4b66a141deee'  # Replace with your Fixer.io API key
        base_currency = 'PKR'
        target_currency = 'USD'

        # Construct the API URL
        api_url = f'http://data.fixer.io/api/latest?access_key=38fc2a5b06739e89673c4b66a141deee'
        headers = {
            'apikey': api_key  # Add your API key as a header
        }

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if 'error' in data:
                st.error(f"Error fetching exchange rate: {data['error']['info']}")
            else:
                exchange_rate = data['rates'][target_currency]

                # Convert the predicted price from PKR to USD
                predicted_price_pkr = np.exp(graphics_card_pipe.predict(query_graphic)[0])
                predicted_price_usd = predicted_price_pkr / exchange_rate
                st.title(f"The predicted price of this configuration is Rs {predicted_price_usd:.2f}")
        else:
            st.error("Unable to fetch exchange rate data. Please check your API key and try again.")

elif product_category == 'Smartwatch':
    st.title("Smartwatch Price Forecaster")

    # You can replace these with the actual column names from your smartwatch dataset
    brand = st.selectbox('Brand', smartwatch_df['Brand'].unique())
    display = st.selectbox('Display', smartwatch_df['Display Type'])
    dialshape = st.selectbox('Shape', smartwatch_df['DialShape'])
    model = st.selectbox('Model', smartwatch_df['Model'])
    heart = st.selectbox('Heart Beat Counter', smartwatch_df['Heart Rate Monitor'])

    # Add more select boxes for other features
    
if st.button('Predict Price - SmartWatch'):
        # Collect user inputs and preprocess them
        # Replace the column names accordingly
    query_smartwatch = np.array([brand,display,dialshape,model,heart])
    query_smartwatch = np.array(query_smartwatch).reshape(1, 5) # Add other features as needed

        # Fetch the latest exchange rate from Fixer.io
    api_key = '38fc2a5b06739e89673c4b66a141deee'
    base_currency = 'PKR'
    target_currency = 'USD'
    api_url = f'http://data.fixer.io/api/latest?access_key=38fc2a5b06739e89673c4b66a141deee'
    headers = {
        'apikey': api_key
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        exchange_rate = data['rates'][target_currency]

        # Convert the predicted price from PKR to USD
        predicted_price_pkr = np.exp(smartwatch_pipe.predict(query_smartwatch)[0])
        predicted_price_usd = predicted_price_pkr / exchange_rate
        st.title(f"The predicted price of this Smartwatch is Rs {predicted_price_usd:.2f} USD")
    else:
            st.error("Unable to fetch exchange rate data. Please check your API key and try again.")
