"""
NLP-Powered Multilingual Translation Module
Innovative feature: Automatic language detection and translation
"""

# Language mappings for Indian regions
REGION_LANGUAGE_MAP = {
    # Telangana (All Major Districts)
    "hyderabad": "te", "secunderabad": "te", "warangal": "te", "nizamabad": "te",
    "khammam": "te", "karimnagar": "te", "ramagundam": "te", "mahbubnagar": "te",
    "nalgonda": "te", "adilabad": "te", "suryapet": "te", "miryalaguda": "te",
    "jagtial": "te", "mancherial": "te", "nirmal": "te", "kamareddy": "te",
    "bhongir": "te", "siddipet": "te", "jangaon": "te", "medak": "te",
    
    # Andhra Pradesh (All Major Districts)
    "vijayawada": "te", "visakhapatnam": "te", "vizag": "te", "guntur": "te",
    "nellore": "te", "kurnool": "te", "kakinada": "te", "rajahmundry": "te",
    "tirupati": "te", "anantapur": "te", "kadapa": "te", "cuddapah": "te",
    "eluru": "te", "ongole": "te", "nandyal": "te", "machilipatnam": "te",
    "tenali": "te", "proddatur": "te", "chittoor": "te", "hindupur": "te",
    "bhimavaram": "te", "madanapalle": "te", "guntakal": "te", "dharmavaram": "te",
    "gudivada": "te", "narasaraopet": "te", "tadepalligudem": "te", "kavali": "te",
    "amaravati": "te", "chilakaluripet": "te", "rayadurg": "te", "sulurpeta": "te",
    "palakollu": "te", "venkatagiri": "te", "markapur": "te", "vinukonda": "te",
    
    # Karnataka
    "bangalore": "kn", "bengaluru": "kn", "mysore": "kn", "mangalore": "kn", "hubli": "kn",
    
    # Tamil Nadu
    "chennai": "ta", "coimbatore": "ta", "madurai": "ta", "salem": "ta", "trichy": "ta",
    
    # Maharashtra
    "mumbai": "mr", "pune": "mr", "nagpur": "mr", "nashik": "mr",
    
    # West Bengal
    "kolkata": "bn", "howrah": "bn", "durgapur": "bn",
    
    # Gujarat
    "ahmedabad": "gu", "surat": "gu", "vadodara": "gu",
    
    # Rajasthan
    "jaipur": "hi", "jodhpur": "hi", "udaipur": "hi",
    
    # Uttar Pradesh & North India
    "delhi": "hi", "lucknow": "hi", "kanpur": "hi", "agra": "hi", "varanasi": "hi",
    
    # Punjab
    "chandigarh": "pa", "ludhiana": "pa", "amritsar": "pa",
    
    # Kerala
    "kochi": "ml", "thiruvananthapuram": "ml", "kozhikode": "ml",
}

# Language names
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "हिंदी (Hindi)",
    "te": "తెలుగు (Telugu)",
    "ta": "தமிழ் (Tamil)",
    "kn": "ಕನ್ನಡ (Kannada)",
    "mr": "मराठी (Marathi)",
    "bn": "বাংলা (Bengali)",
    "gu": "ગુજરાતી (Gujarati)",
    "pa": "ਪੰਜਾਬੀ (Punjabi)",
    "ml": "മലയാളം (Malayalam)",
}

def detect_language_from_city(city):
    """
    Detects preferred language based on city location.
    Innovation: Automatic regional language detection.
    """
    city_lower = city.lower().strip()
    return REGION_LANGUAGE_MAP.get(city_lower, "en")

# Global translator instance (singleton pattern to avoid re-instantiation issues)
_translator_instance = None

def _get_translator():
    """
    Get or create a singleton Translator instance.
    This prevents caching issues from creating new Translator objects.
    """
    global _translator_instance
    if _translator_instance is None:
        try:
            from googletrans import Translator
            _translator_instance = Translator()
        except Exception as e:
            print(f"Failed to initialize Google Translator: {e}")
            _translator_instance = False  # Mark as failed
    return _translator_instance

