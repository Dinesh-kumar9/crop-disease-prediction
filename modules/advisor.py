"""
Disease Advisor Module
Innovation: Provides specific Chemical, Organic, and Cultural treatments for diseases.
"""

# Disease Treatment Database (Multilingual)
# English translations
DISEASE_TREATMENTS_EN = {
    "Healthy": {
        "description": "Your crop is healthy and growing well.",
        "chemical": ["No chemical treatment needed."],
        "organic": ["Maintain regular monitoring.", "Use neem oil as a preventive measure."],
        "cultural": ["Ensure proper spacing.", "Weed regularly to prevent pests."]
    },
    "Early_blight": {
        "description": "Fungal infection causing bullseye-shaped spots on leaves.",
        "chemical": ["Apply Chlorothalonil or Mancozeb fungicides.", "Spray Copper Oxychloride."],
        "organic": ["Spray Bicarbonate of Soda (Baking Soda) solution.", "Use Trichoderma harzianum."],
        "cultural": ["Remove infected leaves immediately.", "Avoid overhead irrigation.", "Rotate crops with non-solanaceous plants."]
    },
    "Late_blight": {
        "description": "Severe fungal disease causing dark lesions and white mold.",
        "chemical": ["Apply Metalaxyl + Mancozeb.", "Use Dimethomorph or Cymoxanil."],
        "organic": ["Copper-based organically approved fungicides.", "Compost tea sprays."],
        "cultural": ["Destroy all infected plants.", "Improve air circulation.", "Avoid wet foliage at night."]
    },
    "Leaf_Miner": {
        "description": "Larvae tunnel inside leaves creating white winding trails.",
        "chemical": ["Apply Abamectin or Spinosad.", "Use Cyantraniliprole."],
        "organic": ["Neem oil sprays.", "Introduce parasitic wasps (Diglyphus isaea)."],
        "cultural": ["Use yellow sticky traps.", "Remove mined leaves manually.", "Plow soil to expose pupae."]
    },
    "Magnesium_Deficiency": {
        "description": "Yellowing between leaf veins (interveinal chlorosis) on older leaves.",
        "chemical": ["Spray Magnesium Sulfate (Epsom Salt).", "Apply Magnesium Nitrate."],
        "organic": ["Dolomite Lime application to soil.", "Composted manure."],
        "cultural": ["Adjust soil pH (Magnesium unavailable in acidic soil).", "Avoid excessive potassium fertilizers."]
    },
    "Nitrogen_Deficiency": {
        "description": "Stunted growth and general yellowing of leaves.",
        "chemical": ["Apply Urea or Ammonium Nitrate.", "Foliar spray of NPK 19:19:19."],
        "organic": ["Apply Vermicompost or Cow Dung Manure.", "Use Fish Emulsion."],
        "cultural": ["Grow leguminous cover crops.", "Ensure adequate soil moisture for nutrient uptake."]
    },
    "Potassium_Deficiency": {
        "description": "Leaf edges turn yellow and brown (scorched appearance).",
        "chemical": ["Apply Murate of Potash (MOP).", "Spray Potassium Sulphate."],
        "organic": ["Wood ash application.", "Banana peel compost."],
        "cultural": ["Maintain soil moisture.", "Avoid high salinity soils."]
    },
    "Spotted_Wilt_Virus": {
        "description": "Viral disease transmitted by thrips causing bronzing and spots.",
        "chemical": ["Control Thrips vectors using Imidacloprid.", "Use Spinetoram."],
        "organic": ["Neem oil to repel thrips.", "Beauveria bassiana."],
        "cultural": ["Remove infected plants immediately (incurable).", "Control weeds.", "Use reflective mulches."]
    },
    "Yellow_Leaf_Curl_Virus": {
        "description": "Viral disease transmitted by whiteflies causing upward curling.",
        "chemical": ["Control Whiteflies using Acetamiprid or Diafenthiuron.", "Imidacloprid spray."],
        "organic": ["Neem oil.", "Sticky traps for whiteflies."],
        "cultural": ["Use virus-resistant varieties.", "Use insect-proof nets.", "Remove infected plants."]
    },
    "Mosaic_Virus": {
        "description": "Viral disease causing mottled light and dark green patterns.",
        "chemical": ["No chemical cure. Control aphids vectors using Dimethoate."],
        "organic": ["Spray milk (10% solution) to prevent spread.", "Neem oil for aphids."],
        "cultural": ["Wash hands and tools (tobacco users caution).", "Remove infected plants.", "Control aphids."]
    }
}

