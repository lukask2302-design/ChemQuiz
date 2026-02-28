from flask import Flask, render_template, request, session, redirect, url_for
import random
import unicodedata

app = Flask(__name__)
app.secret_key = "tajny_klic"

real_acids = {
    # Binary acids (H + halogen)
    "HCl": ["chlorovodíková kyselina", "kyselina monohydrogénchlorovodíková"],  
    "HBr": ["bromovodíková kyselina", "kyselina monohydrogénbromovodíková"],    
    "HI": ["jódovodíková kyselina", "kyselina monohydrogénjódovodíková"],       
    "HF": ["fluovodíková kyselina", "kyselina monohydrogénfluovodíková"],      

    # Sulfur oxoacids
    "H2SO3": ["kyselina siričitá", "kyselina dihydrogénsiričitá"],  
    "H2SO4": ["kyselina sírová", "kyselina dihydrogénsírová"],     

    # Nitrogen oxoacids
    "H2NO2": ["kyselina dusnatá", "kyselina dihydrogéndusnatá"],     
    "HNO2": ["kyselina dusitá", "kyselina monohydrogéndusitá"],      
    "HNO3": ["kyselina dusičná", "kyselina monohydrogéndusičná"],    

    # Phosphorus oxoacids
    "H3PO3": ["kyselina trihydrogénfosforitá"], 
    "H3PO4": ["kyselina trihydrogénfosforečná"], 
    "HPO3": ["kyselina fosforečná", "kyselina monohydrogénfosforečná"],

    # Carbon
    "H2CO3": ["kyselina uhličitá", "kyselina dihydrogénuhličitá"], 

    # Boron
    "H3BO3": ["kyselina trihydrogénboritá"],

    # Arsenic / Antimony
    "H3AsO4": ["kyselina trihydrogénarsenová"],
    "H3SbO4": ["kyselina trihydrogénantimónová"],

    # Selenium / Tellurium
    "H2SeO3": ["kyselina seleničitá", "kyselina dihydrogénseleničitá"],
    "H2SeO4": ["kyselina selenová", "kyselina dihydrogénselénová"],     
    "H2TeO3": ["kyselina telúričitá", "kyselina dihydrogénteluričitá"], 
    "H2TeO4": ["kyselina telúrová", "kyselina dihydrogéntelurová"],   

    # Halogens
    "HBrO2": ["kyselina bromitá", "kyselina monohydrogénbromitá"],  
    "HBrO3": ["kyselina bromečná", "kyselina monohydrogénbromečná"], 
    "HClO3": ["kyselina chlorečná", "kyselina monohydrogénchlorečná"], 
    "HClO4": ["kyselina chloristá", "kyselina monohydrogénchloristá"], 
    "HIO3": ["kyselina jodičná", "kyselina monohydrogénjodičná"],     
    "HIO4": ["kyselina jodistá", "kyselina monohydrogénjodistá"],
    "H3IO5": ["kyselina trihydrogénjódistá"],      
    "H5IO6": ["kyselina pentahydrogénjodistá"], 

    # Silicon
    "H2SiO3": ["kyselina kremičitá", "kyselina dihydrogénkremičitá"],
    "H4SiO4": ["kyselina tetrahydrogénkremičitá"],

    # Manganese
    "H2MnO2": ["kyselina manganatá", "kyselina dihydrogénmanganatá"],
    "HMnO4": ["kyselina manganistá", "kyselina monohydrogénmanganistá "], 
    "H5Mn3O13": ["kyselina pentahydrogéntrimanganistá"], 

    # Molybdenum
    "H2MoO4": ["kyselina molybdénová", "kyselina dihydrogénmolybdénová"],
    "H6Mo2O9": ["kyselina hexahydrogéndimolybdenová"], 

    # Rhodium
    "H3RhO5": ["kyselina trihydrogénrenistá"], 

    # Tungsten / Xenon
    "H2WO4": ["kyselina wolfrámová", "kyselina dihydrogénwolfrámová"], 
    "H2XeO5": ["kyselina xenoničelá", "kyselina dihydrogénxenoničelá"],

    # Polyphosphates
    "H5P3O10": ["kyselina pentahydrogéntripolyfosforečná"], 
    "H4P3O8": ["kyselina tetrahydrogéntrifosforová"],
    "H4P2O7": ["kyselina tetrahydrogéndipolyfosforečná"],

    # Chromium
    "H2CrO4": ["kyselina chrómová", "kyselina dihydrogénchrómová"], 
    "H2Cr4O9": ["kyselina tetrachrómová"],

    # Sulfur oxo-salts
    "H2S2O5": ["kyselina disiričitá"],

    # Arsenic
    "HAs3O5": ["kyselina triarzenitá"],

    # Nitrogen
    "H2N2O2": ["kyselina didusná"],

    # Boron
    "H4B6O11": ["kyselina tetrahydrogénhexaboritá"], 

    # Tungsten / Molybdenum
    "H2W2O5": ["kyselina diwolfrámičitá"], 
    "H2Mo2O7": ["kyselina dimolybdénová"], 
    "H6W2O9": ["kyselina hexahydrogéndiwolfrámová"], 
}


