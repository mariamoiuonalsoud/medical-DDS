import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.database import  drugs_db, interactions_db, allergens_db, condition_rules_db, knowledge_db, conditions_db, common_allergens_db
import json

JSON_PATH = os.path.join(os.path.dirname(__file__), "drug_names.json")

CONDITION_RULES = [
    {"drug": "Ibuprofen", "interacts_with": "Kidney Disease", "severity": "Moderate Risk", "reason": "NSAIDs reduce renal prostaglandin synthesis, causing vasoconstriction and acute kidney injury in pre-existing renal impairment"},
    {"drug": "Naproxen", "interacts_with": "Kidney Disease", "severity": "Moderate Risk", "reason": "NSAIDs may acutely worsen renal function; avoid in eGFR < 30 mL/min"},
    {"drug": "Metformin", "interacts_with": "Kidney Disease", "severity": "High Risk", "reason": "Reduced renal clearance leads to metformin accumulation and risk of potentially fatal lactic acidosis; contraindicated in eGFR < 30 mL/min"},
    {"drug": "Atenolol", "interacts_with": "Asthma", "severity": "High Risk", "reason": "Non-selective beta-blockers cause bronchospasm in asthmatic patients"},
    {"drug": "Propranolol", "interacts_with": "Asthma", "severity": "High Risk", "reason": "Non-selective beta-blockade causes bronchoconstriction; contraindicated in significant reversible airways disease"},
    {"drug": "Ibuprofen", "interacts_with": "Hypertension", "severity": "Moderate Risk", "reason": "NSAIDs cause sodium and water retention, raising blood pressure and reducing efficacy of antihypertensive agents"},
    {"drug": "Naproxen", "interacts_with": "Heart Failure", "severity": "Moderate Risk", "reason": "NSAIDs cause fluid retention and may precipitate acute decompensation in heart failure"},
    {"drug": "Warfarin", "interacts_with": "Liver Disease", "severity": "High Risk", "reason": "The liver synthesises clotting factors; hepatic impairment amplifies warfarin anticoagulant effect"},
    {"drug": "Simvastatin", "interacts_with": "Liver Disease", "severity": "Contraindicated", "reason": "Statins are hepatically metabolised and can worsen hepatotoxicity"},
    {"drug": "Atorvastatin", "interacts_with": "Liver Disease", "severity": "Contraindicated", "reason": "Atorvastatin is contraindicated in active liver disease or unexplained persistent transaminase elevations"},
    {"drug": "Tramadol", "interacts_with": "Epilepsy", "severity": "High Risk", "reason": "Tramadol lowers the seizure threshold and is associated with seizure induction"},
    {"drug": "Clarithromycin", "interacts_with": "Liver Disease", "severity": "Moderate Risk", "reason": "Clarithromycin is extensively hepatically metabolised; dose reduction required in severe hepatic impairment"},
    {"drug": "Metformin", "interacts_with": "Heart Failure", "severity": "Moderate Risk", "reason": "Acute or decompensated heart failure reduces tissue perfusion, increasing lactic acidosis risk"},
    {"drug": "Prednisone", "interacts_with": "Diabetes", "severity": "Moderate Risk", "reason": "Corticosteroids promote gluconeogenesis and cause steroid-induced hyperglycaemia, worsening glycaemic control"},
]

