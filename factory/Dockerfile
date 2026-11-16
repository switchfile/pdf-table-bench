# Factory: Office original → PDF and truth. Pinned base (digest) and pinned package versions; older Debian states
# are on snapshot.debian.org in case a security update replaced the version on the mirror.
FROM debian:trixie-slim@sha256:a72b4433de1cf7d6bae0c4cee74d0547f58601a643b3375f070c51600d63b6b2

ENV DEBIAN_FRONTEND=noninteractive PYTHONDONTWRITEBYTECODE=1 HOME=/tmp
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      libreoffice-calc-nogui=4:25.2.3-2+deb13u9 libreoffice-writer-nogui=4:25.2.3-2+deb13u9 \
      python3-uno=4:25.2.3-2+deb13u9 poppler-utils=25.03.0-5+deb13u4 qpdf=12.2.0-1 \
      fonts-liberation2=1:2.1.5-3 fonts-crosextra-carlito=20230309-2 fonts-crosextra-caladea=20200211-2 \
      fonts-dejavu-core=2.37-8 fonts-noto-core=20201225-2 \
 && rm -rf /var/lib/apt/lists/* \
 && { soffice --version; pdftotext -v 2>&1 | head -1; qpdf --version | head -1; } > /opt/versions.txt
