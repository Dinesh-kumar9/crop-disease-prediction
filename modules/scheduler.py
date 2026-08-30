
def get_farming_schedule(crop_stage, disease_status, weather_forecast):
    """
    Generates a farming schedule based on inputs.
    
    Args:
        crop_stage (str): e.g., "Vegetative", "Flowering", "Fruiting"
        disease_status (str): e.g., "Healthy", "Early_blight"
        weather_forecast (list): List of daily weather dicts
        
    Returns:
        list: List of dicts containing {date, action, reason}
    """
    schedule = []

    # Get today's weather (first item in forecast) with safety check
    today_weather = weather_forecast[0] if weather_forecast and len(weather_forecast) > 0 else {}
    is_raining = "Rain" in today_weather.get("weather", "")

    # --- 1. Disease Management ---
    if disease_status != "Healthy":
        # Clean disease name: remove underscores and format properly
        clean_disease = disease_status.replace("_", " ")
        
        action = {
            "date": "Today",
            "task": f"Treat {clean_disease}",
            "details": f"Detected {clean_disease}. Consult advisory.",
            "icon": "⚠️"
        }
        
        if is_raining:
            action["details"] += " NOTE: Rain expected. Delay chemical application."
            action["task"] += " (DELAYED)"
            
        schedule.append(action)

    # --- 2. Irrigation Logic ---
    irrigation_needed = False
    
    if crop_stage in ["Vegetative", "Fruiting"]:
        irrigation_needed = True # These stages need more water
    
    if is_raining:
        schedule.append({
            "date": "Today",
            "task": "Skip Irrigation",
            "details": "Rain is expected. Save water and prevent waterlogging.",
            "icon": "🌧️"
        })
    elif irrigation_needed:
        schedule.append({
            "date": "Today",
            "task": "Irrigate Crop",
            "details": f"Crop is in {crop_stage} stage and needs moisture.",
            "icon": "💧"
        })

    # --- 3. Stage-Specific Nutrient Management ---
    if crop_stage == "Vegetative":
        schedule.append({
            "date": "Tomorrow",
            "task": "Apply Nitrogen",
            "details": "Promotes leaf growth.",
            "icon": "🌿"
        })
    elif crop_stage == "Flowering":
        schedule.append({
            "date": "Tomorrow",
            "task": "Apply Potassium/Phosphorus",
            "details": "Supports flower retention and fruit set.",
            "icon": "🌸"
        })

    return schedule