def translate_text(text, target_lang="hi"):
    """
    Translates text to target language using Google Translate API.
    Falls back to predefined translations if API unavailable.
    """
    if target_lang == "en":
        return text
    
    translator = _get_translator()
    
    # If translator initialization failed or is unavailable, use fallback
    if translator is False:
        return get_fallback_translation(text, target_lang)
    
    try:
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        print(f"Translation API error: {e}. Using fallback.")
        return get_fallback_translation(text, target_lang)

def get_fallback_translation(text, lang):
    """
    Fallback translations for common farming terms.
    """
    # Common farming phrases in multiple languages
    translations = {
        "hi": {
            # Tasks
            "Irrigate Crop": "फसल की सिंचाई करें",
            "Apply Nitrogen": "नाइट्रोजन डालें",
            "Apply Potassium/Phosphorus": "पोटाशियम/फास्फोरस डालें",
            "Monitor Crop": "फसल की निगरानी करें",
            "Skip Irrigation": "सिंचाई न करें",
            "Apply Treatment": "उपचार लागू करें",
            "Treat": "उपचार करें",
            
            # Time words
            "Today": "आज",
            "Tomorrow": "कल",
            "Day": "दिन",
            
            # Common words
            "Detected": "पता चला",
            "Consult advisory": "सलाह लें",
            "DELAYED": "विलंबित",
            "NOTE": "नोट",
            
            # Details
            "Rain is expected": "बारिश की संभावना है",
            "Delay chemical application": "रासायनिक अनुप्रयोग में देरी करें",
            "Promotes leaf growth": "पत्तियों की वृद्धि को बढ़ावा देता है",
            "Supports flower retention": "फूलों को बनाए रखने में मदद करता है",
            "Supports flower retention and fruit set": "फूलों और फलों को बनाए रखने में मदद करता है",
            "Regular monitoring recommended": "नियमित निगरानी की सिफारिश की जाती है",
            "Crop is in": "फसल",
            "stage": "अवस्था में है",
            "stage and needs moisture": "अवस्था में है और नमी की जरूरत है",
            "Save water and prevent waterlogging": "पानी बचाएं और जलभराव से बचें",
            "Vegetative": "वनस्पति",
            "Flowering": "फूल आना",
            "Fruiting": "फल लगना",
            "Apply recommended fungicide": "अनुशंसित कवकनाशी लागू करें",
            "Follow treatment guidelines": "उपचार दिशानिर्देशों का पालन करें",
        },
        "te": {
            # Tasks
            "Irrigate Crop": "పంటకు నీరు పెట్టండి",
            "Apply Nitrogen": "నత్రజని వేయండి",
            "Apply Potassium/Phosphorus": "పొటాషియం/ఫాస్పరస్ వేయండి",
            "Monitor Crop": "పంటను పర్యవేక్షించండి",
            "Skip Irrigation": "నీరు పెట్టవద్దు",
            "Apply Treatment": "చికిత్స వేయండి",
            "Treat": "చికిత్స చేయండి",
            
            # Time words
            "Today": "ఈరోజు",
            "Tomorrow": "రేపు",
            "Day": "రోజు",
            
            # Common words
            "Detected": "గుర్తించబడింది",
            "Consult advisory": "సలహా తీసుకోండి",
            "DELAYED": "ఆలస్యం",
            "NOTE": "గమనిక",
            
            # Details
            "Rain is expected": "వర్షం అవకాశం ఉంది",
            "Delay chemical application": "రసాయన వినియోగాన్ని ఆలస్యం చేయండి",
            "Promotes leaf growth": "ఎదుగుదలకు సహాయపడుతుంది",
            "Supports flower retention": "పూల నిలుపుదలకు తోడ్పడుతుంది",
            "Supports flower retention and fruit set": "పూలు మరియు ఫలాల నిలుపుదలకు తోడ్పడుతుంది",
            "Regular monitoring recommended": "క్రమం తప్పకుండా పరిశీలించండి",
            "Crop is in": "పంట",
            "stage": "దశలో ఉంది",
            "stage and needs moisture": "దశలో ఉంది మరియు తేమ అవసరం",
            "Save water and prevent waterlogging": "నీటిని ఆదా చేయండి మరియు నీటి నిలుపుదలను నివారించండి",
            "Vegetative": "వృద్ధి దశ",
            "Flowering": "పూత దశ",
            "Fruiting": "ఫలాల దశ",
            "Apply recommended fungicide": "సిఫార్సు చేసిన శిలీంద్ర నాశిని వేయండి",
            "Follow treatment guidelines": "చికిత్స మార్గదర్శకాలను అనుసరించండి",
        },
        "ta": {
            # Tasks
            "Irrigate Crop": "பயிருக்கு நீர் பாய்ச்சவும்",
            "Apply Nitrogen": "நைட்ரஜன் இடவும்",
            "Apply Potassium/Phosphorus": "பொட்டாசியம்/பாஸ்பரஸ் இடவும்",
            "Monitor Crop": "பயிரை கண்காணிக்கவும்",
            "Skip Irrigation": "நீர் பாய்ச்ச வேண்டாம்",
            "Apply Treatment": "சிகிச்சை அளிக்கவும்",
            "Treat": "சிகிச்சை செய்யவும்",
            
            # Time words
            "Today": "இன்று",
            "Tomorrow": "நாளை",
            "Day": "நாள்",
            
            # Common words
            "Detected": "கண்டறியப்பட்டது",
            "Consult advisory": "ஆலோசனை பெறவும்",
            "DELAYED": "தாமதம்",
            "NOTE": "குறிப்பு",
            
            # Details
            "Rain is expected": "மழை எதிர்பார்க்கப்படுகிறது",
            "Delay chemical application": "இரசாயன பயன்பாட்டை தாமதப்படுத்தவும்",
            "Promotes leaf growth": "இலை வளர்ச்சியை ஊக்குவிக்கிறது",
            "Supports flower retention": "பூ தக்கவைப்பை ஆதரிக்கிறது",
            "Supports flower retention and fruit set": "பூ மற்றும் கனி தக்கவைப்பை ஆதரிக்கிறது",
            "Regular monitoring recommended": "வழக்கமான கண்காணிப்பு பரிந்துரைக்கப்படுகிறது",
            "Crop is in": "பயிர்",
            "stage": "நிலையில் உள்ளது",
            "stage and needs moisture": "நிலையில் உள்ளது மற்றும் ஈரப்பதம் தேவை",
            "Save water and prevent waterlogging": "தண்ணீரை சேமிக்கவும் மற்றும் நீர் தேங்குவதை தடுக்கவும்",
            "Vegetative": "தாவர வளர்ச்சி",
            "Flowering": "பூக்கும் நிலை",
            "Fruiting": "கனி நிலை",
            "Apply recommended fungicide": "பரிந்துரைக்கப்பட்ட பூஞ்சைக் கொல்லி இடவும்",
            "Follow treatment guidelines": "சிகிச்சை வழிகாட்டுதல்களைப் பின்பற்றவும்",
        },
        "kn": {
            # Tasks
            "Irrigate Crop": "ಬೆಳೆಗೆ ನೀರು ಹಾಕಿ",
            "Apply Nitrogen": "ಸಾರಜನಕ ಹಾಕಿ",
            "Apply Potassium/Phosphorus": "ಪೊಟ್ಯಾಸಿಯಮ್/ರಂಜಕ ಹಾಕಿ",
            "Monitor Crop": "ಬೆಳೆಯನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ",
            "Skip Irrigation": "ನೀರು ಹಾಕಬೇಡಿ",
            "Apply Treatment": "ಚಿಕಿತ್ಸೆ ನೀಡಿ",
            "Treat": "ಚಿಕಿತ್ಸೆ ಮಾಡಿ",
            
            # Time words
            "Today": "ಇಂದು",
            "Tomorrow": "ನಾಳೆ",
            "Day": "ದಿನ",
            
            # Common words
            "Detected": "ಪತ್ತೆಯಾಗಿದೆ",
            "Consult advisory": "ಸಲಹೆ ಪಡೆಯಿರಿ",
            "DELAYED": "ವಿಳಂಬ",
            "NOTE": "ಗಮನಿಸಿ",
            
            # Details
            "Rain is expected": "ಮಳೆ ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ",
            "Delay chemical application": "ರಾಸಾಯನಿಕ ಅನ್ವಯವನ್ನು ವಿಳಂಬಗೊಳಿಸಿ",
            "Promotes leaf growth": "ಎಲೆ ಬೆಳವಣಿಗೆಯನ್ನು ಉತ್ತೇಜಿಸುತ್ತದೆ",
            "Supports flower retention": "ಹೂವಿನ ಧಾರಣವನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ",
            "Supports flower retention and fruit set": "ಹೂವು ಮತ್ತು ಹಣ್ಣಿನ ಧಾರಣವನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ",
            "Regular monitoring recommended": "ನಿಯಮಿತ ಮೇಲ್ವಿಚಾರಣೆ ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ",
            "Crop is in": "ಬೆಳೆ",
            "stage": "ಹಂತದಲ್ಲಿದೆ",
            "stage and needs moisture": "ಹಂತದಲ್ಲಿದೆ ಮತ್ತು ತೇವಾಂಶ ಅಗತ್ಯವಿದೆ",
            "Save water and prevent waterlogging": "ನೀರನ್ನು ಉಳಿಸಿ ಮತ್ತು ನೀರು ನಿಲುಗಡೆಯನ್ನು ತಡೆಯಿರಿ",
            "Vegetative": "ಸಸ್ಯ ಬೆಳವಣಿಗೆ",
            "Flowering": "ಹೂಬಿಡುವ ಹಂತ",
            "Fruiting": "ಫಲ ಹಂತ",
            "Apply recommended fungicide": "ಶಿಫಾರಸು ಮಾಡಿದ ಶಿಲೀಂಧ್ರನಾಶಕವನ್ನು ಹಾಕಿ",
            "Follow treatment guidelines": "ಚಿಕಿತ್ಸಾ ಮಾರ್ಗಸೂಚಿಗಳನ್ನು ಅನುಸರಿಸಿ",
        },
    }
    
    # Try to find exact translation
    if lang in translations and text in translations[lang]:
        return translations[lang][text]
    
    # Try word-by-word translation for compound phrases
    if lang in translations:
        translated_text = text
        for key, value in translations[lang].items():
            if key in text:
                translated_text = translated_text.replace(key, value)
        if translated_text != text:  # Something was translated
            return translated_text
    
    return text  # Return original if no translation found

