"""
Kevin Gifford
Completed 5/9/2022
Housing Data Project

This program was built to create a visualization of housing data for the City of Cambridge. This was completed using a streamlit webpage.
The webpage displays a homepage with general information as well as a sidebar radio query list for the user to select from.
This list offers a property value map, property type map, and graphs option. Selecting any of these three will open the corresponding page.
the property value map allows the user to select a price range of properties from which to display data for.
The properties that fit this price range will be populated on a map. In addition, the user may choose to display the table format of their data.
The property type map allows the user to filter by type of property, this then populates the map.
Lastly, the graphs query allows the user a choice of two graphs, price changes and year built.
Price changes shows the difference in price from prior data to the current price of properties for a value range selected by the user.
The year built graph also enables the user to select a range of property values to view on the graph displaying the year in which they were built.
Both graphs display the data table of the user selected range.
"""

import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt

df_housing = pd.read_csv("property_database.csv")

# This asks the user to select which query they wish to display
selected_query = st.sidebar.radio("Please select your Query", ["Homepage", "Property Value Map", "Property Type Map", "Graphs"])

# This converts the names of two columns for ease of use
df_housing.rename(columns={"Longitude":"lon", "Latitude":"lat"}, inplace = True)
df_housing = df_housing.dropna(subset=["lon", "lat"])

# This is a general homepage that is opened by default and give background information for the project
if selected_query == "Homepage":
    st.title("Interactive Cambridge Housing Data")
    st.write("by Kevin Gifford")
    st.image('cambridge.jpg')
    """Cambridge is a city in the state of Massachusetts across the Charles River from downtown Boston. Notable points of interest in Cambridge include Harvard University and MIT. Cambridge is also known for expensive real estate prices."""
    
    st.text("By selecting a query along the left column of the page you can choose different \nvisualizations of housing data for the city of Cambridge.")


# This defined function is what displays all maps in the project
def display_map(df, tip):
    df = df.dropna()

    # This portion is the custom icon utilized to mark properties on the maps
    ICON_URL = "https://upload.wikimedia.org/wikipedia/commons/7/71/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_House_%E2%80%93_Offices_%E2%80%93_Default.png"

    icon_data = {
        "url": ICON_URL,
        "width": 25,
        "height": 25,
        "anchorY": 100
        }

    df["icon_data"] = None
    for i in df.index:
        df["icon_data"][i] = icon_data

    icon_layer = pdk.Layer(type="IconLayer",
                           data = df,
                           get_icon="icon_data",
                           get_position='[lon,lat]',
                           get_size=4,
                           size_scale=10,
                           pickable=True)

    view_state = pdk.ViewState(
        latitude=df["lat"].mean(),
        longitude=df["lon"].mean(),
        zoom=12,
        pitch=0)

    # The following two tooltips display related data when the user hovers over one of the map icons
    if tip == 1:
        tool_tip = {"html": "Property Value and Address: (${AssessedValue}) - {Address}",
                    "style": { "backgroundColor": "white",
                                "color": "steelblue"}
                  }
    if tip == 2:
        tool_tip = {"html": "Property Type and Address: ({PropertyClass}) - {Address}",
                    "style": { "backgroundColor": "white",
                                "color": "steelblue"}
                  }
    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/navigation-day-v1',
        layers=[icon_layer],
        initial_view_state= view_state,
        tooltip= tool_tip)

    return st.pydeck_chart(map)


# This section displays the map tab
if selected_query == "Property Value Map":

    # This builds the dataframe of data for the following section
    sdf1 = df_housing.loc[:,["PID","Address","lon","lat","AssessedValue"]]

    # This section creates a slider for the user to filter properties by value
    st.title("Property Value Map")
    min_value = 100000
    max_value = 500000
    price = []
    price = st.slider('Select a range of values',1, 5000000, (min_value, max_value), step= 1000)
    st.write(f'The selected price range is: {price}')

    # This ensures that only the filtered properties are displayed
    sdf1 = sdf1[(sdf1["AssessedValue"] >= price[0]) & (sdf1["AssessedValue"] <= price[1])]
    sdf1.drop(sdf1.index[sdf1["AssessedValue"] == 0], inplace = True)

    # This is a map that will display the user's filtered properties
    display_map(sdf1, 1)

    # This section displays the table of user filtered properties
    show_table = st.checkbox("Show table")
    if show_table:
        st.write(f'Properties that fit your selected range:')
        st.write(sdf1)