# Telugu translations
DISEASE_TREATMENTS_TE = {
    "Healthy": {
        "description": "మీ పంట ఆరోగ్యంగా మరియు బాగా పెరుగుతోంది.",
        "chemical": ["రసాయన చికిత్స అవసరం లేదు."],
        "organic": ["క్రమం తప్పకుండా పర్యవేక్షించండి.", "నివారణ చర్యగా వేప నూనె వాడండి."],
        "cultural": ["సరైన అంతరాన్ని నిర్వహించండి.", "పురుగులను నివారించడానికి క్రమం తప్పకుండా కలుపు తీయండి."]
    },
    "Early_blight": {
        "description": "ఆకులపై లక్ష్య ఆకారపు మచ్చలను కలిగించే శిలీంధ్ర సంక్రమణ.",
        "chemical": ["క్లోరోథలోనిల్ లేదా మాంకోజెబ్ శిలీంధ్రనాశినిని వాడండి.", "కాపర్ ఆక్సీక్లోరైడ్ స్ప్రే చేయండి."],
        "organic": ["బేకింగ్ సోడా ద్రావణాన్ని స్ప్రే చేయండి.", "ట్రైకోడెర్మా హార్జియానం వాడండి."],
        "cultural": ["సోకిన ఆకులను వెంటనే తొలగించండి.", "తలపై నీటి పారుదల నివారించండి.", "టొమాటోయేతర పంటలతో పంట మార్పిడి చేయండి."]
    },
    "Late_blight": {
        "description": "ముదురు గాయాలు మరియు తెల్ల బూజును కలిగించే తీవ్రమైన శిలీంధ్ర వ్యాధి.",
        "chemical": ["మెటలాక్సిల్ + మాంకోజెబ్ వాడండి.", "డైమిథోమార్ఫ్ లేదా సైమోక్సానిల్ వాడండి."],
        "organic": ["రాగి ఆధారిత సేంద్రీయ ఆమోదిత శిలీంధ్రనాశినిని వాడండి.", "కంపోస్ట్ టీ స్ప్రే చేయండి."],
        "cultural": ["సోకిన అన్ని మొక్కలను నాశనం చేయండి.", "గాలి ప్రసరణను మెరుగుపరచండి.", "రాత్రి సమయంలో ఆకులు తడిగా ఉండకుండా చూడండి."]
    },
    "Leaf_Miner": {
        "description": "లార్వా ఆకుల లోపల తెల్లని మెలితిరిగిన గీతలను సృష్టిస్తుంది.",
        "chemical": ["అబామెక్టిన్ లేదా స్పైనోసాడ్ వాడండి.", "సైయాంట్రానిలిప్రోల్ వాడండి."],
        "organic": ["వేప నూనె స్ప్రే చేయండి.", "పరాన్నజీవి కందిరీగలను (డిగ్లిఫస్ ఇసియా) వదలండి."],
        "cultural": ["పసుపు అంటుకునే ఉచ్చులు వాడండి.", "గని చేసిన ఆకులను చేతితో తొలగించండి.", "ప్యూపలను బహిర్గతం చేయడానికి నేలను దున్నండి."]
    },
    "Magnesium_Deficiency": {
        "description": "పాత ఆకులపై ఆకు సిరల మధ్య పసుపు రంగు (ఇంటర్వీనల్ క్లోరోసిస్).",
        "chemical": ["మెగ్నీషియం సల్ఫేట్ (ఎప్సమ్ ఉప్పు) స్ప్రే చేయండి.", "మెగ్నీషియం నైట్రేట్ వాడండి."],
        "organic": ["నేలకు డోలమైట్ లైమ్ వాడండి.", "కంపోస్ట్ చేసిన పేడ వాడండి."],
        "cultural": ["నేల pH సర్దుబాటు చేయండి (మెగ్నీషియం ఆమ్ల నేలలో అందుబాటులో ఉండదు).", "అధిక పొటాషియం ఎరువులను నివారించండి."]
    },
    "Nitrogen_Deficiency": {
        "description": "మొక్కల వృద్ధి నిలిచిపోవడం మరియు ఆకుల సాధారణ పసుపు రంగు.",
        "chemical": ["యూరియా లేదా అమ్మోనియం నైట్రేట్ వాడండి.", "NPK 19:19:19 ఆకుల స్ప్రే చేయండి."],
        "organic": ["వర్మీకంపోస్ట్ లేదా ఆవు పేడ పెట్టండి.", "చేపల ఎమల్షన్ వాడండి."],
        "cultural": ["పప్పు జాతి కవర్ పంటలు పండించండి.", "పోషక గ్రహణానికి తగినంత నేల తేమను నిర్వహించండి."]
    },
    "Potassium_Deficiency": {
        "description": "ఆకు అంచులు పసుపు మరియు గోధుమ రంగులోకి మారడం (కాలిన రూపం).",
        "chemical": ["మురేట్ ఆఫ్ పొటాష్ (MOP) వాడండి.", "పొటాషియం సల్ఫేట్ స్ప్రే చేయండి."],
        "organic": ["చెక్క బూడిద వాడండి.", "అరటి తొక్క కంపోస్ట్ వాడండి."],
        "cultural": ["నేల తేమను నిర్వహించండి.", "అధిక లవణత నేలలను నివారించండి."]
    },
    "Spotted_Wilt_Virus": {
        "description": "త్రిప్స్ ద్వారా వ్యాపించే వైరల్ వ్యాధి కాంస్యం మరియు మచ్చలను కలిగిస్తుంది.",
        "chemical": ["ఇమిడాక్లోప్రిడ్ ఉపయోగించి త్రిప్స్ వెక్టర్లను నియంత్రించండి.", "స్పైనెటోరామ్ వాడండి."],
        "organic": ["త్రిప్స్‌ను తప్పించడానికి వేప నూనె వాడండి.", "బ్యూవేరియా బాసియానా వాడండి."],
        "cultural": ["సోకిన మొక్కలను వెంటనే తొలగించండి (నయం చేయలేము).", "కలుపు మొక్కలను నియంత్రించండి.", "ప్రతిబింబ మల్చ్‌లను వాడండి."]
    },
    "Yellow_Leaf_Curl_Virus": {
        "description": "తెల్ల ఈగల ద్వారా వ్యాపించే వైరల్ వ్యాధి పైకి వంకరగా మారడం కలిగిస్తుంది.",
        "chemical": ["అసిటామిప్రిడ్ లేదా డయాఫెంథియురాన్ ఉపయోగించి తెల్ల ఈగలను నియంత్రించండి.", "ఇమిడాక్లోప్రిడ్ స్ప్రే చేయండి."],
        "organic": ["వేప నూనె వాడండి.", "తెల్ల ఈగల కోసం అంటుకునే ఉచ్చులు వాడండి."],
        "cultural": ["వైరస్-నిరోధక రకాలను వాడండి.", "కీటక-రుద్ధ వలలు వాడండి.", "సోకిన మొక్కలను తొలగించండి."]
    },
    "Mosaic_Virus": {
        "description": "మచ్చల లేత మరియు ముదురు ఆకుపచ్చ నమూనాలను కలిగించే వైరల్ వ్యాధి.",
        "chemical": ["రసాయన నివారణ లేదు. డైమిథోయేట్ ఉపయోగించి అఫిడ్ల వెక్టర్లను నియంత్రించండి."],
        "organic": ["వ్యాప్తిని నివారించడానికి పాలు (10% ద్రావణం) స్ప్రే చేయండి.", "అఫిడ్ల కోసం వేప నూనె వాడండి."],
        "cultural": ["చేతులు మరియు పనిముట్లు కడగండి (పొగాకు వినియోగదారులు జాగ్రత్త).", "సోకిన మొక్కలను తొలగించండి.", "అఫిడ్లను నియంత్రించండి."]
    },
    # --- ADDED BANANA DISEASES (Telugu) ---
    "healthy": {
        "description": "అరటి మొక్క ఆరోగ్యంగా ఉంది.",
        "chemical": ["మంచి నిర్వహణను కొనసాగించండి."],
        "organic": ["సేంద్రీయ ఎరువులు వాడండి."],
        "cultural": ["నిరంతర నీటిపారుదల లేనివ్వండి."]
    },
    "cordana": {
        "description": "కోర్డానా ఆకు మచ్చ - ఆకులపై లేత గోధుమ రంగు మచ్చలు.",
        "chemical": ["మాంకోజెబ్ (0.2%) లేదా ఇసాప్రోఫోస్ స్ప్రే చేయండి."],
        "organic": ["ట్రైకోడెర్మా విరిడి వాడండి.", "వేప నూనె స్ప్రే చేయండి."],
        "cultural": ["వ్యాధి సోకిన ఆకులను తొలగించండి.", "మొక్కల మధ్య తగినంత దూరం పాటించండి."]
    },
    "sigatoka": {
        "description": "సిగటోకా ఆకు మచ్చ తెగులు - ఆకులపై చిన్న, పొడవైన గోధుమ రంగు మచ్చలు.",
        "chemical": ["మాంకోజెబ్ (0.2%) లేదా ప్రొపికొనజోల్ (0.1%) స్ప్రే చేయండి.", "మినరల్ ఆయిల్ (1%) ద్రావణాన్ని పిచికారీ చేయండి."],
        "organic": ["బోర్డో మిశ్రమం (1%) స్ప్రే చేయండి.", "పంచగవ్య పద్ధతిని వాడండి."],
        "cultural": ["వ్యాధి సోకిన ఆకులను కత్తిరించి దూరంగా పారవేయండి.", "మొక్కల మధ్య గాలి వెలుతురు ఉండేలా దూరం పాటించండి."]
    },
    "pestalotiopsis": {
        "description": "పెస్టలోటియోప్సిస్ - ఆకులపై అక్రమ ఆకారపు మచ్చలు.",
        "chemical": ["కాపర్ ఆక్సీక్లోరైడ్ లేదా కార్బెండాజిమ్ స్ప్రే చేయండి."],
        "organic": ["నివారణకు వేప నూనె వాడండి."],
        "cultural": ["తడి వాతావరణంలో పంటను కాపాడండి.", "వ్యాధి సోకిన ఆకులను కాల్చివేయండి."]
    }
}

