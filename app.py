import numpy as np
import pandas as pd
import pickle
import streamlit as sc

sc.set_page_config(
    page_title="Construction Cost Predictor",
    page_icon="🏗️",
    layout="wide"
)

sc.markdown("""
<style>

/* Main Background */
.stApp{
    background: linear-gradient(135deg,#edf5ff,#f7f3ff);
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0f172a,#1e3a8a);
}

/* Sidebar text */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span{
    color:white !important;
    font-weight:600;
}

/* Main Title */
h1{
    text-align:center;
    color:#111827;
    font-size:55px !important;
    font-weight:800 !important;
}

/* Predict Button */
div.stButton > button{
    width:100%;
    background:linear-gradient(90deg,#2563eb,#1d4ed8);
    color:white;
    border:none;
    border-radius:12px;
    height:55px;
    font-size:22px;
    font-weight:bold;
}

div.stButton > button:hover{
    background:linear-gradient(90deg,#1d4ed8,#1e40af);
    color:white;
    transform:scale(1.03);
}

/* White Card */
.card{
    background:white;
    padding:25px;
    border-radius:18px;
    box-shadow:0px 8px 25px rgba(0,0,0,.15);
    margin-top:20px;
}

/* Blue Result Box */
.result{
    background:linear-gradient(135deg,#3b82f6,#2563eb);
    color:white;
    text-align:center;
    padding:30px;
    border-radius:20px;
    box-shadow:0px 10px 25px rgba(37,99,235,.4);
    font-size:32px;
    font-weight:bold;
    margin-top:20px;
}
        
</style>
""", unsafe_allow_html=True)


sc.title("Total_cost of Construction")

pipe=pickle.load(open("pipe.pkl","rb+"))
df=pd.read_csv("Cleaned_data.csv")

Project_ID=sorted(df['Project_ID'].unique())
Project_ID = sc.sidebar.selectbox("Select Project_ID", Project_ID)

Project_Type = sc.sidebar.selectbox("Select Project_Type", ["Residential", "Industrial","Commercial"])

Location = sorted(df['Location'].unique())
Location = sc.sidebar.selectbox("Select Location",Location)

Area_sqft = sc.sidebar.slider("Area (sq.ft)",int(df["Area_sqft"].min()),int(df["Area_sqft"].max()),1500)

Floors = sc.sidebar.slider("Number of Floors",int(df["Floors"].min()),int(df["Floors"].max()),2)

Material_Quality = sc.sidebar.radio("Material Quality",sorted(df["Material_Quality"].unique()))

Labor_Cost = sc.sidebar.number_input("Labor Cost (₹)",min_value=float(df["Labor_Cost"].min()),max_value=float(df["Labor_Cost"].max()),value=float(df["Labor_Cost"].mean()))

Material_Cost = sc.sidebar.number_input("Material Cost (₹)",min_value=int(df["Material_Cost"].min()),max_value=int(df["Material_Cost"].max()),value=int(df["Material_Cost"].mean()))

Equipment_Cost = sc.sidebar.number_input("Equipment Cost (₹)",min_value=int(df["Equipment_Cost"].min()),max_value=int(df["Equipment_Cost"].max()),value=int(df["Equipment_Cost"].mean()))

Duration_Months = sc.sidebar.slider("Project Duration (Months)",int(df["Duration_Months"].min()),int(df["Duration_Months"].max()),12)

Contractor_Experience = sc.sidebar.slider("Contractor Experience (Years)",int(df["Contractor_Experience"].min()),int(df["Contractor_Experience"].max()),10)

Inflation_Rate = sc.sidebar.slider("Inflation Rate (%)",float(df["Inflation_Rate"].min()),float(df["Inflation_Rate"].max()),float(df["Inflation_Rate"].mean()),step=0.1)

Weather_Delay_Days = sc.sidebar.slider("Weather Delay (Days)",int(df["Weather_Delay_Days"].min()),int(df["Weather_Delay_Days"].max()),5)


if sc.sidebar.button("Predict Cost"):
    sc.markdown("<div class='selected-box'>",unsafe_allow_html=True)
    sc.subheader("📋 You Selected")
    col1,col2= sc.columns(2)

    with col1:
        sc.write(f"Project_ID: {Project_ID}") 
        sc.write(f"Project_Type: {Project_Type}")
        sc.write(f"Location: {Location}")
        sc.write(f"Area_sqft: {Area_sqft}")
        sc.write(f"Floors: {Floors}")
        sc.write(f"Material_Quality: {Material_Quality}")
        sc.write(f"Labor_Cost: {Labor_Cost}")

    with col2:
        sc.write(f"Material_Cost: {Material_Cost}")
        sc.write(f"Equipment_Cost: {Equipment_Cost}")
        sc.write(f"Duration_Months: {Duration_Months}")
        sc.write(f"Contractor_Experience: {Contractor_Experience}")
        sc.write(f"Inflation_Rate: {Inflation_Rate}")
        sc.write(f"Weather_Delay_Days: {Weather_Delay_Days}")

        sc.markdown("</div>",unsafe_allow_html=True)

    #check for user input
    myinput = [[Project_ID,Project_Type,Location,Area_sqft,Floors,Material_Quality,Labor_Cost,Material_Cost,Equipment_Cost,Duration_Months,Contractor_Experience,Inflation_Rate,Weather_Delay_Days]]
    columns = ['Project_ID', 'Project_Type', 'Location', 'Area_sqft', 'Floors',
       'Material_Quality', 'Labor_Cost', 'Material_Cost', 'Equipment_Cost',
       'Duration_Months', 'Contractor_Experience', 'Inflation_Rate',
       'Weather_Delay_Days']
    myinput = pd.DataFrame(data = myinput, columns = columns)
    result = pipe.predict(myinput)

    if result[0,0] < 0:
        sc.write("Sorry, the predicted Toatal_cost is negative. Please check your input values.")
    else:
            sc.toast("Prediction Completed Successfully! 🎉", icon="🏗️")
            sc.balloons()
            sc.markdown(f"""<div class="result-box">
            <h2 style="text-align:center;">🏗️ Estimated Total Cost of Construction</h2>
            <h1>₹ {round(result[0,0]):,}</h1>
            </div>
              """, unsafe_allow_html=True)