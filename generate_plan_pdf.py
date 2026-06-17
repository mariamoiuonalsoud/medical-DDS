from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 6, "AI-Driven Clinical Decision Support System (CDSS) - Development Plan", align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title, level=1):
        if level == 1:
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(20, 60, 120)
            self.cell(0, 10, title)
            self.ln(4)
            self.set_draw_color(20, 60, 120)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)
        elif level == 2:
            self.set_font("Helvetica", "B", 11)
            self.set_text_color(40, 80, 140)
            self.cell(0, 8, title)
            self.ln(7)
        elif level == 3:
            self.set_font("Helvetica", "B", 10)
            self.set_text_color(60, 60, 60)
            self.cell(0, 7, title)
            self.ln(6)

    def body_text(self, text):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def bullet(self, text, indent=15):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.set_x(x + indent)
        self.cell(4, 5, "-")
        self.multi_cell(0, 5, text)
        self.ln(1)

    def code_block(self, text):
        self.set_font("Courier", "", 8)
        self.set_fill_color(240, 240, 245)
        self.set_text_color(30, 30, 30)
        lines = text.split("\n")
        for line in lines:
            self.cell(0, 4.5, "  " + line)
            self.ln(4.5)
        self.ln(2)

    def table_header(self, cols, widths):
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(20, 60, 120)
        self.set_text_color(255, 255, 255)
        for i, col in enumerate(cols):
            self.cell(widths[i], 7, col, border=1, fill=True, align="C")
        self.ln()

    def table_row(self, cols, widths):
        self.set_font("Helvetica", "", 8)
        self.set_text_color(40, 40, 40)
        fill = False
        if hasattr(self, "_row_count"):
            fill = self._row_count % 2 == 0
        else:
            self._row_count = 0
        self._row_count += 1
        if fill:
            self.set_fill_color(235, 240, 250)
        for i, col in enumerate(cols):
            self.cell(widths[i], 6, col, border=1, fill=fill, align="C" if i > 0 else "L")
        self.ln()


