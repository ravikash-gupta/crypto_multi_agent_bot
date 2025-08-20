import os, joblib, numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score
from utils.dataset import load_dataset, FEATURE_COLUMNS, TARGET_COLUMN
from utils.logger import get_logger
log = get_logger("train_meta")

def main():
    rows = load_dataset()
    if not rows or len(rows) <=1:
        log.error("No data to train on.")
        return
    header = rows[0]; data = rows[1:]
    idxs = [header.index(c) for c in FEATURE_COLUMNS]; tgt = header.index(TARGET_COLUMN)
    X = np.array([[float(r[i]) for i in idxs] for r in data], dtype=float)
    y = np.array([int(r[tgt]) for r in data], dtype=int)
    X_tr, X_te, y_tr, y_te = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)
    model = GradientBoostingClassifier(random_state=42)
    model.fit(X_tr,y_tr)
    prob = model.predict_proba(X_te)[:,1]; pred = (prob>=0.5).astype(int)
    try:
        auc = roc_auc_score(y_te, prob)
    except Exception:
        auc = float('nan')
    acc = accuracy_score(y_te,pred)
    log.info(f"Validation AUC={auc:.3f} ACC={acc:.3f}")
    out_path = os.getenv("AI_META_MODEL_PATH","training/meta_model.pkl")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    joblib.dump(model,out_path)
    log.info(f"Saved model to {out_path}")

if __name__ == '__main__':
    main()
