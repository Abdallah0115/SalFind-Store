import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as opy
import numpy as np


def date_encode(x):

    if(x.year == 2020):

        if(x.month == 10):

            return 1

        elif(x.month ==11):

            return 2

        else:

            return 3

    else:

        return x.month + 3

class Analysis:

    df = None

    total = None


    def __init__(self,link) :
        #---------------- Enter data --------------------------
        self.df = pd.read_csv(link)
        self.total = pd.read_csv(link)

        self.df = self.df[self.df["price"] >= 1]

        #---------------Detecting outliers and replacing with the median--------------
        threshold_factor = 3
        
        for column in self.df.select_dtypes(include=[np.number]).columns:
            
            #-----------Calculate Z-scores for each numeric column----------------------
            z_scores = (self.df[column] - self.df[column].mean()) / self.df[column].std()
            
            #-----------------Find outliers using Z-score method -----------------------
            outliers = self.df[abs(z_scores) > threshold_factor]
            
            if not outliers.empty:
                #--------------Replace outliers with median value of the respective column--------
                median_value = self.df[column].median()
                self.df.loc[outliers.index, column] = median_value
        
        #---------- Handling missing data----------------------------------
        if self.df is not None:
            #------------- Calculate percentage of missing values in each column --------------
            missing_percentage = (self.df.isnull().sum() / len(self.df)) * 100
            
            #----------------- Check if any column has more than 30% missing values------------
            if any(missing_percentage > 30):
                print("More than 30% missing data. Rejecting dataset.")
                return
            
            #----------------- Deal with missing values based on data types ------------------------
            for column in self.df.columns:
                if self.df[column].dtype == 'object':
                    # ------------ For object (categorical) columns, replace missing values with the mode ------------------
                    self.df[column].fillna(self.df[column].mode()[0], inplace=True)
                else:
                    # ---------------------- For numeric columns, replace missing values with the median -------------------
                    self.df[column].fillna(self.df[column].median(), inplace=True)

        # ------------------- Handling inconsistency-------------------------------------#
        if self.df is not None:
            #---------------------- Check for inconsistency in the dataset -----------------------
            valid_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled']
            inconsistent_rows = self.df[~self.df['status'].isin(valid_statuses)]
            
            if not inconsistent_rows.empty:
                # -------------------------------  If there are inconsistent rows, you can either remove them or handle them based on your requirement ---------------------
                print("Inconsistent rows detected in 'status' column:")
                print(inconsistent_rows)
            else:
                print("No inconsistency detected.")
        else:
            print("DataFrame not provided. Cannot handle inconsistency.")
        ##
        self.df = self.df[self.df["status"] != "canceled"]
        self.df = self.df[self.df["status"] != "order_refunded"]        
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])
        self.df = self.df.drop_duplicates()
        del(self.df['item_id'])
        del(self.df['year'])
        del(self.df['month'])
        del(self.df['ref_num'])
        del(self.df['Name Prefix'])
        del(self.df['First Name'])
        del(self.df['Middle Initial'])
        del(self.df['Last Name'])
        del(self.df['E Mail'])
        del(self.df['Phone No. '])
        del(self.df['Place Name'])
        del(self.df['Zip'])
        del(self.df['Region'])
        del(self.df['User Name'])
        del(self.df['SSN'])
        del(self.df['order_id'])
        self.df['discount_percentage'] = self.df['discount_percentage'].apply(lambda x: float(x) )
        bins = [18, 40, 60 , float('inf')]
        labels = ['Youths', 'Middle age' , 'Old']
        self.df['age_group'] = pd.cut(self.df['age'], bins=bins, labels=labels, right=False)
        self.df['month'] = self.df['order_date'].apply(lambda x: date_encode(x) ) 

    def total_money(self):
        total_sales = self.df['total'].sum()
        return total_sales

    def total_disc(self):
        total_sales = self.df['discount_amount'].sum()
        return total_sales



    def total_peices(self):
        total_qty_ordered = self.df['qty_ordered'].sum()
        return total_qty_ordered

    def total_cust(self):
        unique_customers_count = self.df['cust_id'].nunique()

        return unique_customers_count

    def refunded(self):
        completed_orders = self.total[self.total['status'].isin(['canceled', 'order_refunded', 'refund'])]

