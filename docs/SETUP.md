# Setup Instructions: Intelligent Weather-Based Crop Scheduling Assistant

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get OpenWeatherMap API Key
1. Visit [https://openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to API Keys section
4. Copy your API key

### 3. Configure API Key
You have two options:

**Option A: Environment Variable (Recommended)**
```bash
# Windows (PowerShell)
$env:OWM_API_KEY="your_api_key_here"

# Windows (CMD)
set OWM_API_KEY=your_api_key_here

# Linux/Mac
export OWM_API_KEY="your_api_key_here"
```

**Option B: Direct Edit**
Edit `modules/weather.py` and replace:
```python
API_KEY = os.getenv("OWM_API_KEY", "YOUR_API_KEY_HERE")
```
with:
```python
API_KEY = "your_actual_api_key_here"
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## Usage
1. Select crop type (currently only Tomato is supported)
2. Enter your city name for weather data
3. Upload a clear image of the crop leaf
4. Click "Analyze Crop"
5. View the dashboard with:
   - Disease detection results
   - Growth stage (currently simulated)
   - 5-day weather forecast
   - Recommended farming schedule

## Troubleshooting

### "API Key not set" Error
- Make sure you've set the `OWM_API_KEY` environment variable or edited `modules/weather.py`

### "City not found" Error
- Check the spelling of your city name
- Try using a larger nearby city

### Model Loading Error
- Ensure `tomato_multiclass_model.h5` exists in the project root
- If missing, you need to train the model using `train.py`

## Next Steps
To enable real growth stage detection:
1. Collect/label images for different growth stages
2. Train a new model using the training script
3. Replace the placeholder in `modules/growth_stage.py`