KNOWLEDGE_BASE = [
    {"drug": "Paracetamol", "description": "An analgesic and antipyretic used for mild to moderate pain and fever. Generally safe with anticoagulants at standard doses.", "uses": ["Pain relief", "Fever reduction"], "keywords": ["pain", "analgesic", "warfarin", "safe", "alternative", "fever", "antipyretic"]},
    {"drug": "Cetirizine", "description": "A second-generation antihistamine used for allergy symptom relief. Non-sedating at standard doses with minimal drug interactions.", "uses": ["Allergy relief", "Urticaria", "Hay fever"], "keywords": ["allergy", "antihistamine", "penicillin", "sulfa", "alternative"]},
    {"drug": "Salbutamol", "description": "A short-acting beta-2 agonist bronchodilator used for acute asthma relief and bronchospasm.", "uses": ["Asthma relief", "Bronchospasm", "COPD"], "keywords": ["asthma", "bronchodilator", "inhaler", "relief", "respiratory", "copd"]},
    {"drug": "Metformin", "description": "A biguanide antidiabetic agent used as first-line treatment for type 2 diabetes. Requires adequate renal function (eGFR >= 30).", "uses": ["Type 2 diabetes", "Glucose control"], "keywords": ["diabetes", "glucose", "metformin", "insulin", "kidney", "renal"]},
    {"drug": "Losartan", "description": "An angiotensin II receptor blocker (ARB) used for hypertension. Preferred alternative to ACE inhibitors in patients who develop cough.", "uses": ["Hypertension", "Heart failure", "Diabetic nephropathy"], "keywords": ["hypertension", "blood pressure", "ace", "alternative", "arb", "kidney"]},
    {"drug": "Furosemide", "description": "A loop diuretic used for fluid overload in heart failure and edema.", "uses": ["Heart failure", "Edema", "Hypertension"], "keywords": ["diuretic", "fluid", "edema", "heart failure", "kidney", "potassium"]},
    {"drug": "Bisoprolol", "description": "A selective beta-1 adrenoceptor blocker used for heart failure and hypertension.", "uses": ["Heart failure", "Hypertension", "Angina"], "keywords": ["heart failure", "beta blocker", "hypertension", "cardiac", "asthma", "copd"]},
    {"drug": "Amlodipine", "description": "A dihydropyridine calcium channel blocker used for hypertension and stable angina.", "uses": ["Hypertension", "Angina"], "keywords": ["hypertension", "calcium", "blood pressure", "alternative", "angina"]},
    {"drug": "Warfarin", "description": "A vitamin K antagonist oral anticoagulant. Narrow therapeutic index; INR monitoring essential.", "uses": ["Atrial fibrillation", "DVT prevention", "PE treatment"], "keywords": ["anticoagulant", "bleeding", "inr", "warfarin", "atrial fibrillation"]},
    {"drug": "Aspirin", "description": "A non-selective COX inhibitor used as an antiplatelet agent for cardiovascular protection.", "uses": ["Antiplatelet therapy", "Secondary CV prevention"], "keywords": ["aspirin", "antiplatelet", "bleeding", "nsaid", "cardiovascular"]},
    {"drug": "Lisinopril", "description": "An ACE inhibitor used for hypertension, heart failure, and post-MI cardioprotection.", "uses": ["Hypertension", "Heart failure", "Diabetic nephropathy"], "keywords": ["ace", "hypertension", "heart failure", "kidney", "cough"]},
    {"drug": "Atorvastatin", "description": "A high-intensity statin used for dyslipidaemia and cardiovascular risk reduction.", "uses": ["Dyslipidaemia", "Cardiovascular prevention"], "keywords": ["statin", "cholesterol", "ldl", "cardiovascular", "liver", "atorvastatin"]},
    {"drug": "Simvastatin", "description": "An HMG-CoA reductase inhibitor for lowering LDL cholesterol. Significant interaction risk with CYP3A4 inhibitors.", "uses": ["Dyslipidaemia", "Cardiovascular prevention"], "keywords": ["statin", "cholesterol", "myopathy", "rhabdomyolysis", "simvastatin"]},
    {"drug": "Sertraline", "description": "An SSRI antidepressant used for depression, anxiety, OCD, and PTSD.", "uses": ["Depression", "Anxiety disorders", "OCD", "PTSD"], "keywords": ["antidepressant", "ssri", "depression", "anxiety", "serotonin", "sertraline"]},
    {"drug": "Tramadol", "description": "An opioid-like analgesic with serotonergic properties. Risk of serotonin syndrome with SSRIs.", "uses": ["Moderate to severe pain", "Neuropathic pain"], "keywords": ["opioid", "pain", "serotonin", "seizure", "epilepsy", "tramadol"]},
    {"drug": "Omeprazole", "description": "A proton pump inhibitor (PPI) for gastric acid suppression. Inhibits CYP2C19.", "uses": ["GERD", "Peptic ulcer disease", "NSAID gastroprotection"], "keywords": ["ppi", "acid", "stomach", "ulcer", "gerd", "omeprazole"]},
    {"drug": "Spironolactone", "description": "A potassium-sparing aldosterone antagonist used in heart failure.", "uses": ["Heart failure", "Ascites", "Hypertension"], "keywords": ["diuretic", "potassium", "heart failure", "hyperkalemia", "ace"]},
    {"drug": "Digoxin", "description": "A cardiac glycoside for rate control in atrial fibrillation and heart failure. Narrow therapeutic index.", "uses": ["Atrial fibrillation (rate control)", "Heart failure"], "keywords": ["digoxin", "heart failure", "atrial fibrillation", "toxicity"]},
    {"drug": "Methotrexate", "description": "An antimetabolite used for rheumatoid arthritis. NSAIDs reduce its renal clearance.", "uses": ["Rheumatoid arthritis", "Psoriasis"], "keywords": ["methotrexate", "rheumatoid", "arthritis", "nsaid", "toxicity"]},
    {"drug": "Carbamazepine", "description": "A sodium channel-blocking anticonvulsant. Potent CYP3A4 inducer.", "uses": ["Epilepsy", "Trigeminal neuralgia", "Bipolar disorder"], "keywords": ["anticonvulsant", "epilepsy", "cyp3a4", "carbamazepine"]},
    {"drug": "Prednisone", "description": "A synthetic glucocorticoid for inflammatory and autoimmune conditions.", "uses": ["Autoimmune conditions", "Inflammatory diseases", "Asthma exacerbations"], "keywords": ["steroid", "corticosteroid", "inflammation", "diabetes", "prednisone"]},
    {"drug": "Pantoprazole", "description": "A proton pump inhibitor with minimal CYP2C19 inhibition. Preferred over omeprazole with clopidogrel.", "uses": ["GERD", "Peptic ulcer disease", "NSAID gastroprotection"], "keywords": ["ppi", "acid", "stomach", "ulcer", "gerd", "pantoprazole", "safe"]},
]

