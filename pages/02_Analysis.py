
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots



df = pd.read_csv('df.csv')
hotel_counts = pd.read_csv('hotel_booking_counts.csv')
revenue_counts = pd.read_csv('hotel_revenue_by_type.csv')
monthly_cancellations = pd.read_csv('monthly_cancellations.csv')
monthly_data = pd.read_csv('monthly_average_adr.csv')
yearly_cancellations = pd.read_csv('yearly_cancellations.csv')
yearly_adr = pd.read_csv('yearly_average_adr.csv')
nationality_dist = pd.read_csv('nationality_distribution.csv')
channel_dist = pd.read_csv('channel_distribution.csv')
cancellation_rates = pd.read_csv('cancellation_rates_by_room_type.csv')
request_counts = pd.read_csv('special_request_counts.csv')
lead_time_counts = pd.read_csv('lead_time_counts.csv')
meal_counts = pd.read_csv('meal_plan_counts.csv')
merged = pd.read_csv('detailed_cancellation_analysis.csv')
cancellation_rates_lead_time = pd.read_csv('cancellation_rates_by_lead_time.csv')
avg_cancellation_by_channel = pd.read_csv('avg_cancellation_by_channel.csv')
avg_cancellation_by_segment = pd.read_csv('avg_cancellation_by_segment.csv')
avg_stay_by_country = pd.read_csv('avg_stay_by_country.csv')
avg_adr_by_customer_type = pd.read_csv('avg_adr_by_customer_type.csv')
holiday_counts = pd.read_csv('holiday_booking_counts.csv')
holidays_revenue = pd.read_csv('holidays_revenue.csv')
occupancy_by_channel = pd.read_csv('occupancy_by_channel.csv')
avg_adr_by_deposit = pd.read_csv('avg_adr_by_deposit.csv')
results_df = pd.read_csv('hotel_occupancy_metrics.csv')
parking_data = pd.read_csv('parking_requirements.csv')
length_of_stay = pd.read_csv('length_of_stay.csv')
prev_bookings = pd.read_csv('previous_bookings.csv')
repeated_guests = pd.read_csv('repeated_guests.csv')
hotel_counts_monthly = pd.read_csv('hotel_booking_month.csv')
revenue_counts_monthly = pd.read_csv('hotel_revenue_by_month.csv')
average_waiting_df= pd.read_csv('average_waiting.csv')


df.drop('Unnamed: 0', axis=1, inplace= True)
df_sample= df.head(10)

st.markdown('<h1 style="text-align:center; color: #4169E1;"> Analysis</h1>', unsafe_allow_html=True)