# This section is for the property classification map
if selected_query == "Property Type Map":
    st.title("Property Type Map")
    sdf2 = df_housing.loc[:,["PID","Address","lon","lat","PropertyClass"]]

    # This lists out the different property type options
    property_types = ["Singlefamily", "Multifamily", "Condo", "Affordable Housing", "Non-Residential Commercial", "Nonprofit", "Governmental", "Education"]
    selection = st.selectbox('Select property type to display: ', property_types)

    # This consolidates similar and related property classifications to minimize options
    if selection == "Condo":
        sdf2 = sdf2[(sdf2["PropertyClass"] == "CONDOMINIUM") | (sdf2["PropertyClass"] =="CONDO-BLDG") | (sdf2["PropertyClass"] =="CNDO LUX") | (sdf2["PropertyClass"] =="CNDO-RES-PKG") | (sdf2["PropertyClass"] =="CONDO-PKG-SP") | (sdf2["PropertyClass"] =="MULTI UNIT CNDO") | (sdf2["PropertyClass"] =="MXD CONDOMINIUM")]
    elif selection == "Affordable Housing":
        sdf2 = sdf2[(sdf2["PropertyClass"] == "AFFORDABLE APT") | (sdf2["PropertyClass"] == "Housing Authority") | (sdf2["PropertyClass"] == "Housing, Other") | (sdf2["PropertyClass"] == "Improved City")]
    elif selection == "Non-Residential Commercial":
        sdf2 = sdf2[(sdf2["PropertyClass"] == "AUTO-REPAIR") | (sdf2["PropertyClass"] == "BANK") | (sdf2["PropertyClass"] == "CHILD-CARE") | (sdf2["PropertyClass"] == "CLEAN-MANUF") | (sdf2["PropertyClass"] == "EATING-ESTBL") | (sdf2["PropertyClass"] == "ELEC GEN PLANT") | (sdf2["PropertyClass"] == "ELECT-PLANT") | (sdf2["PropertyClass"] == "GAS-STATION") | (sdf2["PropertyClass"] == "GEN-OFFICE") | (sdf2["PropertyClass"] == "HIGH-TECH") | (sdf2["PropertyClass"] == "HOTEL") | (sdf2["PropertyClass"] == "IND-DEV-LAND") | (sdf2["PropertyClass"] == "INDUST-CONDO") | (sdf2["PropertyClass"] == "INN-RESORT") | (sdf2["PropertyClass"] == "INV-OFFICE") | (sdf2["PropertyClass"] == "MANUFACTURNG") | (sdf2["PropertyClass"] == "MEDICAL-OFFC") | (sdf2["PropertyClass"] == "MULTIUSE-COM") | (sdf2["PropertyClass"] == "MXD GEN-OFFICE") | (sdf2["PropertyClass"] == "MXD RES-LAND-IMP") | (sdf2["PropertyClass"] == "MXD RETAIL-STORE") | (sdf2["PropertyClass"] == "OFFICE-CONDO") | (sdf2["PropertyClass"] == "Other- Scientific") | (sdf2["PropertyClass"] == "PARKING-GAR") | (sdf2["PropertyClass"] == "PARKING-LOT") | (sdf2["PropertyClass"] == "RESRCH IND CND") | (sdf2["PropertyClass"] == "RETAIL-CONDO") | (sdf2["PropertyClass"] == "RETAIL-OFFIC") | (sdf2["PropertyClass"] == "RETAIL-STORE") | (sdf2["PropertyClass"] == "SH-CNTR/MALL") | (sdf2["PropertyClass"] == "SUPERMARKET") | (sdf2["PropertyClass"] == "WAREHOUSE")]
    elif selection == "Nonprofit":
        sdf2 = sdf2[(sdf2["PropertyClass"] == "Charitable Svc") | (sdf2["PropertyClass"] == "Church") | (sdf2["PropertyClass"] == "Other Charitable") | (sdf2["PropertyClass"] == "Rectory, Parsonage")]
    elif selection == "Governmental":
        sdf2 = sdf2[(sdf2["PropertyClass"] == "DCR- State Parks and Rec") | (sdf2["PropertyClass"] == "Hospitals") | (sdf2["PropertyClass"] == "Improved Local Edu") | (sdf2["PropertyClass"] == "Improved Public Safety") | (sdf2["PropertyClass"] == "Imprvd County Admin") | (sdf2["PropertyClass"] == "PUB UTIL REG") | (sdf2["PropertyClass"] == "TELE-EXCH-STA") | (sdf2["PropertyClass"] == "Transportation Authority") | (sdf2["PropertyClass"] == "US Government") | (sdf2["PropertyClass"] == "Utility Authority") | (sdf2["PropertyClass"] == "Vacant City") | (sdf2["PropertyClass"] == "Vacnt Transport Authorit")]
    elif selection == "Education":
        sdf2 = sdf2[(sdf2["PropertyClass"] == "DORM-RS-HALL") | (sdf2["PropertyClass"] == "FRAT-ORGANIZ") | (sdf2["PropertyClass"] == "FRAT-SORORTY") | (sdf2["PropertyClass"] == "Private College, University") | (sdf2["PropertyClass"] == "Private Elementary Education") | (sdf2["PropertyClass"] == "Private Secondary Education") | (sdf2["PropertyClass"] == "Vacant (Private Ed)") | (sdf2["PropertyClass"] == "Vacant Local Education")]
    elif selection == "Multifamily":
        sdf2 = sdf2[(sdf2["PropertyClass"] == "MULTIPLE-RES") | (sdf2["PropertyClass"] == "MULTIUSE-RES") | (sdf2["PropertyClass"] == "MULT-RES->8 APT") | (sdf2["PropertyClass"] == "MULT-RES-1FAM") | (sdf2["PropertyClass"] == "MULT-RES-2FAM") | (sdf2["PropertyClass"] == "MULT-RES-3FAM") | (sdf2["PropertyClass"] == "MULT-RES-4-8-APT") | (sdf2["PropertyClass"] == "MXD 4-8-UNIT-APT") | (sdf2["PropertyClass"] == "MXD TWO-FAM-RES") | (sdf2["PropertyClass"] == "Other") | (sdf2["PropertyClass"] == "Other Open Space") | (sdf2["PropertyClass"] == "PropertyClass") | (sdf2["PropertyClass"] == "RES LND-IMP PT DEV") | (sdf2["PropertyClass"] == "RES LND-IMP UNDEV") | (sdf2["PropertyClass"] == "RES-&-DEV-FC") | (sdf2["PropertyClass"] == "RES-DEV-LAND") | (sdf2["PropertyClass"] == "RES-UDV-LAND") | (sdf2["PropertyClass"] == "RES-UDV-PARK LND") | (sdf2["PropertyClass"] == "THREE-FM-RES") | (sdf2["PropertyClass"] == "TWO-FAM-RES") | (sdf2["PropertyClass"] == ">8-UNIT-APT") | (sdf2["PropertyClass"] =="4-8-UNIT-APT")]
    elif selection == "Singlefamily":
        sdf2 = sdf2[(sdf2["PropertyClass"] == "SINGLE FAM W/AUXILIARY APT") | (sdf2["PropertyClass"] == "SNGL-FAM-RES")]

    # This is a map that will display the user's filtered properties
    display_map(sdf2, 2)

    # This section displays the table of user filtered properties
    show_table2 = st.checkbox("Show table")
    if show_table2:
        st.write(f'Properties that fit your selected range:')
        st.write(sdf2)