'''DRUGS = [
    {"_id": "DRG001", "name": "Aspirin", "therapeutic_class": "Analgesic", "mechanism": "COX-1/COX-2 inhibitor", "contraindications": ["Active bleeding", "Gastric ulcer", "Aspirin allergy"], "common_dosage": "81-325mg QD", "side_effects": ["GI bleeding", "Bruising", "Tinnitus"]},
    {"_id": "DRG002", "name": "Acetaminophen", "therapeutic_class": "Analgesic", "mechanism": "COX-3 inhibitor (central)", "contraindications": ["Liver disease", "Alcoholism"], "common_dosage": "500-1000mg Q4-6H", "side_effects": ["Liver toxicity (high dose)"]},
    {"_id": "DRG003", "name": "Ibuprofen", "therapeutic_class": "NSAID", "mechanism": "COX-1/COX-2 inhibitor", "contraindications": ["GI bleed", "Renal failure", "Aspirin allergy"], "common_dosage": "200-800mg TID", "side_effects": ["GI bleeding", "Renal impairment", "Hypertension"]},
    {"_id": "DRG004", "name": "Naproxen", "therapeutic_class": "NSAID", "mechanism": "COX-1/COX-2 inhibitor", "contraindications": ["GI bleed", "Renal failure", "Aspirin allergy"], "common_dosage": "250-500mg BID", "side_effects": ["GI bleeding", "Renal impairment"]},
    {"_id": "DRG005", "name": "Celecoxib", "therapeutic_class": "NSAID (COX-2 selective)", "mechanism": "COX-2 inhibitor", "contraindications": ["CAD", "Sulfa allergy"], "common_dosage": "100-200mg BID", "side_effects": ["CV events", "GI bleeding (lower risk)"]},
    {"_id": "DRG006", "name": "Tramadol", "therapeutic_class": "Analgesic (opioid)", "mechanism": "Mu-opioid agonist + SNRI", "contraindications": ["Seizure disorder", "MAOI use", "Opioid dependence"], "common_dosage": "50-100mg Q4-6H", "side_effects": ["Seizures", "Serotonin syndrome", "Dependence"]},
    {"_id": "DRG007", "name": "Warfarin", "therapeutic_class": "Anticoagulant", "mechanism": "Vitamin K epoxide reductase inhibitor", "contraindications": ["Active bleeding", "Pregnancy", "Liver disease"], "common_dosage": "2-10mg QD", "side_effects": ["Bleeding", "Bruising", "Skin necrosis"]},
    {"_id": "DRG008", "name": "Heparin", "therapeutic_class": "Anticoagulant", "mechanism": "Antithrombin III activator", "contraindications": ["Active bleeding", "Thrombocytopenia", "Hypersensitivity"], "common_dosage": "IV/SC per protocol", "side_effects": ["Bleeding", "HIT"]},
    {"_id": "DRG009", "name": "Enoxaparin", "therapeutic_class": "Anticoagulant (LMWH)", "mechanism": "Antithrombin III activator (Xa > IIa)", "contraindications": ["Active bleeding", "HIT history"], "common_dosage": "30-40mg SC BID", "side_effects": ["Bleeding", "HIT (rare)"]},
    {"_id": "DRG010", "name": "Rivaroxaban", "therapeutic_class": "Anticoagulant (DOAC)", "mechanism": "Factor Xa inhibitor", "contraindications": ["Active bleeding", "CrCl <15", "Hepatic disease"], "common_dosage": "15-20mg QD", "side_effects": ["Bleeding"]},
    {"_id": "DRG011", "name": "Apixaban", "therapeutic_class": "Anticoagulant (DOAC)", "mechanism": "Factor Xa inhibitor", "contraindications": ["Active bleeding", "CrCl <15", "Hepatic disease"], "common_dosage": "5mg BID", "side_effects": ["Bleeding"]},
    {"_id": "DRG012", "name": "Metformin", "therapeutic_class": "Antidiabetic", "mechanism": "AMPK activator, reduces hepatic gluconeogenesis", "contraindications": ["Renal failure (eGFR <30)", "Metabolic acidosis", "Contrast dye procedure"], "common_dosage": "500-1000mg BID", "side_effects": ["GI upset", "Lactic acidosis (rare)"]},
    {"_id": "DRG013", "name": "Insulin", "therapeutic_class": "Antidiabetic", "mechanism": "Activates insulin receptors", "contraindications": ["Hypoglycemia"], "common_dosage": "Per sliding scale", "side_effects": ["Hypoglycemia", "Weight gain"]},
    {"_id": "DRG014", "name": "Glipizide", "therapeutic_class": "Antidiabetic (sulfonylurea)", "mechanism": "K-ATP channel blocker, increases insulin secretion", "contraindications": ["DKA", "Sulfa allergy"], "common_dosage": "5-10mg QD", "side_effects": ["Hypoglycemia", "Weight gain"]},
    {"_id": "DRG015", "name": "Sitagliptin", "therapeutic_class": "Antidiabetic (DPP-4 inhibitor)", "mechanism": "DPP-4 inhibitor, increases incretin levels", "contraindications": ["Renal failure", "Pancreatitis history"], "common_dosage": "100mg QD", "side_effects": ["Pancreatitis", "Joint pain"]},
    {"_id": "DRG016", "name": "Empagliflozin", "therapeutic_class": "Antidiabetic (SGLT2 inhibitor)", "mechanism": "SGLT2 inhibitor, increases urinary glucose excretion", "contraindications": ["DKA", "Renal failure", "UTI history"], "common_dosage": "10-25mg QD", "side_effects": ["UTI", "DKA", "Dehydration"]},
    {"_id": "DRG017", "name": "Lisinopril", "therapeutic_class": "ACE Inhibitor", "mechanism": "ACE inhibitor, reduces angiotensin II", "contraindications": ["Pregnancy", "Angioedema", "Renal artery stenosis"], "common_dosage": "10-40mg QD", "side_effects": ["Cough", "Hyperkalemia", "Angioedema"]},
    {"_id": "DRG018", "name": "Losartan", "therapeutic_class": "ARB", "mechanism": "Angiotensin II receptor blocker", "contraindications": ["Pregnancy", "Renal artery stenosis"], "common_dosage": "25-100mg QD", "side_effects": ["Hyperkalemia", "Renal impairment"]},
    {"_id": "DRG019", "name": "Metoprolol", "therapeutic_class": "Beta Blocker", "mechanism": "Beta-1 selective adrenergic blocker", "contraindications": ["Bradycardia", "Heart block", "Asthma (caution)"], "common_dosage": "25-200mg QD", "side_effects": ["Bradycardia", "Fatigue", "Bronchospasm"]},
    {"_id": "DRG020", "name": "Atorvastatin", "therapeutic_class": "Statin", "mechanism": "HMG-CoA reductase inhibitor", "contraindications": ["Liver disease", "Pregnancy"], "common_dosage": "10-80mg QD", "side_effects": ["Myalgia", "Rhabdomyolysis", "Liver enzyme elevation"]},
    {"_id": "DRG021", "name": "Amlodipine", "therapeutic_class": "Calcium Channel Blocker", "mechanism": "L-type calcium channel blocker", "contraindications": ["Severe hypotension", "Heart failure (non-dihydropyridine)"], "common_dosage": "5-10mg QD", "side_effects": ["Edema", "Flushing", "Dizziness"]},
    {"_id": "DRG022", "name": "Amoxicillin", "therapeutic_class": "Antibiotic (Penicillin)", "mechanism": "Beta-lactam, inhibits cell wall synthesis", "contraindications": ["Penicillin allergy"], "common_dosage": "500mg TID", "side_effects": ["Rash", "Diarrhea", "Anaphylaxis"]},
    {"_id": "DRG023", "name": "Azithromycin", "therapeutic_class": "Antibiotic (Macrolide)", "mechanism": "50S ribosomal inhibitor", "contraindications": ["QT prolongation", "Cholestatic jaundice"], "common_dosage": "250-500mg QD", "side_effects": ["QT prolongation", "GI upset", "Hepatotoxicity"]},
    {"_id": "DRG024", "name": "Ciprofloxacin", "therapeutic_class": "Antibiotic (Fluoroquinolone)", "mechanism": "DNA gyrase / Topoisomerase IV inhibitor", "contraindications": ["Tendonitis history", "Children", "QT prolongation"], "common_dosage": "250-750mg BID", "side_effects": ["Tendon rupture", "QT prolongation", "CNS effects"]},
    {"_id": "DRG025", "name": "Doxycycline", "therapeutic_class": "Antibiotic (Tetracycline)", "mechanism": "30S ribosomal inhibitor", "contraindications": ["Children <8", "Pregnancy"], "common_dosage": "100mg BID", "side_effects": ["Photosensitivity", "GI upset", "Tooth discoloration"]},
    {"_id": "DRG026", "name": "Cephalexin", "therapeutic_class": "Antibiotic (Cephalosporin)", "mechanism": "Beta-lactam, inhibits cell wall synthesis", "contraindications": ["Penicillin allergy (cross-reactive)"], "common_dosage": "250-500mg QID", "side_effects": ["Rash", "Diarrhea", "Anaphylaxis"]},
    {"_id": "DRG027", "name": "Sertraline", "therapeutic_class": "SSRI", "mechanism": "Serotonin reuptake inhibitor", "contraindications": ["MAOI use", "Bipolar (mania)"], "common_dosage": "50-200mg QD", "side_effects": ["Nausea", "Insomnia", "Sexual dysfunction"]},
    {"_id": "DRG028", "name": "Fluoxetine", "therapeutic_class": "SSRI", "mechanism": "Serotonin reuptake inhibitor", "contraindications": ["MAOI use"], "common_dosage": "20-80mg QD", "side_effects": ["Nausea", "Insomnia", "Sexual dysfunction"]},
    {"_id": "DRG029", "name": "Alprazolam", "therapeutic_class": "Benzodiazepine", "mechanism": "GABA-A receptor positive modulator", "contraindications": ["CNS depression", "Glaucoma", "Substance abuse"], "common_dosage": "0.25-0.5mg TID", "side_effects": ["Dependence", "Sedation", "Cognitive impairment"]},
    {"_id": "DRG030", "name": "Lorazepam", "therapeutic_class": "Benzodiazepine", "mechanism": "GABA-A receptor positive modulator", "contraindications": ["CNS depression", "Glaucoma"], "common_dosage": "0.5-2mg BID-TID", "side_effects": ["Dependence", "Sedation"]},
    {"_id": "DRG031", "name": "Duloxetine", "therapeutic_class": "SNRI", "mechanism": "Serotonin + norepinephrine reuptake inhibitor", "contraindications": ["MAOI use", "Liver disease", "Glaucoma"], "common_dosage": "30-60mg QD", "side_effects": ["Nausea", "Insomnia", "Hypertension"]},
    {"_id": "DRG032", "name": "Omeprazole", "therapeutic_class": "PPI", "mechanism": "Proton pump inhibitor (H+/K+ ATPase)", "contraindications": ["Long-term use (Caution)"], "common_dosage": "20-40mg QD", "side_effects": ["C diff risk", "Osteoporosis", "B12 deficiency"]},
    {"_id": "DRG033", "name": "Pantoprazole", "therapeutic_class": "PPI", "mechanism": "Proton pump inhibitor (H+/K+ ATPase)", "contraindications": ["Long-term use (Caution)"], "common_dosage": "20-40mg QD", "side_effects": ["C diff risk", "Osteoporosis"]},
    {"_id": "DRG034", "name": "Ondansetron", "therapeutic_class": "Antiemetic", "mechanism": "5-HT3 receptor antagonist", "contraindications": ["QT prolongation"], "common_dosage": "4-8mg TID", "side_effects": ["QT prolongation", "Headache"]},
    {"_id": "DRG035", "name": "Metoclopramide", "therapeutic_class": "Antiemetic / Prokinetic", "mechanism": "Dopamine D2 receptor antagonist", "contraindications": ["Parkinson's", "GI obstruction", "Seizure disorder"], "common_dosage": "10mg TID", "side_effects": ["Dystonia", "Tardive dyskinesia", "Sedation"]},
    {"_id": "DRG036", "name": "Prednisone", "therapeutic_class": "Corticosteroid", "mechanism": "Glucocorticoid receptor agonist", "contraindications": ["Systemic fungal infection", "Live vaccine"], "common_dosage": "5-60mg QD taper", "side_effects": ["Hyperglycemia", "Osteoporosis", "Immunosuppression"]},
    {"_id": "DRG037", "name": "Furosemide", "therapeutic_class": "Loop Diuretic", "mechanism": "Na-K-2Cl cotransporter inhibitor", "contraindications": ["Anuria", "Severe hypokalemia", "Sulfa allergy"], "common_dosage": "20-80mg BID", "side_effects": ["Hypokalemia", "Dehydration", "Ototoxicity"]},
    {"_id": "DRG038", "name": "Levothyroxine", "therapeutic_class": "Thyroid Hormone", "mechanism": "Thyroid receptor agonist", "contraindications": ["Hyperthyroidism", "Adrenal insufficiency"], "common_dosage": "50-200mcg QD", "side_effects": ["Tachycardia", "Weight loss", "Insomnia"]},
    {"_id": "DRG039", "name": "Allopurinol", "therapeutic_class": "Xanthine Oxidase Inhibitor", "mechanism": "Xanthine oxidase inhibitor, reduces uric acid", "contraindications": ["Hypersensitivity"], "common_dosage": "100-300mg QD", "side_effects": ["Rash", "Hypersensitivity syndrome"]},
]'''

