# ArcheoRAG UI

This folder contains a simple Streamlit application that uses
[PaperQA2](https://github.com/Future-House/paper-qa) to query your
personal PDF library.

The app supports different settings profiles such as `fast` or
`contracrow` (for contradiction detection). It can be extended with the
helpers in `paperqa.contrib` to download open‑access papers from sources
like OpenReview or Zotero.

## Requirements

- Python 3.11+
- `streamlit`
- `paper-qa`

Install the dependencies:

```bash
pip install streamlit paper-qa
```

Set your LLM API key (e.g. `OPENAI_API_KEY`) before running the app.

## Usage

From the repository root run:

```bash
streamlit run archeorag/app.py
```

Upload PDFs, select a settings profile and ask questions about your
library.

## Optional: fetch papers automatically

You can fetch open‑access papers with the included helpers. For
instance, to download relevant submissions from an OpenReview venue:

```python
from paperqa import Settings
from paperqa.contrib.openreview_paper_helper import OpenReviewPaperHelper

helper = OpenReviewPaperHelper(Settings.from_name("openreview"), venue_id="ICLR.cc/2025/Conference")
submissions = helper.fetch_relevant_papers("bronze age pottery")
await helper.aadd_docs(submissions, docs)
```