compounds = {
    # --- Halogenides ---
    "NaCl": "chlorid sodný",
    "KBr": "bromid draselný",
    "CaF2": "fluorid vápenatý",
    "LiCl": "chlorid lítny",
    "MgCl2": "chlorid horečnatý",
    "AlCl3": "chlorid hlinitý",
    "CuCl2": "chlorid meďnatý",
    "FeCl3": "chlorid železitý",
    "ZnCl2": "chlorid zinočnatý",
    "AgCl": "chlorid strieborný",
    
    # --- Oxides ---
    "CO": "oxid uhoľnatý",
    "CO2": "oxid uhličitý",
    "SO2": "oxid siričitý",
    "SO3": "oxid sírový",
    "NO": "oxid dusnatý",
    "NO2": "oxid dusičitý",
    "N2O": "oxid dusný",
    "H2O": "voda",
    "Fe2O3": "oxid železitý",
    "Al2O3": "oxid hlinitý",
    "K2O": "oxid draselný",
    "Na2O": "oxid sodný",
    "MgO": "oxid horečnatý",
    "FeO": "oxid železnatý",
    "Cu2O": "oxid meďný",
    "CuO": "oxid meďnatý",
    "ZnO": "oxid zinočnatý",
    "PbO": "oxid olovnatý",
    "SnO": "oxid cínnatý",
    
    # --- Sulfides ---
    "H2S": "sulfid vodíka",
    "FeS": "sulfid železnatý",
    "CuS": "sulfid meďnatý",
    "ZnS": "sulfid zinočitý",
    "PbS": "sulfid olovnatý",
    "Ag2S": "sulfid strieborný",
    "MnS": "sulfid manganatý",
    "CdS": "sulfid kademnatý",
    "CoS": "sulfid kobaltnatý",
    "NiS": "sulfid nikelnatý",
    "Al2S3": "sulfid hlinitý",
    "PbS": "sulfid olovnatý",
    
    # --- Borides ---
    "MgB2": "borid horečnatý",
    "TiB2": "borid titánu",
    "AlB2": "borid hlinitý",
    "FeB": "borid železa",
    "CrB2": "borid chrómu",
    "BH3": "borán",
    
    # --- Phosphides ---
    "Ca3P2": "fosfid vápenatý",
    "AlP": "fosfid hliníka", "fosfid hlinitý"
    "Zn3P2": "fosfid zinočitý",
    "GaP": "fosfid gália",
    
    # --- Hydrides ---
    "NaH": "hydrid sodný",
    "LiH": "hydrid lítny",
    "AlH3": "hydrid hlinitý",
    "CaH2": "hydrid vápenatý",
    "MgH2": "hydrid horečnatý",
    "TiH2": "hydrid titánu",
    
    # --- Nitrides ---
    "BN": "nitrid bóru","nitrid bórny"
    "AlN": "nitrid hlinitý",
    "TiN": "nitrid titánu",
    "Si3N4": "nitrid kremíka",
    "GaN": "nitrid gália",
    "Ca3N2": "nitrid vápenatý",
    "Mg3N2": "nitrid horečnatý",
    
    # --- Carbides ---
    "CaC2": "karbid vápenatý",
    "SiC": "karbid kremíka",
    "WC": "karbid volfrámu",
    "Fe3C": "karbid železa",
    "TiC": "karbid titánu",
}