# Add English translations for Banana diseases to the main dictionary as well
DISEASE_TREATMENTS_EN.update({
    "healthy": {
        "description": "Your Banana plant is healthy.",
        "chemical": ["Maintain good irrigation."],
        "organic": ["Use compost regularly."],
        "cultural": ["Ensure proper drainage."]
    },
    "cordana": {
        "description": "Cordana Leaf Spot - pale brown oval spots on leaves.",
        "chemical": ["Apply Mancozeb or Isoprothiolane."],
        "organic": ["Trichoderma viride application.", "Neem oil spray."],
        "cultural": ["Remove infected leaves.", "Provide proper spacing."]
    },
    "sigatoka": {
        "description": "Black Sigatoka causes dark leaf spots and significant yield loss.",
        "chemical": ["Fungicides like Mancozeb or Propiconazole.", "Mineral oil sprays."],
        "organic": ["Copper-based fungicides.", "Bio-fungicides based on Bacillus subtilis."],
        "cultural": ["Remove infected leaves (de-leafing).", "Reduce planting density.", "Efficient drainage."]
    },
    "pestalotiopsis": {
        "description": "Pestalotiopsis - Irregular leaf spots and blight.",
        "chemical": ["Copper Oxychloride or Carbendazim sprays."],
        "organic": ["Neem oil for prevention."],
        "cultural": ["Avoid overhead irrigation.", "Remove and burn infected leaves."]
    }
})

