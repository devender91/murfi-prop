import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Murfi Dashboard", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Murfi Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)


df = pd.read_excel('haryana7.xlsx')

col1, col2, col3 = st.columns((3))
df["Date"] = pd.to_datetime(df["Date"])

# Getting the min and max date 
startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime('today')

with col1:
          st.markdown('<p style="font-size:32px; color:blue; font-weight:bold;">Historical Analysis</p>', unsafe_allow_html=True)
with col2:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col3:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()


#Sidebar code start here

st.sidebar.header("Choose your filter: ")

District = st.sidebar.multiselect("Select your District", df["District"].unique())
if not District:
    df2 = df.copy()
else:
    df2 = df[df["District"].isin(District)]


Colony = st.sidebar.multiselect("Select your Colony", df2["Colony"].unique())
if not Colony:
    df3 = df2.copy()
else:
    df3 = df2[df2["Colony"].isin(Colony)]


Vendor = st.sidebar.multiselect("Select the Vendor",df3["Vendor"].unique())

# Filter the data based on District, Colony and Vendor

if not District and not Colony and not Vendor:
    filtered_df = df
elif not Colony and not Vendor:
    filtered_df = df[df["District"].isin(District)]
elif not District and not Vendor:
    filtered_df = df[df["Colony"].isin(Colony)]
elif Colony and Vendor:
    filtered_df = df3[df["Colony"].isin(Colony) & df3["Vendor"].isin(Vendor)]
elif District and Vendor:
    filtered_df = df3[df["District"].isin(District) & df3["Vendor"].isin(Vendor)]
elif District and Colony:
    filtered_df = df3[df["District"].isin(District) & df3["Colony"].isin(Colony)]
elif Vendor:
    filtered_df = df3[df3["Vendor"].isin(Vendor)]
else:
    filtered_df = df3[df3["District"].isin(District) & df3["Colony"].isin(Colony) & df3["Vendor"].isin(Vendor)]


result = filtered_df.groupby(['District', 'Vendor'])['Property_ID'].nunique().reset_index()
result = result.rename(columns={'Property_ID': 'Properties_Covered'})
total_properties_covered = filtered_df['Property_ID'].nunique()

result1 = filtered_df.groupby(['District', 'Colony'])['Property_ID'].nunique().reset_index()
result1 = result1.rename(columns={'Property_ID': 'Properties Covered'})
total_properties_covered1 = filtered_df['Property_ID'].nunique()

result2 = filtered_df.groupby(['Vendor', 'Colony'])['Property_ID'].nunique().reset_index()
result2 = result2.rename(columns={'Property_ID': 'Properties Covered'})
total_properties_covered2 = filtered_df['Property_ID'].nunique()

result3 = filtered_df.groupby(['Colony', 'Vendor'])['Property_ID'].nunique().reset_index()
result3 = result3.rename(columns={'Property_ID': 'Properties Covered'})
total_properties_covered3 = filtered_df['Property_ID'].nunique()

result4 = filtered_df.groupby(['Vendor','Phone', 'Colony'])['Property_ID'].nunique().reset_index()
result4 = result4.rename(columns={'Property_ID': 'Properties Covered'})
total_properties_covered4 = filtered_df['Property_ID'].nunique()

result5 = filtered_df.groupby(['Colony',])['Property_ID'].nunique().reset_index()
result5 = result5.rename(columns={'Property_ID': 'Properties Covered'})
total_properties_covered5 = filtered_df['Property_ID'].nunique()

#pdf code
def df_to_pdf(df):
    buffer = BytesIO()

    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    
    table_data = [df.columns.tolist()] + df.values.tolist()

    style = TableStyle([ ('GRID', (0, 0), (-1, -1), 1, 'BLACK'),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ])

    table = Table(table_data, style=style)

    pdf.build([table])

    buffer.seek(0)
    return buffer

