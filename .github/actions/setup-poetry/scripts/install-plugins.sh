#!/bin/bash
# Install any Poetry plugins that the caller has requested
set -e
if [ ! -z "$POETRY_PLUGINS" ]; then
  while IFS=',' read -ra PARSED; do
    for PLUGIN_NAME in "${PARSED[@]}"; do
      poetry self add "$PLUGIN_NAME"
    done
  done <<< "$POETRY_PLUGINS"
fi 