# Calculate the total number of completed orders
        total_completed_orders = completed_orders.shape[0]
        return total_completed_orders

    def canceld(self):
        canceled_orders = self.total[self.total['status'] == 'canceled']

# Calculate the total number of orders canceled      
        total_orders_canceled = canceled_orders.shape[0]

        return total_orders_canceled 

    def ref(self):
        canceled_orders = self.total[self.total['status'] == 'order_refunded']

# Calculate the total number of orders canceled
        total_orders_canceled = canceled_orders.shape[0]
        return total_orders_canceled

    def gauge_total(self):

        total_sales = self.total_money()

# Create a gauge figure
        fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_sales,
                title = {'text': "Total Sales"},
                gauge = {
                        'axis': {'range': [None, 100000000],
                                'tickwidth': 1,
                                'tickcolor': "white",
                                'tickfont': {'size': 30},
                                },                                
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                                {'range': [0, 20000000], 'color': "red"},
                                {'range': [20000000, 40000000], 'color': "orange"},
                                {'range': [40000000, 60000000], 'color': "yellow"},
                                {'range': [60000000, 80000000], 'color': "lightgreen"},
                                {'range': [80000000, 100000000], 'color': "green"}
                        ],
                        'threshold': {
                                'line': {'color': "black", 'width': 4},
                                'thickness': 0.75,
                                'value': total_sales
                                }
                        }
                
        ))

        fig.update_layout(width=700, height=300 , plot_bgcolor="#212121")

        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def gauge_order_can(self):
        total_sales = self.refunded()

        fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_sales,
                title = {'text': "Non-Completed Orders"},
                gauge = {
                        'axis': {'range': [None, 250000],
                                'tickwidth': 1,
                                'tickcolor': "white",
                                'tickfont': {'size': 30},
                                },                                
                        'bar': {'color': "darkblue"},
                        'bgcolor': "white",
                        'borderwidth': 2,
                        'bordercolor': "gray",
                        'steps': [
                                {'range': [0, 50000], 'color': "red"},
                                {'range': [100000, 150000], 'color': "orange"},
                                {'range': [150000, 200000], 'color': "yellow"},
                                {'range': [200000, 2500000], 'color': "green"}
                        ],
                        'threshold': {
                                'line': {'color': "black", 'width': 4},
                                'thickness': 0.75,
                                'value': total_sales
                                }
                        }
                
        ))

        fig.update_layout(width=700, height=300 , plot_bgcolor="#212121")

        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def total_per_mon(self):
        month_names = [ 'Oct', 'Nov', 'Dec','Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',]

# Assuming you have already loaded your data into a DataFrame called df
# Grouping data by month and summing total sales
        df_salesPerMonth = self.df.groupby('month')['total'].sum().reset_index()

# Create an interactive line chart with Plotly Express
        fig = px.line(df_salesPerMonth, x='month', y='total', 
              title='Total Sales Distribution by Month', 
              labels={'month': 'Month', 'total': 'Total Sales'},
              color_discrete_sequence=['blue'])  # Set line color to blue

# Customize the layout
        fig.update_layout(xaxis_title='Month', yaxis_title='Total Sales', title_font_size=20)

# Update x-axis tick labels with month names
        fig.update_xaxes(ticktext=month_names, tickvals=list(range(1, 13)))

        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Total_Sales_By_Category(self):

        df_grouped = self.df.groupby('category')['total'].sum().reset_index()

        fig = px.bar (df_grouped.sort_values(by='total', ascending=False), 
                        x='category', 
                        y='total', 
                        color='category', 
                        title='Total Sales by Category',
                        labels={'category': 'Category', 'total': 'Total Sales'},
                        height=600)
        # Rotate x-axis labels for better readability
        fig.update_layout(xaxis=dict(tickangle=45))

        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Order_Of_Category(self):
        df_grouped2 = self.df.groupby('category')['qty_ordered'].sum().reset_index()