def build_pdf():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ── Cover Page ──
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(20, 60, 120)
    pdf.ln(50)
    pdf.cell(0, 12, "AI-Driven Clinical Decision", align="C")
    pdf.ln(12)
    pdf.cell(0, 12, "Support System (CDSS)", align="C")
    pdf.ln(20)
    pdf.set_font("Helvetica", "", 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Development & Architecture Plan", align="C")
    pdf.ln(20)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 8, "Based on the System Requirements Specification (SRS)", align="C")
    pdf.ln(40)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "Advanced Database Systems - Project", align="C")

    # ── Table of Contents ──
    pdf.add_page()
    pdf.section_title("Table of Contents")
    pdf.set_font("Helvetica", "", 10)
    toc = [
        "1.  Project Overview",
        "2.  Current State Analysis",
        "3.  Requirements Gap Analysis",
        "4.  Technology Stack",
        "5.  System Architecture & Data Flow",
        "6.  Implementation Roadmap",
        "7.  File Plan: Create vs Modify",
        "8.  Seed Data Strategy",
        "9.  UI Layout for Validation Page",
        "10. Implementation Sequencing",
    ]
    for item in toc:
        pdf.cell(0, 7, item)
        pdf.ln(7)

    # ── 1. Project Overview ──
    pdf.add_page()
    pdf.section_title("1. Project Overview")
    pdf.body_text(
        'The AI-Driven Clinical Decision Support System (CDSS) is an advanced database system '
        "designed for physicians and clinicians to validate new prescriptions during patient consultations. "
        "It leverages NoSQL Multi-Model architectures and AI to prevent adverse drug events (ADEs) "
        "by cross-referencing new prescriptions with the patient's flexible medical history and existing medications."
    )
    pdf.body_text(
        "The system serves as a point-of-care tool for doctors. When a doctor queries a patient profile "
        "and inputs a proposed medication, the system utilizes a Graph Database model to instantly flag "
        "exact drug-drug interactions or allergen conflicts, while employing a Vector Database and LLM "
        "(RAG pipeline) to generate alternative clinical options and precise medical reasoning."
    )

    # ── 2. Current State Analysis ──
    pdf.section_title("2. Current State Analysis")
    pdf.body_text(
        "The project currently exists as a basic Streamlit + MongoDB patient management system "
        "with the following structure:"
    )
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(30, 30, 30)
    structure = [
        "dds/",
        "  app.py              -- Main entry, page routing",
        "  config/",
        "    database.py        -- MongoDB connection (local:27017, DB: medical_DDS)",
        "  layouts/",
        "    sidebar.py         -- Navigation (Home, Dashboard, Add Patient, View Patients)",
        "  services/",
        "    model.py           -- Empty",
        "    patient_service.py -- CRUD for patients",
        "  ui/",
        "    add_patient.py     -- Form: name, DOB, gender, chronic conditions",
        "    view_patient.py    -- Table view with search",
        "    dashboard.py       -- Empty",
        "    validation.py      -- Empty",
        "  .vscode/",
        "    settings.json",
    ]
    for line in structure:
        pdf.cell(0, 4.5, "  " + line)
        pdf.ln(4.5)
    pdf.ln(3)
    pdf.body_text(
        "Key observations: MongoDB holds patients, medications, and counters collections. "
        "The model.py, dashboard.py, and validation.py files are empty -- the core CDSS "
        "functionality (drug interaction checking, AI clinical advisor) has not been implemented yet."
    )

    # ── 3. Requirements Gap Analysis ──
    pdf.add_page()
    pdf.section_title("3. Requirements Gap Analysis")
    pdf.body_text("Below is the mapping of SRS functional requirements to current implementation status:")

    cols = ["Requirement", "Status", "Gap"]
    widths = [55, 30, 105]
    pdf.table_header(cols, widths)
    rows = [
        ["FR-1.1/1.2  (Doc Store)", "Partial", "Basic patient info exists; no medical history, active meds, or allergies embedded"],
        ["FR-2.1-2.3  (Graph Store)", "Missing", "No Neo4j or graph traversal; no drug interaction or allergy conflict checking"],
        ["FR-3.1-3.3  (Vector & LLM)", "Missing", "No vector DB, no embeddings, no LLM RAG pipeline"],
        ["NFR-1.1  (Deterministic first)", "Missing", "No separation of deterministic vs probabilistic outputs in UI"],
        ["NFR-1.2  (Speed < 1s)", "Missing", "No graph adjacency traversal implemented"],
    ]
    for r in rows:
        pdf.table_row(r, widths)

    pdf.ln(5)
    pdf.body_text(
        "Because the project currently lacks a dedicated graph database (Neo4j), the graph traversal "
        "requirement will be implemented using MongoDB edge documents -- storing drug-drug interactions "
        "and drug-allergen relationships as structured documents with source and target references, "
        "queried via MongoDB aggregation pipelines."
    )

    # ── 4. Technology Stack ──
    pdf.add_page()
    pdf.section_title("4. Technology Stack")
    pdf.body_text("The following technologies were selected after evaluating project constraints and academic context:")

    cols2 = ["Layer", "Technology", "Purpose"]
    widths2 = [35, 55, 100]
    pdf.table_header(cols2, widths2)
    tech_rows = [
        ["Frontend", "Streamlit", "Physician UI -- dashboards, forms, alerts"],
        ["Doc Store", "MongoDB (local)", "Patient charts, medical history, conditions"],
        ["Graph Logic", "MongoDB edge docs", "Drug-drug and drug-allergen relationships (no Neo4j)"],
        ["Vector Store", "ChromaDB (local)", "Semantic search of medical knowledge base"],
        ["Embeddings", "all-MiniLM-L6-v2", "Sentence-transformers for drug/condition vectors"],
        ["LLM", "Ollama + Mistral", "Local RAG pipeline -- no API costs, fully offline"],
        ["Language", "Python 3", "Backend orchestration and data processing"],
    ]
    for r in tech_rows:
        pdf.table_row(r, widths2)

    pdf.ln(4)
    pdf.body_text("Justification for key decisions:")
    pdf.bullet("MongoDB-as-Graph: User has no Neo4j installed; edge documents in MongoDB provide an elegant compromise for an academic project while still demonstrating graph traversal concepts.")
    pdf.bullet("ChromaDB: Lightweight, file-based, no server process needed. Pairs naturally with local development. MongoDB Atlas Vector Search requires cloud migration.")
    pdf.bullet("Ollama + Mistral: Free, fully offline, academic-friendly. Set up with ollama pull mistral. Can be swapped to OpenAI by changing one config value.")

    # ── 5. System Architecture & Data Flow ──
    pdf.add_page()
    pdf.section_title("5. System Architecture & Data Flow")
    pdf.body_text("End-to-end flow when a doctor validates a prescription:")

    pdf.set_font("Courier", "", 8)
    pdf.set_fill_color(230, 235, 245)
    flow = [
        "  Doctor enters Patient ID + Proposed Drug",
        "         |",
        "         v",
        "  +-----------------------------------------+",
        "  |  MongoDB (Document Store)               |",
        "  |  FR-1.1 / FR-1.2                        |",
        "  |  Returns patient chart, meds, allergies  |",
        "  +-------------------+---------------------+",
        "                      | patient data",
        "                      v",
        "  +-----------------------------------------+",
        "  |  MongoDB Edge Documents (Graph Logic)   |",
        "  |  FR-2.1 / FR-2.2 / FR-2.3              |",
        "  |  Graph traversal -> Clinical Alert      |",
        "  |  (High / Moderate / Low severity)        |",
        "  +-------------------+---------------------+",
        "                      | conflict + patient data",
        "                      v",
        "  +-----------------------------------------+",
        "  |  ChromaDB (Vector Store)                |",
        "  |  FR-3.1                                 |",
        "  |  Semantic search for safe alternatives   |",
        "  +-------------------+---------------------+",
        "                      | top-k alternatives",
        "                      v",
        "  +-----------------------------------------+",
        "  |  Ollama + Mistral (LLM RAG Pipeline)    |",
        "  |  FR-3.2 / FR-3.3                        |",
        "  |  Synthesizes clinical brief with:        |",
        "  |   - Biomolecular conflict reason         |",
        "  |   - Recommended alternatives             |",
        "  |   - Dosage timing guidance               |",
        "  +-------------------+---------------------+",
        "                      |",
        "                      v",
        "  +-----------------------------------------+",
        "  |  Streamlit UI                           |",
        "  |  NFR-1.1: Deterministic (alert) FIRST   |",
        "  |            then Probabilistic (LLM)      |",
        "  +-----------------------------------------+",
    ]
    for line in flow:
        pdf.cell(0, 4.5, " " + line)
        pdf.ln(4.5)
    pdf.ln(3)

    pdf.body_text("Architecture notes:")
    pdf.bullet("NFR-1.1 (Separation): The UI displays the deterministic graph-derived alert in a distinct colored banner BEFORE any LLM-generated content. A visual separator and label ('AI Clinical Advisor') clearly distinguish probabilistic content.")
    pdf.bullet("NFR-1.2 (Speed): MongoDB indexes on drug_a, drug_b, and patient_id fields ensure sub-second lookups. For a production system, Neo4j's index-free adjacency would provide faster traversals, but for academic scale (~100 drugs), MongoDB aggregation performs well enough.")

    # ── 6. Implementation Roadmap ──
    pdf.add_page()
    pdf.section_title("6. Implementation Roadmap")
    pdf.body_text("The implementation is organized into six logical phases:")

    pdf.section_title("Phase 1: Enhance Document Store (MongoDB)", level=2)
    pdf.bullet("Define Pydantic models for Patient, Medication, Allergy, DrugInteraction, DrugNode in services/model.py")
    pdf.bullet("Add drug_interactions, drug_kb, allergens collections to config/database.py")
    pdf.bullet("Add service functions: get_patient_by_id(), add_medication(), add_allergy()")
    pdf.bullet("Enhance ui/add_patient.py with fields for current medications, allergies, medical history")
    pdf.bullet("Enhance ui/view_patient.py with full patient chart (history, conditions, active meds, allergies)")

    pdf.section_title("Phase 2: Graph Logic -- Drug Interaction Checking", level=2)
    pdf.bullet("Create services/drug_graph_service.py -- graph traversal logic on MongoDB edge documents")
    pdf.bullet("Drug interaction document schema: { drug_a, drug_b, type, severity, mechanism }")
    pdf.bullet("Functions: check_drug_interaction(patient_id, proposed_drug) -> Alert object")
    pdf.bullet("Match proposed drug vs patient's active medications; match vs patient's allergies")
    pdf.bullet("Return structured alert: severity (high/moderate/low), conflicting items, interaction mechanism")

    pdf.section_title("Phase 3: Vector Store -- ChromaDB", level=2)
    pdf.bullet("Create config/vector_db.py -- ChromaDB client + embedding function (sentence-transformers)")
    pdf.bullet("Create services/rag_service.py with seed_knowledge_base() and vector_search_alternatives()")
    pdf.bullet("Chunk medical knowledge on drug classes and alternatives into vector DB")
    pdf.bullet("Semantic search: given therapeutic class and patient allergies, find safe alternatives")

    pdf.section_title("Phase 4: LLM -- Ollama RAG Pipeline", level=2)
    pdf.bullet("Create services/llm_client.py -- Ollama API abstraction (requests to localhost:11434)")
    pdf.bullet("Build structured prompt: conflict details + alternatives + patient history + system instruction")
    pdf.bullet("Function: query_llm(prompt) -> clinical brief with biomolecular reason, alternatives, dosage timing")
    pdf.bullet("Abstracted interface -- swapping to OpenAI requires changing only the client implementation")

    pdf.section_title("Phase 5: UI -- Prescription Validation Page", level=2)
    pdf.bullet("Transform ui/validation.py into the core CDSS page")
    pdf.bullet("Patient ID lookup with auto-fill patient chart summary")
    pdf.bullet("Drug name input with autocomplete from drug knowledge base")
    pdf.bullet("TOP SECTION (deterministic): Clinical Alert banner -- red/orange/green with severity and details")
    pdf.bullet("BOTTOM SECTION (probabilistic): AI Clinical Advisor box with LLM-generated brief")
    pdf.bullet("Clear visual separator between deterministic and probabilistic content (NFR-1.1)")

    pdf.section_title("Phase 6: Dashboard & Integration", level=2)
    pdf.bullet("Complete ui/dashboard.py with summary stats, recent flagged interactions, quick patient lookup")
    pdf.bullet("Update layouts/sidebar.py with Prescription Validation navigation item")
    pdf.bullet("Wire all pages in app.py")

    # ── 7. File Plan ──
    pdf.add_page()
    pdf.section_title("7. File Plan: Create vs Modify")
    pdf.body_text("Summary of all files to be created and modified during implementation:")

    pdf.section_title("New Files to Create", level=2)
    cols3 = ["File", "Purpose"]
    widths3 = [60, 130]
    pdf.table_header(cols3, widths3)
    new_files = [
        ["services/model.py", "Pydantic models: Patient, Medication, Allergy, DrugInteraction, DrugNode"],
        ["services/drug_graph_service.py", "Drug interaction graph traversal on MongoDB edge documents"],
        ["config/vector_db.py", "ChromaDB client, embedding function, collection management"],
        ["services/rag_service.py", "Vector search, knowledge base seeding, RAG prompt builder"],
        ["services/llm_client.py", "Ollama API abstraction layer"],
        ["data/seed_drugs.py", "Seed ~40 common drugs with therapeutic classes and classifications"],
        ["data/seed_interactions.py", "Seed ~20 known drug-drug interactions with severity and mechanisms"],
        ["data/seed_knowledge.py", "Seed ChromaDB with chunked medical knowledge text"],
    ]
    for r in new_files:
        pdf.table_row(r, widths3)

    pdf.ln(4)
    pdf.section_title("Existing Files to Modify", level=2)
    pdf.table_header(cols3, widths3)
    mod_files = [
        ["config/database.py", "Add drug_interactions, drug_kb, allergens collections"],
        ["services/patient_service.py", "Add: get_patient_by_id(), add_medication(), add_allergy()"],
        ["ui/add_patient.py", "Add fields: current medications, allergies, medical history notes"],
        ["ui/view_patient.py", "Show full patient chart with collapsible sections"],
        ["ui/validation.py", "Full implementation: prescription input, alert display, AI advisor"],
        ["ui/dashboard.py", "Full implementation: physician dashboard with stats and alerts feed"],
        ["layouts/sidebar.py", "Add Prescription Validation navigation option"],
        ["app.py", "Wire validation and dashboard pages"],
    ]
    for r in mod_files:
        pdf.table_row(r, widths3)

    # ── 8. Seed Data Strategy ──
    pdf.add_page()
    pdf.section_title("8. Seed Data Strategy")
    pdf.body_text("To make the system demonstrable, the following seed data will be loaded:")

    pdf.section_title("Drugs (~40 drugs)", level=3)
    pdf.bullet("Analgesics: Aspirin, Acetaminophen, Ibuprofen, Naproxen, Celecoxib, Tramadol")
    pdf.bullet("Anticoagulants: Warfarin, Heparin, Enoxaparin, Rivaroxaban, Apixaban")
    pdf.bullet("Antidiabetics: Metformin, Insulin, Glipizide, Sitagliptin, Empagliflozin")
    pdf.bullet("Cardiovascular: Lisinopril, Losartan, Metoprolol, Atorvastatin, Amlodipine")
    pdf.bullet("Antibiotics: Amoxicillin, Azithromycin, Ciprofloxacin, Doxycycline, Cephalexin")
    pdf.bullet("Psychiatric: Sertraline, Fluoxetine, Alprazolam, Lorazepam, Duloxetine")
    pdf.bullet("GI: Omeprazole, Pantoprazole, Ondansetron, Metoclopramide")
    pdf.bullet("Other: Prednisone, Furosemide, Levothyroxine, Allopurinol")

    pdf.section_title("Drug Interactions (~20 pairs)", level=3)
    pdf.body_text("Example interactions seeded with type, severity, and biomolecular mechanism:")
    pdf.bullet("Warfarin + Aspirin -> HIGH: Increased bleeding risk, synergistic anticoagulation")
    pdf.bullet("Warfarin + Ibuprofen -> HIGH: NSAID inhibits platelet aggregation, increases INR")
    pdf.bullet("ACE Inhibitors + NSAIDs -> HIGH: Reduced antihypertensive effect, risk of renal failure")
    pdf.bullet("Metformin + Contrast Dye -> MODERATE: Risk of lactic acidosis in renal impairment")
    pdf.bullet("Ciprofloxacin + NSAIDs -> MODERATE: Increased risk of CNS stimulation and seizures")
    pdf.bullet("Statins + Macrolide antibiotics -> HIGH: Increased risk of rhabdomyolysis")
    pdf.bullet("SSRIs + MAOIs -> HIGH: Risk of serotonin syndrome")
    pdf.bullet("SSRIs + NSAIDs -> MODERATE: Increased bleeding risk")
    pdf.bullet("Warfarin + Amoxicillin -> MODERATE: Antibiotics alter gut flora, potentiate warfarin")
    pdf.bullet("Metformin + Beta Blockers -> LOW: Beta blockers mask hypoglycemia symptoms")
    pdf.bullet("Aspirin + Ibuprofen -> MODERATE: Ibuprofen may reduce aspirin's cardioprotective effect")

    pdf.section_title("Allergens", level=3)
    pdf.bullet("Drug allergens: Penicillin, Sulfa, Aspirin/NSAIDs, Codeine, ACE Inhibitors, Statins")
    pdf.bullet("Environmental/Other: Latex, Iodine contrast, Peanuts (for excipient checking)")

    pdf.section_title("Knowledge Base (Vector DB)", level=3)
    pdf.body_text(
        "Chunked medical text covering therapeutic classes, mechanism of action, common alternatives, "
        "and dosing guidelines. Each chunk is 100-200 tokens, embedded with all-MiniLM-L6-v2, "
        "stored in ChromaDB with metadata (therapeutic_class, drug_name, source)."
    )

    # ── 9. UI Layout ──
    pdf.add_page()
    pdf.section_title("9. UI Layout for Validation Page")
    pdf.body_text("The prescription validation page is the core interface of the CDSS. Below is the wireframe layout:")

    pdf.set_font("Courier", "", 8)
    pdf.set_fill_color(245, 245, 250)
    layout = [
        "  +--------------------------------------------------+",
        "  |  PATIENT LOOKUP                                   |",
        "  |  Patient ID: [P001]  [Lookup]                     |",
        "  |                                                   |",
        "  |  Patient: John Doe (65, Male)                     |",
        "  |  Conditions: Hypertension, Diabetes, Atrial Fib   |",
        "  |  Active Meds: Metformin, Lisinopril, Warfarin     |",
        "  |  Allergies: Penicillin, Sulfa                     |",
        "  +--------------------------------------------------+",
        "  |  PRESCRIPTION VALIDATION                           |",
        "  |  Proposed Drug: [Aspirin...........]              |",
        "  |  [Check Interaction]                               |",
        "  +--------------------------------------------------+",
        "  |  +----------------------------------------------+ |",
        "  |  |  CLINICAL ALERT -- HIGH RISK                 | |",
        "  |  |  Warfarin + Aspirin: Increased bleeding risk | |",
        "  |  |  Synergistic anticoagulation. Avoid combo.   | |",
        "  |  +----------------------------------------------+ |",
        "  |            --- DETERMINISTIC DATA ABOVE ---       |",
        "  |            --- PROBABILISTIC DATA BELOW ---       |",
        "  |  +----------------------------------------------+ |",
        "  |  |  AI CLINICAL ADVISOR                          | |",
        "  |  |  Generated by AI - for clinical reference     | |",
        "  |  |                                               | |",
        "  |  |  Biomolecular Reason:                         | |",
        "  |  |  Warfarin inhibits vitamin K epoxide          | |",
        "  |  |  reductase; aspirin irreversibly inhibits     | |",
        "  |  |  COX-1. Combined use increases INR >5.       | |",
        "  |  |                                               | |",
        "  |  |  Recommended Alternatives:                   | |",
        "  |  |  - Clopidogrel (less GI bleed risk)          | |",
        "  |  |  - Apixaban (if anticoagulation needed)       | |",
        "  |  |                                               | |",
        "  |  |  Dosage Guidance:                             | |",
        "  |  |  If anticoagulation must continue, monitor    | |",
        "  |  |  INR every 48h. Take with food. Avoid         | |",
        "  |  |  concurrent NSAIDs including OTC.             | |",
        "  |  +----------------------------------------------+ |",
        "  +--------------------------------------------------+",
    ]
    for line in layout:
        pdf.cell(0, 4.5, " " + line)
        pdf.ln(4.5)
    pdf.ln(3)
    pdf.body_text(
        "NFR-1.1 is enforced by the clear visual separator and distinct styling between "
        "the deterministic alert (bordered, red/orange/green) and the probabilistic AI advisor "
        "(boxed, labeled 'Generated by AI')."
    )

    # ── 10. Implementation Sequencing ──
    pdf.add_page()
    pdf.section_title("10. Implementation Sequencing")
    pdf.body_text("The following order ensures each step builds on the previous one: ")

    steps = [
        ["1", "services/model.py", "Define data models", "Foundation for all data structures"],
        ["2", "config/database.py", "Add new collections", "Backend schema expansion"],
        ["3", "services/patient_service.py", "Add lookup & med/allergy functions", "Enhanced data access layer"],
        ["4", "services/drug_graph_service.py", "Interaction checking logic", "Core graph traversal engine"],
        ["5", "config/vector_db.py", "ChromaDB setup", "Vector infrastructure"],
        ["6", "services/llm_client.py", "Ollama client", "LLM integration layer"],
        ["7", "services/rag_service.py", "RAG pipeline", "Combines vectors + LLM"],
        ["8", "data/seed_drugs.py", "Seed drug data", "Populate drug knowledge base"],
        ["9", "data/seed_interactions.py", "Seed interactions", "Populate interaction graph"],
        ["10", "data/seed_knowledge.py", "Seed vector DB", "Populate medical knowledge"],
        ["11", "ui/add_patient.py", "Enhance form", "Richer patient data entry"],
        ["12", "ui/view_patient.py", "Enhance chart view", "Full patient chart display"],
        ["13", "ui/validation.py", "Full implementation", "Core CDSS page"],
        ["14", "ui/dashboard.py", "Full implementation", "Physician dashboard"],
        ["15", "layouts/sidebar.py", "Add nav item", "Navigation update"],
        ["16", "app.py", "Wire all pages", "Final integration"],
    ]
    cols4 = ["#", "File", "Action", "Description"]
    widths4 = [8, 50, 45, 87]
    pdf.table_header(cols4, widths4)
    for s in steps:
        pdf.table_row(s, widths4)

    # ── Save ──
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "CDSS_Development_Plan.pdf"
    )
    pdf.output(output_path)
    return output_path

if __name__ == "__main__":
    path = build_pdf()
    print(f"PDF saved to: {path}")
