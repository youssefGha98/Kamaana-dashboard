import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Set page configuration
st.set_page_config(
    page_title="Kamaana Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load sales data
sales_df = pd.read_excel(
    "Ventes Produits 2024.xlsx",
    header=2,
    sheet_name="Total Ventes KAMAANA",
)
sales_df.columns = ["produit"] + sales_df.columns[1:].to_list()


# Define functions
def create_heatmap(data):
    fig = px.imshow(
        data.drop(columns=["TOTAL"]).set_index("produit").T,
        labels=dict(x="Product", y="Month", color="Sales"),
        x=data["produit"],
        y=[
            "Janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ],
    )
    fig.update_layout(
        title="Monthly Sales Heatmap",
        xaxis_title="Product",
        yaxis_title="Month",
        xaxis=dict(tickmode="linear"),
        yaxis=dict(tickmode="linear"),
        width=1000,
        height=700,
    )
    return fig


def make_donut(percentage, color):
    if color == "blue":
        chart_color = ["#29b5e8", "#155F7A"]
    elif color == "green":
        chart_color = ["#27AE60", "#12783D"]
    elif color == "orange":
        chart_color = ["#F39C12", "#875A12"]
    elif color == "red":
        chart_color = ["#E74C3C", "#781F16"]
    else:
        raise ValueError("Color must be one of 'blue', 'green', 'orange', or 'red'")

    source = pd.DataFrame(
        {
            "Topic": ["Remaining", "Percentage"],
            "% value": [100 - percentage, percentage],
        }
    )

    plot = (
        alt.Chart(source)
        .mark_arc(innerRadius=65, cornerRadius=25)
        .encode(
            theta="% value",
            color=alt.Color(
                "Topic:N",
                scale=alt.Scale(domain=["Remaining", "Percentage"], range=chart_color),
                legend=None,
            ),
        )
        .properties(width=180, height=180)
    )

    text = (
        alt.Chart(source)
        .mark_text(
            align="center",
            color=chart_color[0],
            font="Lato",
            fontSize=32,
            fontWeight=700,
            fontStyle="italic",
        )
        .encode(text=alt.value(f"{percentage} %"))
    )

    return plot + text


# Sidebar for month selection
months = [
    "Janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
]
selected_month = st.sidebar.selectbox("Select a month to display", months, index=0)

# Layout with three columns
col1, col2, col3 = st.columns((1.5, 4.5, 2), gap="medium")

# Main content in col2
with col2:
    st.plotly_chart(create_heatmap(sales_df))

# Prepare sales data for further processing
sales_df = sales_df.drop(["TOTAL"], axis=1)
df_long = sales_df.melt(id_vars=["produit"], var_name="Month", value_name="Sales")

# Top Sales section
with col3:
    st.markdown("#### Top Sales")
    st.dataframe(
        df_long[df_long["Month"] == selected_month],
        column_order=("produit", "Sales"),
        hide_index=True,
        width=None,
        column_config={
            "produit": st.column_config.TextColumn("produit"),
            "Sales": st.column_config.ProgressColumn(
                "Sales",
                format="%f",
                min_value=0,
                max_value=max(df_long.Sales),
            ),
        },
    )

# Product prices and costs data
data = {
    "Product": [
        "Curl Booster 150mL",
        "Gelée Mauve 200mL",
        "Gelée Mauve 100mL",
        "Gelée Jaune 200mL",
        "Gelée Jaune 100mL",
        "Selfcare Butter (Grenade)",
        "Hair Spray",
        "Mini Curly Care Box",
        "Serum",
    ],
    "prices": [38, 35, 20, 35, 25, 40, 30, 60, 30],
}
df_prices = pd.DataFrame(data).set_index("Product")
with st.expander("Edit the product prices :"):
    df_prices = st.data_editor(df_prices, num_rows="dynamic", use_container_width=True)

fixed_costs_data = {
    "Cost Type": [
        "Internet",
        "telephone",
        "Electricité et eau",
        "loyer bureau",
        "honoraires comptable",
        "impots mensuels",
        "frais bilan",
        "frais de deplacements",
    ],
    "Monthly Cost": [100, 50, 100, 500, 150, 100, 150, 150],
}
df_fixed_costs = pd.DataFrame(fixed_costs_data)
with st.expander("Edit the fixed costs :"):
    df_fixed_costs = st.data_editor(
        df_fixed_costs, num_rows="dynamic", use_container_width=True
    )

# Product components data
products = {
    "Gelée Mauve 100mL": {
        "Bouteille (flacon)": 0.417,
        "Pompe dispenser (egouteuse)": 0.522,
        "Etiquette collante": 0.5,
        "Emballage": 2,
        "sac expédition": 0.4,
        "carte": 0.75,
        "coût produit": 7.259,
    },
    "Gelée Mauve 200mL": {
        "Bouteille (flacon)": 0.69,
        "Pompe dispenser (egouteuse)": 0.522,
        "Etiquette collante": 0.816,
        "Emballage": 2.1,
        "sac expédition": 0.4,
        "carte": 0.75,
        "coût produit": 14.518,
    },
    "Gelée Jaune 100mL": {
        "Bouteille (flacon)": 0.417,
        "Pompe dispenser (egouteuse)": 0.522,
        "Etiquette collante": 0.5,
        "Emballage": 2,
        "sac expédition": 0.4,
        "carte": 0.75,
        "coût produit": 7.259,
    },
    "Gelée Jaune 200mL": {
        "Bouteille (flacon)": 0.69,
        "Pompe dispenser (egouteuse)": 0.522,
        "Etiquette collante": 0.816,
        "Emballage": 2.1,
        "sac expédition": 0.4,
        "carte": 0.75,
        "coût produit": 14.518,
    },
    "Serum": {
        "Bouteille (flacon)": 1.975,
        "Pompe dispenser (egouteuse)": 0.69,
        "Etiquette collante": 1.904,
        "Emballage": 0.41,
        "sac expédition": 2.1,
        "coût produit": 8.33,
    },
    "Selfcare Butter (Grenade)": {
        "pot": 1.964,
        "Etiquette collante": 0.37,
        "coût produit": 16.303,
    },
    "Hair Spray": {
        "Bouteille (flacon)": 0.714,
        "Pompe dispenser (egouteuse)": 1.012,
        "Etiquette collante": 0.816,
        "Emballage": 2.1,
        "sac expédition": 0.4,
        "carte": 0.75,
        "coût produit": 11.6025,
    },
    "Curl Booster 150mL": {
        "Bouteille (flacon)": 0.69,
        "Pompe dispenser (egouteuse)": 0.522,
        "Etiquette collante": 0.816,
        "coût produit": 16.2435,
    },
    "Mini Curly Care Box": {
        "prix unité gel": 8.698,
        "prx unité creme": 12.541,
        "prix petit pot chantilly": 1.83115,
        "emballage": 2.1,
        "carte": 0.75,
    },
}

# Convert the products dictionary to a DataFrame
products_df = pd.DataFrame(products).T

# Display editable DataFrame
with st.expander("Edit the product costs and prices below:"):
    edited_products_df = st.data_editor(
        products_df, num_rows="dynamic", use_container_width=True
    )
# Calcul du coût total de revient pour chaque produit
for product, details in products.items():
    total_cost = sum(details.get(component, 0) for component in details)
    products[product]["total_cost"] = total_cost

# Affichage des résultats
products_df = pd.DataFrame(products).transpose()
products_df = products_df.join(df_prices, how="inner")

products_df["marge_brute"] = products_df["prices"] - products_df["total_cost"]
products_df["marge_brute_%"] = products_df["marge_brute"] / products_df["prices"]

# Display editable DataFrame
with st.expander("Edit the product margins"):
    products_margins_df = st.data_editor(
        products_df[["marge_brute", "marge_brute_%"]],
        num_rows="dynamic",
        use_container_width=True,
    )

# Integrate sales data
sales_df = sales_df.set_index("produit")
combined_df = products_df.join(sales_df, how="inner")

# Monthly margins
with col1:
    st.markdown("#### Monthly margins")
    monthly_margin_df = pd.DataFrame(
        combined_df[selected_month] * combined_df["marge_brute"]
    )
    st.write(monthly_margin_df)
    total = round(monthly_margin_df.sum()[0])
    st.write(f"Total : {total}")

    total_fixed_costs = df_fixed_costs["Monthly Cost"].sum()
    st.write(f"Total Fixed Cost: {total_fixed_costs}")

    earnings_to_fixed_costs_ratio = total / total_fixed_costs

    earnings_to_fixed_costs_percentage = round(earnings_to_fixed_costs_ratio, 1) * 100
    color = "green" if earnings_to_fixed_costs_ratio > 1 else "red"
    donut_chart = make_donut(earnings_to_fixed_costs_percentage, color)
    st.altair_chart(donut_chart)