INTERACTIONS = [
    {"drug_a": "Warfarin", "drug_b": "Aspirin", "severity": "High", "mechanism": "Synergistic anticoagulation — both drugs impair coagulation cascade", "recommendation": "Avoid concurrent use. Consider alternative analgesic (acetaminophen)."},
    {"drug_a": "Warfarin", "drug_b": "Ibuprofen", "severity": "High", "mechanism": "NSAIDs inhibit platelet aggregation and increase INR", "recommendation": "Avoid NSAIDs in warfarin patients. Use acetaminophen for pain."},
    {"drug_a": "Warfarin", "drug_b": "Amoxicillin", "severity": "Moderate", "mechanism": "Antibiotics alter gut flora which produce vitamin K, potentiating warfarin", "recommendation": "Monitor INR closely during antibiotic course. Adjust warfarin dose as needed."},
    {"drug_a": "Warfarin", "drug_b": "Ciprofloxacin", "severity": "High", "mechanism": "Ciprofloxacin inhibits CYP1A2 and CYP3A4, increasing warfarin levels", "recommendation": "Avoid combination or reduce warfarin dose and monitor INR daily."},
    {"drug_a": "Warfarin", "drug_b": "Metronidazole", "severity": "High", "mechanism": "Metronidazole inhibits warfarin metabolism via CYP inhibition", "recommendation": "Reduce warfarin dose by 30-50% and monitor INR closely."},
    {"drug_a": "Lisinopril", "drug_b": "Ibuprofen", "severity": "High", "mechanism": "NSAIDs reduce antihypertensive effect of ACE inhibitors; risk of renal failure", "recommendation": "Avoid NSAIDs. Monitor BP and renal function if combination unavoidable."},
    {"drug_a": "Lisinopril", "drug_b": "Spironolactone", "severity": "Moderate", "mechanism": "Both increase potassium levels — risk of life-threatening hyperkalemia", "recommendation": "Monitor serum K+ regularly. Avoid K+ supplements."},
    {"drug_a": "Metformin", "drug_b": "Contrast Dye (Iodinated)", "severity": "Moderate", "mechanism": "Contrast dye can precipitate acute kidney injury, increasing lactic acidosis risk with metformin", "recommendation": "Hold metformin 48h before contrast procedure and 48h after."},
    {"drug_a": "Ciprofloxacin", "drug_b": "Ibuprofen", "severity": "Moderate", "mechanism": "NSAIDs increase CNS penetration of fluoroquinolones — seizure risk", "recommendation": "Avoid combination in patients with seizure history."},
    {"drug_a": "Atorvastatin", "drug_b": "Azithromycin", "severity": "High", "mechanism": "Macrolide antibiotics inhibit CYP3A4, increasing statin levels; risk of rhabdomyolysis", "recommendation": "Consider alternative antibiotic (doxycycline) or hold statin temporarily."},
    {"drug_a": "Sertraline", "drug_b": "MAO Inhibitor", "severity": "High", "mechanism": "Combined serotonin excess leads to serotonin syndrome (hyperthermia, rigidity, death)", "recommendation": "Absolute contraindication. Allow 14-day washout between MAOI and SSRI."},
    {"drug_a": "Sertraline", "drug_b": "Ibuprofen", "severity": "Moderate", "mechanism": "SSRIs impair platelet aggregation; NSAIDs add further bleeding risk", "recommendation": "Use acetaminophen for analgesia if possible. Monitor for bruising/bleeding."},
    {"drug_a": "Aspirin", "drug_b": "Ibuprofen", "severity": "Moderate", "mechanism": "Ibuprofen competes for COX-1 binding site, reducing aspirin's antiplatelet effect", "recommendation": "Take aspirin at least 2h before ibuprofen, or use alternative analgesic."},
    {"drug_a": "Metoprolol", "drug_b": "Insulin", "severity": "Low", "mechanism": "Beta blockers mask tachycardia, a key symptom of hypoglycemia", "recommendation": "Educate patient on non-tachycardia hypoglycemia symptoms (sweating, confusion)."},
    {"drug_a": "Furosemide", "drug_b": "Metformin", "severity": "Low", "mechanism": "Diuretics can cause dehydration and prerenal azotemia, reducing metformin clearance", "recommendation": "Monitor renal function periodically."},
    {"drug_a": "Prednisone", "drug_b": "Insulin", "severity": "Moderate", "mechanism": "Corticosteroids induce insulin resistance and hyperglycemia", "recommendation": "Increase insulin dose during corticosteroid therapy. Monitor blood glucose."},
    {"drug_a": "Prednisone", "drug_b": "Ibuprofen", "severity": "Moderate", "mechanism": "Both drugs increase GI bleeding risk synergistically", "recommendation": "Use PPI for GI protection. Consider COX-2 selective NSAID (caution with CAD)."},
    {"drug_a": "Warfarin", "drug_b": "Fluconazole", "severity": "High", "mechanism": "Azole antifungals strongly inhibit warfarin metabolism via CYP2C9", "recommendation": "Reduce warfarin dose by 30-50% and monitor INR daily."},
    {"drug_a": "Digoxin", "drug_b": "Furosemide", "severity": "High", "mechanism": "Furosemide-induced hypokalemia potentiates digoxin toxicity (arrhythmias)", "recommendation": "Monitor K+ levels. Maintain K+ > 4.0 mEq/L."},
    {"drug_a": "Allopurinol", "drug_b": "Azathioprine", "severity": "High", "mechanism": "Allopurinol inhibits xanthine oxidase, blocking azathioprine metabolism → severe myelosuppression", "recommendation": "Reduce azathioprine dose by 60-75%. Monitor CBC closely."},
    {"drug_a": "Naproxen", "drug_b": "Warfarin", "severity": "High", "mechanism": "NSAIDs enhance anticoagulant effect and increase risk of GI haemorrhage", "recommendation": "Avoid NSAIDs in warfarin patients. Use acetaminophen."},
    {"drug_a": "Lisinopril", "drug_b": "Potassium Supplements", "severity": "Moderate", "mechanism": "ACE inhibitors reduce aldosterone; concurrent potassium supplementation raises hyperkalemia risk", "recommendation": "Monitor serum K+ regularly. Avoid K+ supplements with ACE inhibitors."},
    {"drug_a": "Clopidogrel", "drug_b": "Aspirin", "severity": "Moderate", "mechanism": "Dual antiplatelet therapy increases bleeding risk", "recommendation": "Benefit vs risk must be weighed per indication. Use lowest effective dose."},
    {"drug_a": "Methotrexate", "drug_b": "Ibuprofen", "severity": "High", "mechanism": "NSAIDs reduce renal clearance of methotrexate, raising risk of severe toxicity (myelosuppression, mucositis)", "recommendation": "Avoid NSAIDs in patients on methotrexate."},
    {"drug_a": "Simvastatin", "drug_b": "Clarithromycin", "severity": "High", "mechanism": "Clarithromycin inhibits CYP3A4, dramatically increasing simvastatin plasma levels and rhabdomyolysis risk", "recommendation": "Avoid combination. Consider alternative antibiotic or hold statin."},
    {"drug_a": "Lithium", "drug_b": "Ibuprofen", "severity": "High", "mechanism": "NSAIDs reduce renal lithium clearance, raising lithium levels into the toxic range", "recommendation": "Avoid NSAIDs in patients on lithium. Monitor lithium levels if unavoidable."},
    {"drug_a": "Tramadol", "drug_b": "Sertraline", "severity": "High", "mechanism": "Combined serotonergic effect raises risk of serotonin syndrome (agitation, hyperthermia, myoclonus)", "recommendation": "Avoid combination. Consider alternative analgesic."},
    {"drug_a": "Digoxin", "drug_b": "Amiodarone", "severity": "High", "mechanism": "Amiodarone inhibits P-glycoprotein and renal digoxin clearance", "recommendation": "Reduce digoxin dose by 50% and monitor serum levels."},
    {"drug_a": "Phenytoin", "drug_b": "Warfarin", "severity": "Moderate", "mechanism": "Phenytoin initially inhibits warfarin metabolism (INR increase) then induces CYP enzymes (INR decrease)", "recommendation": "Monitor INR closely when starting or stopping phenytoin."},
    {"drug_a": "Sildenafil", "drug_b": "Nitroglycerin", "severity": "High", "mechanism": "Both agents cause vasodilation via cGMP; combination produces severe hypotension", "recommendation": "Absolute contraindication. Do not prescribe together."},
    {"drug_a": "Clopidogrel", "drug_b": "Omeprazole", "severity": "Moderate", "mechanism": "Omeprazole inhibits CYP2C19, reducing clopidogrel activation and antiplatelet efficacy", "recommendation": "Use pantoprazole instead of omeprazole with clopidogrel."},
    {"drug_a": "Carbamazepine", "drug_b": "Oral Contraceptives", "severity": "Moderate", "mechanism": "Carbamazepine induces CYP3A4, accelerating oestrogen and progestogen metabolism", "recommendation": "Advise alternative contraception method."},
    {"drug_a": "Atorvastatin", "drug_b": "Clarithromycin", "severity": "High", "mechanism": "CYP3A4 inhibition by clarithromycin raises atorvastatin exposure and risk of myopathy", "recommendation": "Consider alternative antibiotic or hold statin temporarily."},
]