# Create tabs for different analyses
tap1, tap2 = st.tabs(['📈 Univariate Analysis', '📊 Bivariate Analysis'])
with tap1:
    st.header('Sample Data')
    st.dataframe(df_sample, hide_index=True)

    st.title("Hotel Occupancy")
    occupancy_rate = results_df.loc[results_df['Metric'] == 'Occupancy Rate (%)', 'Value'].values[0]
    st.metric(label="Average Occupancy Rate", 
            value=f"{occupancy_rate:.2f}%",
            help="Calculated as (booked rooms / total rooms) × 100")

    st.title("Percentage Requiring Parking")
    parking_requirements = parking_data.loc[parking_data['Metric'] == 'Percentage Requiring Parking', 'Value'].values[0]
    st.metric(label="Percentage Requiring Parking", 
            value=f"{parking_requirements:.2f}%",
            help="Calculated as (guests_requiring_parking / total_guests) * 100")


    st.title("Hotel Guest Stay Duration")
    average_length_of_stay = length_of_stay.loc[length_of_stay['Metric'] == 'Average Length of Stay (Nights)', 'Value'].values[0]
    st.metric(
        label="Average Length of Stay", 
        value=f"{average_length_of_stay:.0f} nights",
        help="Average nights stayed (weekend + week nights combined)"
    )

    st.title("Average Previous Bookings")
    avg_prev_bookings = prev_bookings.loc[prev_bookings['Metric'] == 'Average Previous Bookings per Guest', 'Value'].values[0]
    st.metric(
        label="Average Previous Bookings", 
        value=f"{avg_prev_bookings:.1f} bookings",
        help="Average number of non-canceled previous bookings per guest"
    )


    st.title("Repeated Guests")
    avg_repeated_guests = repeated_guests.loc[repeated_guests['Metric'] == 'Repeated Guests Count', 'Value'].values[0]
    st.metric(
        label="Average Repeated Guests", 
        value=f"{avg_repeated_guests: 0}", 
        help="Proportion of guests who have stayed before"
    )
    
    st.title("Average Length of Waiting")
    avg_waiting_days = average_waiting_df.loc[average_waiting_df['Metric'] == 'Average Length of Waiting', 'Value'].values[0]
    st.metric(
        label="Average Length of Waiting", 
        value=f"{avg_waiting_days:.0f} Days", 
        help="Average number of days guests have waited for their booking"
        
    )




    hotel_counts = df['hotel'].value_counts().reset_index()
    hotel_counts.columns = ['Hotel Type', 'Booking Count']

    fig0 = px.bar(
    hotel_counts,
    x='Hotel Type',
    y='Booking Count',
    title='Hotel Booking Counts by Type',
    text='Booking Count',
    color='Hotel Type',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    height=500
    )

    fig0.update_layout(
    xaxis_title='Hotel Type',
    yaxis_title='Number of Bookings',
    hovermode='x',
    )

    fig0.update_traces(
    texttemplate='%{text:,}',
    textposition='outside',
    )


    revenue_counts = df.groupby('hotel')['adr'].sum().reset_index()
    revenue_counts.columns = ['Hotel Type', 'Total Revenue']

    fig00 = px.bar(
    revenue_counts,
    x='Hotel Type',
    y='Total Revenue',
    title='Total Revenue by Hotel Type',
    text='Total Revenue',
    color='Hotel Type',
    color_discrete_sequence=px.colors.qualitative.Prism,
    height=500
    )

    fig00.update_layout(
    xaxis_title='Hotel Type',
    yaxis_title='Total Revenue (USD)',
    hovermode='x',
    hoverlabel=dict(bgcolor='white', font_size=12)
    )

    fig00.update_traces(
    texttemplate='\$%{text:,.0f}',  # Format as currency
    textposition='outside',
    )




    monthly_cancellations = df.groupby('arrival_date_month').agg(cancellations=('is_canceled', 'sum')).reset_index()

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_cancellations['arrival_date_month'] = pd.Categorical(monthly_cancellations['arrival_date_month'], 
                                                                  categories=month_order, 
                                                                  ordered=True)
    monthly_cancellations = monthly_cancellations.sort_values('arrival_date_month')


    month_orders = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']

    df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], 
                                               categories=month_orders, 
                                               ordered=True)

    monthly_data = df.groupby('arrival_date_month').agg(adr=('adr', 'mean')).reset_index()


    Yearly_cancellations = df.groupby('arrival_date_year').agg(cancellations=('is_canceled', 'sum')).reset_index()


    Yearly_cancellations['arrival_date_year'] = Yearly_cancellations['arrival_date_year'].astype(str)



    Yearly_adr = df.groupby('arrival_date_year').agg(adr=('adr', 'mean')).reset_index()


    Yearly_adr['arrival_date_year'] = Yearly_adr['arrival_date_year'].astype(str)


    figs = make_subplots(
        rows=2, 
        cols=2, 
        start_cell='bottom-left',
        subplot_titles=(
            "Cancelation Over Months", 
            "Cancelation Over Years",
            "ADR Over Months",
            "ADR Over Years"
        )
    )

    fig1 = px.bar(monthly_cancellations, 
                  x='arrival_date_month', 
                  y='cancellations',
                  title='Booking Cancellations by Month',
                  labels={'arrival_date_month': 'Month', 'cancellations': 'Number of Cancellations'},
                  text='cancellations', color_discrete_sequence=px.colors.sequential.Cividis)
    figs.add_trace(fig1.data[0], row=1, col=1)

    fig2 = px.bar(Yearly_cancellations, 
                     x='arrival_date_year', 
                     y='cancellations',
                     title='Booking Cancellations by Year',
                     labels={'arrival_date_year': 'Year', 'cancellations': 'Number of Cancellations'},
                     text='cancellations', 
                     color_discrete_sequence=px.colors.sequential.Cividis)
    figs.add_trace(fig2.data[0], row=1, col=2)

    fig3 = px.line(monthly_data, 
                  x='arrival_date_month', 
                  y='adr',
                  title='Average Daily Rate (ADR) by Month',
                  labels={'arrival_date_month': 'Month', 'adr': 'Average Daily Rate (€)'},
                  markers=True, color_discrete_sequence=px.colors.sequential.Cividis) 
    figs.add_trace(fig3.data[0], row=2, col=1)

    fig4 = px.line(Yearly_adr, 
                  x='arrival_date_year', 
                  y='adr',
                  title='Average Daily Rate (ADR) by Year',
                  labels={'arrival_date_year': 'Month', 'adr': 'Average Daily Rate (€)'},
                  markers=True, color_discrete_sequence=px.colors.sequential.Cividis) 
    figs.add_trace(fig4.data[0], row=2, col=2)


    figs.update_layout(  
        title_x=0.5, 
        height=600,  
        width=800,   
        margin=dict(l=40, r=40, t=40, b=40)
    )


    nationality_dist = df['country'].value_counts().reset_index().head(15)
    nationality_dist.columns = ['Nationality', 'Count']  # Rename columns

    fig5 = px.pie(
        nationality_dist,
        values='Count',        
        names='Nationality',   
        title='<b>Distribution of Guest Nationalities</b>',
        color_discrete_sequence=px.colors.sequential.Cividis,
        height=600,           
        labels={'Nationality': 'Guest Nationality'},
    )



    channel_dist = df['distribution_channel'].value_counts().reset_index()
    channel_dist.columns = ['channel', 'count']
    channel_dist['percentage'] = (channel_dist['count'] / channel_dist['count'].sum()) * 100

    fig6 = px.pie(channel_dist,
                 values='count',
                 names='channel',
                 title='Booking Distribution by Channel',
                 hover_data=['percentage'],
                 labels={'percentage': 'Percentage (%)'},
                 color='channel',
                 color_discrete_sequence=px.colors.sequential.Cividis,
                 hole=0.3)



    cancellation_rates = df[df['is_canceled'] == 1].groupby('room_type_preference').agg(
        canceled_bookings=('is_canceled', 'sum')
    ).reset_index()

    # Calculate cancellation rate
    cancellation_rates['cancellation_rate'] = (cancellation_rates['canceled_bookings'] / len(df)) * 100

    fig7 = px.bar(
        cancellation_rates,

        x='room_type_preference',
        y='cancellation_rate',
        title='<b>Cancellation Rate by Room Type</b>',
        labels={
            'room_type_preference': 'Room Type',
            'cancellation_rate': 'Cancellation Rate (%)'
        },
        text='cancellation_rate',  
        color='room_type_preference',
        color_discrete_sequence=px.colors.sequential.Viridis,
        hover_data={'canceled_bookings': True},  
    )

    fig7.update_traces(
        texttemplate='%{text:.1f}%',  
        textposition='outside',
        marker_line_width=1,
        marker_line_color='gray'
    )
    fig7.update_layout(
        xaxis_title='<b>Room Type</b>',
        yaxis_title='<b>Cancellation Rate (%)</b>',
        hovermode='x unified',
        uniformtext_minsize=8,
        showlegend=False  
    )



    ## How many guests typically make special requests?
    request_counts = df['total_of_special_requests'].value_counts().reset_index()
    request_counts.columns = ['Special Request', 'Count']


    # Bar Chart (Best for discrete counts)
    fig8 = px.bar(
        request_counts,
        x='Special Request',
        y='Count',
        title='<b>Number of Guests with Special Requests</b>',
        color='Special Request',
        color_discrete_sequence=px.colors.sequential.Cividis,
        text='Count',
        template='plotly_white'
    )
    fig8.update_traces(textposition='outside')



    lead_time_counts = df['lead_time_category'].value_counts().reset_index()
    lead_time_counts.columns = ['lead_time_category', 'count']

    lead_time_counts['proportion'] = lead_time_counts['count'] / lead_time_counts['count'].sum()

    fig9 = px.bar(
        lead_time_counts,
        x='lead_time_category',
        y='proportion',
        color='lead_time_category',
        color_discrete_sequence=px.colors.sequential.Cividis,
        text='proportion',
        title='Booking Lead Time Category Distribution',
        labels={
            'lead_time_category': 'Lead Time Category',
            'proportion': 'Proportion of Bookings'
        }
    )

    fig9.update_traces(texttemplate='%{text:.1%}', textposition='outside')



    meal_counts = df['meal'].value_counts().reset_index()
    meal_counts.columns = ['meal_plan', 'count']

    meal_counts['percentage'] = round(meal_counts['count'] / meal_counts['count'].sum() * 100, 1)

    meal_counts = meal_counts.sort_values('count', ascending=False)

    fig10 = px.bar(
        meal_counts,
        x='count',
        y='meal_plan',
        color='meal_plan',
        text='percentage',
        title='Distribution of Meal Plan Selections Among Guests',
        labels={'meal_plan': 'Meal Plan', 'count': 'Number of Guests'},
        color_discrete_sequence=px.colors.sequential.Cividis,
    )

    fig10.update_traces(texttemplate='%{text:.1f}%', textposition='outside')

    fig10.update_layout(
        xaxis_title='Number of Guests',
        yaxis_title='Meal Plan',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(
            x=0.5,  # Center the title
            font=dict(size=20)
        ),
        margin=dict(t=50, b=50)
    )




    st.header("Hotel Type Counts")
    st.plotly_chart(fig0)

    st.header("Hotel Type Revenue")
    st.plotly_chart(fig00)


    st.header("Monthly / Yearly ADR & Cancelations")
    st.plotly_chart(figs)

    st.header("Distribution of Guest Nationalities")
    st.plotly_chart(fig5)

    st.header("Booking Distribution by Channel")
    st.plotly_chart(fig6)

    st.header("Cancellation Rate by Room Type")
    st.plotly_chart(fig7)

    st.header("Number of Guests with Special Requests")
    st.plotly_chart(fig8)

    st.header("Booking Lead Time Category Distribution")
    st.plotly_chart(fig9)

    st.header("Distribution of Meal Plan Selections Among Guests")
    st.plotly_chart(fig10)
    