# Create an interactive bar plot with Plotly using a different color palette
        fig = px.bar(df_grouped2.sort_values(by='qty_ordered', ascending=False), 
            x='category', 
            y='qty_ordered', 
            color='category', 
            title='Order of Category',
            labels={'category': 'Category', 'qty_ordered': 'Orders'},
            height=600,
            color_discrete_sequence=px.colors.qualitative.Pastel)  # Using the 'Pastel' color palette
# Rotate x-axis labels for better readability
        fig.update_layout(xaxis=dict(tickangle=45))

        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def total_Sales_By_Destrib_By_Month(self):
        month_names = ['Oct', 'Nov', 'Dec','Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep']
        df_salesPerMonth = self.df.groupby('month')['total'].sum().reset_index()

# Create an interactive histogram-like plot with Plotly Express
        fig = px.bar(df_salesPerMonth, x='month', y='total', 
             title='Total Sales Distribution by Month', 
             labels={'month': 'Month', 'total': 'Total Sales'},
             color='total',  # Use total sales for color mapping
             color_discrete_sequence=px.colors.qualitative.Pastel,  # Set color palette to Pastel
             category_orders={'month': [month_names[i-1] for i in range(1, 13)]},height=600) # Use month_names for ordering

# Customize the layout
        fig.update_layout(xaxis_title='Month', yaxis_title='Total Sales', title_font_size=20)

# Update x-axis tick labels with month names
        fig.update_xaxes(ticktext=month_names, tickvals=list(range(1, 13)))

# Manually set the range of the y-axis to ensure appropriate scaling
        fig.update_layout(yaxis_range=[0, df_salesPerMonth['total'].max() * 1.1])


        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Total_Sales_By_Gender(self):
        df_gender = self.df.groupby('Gender')['total'].sum().reset_index()

# Create an interactive donut chart with Plotly Express
        fig = px.pie(df_gender, values='total', names='Gender', 
                    title='Total Sales by Gender',
                    hole=0.4,  # Set the size of the hole in the middle
                    labels={'Gender': 'Gender', 'total': 'Total Sales'},
                    color_discrete_sequence=['#1f77b4', '#ff7f0e']
                    ,height=600 )  # Specify custom colors

# Customize the layout
        fig.update_traces(textinfo='percent+label', pull=[0.1, 0], textposition='inside')  # Add percentage labels inside the slices
        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Num_Of_Orders_By_Gendr(self):
# Create an interactive bar chart with Plotly Express
        labels = ['Youths', 'Middle age' , 'Old']
        fig = px.bar(self.df.groupby(['age_group', 'Gender']).size().reset_index(name='Count'), 
                    x='age_group', y='Count', color='Gender',
                    barmode='group',
                    title='Number of Orders by Age Group and Gender',
                    labels={'age_group': 'Age Group', 'Count': 'Number of Orders'},
                    category_orders={'age_group': labels},
                    hover_data={'Gender': True, 'Count': True},height=600)