ALLERGENS = [
    {"drug": "Amoxicillin", "allergen_class": "Penicillin", "cross_reactives": ["Cephalexin", "Cefuroxime", "Ceftriaxone"]},
    {"drug": "Ampicillin", "allergen_class": "Penicillin", "cross_reactives": ["Cephalexin", "Cefuroxime", "Ceftriaxone"]},
    {"drug": "Penicillin V", "allergen_class": "Penicillin", "cross_reactives": ["Cephalexin", "Cefuroxime", "Ceftriaxone"]},
    {"drug": "Cephalexin", "allergen_class": "Cephalosporin", "cross_reactives": ["Penicillin"]},
    {"drug": "Sulfamethoxazole", "allergen_class": "Sulfa", "cross_reactives": ["Furosemide", "Glipizide"]},
    {"drug": "Furosemide", "allergen_class": "Sulfa", "cross_reactives": ["Sulfamethoxazole", "Glipizide"]},
    {"drug": "Glipizide", "allergen_class": "Sulfa", "cross_reactives": ["Furosemide", "Sulfamethoxazole"]},
    {"drug": "Aspirin", "allergen_class": "Salicylate/NSAID", "cross_reactives": ["Ibuprofen", "Naproxen", "Celecoxib"]},
    {"drug": "Ibuprofen", "allergen_class": "NSAID", "cross_reactives": ["Aspirin", "Naproxen"]},
    {"drug": "Codeine", "allergen_class": "Opioid", "cross_reactives": ["Morphine", "Hydrocodone"]},
    {"drug": "Lisinopril", "allergen_class": "ACE Inhibitor", "cross_reactives": ["Enalapril", "Ramipril"]},
    {"drug": "Atorvastatin", "allergen_class": "Statin", "cross_reactives": ["Simvastatin", "Rosuvastatin"]},
]


