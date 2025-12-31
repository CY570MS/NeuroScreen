# phase1/predict_BBB_drugs.py
import os
import pandas as pd
import joblib
from B3DB import B3DB_DATA_DICT
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# -----------------------------------------
# Configuration
# -----------------------------------------
# Define where outputs should go
OUTPUT_DIR = "phase1/outputs" 
MODEL_PATH = os.path.join(OUTPUT_DIR, "phase1_model.pkl")
CSV_PATH = os.path.join(OUTPUT_DIR, "bbb_positive_drugs_v2.csv")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    print("🧠 Phase 1: Loading B3DB Dataset...")
    
    # 1. Load the extended classification dataset
    df_ext = B3DB_DATA_DICT["B3DB_classification_extended"]
    
    print(f"   - Total compounds loaded: {len(df_ext)}")

    # 2. Prepare features (X) and target (y)
    # removing metadata columns to leave only numerical features
    X_ext = df_ext.drop(columns=[
        "compound_name", "IUPAC_name", "SMILES", "BBB+/BBB-",
        "Inchi", "reference", "group", "comments"
    ]).values

    # Map target: BBB+ = 1, BBB- = 0
    y_ext = df_ext["BBB+/BBB-"].map({"BBB+": 1, "BBB-": 0}).values

    # 3. Train/Test Split
    print("⚙️  Training Random Forest Model...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_ext, y_ext, test_size=0.2, random_state=42, stratify=y_ext
    )

    # 4. Train Model
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # 5. Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model Accuracy: {acc:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 6. Save the Model (Local File)
    joblib.dump(model, MODEL_PATH)
    print(f"💾 Model saved to: {MODEL_PATH}")

    # 7. Extract BBB+ Candidates for Phase 2
    print("🔍 Extracting known BBB+ drugs for Phase 2...")
    
    # Filter for drugs that are actually BBB+ in the dataset
    bbb_positive = df_ext[df_ext["BBB+/BBB-"] == "BBB+"]
    
    # Select useful columns
    final_list = bbb_positive[["compound_name", "SMILES"]]
    
    # Save to CSV
    final_list.to_csv(CSV_PATH, index=False)
    print(f"📄 Candidate list saved to: {CSV_PATH}")
    print(f"   - Count: {len(final_list)} drugs ready for analysis.")

if __name__ == "__main__":
    main()