salts = {
    "NaCl": "chlorid sodný",
    "KCl": "chlorid draselný",
    "CaCl2": "chlorid vápenatý",
    "MgCl2": "chlorid horečnatý",
    "AlCl3": "chlorid hlinitý",
    "FeCl3": "chlorid železitý",

    "NaBr": "bromid sodný",
    "KI": "jodid draselný",

    "Na2SO4": "síran sodný",
    "K2SO4": "síran draselný",
    "MgSO4": "síran horečnatý",
    "CaSO4": "síran vápenatý",
    "FeSO4": "síran železnatý",
    "Fe2(SO4)3": "síran železitý",
    "CuSO4": "síran meďnatý",
    "ZnSO4": "síran zinočnatý",

    "Na2SO3": "siričitan sodný",
    "K2SO3": "siričitan draselný",
    "CaSO3": "siričitan vápenatý",

    "NaNO3": "dusičnan sodný",
    "KNO3": "dusičnan draselný",
    "AgNO3": "dusičnan strieborný",
    "Ca(NO3)2": "dusičnan vápenatý",

    "NaNO2": "dusitan sodný",
    "KNO2": "dusitan draselný",

    "Na2CO3": "uhličitan sodný",
    "K2CO3": "uhličitan draselný",
    "CaCO3": "uhličitan vápenatý",
    "MgCO3": "uhličitan horečnatý",

    "Na3PO4": "fosforečnan sodný",
    "Ca3(PO4)2": "fosforečnan vápenatý",
    "K3PO4": "fosforečnan draselný",

    "Na2SiO3": "kremičitan sodný",
    "CaSiO3": "kremičitan vápenatý",

    "K2CrO4": "chroman draselný",
    "K2Cr2O7": "dichroman draselný",

    "KMnO4": "manganistan draselný",

    "CuCl2": "chlorid meďnatý",
    "ZnCl2": "chlorid zinočnatý",
    "Pb(NO3)2": "dusičnan olovnatý"
}


def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8').lower()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/quiz/<category>")
def quiz_start(category):
    session["category"] = category
    session["current"] = 0
    session["score"] = 0
    session["wrong_answers"] = []  # ← Initialize empty list here

    questions_pool = []

    if category == "salts":
        for formula, name in salts.items():
            questions_pool.append((f"Napíš názov soli {formula}:", name))
            questions_pool.append((f"Napíš vzorec pre {name}:", formula))

    elif category == "compounds":
        for formula, name in compounds.items():
            questions_pool.append((f"Napíš názov zlúčeniny {formula}:", name))
            questions_pool.append((f"Napíš vzorec pre {name}:", formula))

    elif category == "acids":
        for formula, names in real_acids.items():
            questions_pool.append((f"Napíš názov kyseliny {formula}:", names[0]))
            for name_variant in names:
                questions_pool.append((f"Napíš vzorec pre {name_variant}:", formula))

    random.shuffle(questions_pool)
    session["questions"] = questions_pool[:50]

    return redirect(url_for("quiz_question"))

@app.route("/quiz/question", methods=["GET","POST"])
def quiz_question():
    if "questions" not in session:
        return redirect(url_for("home"))

    current = session["current"]
    questions = session["questions"]

    if request.method=="POST":
        answer = request.form.get("answer","").strip()
        question_text, correct_answer = questions[current]

        if normalize(answer) == normalize(correct_answer):
            session["score"] += 1
        else:
            session["wrong_answers"].append({
                "question": question_text,
                "your_answer": answer,
                "correct_answer": correct_answer
            })

        session["current"] += 1
        current = session["current"]

        if current >= len(questions):
            return redirect(url_for("quiz_result"))

    question_text, _ = questions[current]
    return render_template("quiz.html", question=question_text, number=current+1, total=len(questions))

@app.route("/quiz/result")
def quiz_result():
    score = session.get("score",0)
    total = len(session.get("questions",[]))
    wrong_answers = session.get("wrong_answers", [])
    return render_template("result.html", score=score, total=total, wrong_answers=wrong_answers)

if __name__ == "__main__":
    app.run(debug=True)