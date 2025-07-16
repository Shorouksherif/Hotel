import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

pipeline = joblib.load('cancelation prediction.h5')
inputs = joblib.load('input.h5')
countrylist= joblib.load('countryList.h5')
segmentlist= joblib.load('segmentList.h5')
distlist= joblib.load('distrbutionlist.h5')
assignedlist = joblib.load('assignedlist.h5')

def predict(hotel, meal,country,market_segment,distribution_channel,assigned_room_type,days_in_waiting_list,customer_type,lead_time_category,adults,adr,season,Day_Name,is_holiday,room_type_preference,total_length_of_stay):
    test_df= pd.DataFrame(columns=inputs)
    test_df.at[0,'hotel']=hotel
    test_df.at[0,'adults']=adults
    test_df.at[0,'meal']=meal
    test_df.at[0,'country']=country
    test_df.at[0,'market_segment']=market_segment
    test_df.at[0,'distribution_channel']=distribution_channel
    test_df.at[0,'assigned_room_type']=assigned_room_type
    test_df.at[0,'days_in_waiting_list']=days_in_waiting_list
    test_df.at[0,'customer_type']=customer_type
    test_df.at[0,'lead_time_category']=lead_time_category
    test_df.at[0,'adr']=adr
    test_df.at[0,'season']=season
    test_df.at[0,'Day_Name']=Day_Name
    test_df.at[0,'is_holiday']=is_holiday
    test_df.at[0,'room_type_preference']=room_type_preference
    test_df.at[0,'total_length_of_stay']=total_length_of_stay
    if pipeline.predict(test_df)[0]== 0:
        return  'Customer wont Cancel'
    elif pipeline.predict(test_df)[0]== 1:
        result = 'Customer will Cancel'
    return result
    
        
    
def main():
    st.title('Cancelation predictions')
    hotel = st.selectbox("hotel",['Resort Hotel', 'City Hotel'])
    adults = st.slider('adults',min_value = 0 , max_value= 55, value= 2, step=1)
    meal = st.selectbox("meal",['BB' ,'FB', 'HB', 'SC' ,'Undefined'])
    country = st.selectbox("country",countrylist)
    market_segment = st.selectbox("market_segment",segmentlist)
    distribution_channel = st.selectbox("distribution_channel",distlist)
    assigned_room_type = st.selectbox("assigned_room_type",assignedlist)
    days_in_waiting_list = st.slider('days_in_waiting_list',min_value = 0 , max_value= 400, value= 0, step=1)
    customer_type = st.selectbox("customer_type",['Transient', 'Contract' ,'Transient-Party', 'Group'])
    lead_time_category = st.selectbox("lead_time_category",['long', 'short', 'medium'])
    adr = st.slider('adr',min_value = 0 , max_value= 600, value= 50, step=1)
    season = st.selectbox("season",['peak', 'shoulder', 'off-peak'])
    Day_Name = st.selectbox("Day_Name",['Wednesday', 'Thursday', 'Friday', 'Tuesday', 'Sunday' ,'Monday' ,'Saturday'])
    is_holiday = st.selectbox("is_holiday",['weekdays', 'holiday'])
    room_type_preference = st.selectbox("room_type_preference",['Preferred' ,'Not Preferred'])
    total_length_of_stay = st.slider('total_length_of_stay',min_value = 0 , max_value= 70, value= 2, step=1)
    if st.button("Predict"):
        result = predict(hotel, meal,country,market_segment,distribution_channel,assigned_room_type,days_in_waiting_list,customer_type,lead_time_category,adults,adr,season,Day_Name,is_holiday,room_type_preference,total_length_of_stay)
        st.write(result)
if __name__ =='__main__':
    main()
