import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Tallahassee Leon County Scenario Dashboard", layout="wide"
)

st.title("Tallahassee Leon County Urban Plannning Scenario Dashboard")
st.write(
    "Adjust the slider to view, in the impact on water quality, traffic, and taxes resulting from changes in the number of housing units developed in the northern area."
)

# 1. Side-bar / Slider Set-up
housing_north = st.slider(
    "Housing Supply in North",
    min_value=0,
    max_value=23000,
    value=23000,
    step=1000,
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
septic_load = 1000 if housing_north > 0 else 8000
runoff_load = impervious_area * 2
total_p_load = septic_load + runoff_load
water_quality = max(0, 100 - (total_p_load * 0.01))

# Infrastructure Budget
sewer_cost = (total_demand * 2000) + (
    5000000 if housing_north > 0 else 15000000
)
stormwater_cost = (housing_north * 2000) + (sprawl_south * 1000)
total_infra_budget = road_cost + sewer_cost + stormwater_cost

housing_price = 350000 * (1 + 0.05 * (sprawl_south / 1000))
tax_house_price = (housing_price - 350000) * 0.016
tax_infra_bond = (total_infra_budget * 0.5) / 25 / 115000
taxpayer_burden = tax_house_price + tax_infra_bond

# 3. Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Lake Jackson Water Quality", f"{water_quality:.0f}/100")
col2.metric("Annual Tax Increase", f"${taxpayer_burden:,.0f}")
col3.metric("Urban Sprawl", f"{sprawl_south:,} household")
col4.metric("Infrastructure Budget", f"${total_infra_budget:,.0f}")

# 4. Visualization
fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=water_quality,
        title={"text": "Lake Jackson Water Quality (WQI)"},
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
st.plotly_chart(fig, use_container_width=True)