# Maintain backward compatibility
DISEASE_TREATMENTS = DISEASE_TREATMENTS_EN

def get_recommendations(disease_status, language="en"):
    """
    Retrieves recommendation dictionary for a given disease.
    
    Args:
        disease_status: The disease name (e.g., "Early_blight")
        language: Language code ("en" for English, "te" for Telugu, etc.)
    
    Returns:
        Dictionary containing disease description and treatment recommendations
    """
    # Select the appropriate treatment database based on language
    if language == "te":
        treatments_db = DISEASE_TREATMENTS_TE
    else:
        # Default to English for all other languages
        treatments_db = DISEASE_TREATMENTS_EN
    
    # Normalize key (handle case or cleaned strings if necessary)
    # The app passes raw string like "Early_blight"
    
    return treatments_db.get(disease_status, {
        "description": "Disease details not available." if language == "en" else "వ్యాధి వివరాలు అందుబాటులో లేవు.",
        "chemical": ["Consult local agricultural officer."] if language == "en" else ["స్థానిక వ్యవసాయ అధికారిని సంప్రదించండి."],
        "organic": ["Apply general organic immunity boosters."] if language == "en" else ["సాధారణ సేంద్రీయ రోగనిరోధక శక్తిని పెంచే పదార్థాలను వాడండి."],
        "cultural": ["Maintain field hygiene."] if language == "en" else ["పొలం పరిశుభ్రతను నిర్వహించండి."]
    })