# Customize the layout
        fig.update_layout(xaxis={'title': 'Age Group'}, yaxis={'title': 'Number of Orders'}, 
                        legend={'title': 'Gender'}, title_font_size=20)
        
        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def plot_income_by_age_group(self):
        data_age_einco = self.df.groupby(['age_group', 'Gender'], as_index=False)['total'].sum().sort_values(by='total')

        fig = px.bar(data_age_einco, x='age_group', y='total', color='Gender',
                        title='Income of Each Age Interval', labels={'total': 'Total Income', 'age_group': 'Age Group'},
                        barmode='group')

        fig.update_layout(xaxis=dict(tickfont=dict(size=12), tickangle=45),
                        yaxis=dict(tickfont=dict(size=12)),
                        legend=dict(font=dict(size=12)),
                        font=dict(size=12),height=600)

        fig.update_traces(texttemplate='%{y:.2s}', textposition='outside')

        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def plot_sales_by_status(self):
        df_status = self.df.groupby(['status'])['total'].sum().reset_index()

        fig = px.bar(df_status.sort_values(by='total', ascending=False), x='status', y='total', 
                        title='Total Sales by Transaction Status', labels={'total': 'Total Sales', 'status': 'Transaction Status'},
                        color='status')

        fig.update_layout(xaxis=dict(tickfont=dict(size=12), tickangle=45),
                        yaxis=dict(tickfont=dict(size=12)),
                        legend=dict(font=dict(size=12)),
                        font=dict(size=12),height=600)

        fig.update_traces(texttemplate='%{y:.2s}', textposition='outside')
        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Pie_Chart_of_Status_Distribution(self):

        status_counts = self.total['status'].value_counts()

        fig = px.pie(status_counts, values=status_counts.values, names=status_counts.index, 
                        title='Pie Chart of Status Distribution', 
                        hole=0.4,  # Adjust hole size
                        labels={'label': 'Status', 'value': 'Count'},
                        color_discrete_sequence=px.colors.qualitative.Set3 ,height=400)  # Use a consistent color palette

# Remove slice separation
        fig.update_traces(marker=dict(line=dict(color='white', width=0)))

# Add data labels inside slices
        fig.update_traces(textposition='inside')

# Add hover information
        fig.update_traces(hoverinfo='label+percent+value')
        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def orders_per_state(self):
        state_counts = self.df["State"].value_counts()

# Create a choropleth map
        fig = go.Figure(data=go.Choropleth(
                        locations=state_counts.index,
                        z=state_counts.values.astype(float),
                        locationmode="USA-states",
                        colorscale="Blues",  # You can change the color scale as needed
                        colorbar_title="Number of Orders",
                ))

# Update layout
        fig.update_layout(
                        titlfe_text="Number of Orders per State",
                        geo_scope="usa", height = 600
                )
        chart = fig.to_html()

        return chart

    def Top_10_States_with_Total_Income(self):

        g = self.df.groupby("State")["total"].sum().reset_index()
        s = g.sort_values("total", ascending=False)

# Select top 10 states
        top_10_states = s.head(10)

# Create an interactive bar plot with Plotly
        fig = px.bar(top_10_states, x='State', y='total', color='State', 
                title='Top 10 States with Total Sales', 
                labels={'total': 'Total Sales', 'State': 'State'},
                height=600)

# Rotate x-axis labels for better readability
        fig.update_layout(xaxis=dict(tickangle=45))

        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Low_10_States_with_Total_Income(self):
        g = self.df.groupby("State")["total"].sum().reset_index()
        s = g.sort_values("total", ascending=True)

# Select lowest 10 states
        lowest_10_states = s.head(10)

# Create an interactive bar plot with Plotly
        fig = px.bar(lowest_10_states, x='State', y='total', color='State', 
                title='Lowest 10 States with Total Sales', 
                labels={'total': 'Total Sales', 'State': 'State'},
                height=600)

# Rotate x-axis labels for better readability
        fig.update_layout(xaxis=dict(tickangle=45))
        
        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Top_5_Counties_by_Quantity_Ordered(self):

        df_qty_per_county = self.df.groupby('County')['qty_ordered'].sum().reset_index()

# Sorting the dataframe by quantity ordered in descending order
        df_qty_per_county_sorted = df_qty_per_county.sort_values(by='qty_ordered', ascending=False)

# Selecting the top 5 counties
        top_5_counties = df_qty_per_county_sorted.head(10)

# Create a pie chart with Plotly Express
        fig = px.pie(top_5_counties, values='qty_ordered', names='County',
                title='Top 10 Counties by Quantity Ordered', 
                color_discrete_sequence=px.colors.qualitative.Set3  # Use a consistent color palette
                ,hole = 0.6,height=600
        )

        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Lower_5_Counties_by_Quantity_Ordered(self):

        df_qty_per_county = self.df.groupby('County')['qty_ordered'].sum().reset_index()

# Sorting the dataframe by quantity ordered in descending order
        df_qty_per_county_sorted = df_qty_per_county.sort_values(by='qty_ordered', ascending=False)

