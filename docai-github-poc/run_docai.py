import os, json, glob, pathlib, sys
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

ENDPOINT = os.environ.get("DOCAI_ENDPOINT")
KEY      = os.environ.get("DOCAI_KEY")
MODEL_ID = os.environ.get("MODEL_ID", "prebuilt-invoice")
INPUT_DIR = os.environ.get("INPUT_DIR", "./data/invoices")
DOC_URL   = os.environ.get("DOC_URL")  # if set, analyze that single URL
OUT_DIR   = os.environ.get("OUT_DIR", "./out")

if not ENDPOINT or not KEY:
    sys.exit("Missing DOCAI_ENDPOINT or DOCAI_KEY")

client = DocumentAnalysisClient(ENDPOINT, AzureKeyCredential(KEY))
pathlib.Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

def dump_result(name, result):
    try:
        payload = result.to_dict()
    except AttributeError:
        payload = {"model_id": MODEL_ID, "pages": len(getattr(result, "pages", []))}
    out_path = os.path.join(OUT_DIR, f"{name}.json")
    with open(out_path, "w", encoding="utf-8") as w:
        json.dump(payload, w, indent=2)
    print("Wrote", out_path)

if DOC_URL:
    poller = client.begin_analyze_document_from_url(MODEL_ID, DOC_URL)
    result = poller.result()
    dump_result("from_url", result)
    sys.exit(0)

exts = ("*.pdf", "*.jpg", "*.jpeg", "*.png", "*.tif", "*.tiff")
files = []
for ext in exts:
    files.extend(glob.glob(os.path.join(INPUT_DIR, ext)))
if not files:
    sys.exit(f"No files found under {INPUT_DIR}")

for p in files:
    with open(p, "rb") as f:
        poller = client.begin_analyze_document(MODEL_ID, f)
    result = poller.result()
    base = pathlib.Path(p).with_suffix("").name
    dump_result(base, result)

print(f"Done. Model={MODEL_ID} Files={len(files)} OutputDir={OUT_DIR}")