def seed_all():
    print("Note: Drugs collection not seeded here. Run 'python data/seed_data.py --drugs' to seed from scraped data.")
    
    
    print("Seeding interactions...")
    interactions_db.delete_many({})
    interactions_db.insert_many(INTERACTIONS)

    print("Seeding condition rules...")
    condition_rules_db.delete_many({})
    condition_rules_db.insert_many(CONDITION_RULES)

    print("Seeding knowledge base...")
    knowledge_db.delete_many({})
    knowledge_db.insert_many(KNOWLEDGE_BASE)
    
    print("Seeding allergens...")
    allergens_db.delete_many({})
    allergens_db.insert_many(ALLERGENS)

    print("Done! Seeded {} interactions, {} allergens, {} condition rules, {} knowledge entries".format(
        len(INTERACTIONS), len(ALLERGENS),
        len(CONDITION_RULES), len(KNOWLEDGE_BASE)
    ))

def seed_drugs_from_json(filepath=JSON_PATH):
    if not os.path.exists(filepath):
        print(f"Cannot seed drugs: file not found at '{filepath}'")
        print("Run 'python data/scrape_drugs.py' first to generate the JSON file.")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        drugs = json.load(f)

    # Clear existing drugs and insert new ones
    deleted = drugs_db.delete_many({})
    print(f"Cleared {deleted.deleted_count} existing drugs from MongoDB")

    drugs_db.insert_many(drugs)
    print(f"Seeded {len(drugs)} drugs into MongoDB from {filepath}")
  


