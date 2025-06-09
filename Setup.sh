#!/bin/bash

if [ ! -f config.json ]; then
    echo "❌ config.json not found in current directory."
    exit 1
fi

# Read stock symbols from config.json
SYMBOLS=$(jq -r '.stocks[]' config.json)

# Loop through each symbol
for SYMBOL in $SYMBOLS; do
  DIR="${SYMBOL}-Trader"
  mkdir -p "$DIR"

  cat <<EOF > "$DIR/Dockerfile"
FROM python:3.10-slim

WORKDIR /app

COPY setup.py ./
RUN pip install --no-cache-dir .

CMD ["python", "setup.py", "-sy", "${SYMBOL}"]
EOF

  echo "✅ Created Dockerfile for ${SYMBOL} in ${DIR}/Dockerfile"
done
