# Document Intelligence POC (Commercial Azure) — GitHub-hosted test data

**Two ways to test**

### A) Clone & run from Azure ML compute (recommended)
```bash
git clone <your-repo-url> docai-github-poc
cd docai-github-poc
pip install azure-ai-formrecognizer
export DOCAI_ENDPOINT="https://<your-di>.cognitiveservices.azure.com/"
export DOCAI_KEY="<your-key>"
# drop PDFs/JPGs into data/invoices or data/receipts
python run_docai.py
```

### B) Use raw GitHub URLs (public repo only)
```bash
pip install azure-ai-formrecognizer
export DOCAI_ENDPOINT="https://<your-di>.cognitiveservices.azure.com/"
export DOCAI_KEY="<your-key>"
export DOC_URL="https://raw.githubusercontent.com/<you>/<repo>/main/data/invoices/sample1.pdf"
python run_docai.py
```

Notes: Private repos won't work with URL-based analysis (no auth headers). Keep files under ~100 MB. Avoid Git LFS for this POC.
