"""
Agri-Economic Intelligence Module
Innovation: Estimates yield, market prices, and financial impact of diseases.
"""

import random

# Base Market Prices (₹ per kg) - Mock realtime data
MARKET_PRICES = {
    "tomato": {"min": 25, "max": 60, "trend": "rising"},
    "banana": {"min": 30, "max": 50, "trend": "stable"},
    "chilli": {"min": 150, "max": 250, "trend": "falling"},
}

# Yield Estimates (Tons per acre)
YIELD_PER_ACRE = {
    "tomato": 25,
    "banana": 30,
    "chilli": 4,
}

# Economic Impact of Diseases (Percentage Loss)
DISEASE_LOSS_IMPACT = {
    "Healthy": 0,
    "Early_blight": 15,    # Mild loss
    "Late_blight": 30,     # Severe loss
    "Leaf_Miner": 10,
    "Magnesium_Deficiency": 12,
    "Nitrogen_Deficiency": 20, # Stunted growth
    "Potassium_Deficiency": 15,
    "Spotted_Wilt_Virus": 50,  # Devastating
    "Yellow_Leaf_Curl_Virus": 40,
    "Mosaic_Virus": 35,
    # --- ADDED BANANA DISEASES ---
    "healthy": 0,
    "cordana": 20,           # Moderate leaf damage
    "sigatoka": 40,          # Severe leaf damage
    "pestalotiopsis": 25,    # Fungal infection

}

def get_market_data(crop, city):
    """
    Simulates fetching real-time market price for a city.
    Innovation: Location-based price intelligence.
    """
    crop = crop.lower()
    base = MARKET_PRICES.get(crop, {"min": 30, "max": 40, "trend": "stable"})
    
    # Simulate slight regional variation based on city name length (deterministic randomness)
    variation = len(city) % 5 
    
    current_price = base["max"] - variation
    return {
        "price": current_price,
        "trend": base["trend"],
        "unit": "kg"
    }

def calculate_economics(crop, disease_status, market_data):
    """
    Calculates detailed economic analysis.
    Innovation: Quantifies disease impact in financial terms.
    """
    crop = crop.lower()
    base_yield = YIELD_PER_ACRE.get(crop, 20) # Tons
    price_per_ton = market_data["price"] * 1000
    
    # Calculate Loss
    loss_percent = DISEASE_LOSS_IMPACT.get(disease_status, 10)
    actual_yield = base_yield * (1 - (loss_percent / 100))
    
    # Financials
    potential_revenue = base_yield * price_per_ton
    actual_revenue = actual_yield * price_per_ton
    money_lost = potential_revenue - actual_revenue
    
    return {
        "yield_potential": round(base_yield, 1),
        "yield_expected": round(actual_yield, 1),
        "loss_percentage": loss_percent,
        "price_per_kg": market_data["price"],
        "potential_income": f"{potential_revenue:,.0f}",
        "expected_income": f"{actual_revenue:,.0f}",
        "loss_amount": f"{money_lost:,.0f}",
        "currency": "₹",
        "unit": "kg"
    }

def get_economic_advice(data, language="en"):
    """
    Generates business advice based on financials.
    """
    loss = int(data["loss_amount"].replace(",", ""))
    
    if loss == 0:
        return "Excellent! Your crop value is maximized. Plan for harvest."
    elif loss < 50000:
        return f"Minor financial risk. Treat immediately to save ₹{data['loss_amount']}."
    else:
        return f"CRITICAL: You are losing ₹{data['loss_amount']}! Immediate intervention needed."
