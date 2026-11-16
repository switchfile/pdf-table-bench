# Candidates at pinned versions, one venv each (no dependency conflicts between them).
# Docling downloads its models at build time; measurement runs offline.
FROM debian:trixie-slim@sha256:a72b4433de1cf7d6bae0c4cee74d0547f58601a643b3375f070c51600d63b6b2

ENV DEBIAN_FRONTEND=noninteractive PIP_DISABLE_PIP_VERSION_CHECK=1 PYTHONDONTWRITEBYTECODE=1 HOME=/opt/home
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates python3 python3-venv poppler-utils=25.03.0-5+deb13u4 \
      libgl1 libglib2.0-0t64 \
 && rm -rf /var/lib/apt/lists/* && mkdir -p /opt/home && chmod 777 /opt/home
RUN python3 -m venv /opt/markitdown && /opt/markitdown/bin/pip install --no-cache-dir "markitdown[pdf]==0.1.9"
RUN python3 -m venv /opt/pdfplumber && /opt/pdfplumber/bin/pip install --no-cache-dir "pdfplumber==0.11.10"
RUN python3 -m venv /opt/pymupdf4llm && /opt/pymupdf4llm/bin/pip install --no-cache-dir "pymupdf4llm==2.1"
RUN python3 -m venv /opt/docling && /opt/docling/bin/pip install --no-cache-dir \
      --extra-index-url https://download.pytorch.org/whl/cpu "docling==2.150.1" \
 && /opt/docling/bin/docling-tools models download \
 && chmod -R a+rX /opt/home
RUN for v in markitdown pdfplumber pymupdf4llm docling; do echo "== $v"; /opt/$v/bin/pip freeze; done > /opt/versions.txt \
 && pdftotext -v 2>&1 | head -1 >> /opt/versions.txt
ENV HF_HUB_OFFLINE=1 OMP_NUM_THREADS=4 DOCLING_ARTIFACTS_PATH=/opt/home/.cache/docling/models
