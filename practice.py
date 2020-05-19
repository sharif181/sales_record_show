import pandas as pd 
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
DATA_URL = 'SalesJan2009.csv'

@st.cache(persist = True)
def data_load():
    data = pd.read_csv(DATA_URL)
    data['Account_Created'] = pd.to_datetime(data['Account_Created'])
    data['Last_Login']= pd.to_datetime(data['Last_Login'])
    data['Price'] = pd.to_numeric(data['Price'])
    return data


data = data_load()

st.title("This app is showing the sales info of January 2009")

st.map(data)
price_mean = data['Price'].mean()

md = data[data['Price'] <= price_mean]

md2 = data[data['Price'] > price_mean]

st.subheader("This map shows sales under average price")
st.map(md)

st.subheader("This map shows sales above average price")
st.map(md2)



# fig = go.Figure(go.Scattermapbox(
#     mode = "markers+lines",
#     lon = data['longitude'],
#     lat = data['latitude'],
#     marker = {'size': 10}))

# fig.add_trace(go.Scattermapbox(
#     mode = "markers+lines",
#     lon = data['longitude'],
#     lat = data['latitude'],
#     marker = {'size': 10}))

# fig.update_layout(
#     margin ={'l':0,'t':0,'b':0,'r':0},
#     mapbox = {
#         'center': {'lon': 10, 'lat': 10},
#         'style': "stamen-terrain",
#         'center': {'lon': -20, 'lat': -20},
#         'zoom': 1})
# st.plotly_chart(fig)

st.sidebar.title("This is sidebar")
AcTime = st.sidebar.slider('Account Created time',0,23)

modfied_data = data[data['Account_Created'].dt.hour == AcTime]
st.subheader("Map by Account created hour")
st.map(modfied_data)

lastLogin = st.sidebar.slider("Last login hour",0,23)
modfied_data = data[data['Last_Login'].dt.hour == lastLogin]
st.map(modfied_data)

product = data['Product'].value_counts()
product = pd.DataFrame({
    'Product':product.index,
    'Qantity':product.values
})

select = st.sidebar.selectbox("Select a chart",("None","hist","pie"))
if select == 'hist':
    fig = px.bar(product,x='Product',y='Qantity' ,color='Qantity',height=299)
    st.plotly_chart(fig)
elif select== 'pie':
    fig = px.pie(product,values='Qantity',names='Product')
    st.plotly_chart(fig)
else:
    pass



paymentType = data['Payment_Type'].value_counts()
paymentType = pd.DataFrame({
    'Type':paymentType.index,
    'Quantity':paymentType.values
})

fig = px.scatter(paymentType,x='Type',y='Quantity',color='Quantity')
st.plotly_chart(fig)
