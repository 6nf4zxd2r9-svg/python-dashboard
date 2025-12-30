import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("Sales Performance Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('data/sales_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()
# Add sidebar filters
st.sidebar.header("Filters")
# Product filter
products = st.sidebar.multiselect(
"Select Products",
options=df['Product'].unique(),
default=df['Product'].unique()
)
# Region filter
regions = st.sidebar.multiselect(
"Select Regions",
options=df['Region'].unique(),
default=df['Region'].unique()
)
# Apply filters
df = df[df['Product'].isin(products) & df['Region'].isin(regions)]

st.header("Key Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    total_revenue = df['Total'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.0f}")

with col2:
    total_sales = len(df)
    st.metric("Total no. Sales", f"{total_sales:,}")
with col3:
    avg_sale = df['Total'].mean()
    st.metric("Average Sale", f"${avg_sale:.0f}")
st.divider()


product_revenue = df.groupby('Product')['Total'].sum().sort_values(ascending=True)
fig1, ax1 = plt.subplots(figsize=(10, 6))
sns.barplot(x=product_revenue.values, y=product_revenue.index, palette='viridis', ax=ax1)
ax1.set_xlabel('Revenue ($)')
ax1.set_ylabel('Product')
ax1.set_title('Revenue by Product')



df['Month'] = df['Date'].dt.to_period('M').astype(str)
monthly_sales = df.groupby('Month')['Total'].sum()
fig2, ax2 = plt.subplots(figsize=(10, 6))
monthly_sales.plot(kind='line', marker='o', ax=ax2)
ax2.set_xlabel('Month')
ax2.set_ylabel('Revenue ($)')
ax2.set_title('Monthly Revenue Trend')
ax2.grid(True, alpha=0.3)
plt.xticks(rotation=45)



region_sales = df.groupby('Region')['Total'].sum()
fig3, ax3 = plt.subplots(figsize=(10, 4))
colors = sns.color_palette('pastel')
ax3.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%',
colors=colors, startangle=90)
ax3.set_title('Revenue Distribution by Region')




fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='Quantity', y='Total', s=80)

ax4.set_xlabel('Quantity Sold')
ax4.set_ylabel('Revenue ($)')
ax4.set_title('Revenue vs Quantity')
ax4.grid(True, alpha=0.3)

st.header("Dashboard")
col1, col2 = st.columns(2)
with col1:
    st.header("Revenue by Product")
    st.pyplot(fig1)
with col2:
    st.header("Monthly Sales Trend")
    st.pyplot(fig2)

col3, col4 = st.columns(2)
with col3:
    st.header("Sales by Region")
    st.pyplot(fig3)
with col4:
    st.header("Revenue vs Quantity")
    st.pyplot(fig4)


st.header("Raw Data")
st.dataframe(df, use_container_width=True)