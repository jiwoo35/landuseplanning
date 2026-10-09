import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Tallahassee Leon County Scenario Dashboard", layout="wide"
)

st.title("Tallahassee Leon County Urban Planning Scenario Dashboard")
st.write(
    "Adjust the slider to view, in the impact on water quality, traffic, and taxes resulting from changes in the number of housing units developed in the northern area."
)

# 1. Side-bar / Slider Set-up
st.sidebar.header("Features")

# Feature 1: Housing Supply in North 
housing_north = st.sidebar.slider(
    "1. Housing Supply in North",
    min_value=0,
    max_value=23000,
    value=23000,
    step=1000,
    help="New housing supply in Lake Jackson North",
)

# Feature 2: Septic Tank Sewer Conversion Rate
default_conversion = 100 if housing_north > 0 else 0
septic_conversion = st.sidebar.slider(
    "2. Septic Conversion Ratio (%)",
    min_value=0,
    max_value=100,
    value=default_conversion,
    step=10,
    help="Rate of replacing aging septic tanks to the sewer system (among 2000 units) (%)",
)

# Feature 3: Public Subsidy for Sewer Infrastructure
default_subsidy = 5000000 if housing_north > 0 else 15000000
public_subsidy = st.sidebar.slider(
    "3. Public Subsidy ($)",
    min_value=0,
    max_value=20000000,
    value=default_subsidy,
    step=1000000,
    format="$%d",
    help="Public subsidy budget allocated by local governments for the construction of new sewer pipes ($)",
)

# Feature 4: VPH per house - Traffic Factor
vph_per_house = st.sidebar.slider(
    "4. Traffic Congestion (VPH per house)",
    min_value=0.4,
    max_value=1.2,
    value=0.8,
    step=0.1,
    help="Peak-hour passenger car trip generation per household based on public transport and mobility policies",
)

# Feature 5: Property Tax Rate
property_tax = (
    st.sidebar.slider(
        "5. Property Tax Rate (%)",
        min_value=1.0,
        max_value=2.5,
        value=1.6,
        step=0.1,
        help="Property tax rates applied to rising housing prices (%)",
    )
    / 100.0
)

# 2. Formula
total_demand = 23000
sprawl_south = total_demand - housing_north

# Traffic Congestion & Road Expansion
new_traffic = sprawl_south * 0.8 * 0.2
total_traffic = 1500 + new_traffic
road_cost = sprawl_south * 5000

# P-Load & Water Quality
impervious_area = housing_north * 0.2
old_septic_count = 2000
replaced_septic = old_septic_count * (septic_conversion / 100.0)
unreplaced_septic = old_septic_count * (1.0-(septic_conversion / 100.0))

septic_load = (replaced_septic * 0.5) + (unreplaced_septic * 4.0)
runoff_load = impervious_area * 2
total_p_load = septic_load + runoff_load
water_quality = max(0, 100 - (total_p_load * 0.01))

# Infrastructure Budget
sewer_cost = (total_demand * 2000) + public_subsidy
stormwater_cost = (housing_north * 2000) + (sprawl_south * 1000)
total_infra_budget = road_cost + sewer_cost + stormwater_cost

# Housing Price & Tax Burden
avg_house_price = 350000
new_housing_price = avg_house_price * (1 + 0.05 * (sprawl_south / 1000))
tax_house_price = (new_housing_price - avg_house_price ) * property_tax
tax_infra_bond = (total_infra_budget * 0.5) / 25 / 115000
taxpayer_burden = tax_house_price + tax_infra_bond

# 3. Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Lake Jackson Water Quality", f"{water_quality:.0f}/100")
col2.metric("Annual Tax Increase", f"${taxpayer_burden:,.0f}")
col3.metric("Traffic Congestion (VPH)", f"{total_traffic:,.0f} VPH")
col4.metric("Infrastructure Budget", f"${total_infra_budget:,.0f}")

st.markdown("---")

# 4. Visualization
col_left, col_right = st.columns(2)

with col_left:
    fig_wqi = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=water_quality,
            title={"text": "Lake Jackson Water Quality Index (WQI)"},
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 40], "color": "lightcoral"},
                    {"range": [40, 70], "color": "khaki"},
                    {"range": [70, 100], "color": "lightgreen"},
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 30,
                },
            },
        )
    )
    st.plotly_chart(fig_wqi, use_container_width=True)

with col_right:
    fig_budget = go.Figure(
        data=[
            go.Bar(name="Road Expansion Cost", x=["Infrastructure Budget"], y=[road_cost]),
            go.Bar(name="Sewerage Maintenance Cost", x=["Infrastructure Budget"], y=[sewer_cost]),
            go.Bar(name="Stormwater Maintenance Cost", x=["Infrastructure Budget"], y=[stormwater_cost]),
            ]
        )
    fig_budget.update_layout(
        barmode="stack",
        title="Infrastructure Budget ($)",
        showlegend=True,
        )
    st.plotly_chart(fig_budget, use_container_width=True)