if selected_query == "Graphs":
    st.title("Data Graphs")

    # This is where the user selects which graph they wish to display
    selected_graph = st.radio("Pick a graph", ["Price Changes", "Year Built"])

    # This functions similarly to the other queries by creating a slider based upon property value
    min_value2 = 100000
    max_value2 = 500000
    price = []
    price = st.slider('Select a range of values',1, 5000000, (min_value2, max_value2), step= 1000)
    st.write(f'The selected price range is: {price}')
    sdf3 = df_housing.loc[:,["PID","Address","lon","lat","AssessedValue", "Condition_YearBuilt", "PreviousAssessedValue"]]

    # This graph displays the price changes of properties
    if selected_graph == "Price Changes":
        st.write(f'Properties that fit your selected range:')

        # This collects all the properties within the user's range and calculates the percentage change in value
        sdf3 = sdf3[(sdf3["PreviousAssessedValue"] >= price[0]) & (sdf3["PreviousAssessedValue"] <= price[1])]
        sdf3 = sdf3[(sdf3["AssessedValue"] >= price[0]) & (sdf3["AssessedValue"] <= price[1])]
        sdf3.drop(sdf3.index[sdf3["PreviousAssessedValue"] == 0], inplace = True)
        sdf3.drop(sdf3.index[sdf3["AssessedValue"] == 0], inplace = True)
        price_change = (sdf3["AssessedValue"] / sdf3["PreviousAssessedValue"] -1) * 100
        sdf3["Percentage_Change"] = price_change
        sdf3.sort_values(["Percentage_Change"],
                        axis=0,
                        ascending=[True],
                        inplace=True)
        sdf3 = sdf3.dropna()

        sdf3_2 = sdf3.loc[:,["AssessedValue", "PreviousAssessedValue"]]
        sdf3_3 = sdf3.loc[:,["Address", "Percentage_Change"]]

        st.header("Difference in Price")
        st.area_chart(sdf3_2)
        st.write(sdf3_3["Percentage_Change"])

    # This is the option for the year of construction graph
    if selected_graph == "Year Built":
        st.header("Construction Year of Properties in Price Range")

        # A similarly selected data subset is created by the user's price range
        sdf3 = sdf3[(sdf3["AssessedValue"] >= price[0]) & (sdf3["AssessedValue"] <= price[1])]
        sdf3_4 = sdf3.loc[:,["Condition_YearBuilt"]]
        sdf3_4.drop(sdf3_4.index[sdf3_4["Condition_YearBuilt"] == 0], inplace = True)
        sdf3_4.sort_values(["Condition_YearBuilt"],
                        axis=0,
                        ascending=[True],
                        inplace=True)
        new_df = sdf3_4
        new_df.reset_index()
        year = list(new_df["Condition_YearBuilt"])

        # The year built is displayed on a dynamically scaling graph allowing the user to view the general period of when properties were built
        fig = plt.figure(figsize=(7,3))
        ax = plt.axes()

        ax.plot(year)
        plt.gcf().autofmt_xdate()
        st.pyplot(fig)
        st.write(new_df)

