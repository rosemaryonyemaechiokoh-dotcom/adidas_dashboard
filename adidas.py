import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Getting the acronyms of the states
us_state_to_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
    "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI",
    "Wyoming": "WY", "District of Columbia": "DC"
}

st.set_page_config(page_title="###  Adidas US Sales Datasets Dashboard", layout="wide")
df = pd.read_excel("Adidas US Sales Datasets.xlsx", header=4)
df = df.drop("Unnamed: 0", axis=1)

sales_per_product = (df.groupby(["Retailer", "Product"])["Total Sales"].sum().reset_index())

units_sold_per_product = df.groupby('Product')["Units Sold"].sum().reset_index()

df["Date"] = pd.to_datetime(df["Invoice Date"])


df["Weekday"] = df["Date"].dt.day_name()
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df["Weekday"] = pd.Categorical(df["Weekday"], categories=weekday_order, ordered=True)
avg_units_per_weekday = (df.groupby("Weekday")["Units Sold"].mean().reset_index())

# most_popular_method = df["Sales Method"].mode()[0]

sales_method_counts = df["Sales Method"].value_counts().reset_index()
sales_method_counts.columns = ["Sales Method", "Transactional_Count"]

revenue_by_region = df.groupby("Region")["Total Sales"].sum().reset_index()

df["State_Code"] = df["State"].map(us_state_to_abbrev)
state_revenue = df.groupby("State_Code")["Total Sales"].sum().reset_index()
region_revenue = df.groupby(["State_Code", "Region"])["Total Sales"].sum().reset_index()

total_sales = df["Total Sales"].sum()

df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])
monthly_revenue = df.set_index("Invoice Date")["Total Sales"].resample("M").sum().reset_index()
monthly_revenue["Month_Year_Label"] = monthly_revenue["Invoice Date"].dt.strftime("%B %Y")

st.title("Adidas US Sales Dashboard")

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue Generated", f'${df["Total Sales"].sum():,.2f}')
col2.metric("Total Units Sold", df["Units Sold"].sum())
col3.metric("Total Number of Retailers", df["Retailer"].nunique())

col4, col5 = st.columns((8,7))


with col4:
    st.subheader("Total Monthly Revenue")
    chart_data_col1 = monthly_revenue.set_index("Month_Year_Label")
    st.bar_chart(chart_data_col1["Total Sales"])

with col5:
    st.subheader("Unit Sold: Proportional Breakdown (Treemap)")
    fig_treemap = px.treemap(units_sold_per_product, path=["Product"], values="Units Sold",
                            )

    st.plotly_chart(fig_treemap, use_container_width=True)

col6, col7 = st.columns((8,7))

with col6:
    st.subheader("Retailer Sales (Total Revenue)")
    fig_col3 = px.bar(sales_per_product, x="Total Sales", y="Retailer", orientation="h")
    fig_col3.update_layout(xaxis_title="Total Sales($)", yaxis_title="Retailer")

    st.plotly_chart(fig_col3, use_container_width=True)


with col7:
    st.subheader("Average Units Sold per Weekday")
    fig, ax = plt.subplots(figsize=(7,4))
    sns.barplot(data=avg_units_per_weekday, x="Weekday", y="Units Sold", ax=ax)
    ax.set_title("Average Units Sold by Day of the Week")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig)

col8, col9 = st.columns((7,7))

with col8:
    st.subheader("Most Popular Sales Method")
    fig_pie = px.pie(sales_method_counts, names="Sales Method", values="Transactional_Count",
                     title="Highest Sales Method Trend")

    st.plotly_chart(fig_pie, use_container_width=True)

with col9:
    st.subheader("Revenue Distribution by Region")
    fig, ax = plt.subplots(figsize=(7,4))
    sns.barplot(data=region_revenue, x="Region", y="Total Sales", hue="Region", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig)


st.subheader("Total Revenue per State")
fig = px.choropleth(state_revenue, locations="State_Code", color="Total Sales", locationmode="USA-states",
                    scope="usa", color_continuous_scale="Viridis", title="Total Sales per State",
                    height=550
                    )
fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)

st. markdown(" Adidas US Datasets Table")
st.dataframe(data=df.head(20))

st.markdown('''
--------------------------------------------
Designed by Rosamaria:
''')