def translate_schedule(schedule, target_lang):
    """
    Translates entire farming schedule to target language.
    Innovation: Context-aware agricultural translation.
    """
    if target_lang == "en":
        return schedule
    
    translated_schedule = []
    for item in schedule:
        translated_item = {
            "date": item["date"],
            "task": translate_text(item["task"], target_lang),
            "details": translate_text(item["details"], target_lang),
            "icon": item["icon"]
        }
        translated_schedule.append(translated_item)
    
    return translated_schedule

def get_voice_enabled_html(text, lang="en"):
    """
    Innovation: Generates HTML with text-to-speech capability.
    Allows farmers to hear recommendations in their language.
    """
    # Language codes for speech synthesis
    voice_codes = {
        "en": "en-US",
        "hi": "hi-IN",
        "te": "te-IN",
        "ta": "ta-IN",
        "kn": "kn-IN",
        "mr": "mr-IN",
        "bn": "bn-IN",
        "gu": "gu-IN",
        "pa": "pa-IN",
        "ml": "ml-IN",
    }
    
    voice_code = voice_codes.get(lang, "en-US")
    
    return f'''
    <div class="voice-enabled">
        <button onclick="speakText('{text}', '{voice_code}')" class="voice-btn">
            🔊 Listen
        </button>
    </div>
    '''