with tap2:
    #Group by hotel type and month for booking counts
    hotel_counts_monthly = df.groupby(['hotel', 'arrival_date_month']).size().reset_index(name='Booking Count')
    hotel_counts_monthly.columns = ['Hotel Type', 'Month', 'Booking Count']

    fig10 = px.bar(
        hotel_counts_monthly,
        x='Month',
        y='Booking Count',
        color='Hotel Type',
        title='Monthly Hotel Booking Counts by Type',
        text='Booking Count',
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=500
    )

    # Customize layout for booking counts
    fig10.update_layout(
        xaxis_title='Month',
        yaxis_title='Number of Bookings',
        hovermode='x',
    )

    fig10.update_traces(
        texttemplate='%{text:,}',
        textposition='outside',
    )


    # Group by hotel type and month for total revenue
    revenue_counts_monthly = df.groupby(['hotel', 'arrival_date_month'])['adr'].sum().reset_index()
    revenue_counts_monthly.columns = ['Hotel Type', 'Month', 'Total Revenue']


    fig11 = px.bar(
        revenue_counts_monthly,
        x='Month',
        y='Total Revenue',
        color='Hotel Type',
        title='Monthly Total Revenue by Hotel Type',
        text='Total Revenue',
        color_discrete_sequence=px.colors.qualitative.Prism,
        height=500
    )

    # Customize layout for revenue
    fig11.update_layout(
        xaxis_title='Month',
        yaxis_title='Total Revenue (USD)',
        hovermode='x',
        hoverlabel=dict(bgcolor='white', font_size=12)
    )

    fig11.update_traces(
        texttemplate='$%{text:,.0f}',  # Format as currency
        textposition='outside',
    )

    # Calculate cancellation rates by lead category and hotel type
    cancellation_rates = df.groupby(['lead_time_category', 'hotel'])['is_canceled'].mean().reset_index()
    cancellation_rates['cancellation_rate'] = cancellation_rates['is_canceled'] * 100
    cancellation_rates.rename(columns={'is_canceled': 'cancel_rate'}, inplace=True)

    # Create the visualization
    fig12 = px.scatter(
        cancellation_rates,
        x='lead_time_category',
        y='cancellation_rate',
        size='cancellation_rate',
        color='hotel',  # Use hotel type for color
        hover_name='lead_time_category',
        size_max=40,
        title='Cancellation Rate by Lead Time Category and Hotel Type',
        labels={
            'lead_time_category': 'Lead Time (days)',
            'cancellation_rate': 'Cancellation Rate (%)',
            'hotel': 'Hotel Type'
        },
        color_discrete_sequence=px.colors.qualitative.Set1  # Use a qualitative color scale for hotel types
    )

    # Customize layout
    fig12.update_layout(
        xaxis_title='Lead Time (days)',
        yaxis_title='Cancellation Rate (%)',
        hovermode='closest'
    )


    ## cancellation rates reationship by different categories
    cancelations = df[df['is_canceled'] == 1].groupby([
        'distribution_channel',
        'market_segment', 
        'total_of_special_requests',
        'booking_changes',
        'days_in_waiting_list'
    ]).agg(
        canceled_rooms=('adults', 'count')
    ).reset_index()

    total_bookings = df.groupby([
        'distribution_channel',
        'market_segment', 
        'total_of_special_requests',
        'booking_changes',
        'days_in_waiting_list'
    ]).agg(
        total_rooms=('adults', 'count')
    ).reset_index()

    merged = pd.merge(cancelations, total_bookings, on=[
        'distribution_channel',
        'market_segment',
        'total_of_special_requests',
        'booking_changes',
        'days_in_waiting_list'
    ])
    merged['cancellation_rate'] = (merged['canceled_rooms'] / merged['total_rooms']) * 100



    avg_cancellation_by_channel = merged.groupby('distribution_channel')['cancellation_rate'].mean().reset_index()



    avg_cancellation_by_segment = merged.groupby('market_segment')['cancellation_rate'].mean().reset_index()


    # 1. Distribution Channel vs Cancellation Rate
    fig13 = px.bar(avg_cancellation_by_channel, 
                    x='distribution_channel', 
                    y='cancellation_rate',
                    title='Average Cancellation Rate by Distribution Channel',
                    labels={'distribution_channel': 'Distribution Channel',
                            'cancellation_rate': 'Average Cancellation Rate (%)'},
                    color = 'distribution_channel')

    # 2. Market Segment vs Cancellation Rate
    fig14 = px.bar(avg_cancellation_by_segment, 
                    x='market_segment', 
                    y='cancellation_rate',
                    title='Average Cancellation Rate by Market Segment',
                    labels={'market_segment': 'Market Segment',
                            'cancellation_rate': 'Average Cancellation Rate (%)'},
                    color = 'market_segment' )

    ## correlation matrix for numerical Categories
    numerical_vars = ['total_of_special_requests', 'booking_changes', 'days_in_waiting_list', 'cancellation_rate']
    corr_matrix = merged[numerical_vars].corr()

    fig15 = px.imshow(corr_matrix,
                    labels=dict(x="Variable", y="Variable", color="Correlation"),
                    x=numerical_vars,
                    y=numerical_vars,
                    title='Correlation Matrix of Cancellation Factors')

    ## relationship between Occupancy Rate and Distribution Channel
    total_no_cancel = len(df[df['is_canceled'] == 0])
    total_bookings = len(df)
    overall_occupancy = (total_no_cancel / total_bookings) * 100

    occupancy_by_channel = (
        df.groupby('distribution_channel')
        .apply(lambda x: (len(x[x['is_canceled'] == 0]) / len(x)) * 100)
        .reset_index(name='occupancy_rate')
    )

    occupancy_by_channel.to_csv('occupancy_by_channel.csv', index=False)


    fig16 = px.bar(
        occupancy_by_channel,
        x='distribution_channel',
        y='occupancy_rate',
        title='Occupancy Rate by Distribution Channel',
        labels={
            'distribution_channel': 'Distribution Channel',
            'occupancy_rate': 'Occupancy Rate (%)'
        },
        text_auto='.1f', 
        color='distribution_channel',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig16.add_hline(
        y=overall_occupancy,
        line_dash="dot",
        annotation_text=f"Overall Occupancy: {overall_occupancy:.1f}%",
        annotation_position="bottom right"
    )

    fig16.update_layout(
        hovermode="x unified",
        showlegend=False,
        yaxis_range=[0, 100]  
    )

    ## Relationship between Average Length of Stay by Country

    df['length_of_stay'] = df['stays_in_weekend_nights'] + df['stays_in_week_nights']
    avg_stay_by_country = df.groupby('country')['length_of_stay'].mean().reset_index()

    avg_stay_by_country.to_csv('avg_stay_by_country.csv', index=False)


    fig17 = px.choropleth(
        avg_stay_by_country,
        locations='country',  
        locationmode='country names',  
        color='length_of_stay',  
        hover_name='country',  
        color_continuous_scale='viridis', 
        title='Average Length of Stay by Country of Origin',
        labels={'length_of_stay': 'Average Nights Stayed'}
    )

    fig17.update_geos(showcoastlines=True, coastlinecolor="Black")
    fig17.update_layout(
        coloraxis_colorbar=dict(title='Average Nights Stayed'),
        height=600
    )



    ## How does the average ADR vary with the type of deposit made?
    avg_adr_by_deposit = df.groupby(['deposit_type', 'hotel'])['adr'].mean().reset_index()

    # Save to CSV
    avg_adr_by_deposit.to_csv('avg_adr_by_deposit.csv', index=False)

    # Create the visualization
    fig18 = px.bar(
        avg_adr_by_deposit.sort_values('adr', ascending=False),
        x='deposit_type',
        y='adr',
        title='Average ADR by Deposit Type and Hotel Type',
        labels={
            'deposit_type': 'Deposit Type',
            'adr': 'Average Daily Rate (ADR)'
        },
        color='hotel',  # Use hotel type for color
        color_discrete_sequence=px.colors.qualitative.Set1,  # Use a qualitative color scale for hotel types
        text_auto='.2f'
    )

    fig18.update_layout(
        xaxis={'categoryorder': 'total descending'},
        hovermode="x unified",
        height=600
    )

    ## How does the average ADR vary with the type of customer made?

    avg_adr_by_customer_type = df.groupby(['customer_type', 'hotel'])['adr'].mean().reset_index()

    # Create the visualization
    fig19 = px.bar(
        avg_adr_by_customer_type.sort_values('adr', ascending=False),
        x='customer_type',
        y='adr',
        title='Average ADR by Customer Type and Hotel Type',
        labels={
            'customer_type': 'Customer Type',
            'adr': 'Average Daily Rate (ADR)'
        },
        color='hotel',  # Use hotel type for color
        color_discrete_sequence=px.colors.qualitative.Set1,  # Use a qualitative color scale for hotel types
        text_auto='.2f'
    )

    fig19.update_layout(
        xaxis={'categoryorder': 'total descending'},
        hovermode="x unified",
        height=600
    )

    ## Relationship between Booking Count in Holiday vs Non-Holiday (by Month and Season)'
    holiday_counts = df[df['is_canceled'] == 0].groupby(['is_holiday', 'arrival_date_month', 'season']).size().reset_index(name='booking_count')

    fig20 = px.bar(
        holiday_counts,
        x='arrival_date_month',
        y='booking_count',
        color='is_holiday',
        facet_col='season', 
        title='Booking Count: Holiday vs Non-Holiday (by Month and Season)',
        labels={
            'Booking Count': 'name',
            'arrival_date_month': 'Month',
            'is_holiday': 'Is Holiday?' 
        },
        hover_data=['season'],
        barmode='group', 
        color_discrete_map={0: '#636EFA', 1: '#EF553B'},  
        category_orders={
            'arrival_date_month': ['January', 'February', 'March', 'April', 'May', 'June', 
                                  'July', 'August', 'September', 'October', 'November', 'December'],
        }
    )




    ## Relationship between Booking Revenue in Holiday vs Non-Holiday (by Month and Season)',

    Holidays_Revenue = df[df['is_canceled'] == 0].groupby(['is_holiday','arrival_date_month', 'season']).agg(revenue=('adr', 'sum')).reset_index()

    fig21 = px.bar(
        Holidays_Revenue,
        x='arrival_date_month',
        y='revenue',
        color='is_holiday',
        facet_col='season', 
        title='Revenue: Holiday vs Non-Holiday (by Month and Season)',
        labels={
            'revenue': 'Revenue',
            'arrival_date_month': 'Month',
            'is_holiday': 'Is Holiday?' 
        },
        hover_data=['season'],
        barmode='group', 
        color_discrete_map={0: '#636EFA', 1: '#EF553B'},  
        category_orders={
            'arrival_date_month': ['January', 'February', 'March', 'April', 'May', 'June', 
                                  'July', 'August', 'September', 'October', 'November', 'December'],
        }
    )
    
    st.header("hotel type and month for booking counts")
    st.plotly_chart(fig10)

    st.header("hotel type and month for total revenue")
    st.plotly_chart(fig11)


    st.header("cancellation rates by lead category and hotel type")
    st.plotly_chart(fig12)

    st.header("cancellation rates reationship by channels")
    st.plotly_chart(fig13)

    st.header("cancellation rates reationship by segemnt")
    st.plotly_chart(fig14)

    st.header("cancellation rates reationship by different categories")
    st.plotly_chart(fig15)

    st.header("occupancy_by_channel")
    st.plotly_chart(fig16)

    st.header("Average Length of Stay by Country of Origin")
    st.plotly_chart(fig17)

    st.header("Average ADR by Deposit Type and Hotel Type")
    st.plotly_chart(fig18)
    
    st.header("Average ADR by Customer Type and Hotel Type")
    st.plotly_chart(fig19)
    
    st.header("Booking Count: Holiday vs Non-Holiday (by Month and Season)")
    st.plotly_chart(fig20)
    
    st.header("Revenue: Holiday vs Non-Holiday (by Month and Season)")
    st.plotly_chart(fig21)
    