col4, col5 = st.columns((2))
with col4:
    name = 'Total Property:'
    age = total_properties_covered
    st.subheader( (f" {name} {age}"))
    st.dataframe(result)
    
    
    pdf_buffer = df_to_pdf(result)
    csv = result.to_csv(index = False).encode('utf-8')
    
    col1, col2,col3 = st.columns(3)
    with col1:
        st.download_button(label="Download PDF", data=pdf_buffer, file_name="dataframe.pdf", mime="application/pdf",key=14)  
    with col2:
        st.download_button(label="Download CSV ",data =csv,file_name="Property.csv",mime="text/csv",key=0)
    with col3:
        st.write('') 

with col5:
    name1 = 'District/Colony:'
    age1 = total_properties_covered1
    st.subheader( (f" {name1} "))
    st.dataframe(result1)

    pdf_buffer1 = df_to_pdf(result1)
    
    csv1 = result1.to_csv(index = False).encode('utf-8')
    
    col1, col2,col3 = st.columns(3)
    with col1:
            st.download_button(label="Download PDF", data=pdf_buffer1, file_name="dataframe.pdf", mime="application/pdf",key=13)
    with col2:
            st.download_button(label=" Download CSV ",data =csv1,file_name="Property.csv",mime="text/csv",key=1)
    with col3:
        st.write('') 

col6, col7 = st.columns((2))
with col6:
    name2 = 'Vendor/Colony:'
    age2 = total_properties_covered2
    st.subheader( (f" {name2} "))
    st.dataframe(result2)
    
    pdf_buffer2 = df_to_pdf(result2)
    csv2 = result3.to_csv(index = False).encode('utf-8')
    
    col1, col2,col3 = st.columns(3)
    with col1:
            st.download_button(label="Download PDF", data=pdf_buffer2, file_name="dataframe.pdf", mime="application/pdf",key=12)
    with col2:
        st.download_button(label="Download CSV ",data =csv2,file_name="Property.csv",mime="text/csv",key=2)
    with col3:
        st.write('') 

with col7:
    name3 = 'Colony/Vendor:'
    age3 = total_properties_covered3
    st.subheader( (f" {name3} "))
    st.dataframe(result3)
    
    pdf_buffer3 = df_to_pdf(result3)
    csv3 = result4.to_csv(index = False).encode('utf-8')
    
    col1, col2,col3 = st.columns(3)
    with col1:
            st.download_button(label="Download PDF", data=pdf_buffer3, file_name="dataframe.pdf", mime="application/pdf",key=11) 
    with col2:
        st.download_button(label="Download CSV ",data =csv3,file_name="Property.csv",mime="text/csv",key=3)
    with col3:
        st.write('')    

col8, col9 = st.columns((2))
    
with col8:

    name4= 'Phone no wise:'
    age4 = total_properties_covered4
    st.subheader( (f" {name4} "))
    st.dataframe(result4)
    
    pdf_buffer4 = df_to_pdf(result4)
    
    csv4 = result5.to_csv(index = False).encode('utf-8')
    
    col1, col2,col3 = st.columns(3)
    with col1:
        st.download_button(label="Download PDF", data=pdf_buffer4, file_name="dataframe.pdf", mime="application/pdf",key=9)   
    with col2:
        st.download_button(label="Download CSV ",data =csv4,file_name="Property.csv",mime="text/csv",key=4)
    with col3:
        st.write('') 
with col9:
    name5 = 'Colonies wise:'
    age5 = total_properties_covered5
    st.subheader( (f" {name5} "))
    st.dataframe(result5)
    
    pdf_buffer5 = df_to_pdf(result5)
    
    csv5 = result5.to_csv(index = False).encode('utf-8')

    col1, col2,col3 = st.columns(3)
    with col1:
            st.download_button(label="Download PDF", data=pdf_buffer5, file_name="dataframe.pdf", mime="application/pdf",key=10)
    with col2:
        st.download_button(label=" Download CSV ",data =csv5,file_name="Property.csv",mime="text/csv",key=5) 
    with col3:
        st.write('') 
