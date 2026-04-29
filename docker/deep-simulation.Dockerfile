FROM node:20-bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/daos
COPY . .

RUN node --version \
    && npm --version \
    && python3 --version

VOLUME ["/simulation-output"]

CMD ["python3", "devtools/deep_simulation_audit.py", "--repo", "/workspace/daos", "--transcript", "/simulation-output/daos-v02-deep-simulation-audit.md"]