# Selecting the top 5 counties
        top_5_counties = df_qty_per_county_sorted.tail(10)

# Create a pie chart with Plotly Express
        fig = px.pie(top_5_counties, values='qty_ordered', names='County',
                title='Lower 10 Counties by Quantity Ordered', 
                color_discrete_sequence=px.colors.qualitative.Set3  # Use a consistent color palette
                ,hole = 0.6,height=600
        )
        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Total_Sales_by_Payment_Method(self):
        df_salesPerPaymentMethod =self.df.groupby('payment_method')['total'].sum().reset_index()

# Create an interactive bar chart with Plotly Express
        fig = px.bar(df_salesPerPaymentMethod, x='payment_method', y='total', 
                title='Total Sales by Payment Method', 
                labels={'payment_method': 'Payment Method', 'total': 'Total Sales'},
                color='total',  # Color by total sales
                color_continuous_scale='purples',  # Use a continuous color scale
                color_continuous_midpoint=0.5,height=600)  # Set midpoint to avoid lightest colors

# Customize the layout
        fig.update_layout(xaxis_title='Payment Method', yaxis_title='Total Sales', title_font_size=20)
        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Discount_Percentage_by_Payment_Method(self):

        fig = px.scatter(self.df, x='payment_method', y='discount_percentage', 
                title='Discount Percentage by Payment Method',
                labels={'payment_method': 'Payment Method', 'discount_percentage': 'Discount Percentage'},
                color='payment_method',  # Color by payment method
                category_orders={'payment_method': ['method1', 'method2', 'method3']},height=600)  # Order payment methods

# Customize the layout
        fig.update_layout(xaxis_title='Payment Method', yaxis_title='Discount Percentage', title_font_size=20)
        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def Average_Discount_Percentage_by_Payment_Method(self):

        df_avg_discount_per_method = self.df.groupby('payment_method')['discount_percentage'].mean().reset_index()

# Create an interactive bar chart with Plotly Express
        fig = px.bar(df_avg_discount_per_method, x='payment_method', y='discount_percentage', 
                title='Average Discount Percentage by Payment Method', 
                labels={'payment_method': 'Payment Method', 'discount_percentage': 'Average Discount Percentage'},
                color='payment_method' , height=600)  # Color by payment method

# Customize the layout
        fig.update_layout(xaxis_title='Payment Method', yaxis_title='Average Discount Percentage', title_font_size=20)

        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def ref_per_status(self):
        refunded_orders = self.df[self.df['status'] == 'refund']

# Calculate the number of refunded orders per state
        refunded_state_counts = refunded_orders['State'].value_counts()

# Create a choropleth map
        fig = go.Figure(data=go.Choropleth(
                        locations=refunded_state_counts.index,
                        z=refunded_state_counts.values.astype(float),
                        locationmode="USA-states",
                        colorscale="Purples",  # You can change the color scale as needed
                        colorbar_title="Number of Refunded Orders",
                ))

# Update layout
        fig.update_layout(
                title_text="Number of Refunded Orders per State",
                geo_scope="usa"
                )
        
        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart

    def disc_per_month(self):
        df_discounts_per_month = self.df.groupby('month')['discount_amount'].sum().reset_index()

# Define month names
        month_names = [ 'Oct', 'Nov', 'Dec','Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',]

# Create an interactive pie chart with Plotly Express
        fig = px.pie(df_discounts_per_month, values='discount_amount', names=df_discounts_per_month['month'].map({i+1: month_names[i] for i in range(12)}),
             title='Total Discounts Distribution by Month',
             color_discrete_sequence=px.colors.qualitative.Set3,  # Use a consistent color palette
             hole=0.6,  # Set the size of the hole in the center
             labels={'month': 'Month', 'discount_amount': 'Total Discounts'},height=600)

# Update layout
        fig.update_layout(title_font_size=20)

# Update x-axis tick labels with month names
        fig.update_traces(textinfo='percent+label')
        chart = opy.plot(fig, auto_open=False, output_type='div')

        return chart