def seed_conditions_from_json(filepath=None):
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), "icd10_conditions.json")
    if not os.path.exists(filepath):
        print(f"Cannot seed conditions: file not found at '{filepath}'")
        print("Run 'python data/scrape_icd10.py' first to generate the JSON file.")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        conditions = json.load(f)
    deleted = conditions_db.delete_many({})
    print(f"Cleared {deleted.deleted_count} existing conditions from MongoDB")
    conditions_db.insert_many(conditions)
    print(f"Seeded {len(conditions)} conditions into MongoDB from {filepath}")


def seed_allergens_from_json(filepath=None):
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), "allergens_extended.json")

    # Start with the curated hardcoded allergens (well-validated)
    combined = list(ALLERGENS)

    # Merge in scraped data if available
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            scraped = json.load(f)
        # Add scraped entries that don't duplicate existing ones
        existing_keys = {(a["drug"].lower(), a["allergen_class"]) for a in combined}
        for a in scraped:
            key = (a["drug"].lower(), a["allergen_class"])
            if key not in existing_keys:
                combined.append(a)
                existing_keys.add(key)
        print(f"Merged {len(scraped)} scraped entries ({len(combined) - len(ALLERGENS)} new)")
    else:
        print(f"Scraped file not found at '{filepath}', using curated data only.")

    deleted = allergens_db.delete_many({})
    print(f"Cleared {deleted.deleted_count} existing allergens from MongoDB")
    allergens_db.insert_many(combined)
    print(f"Seeded {len(combined)} allergens into MongoDB ({len(combined)} total)")


def seed_common_allergens(filepath=None):
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), "common_allergens.json")
    if not os.path.exists(filepath):
        print(f"Cannot seed common allergens: file not found at '{filepath}'")
        print("Run 'python data/scrape_common_allergens.py' first to generate the JSON file.")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        allergens = json.load(f)
    deleted = common_allergens_db.delete_many({})
    print(f"Cleared {deleted.deleted_count} existing common allergens from MongoDB")
    common_allergens_db.insert_many(allergens)
    print(f"Seeded {len(allergens)} common allergens into MongoDB from {filepath}")


if __name__ == "__main__":
    if "--drugs" in sys.argv:
        seed_drugs_from_json()
    elif "--conditions" in sys.argv:
        seed_conditions_from_json()
    elif "--common-allergens" in sys.argv:
        seed_common_allergens()
    elif "--allergens" in sys.argv:
        seed_allergens_from_json()
    elif "--all" in sys.argv:
        seed_all()
        seed_drugs_from_json()
        seed_conditions_from_json()
        seed_allergens_from_json()
        seed_common_allergens()
    else:
        seed_all()