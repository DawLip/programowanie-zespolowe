#!/bin/bash

OUTPUT_FILE="all-docs.md"
ROOT_DIR="docs"

# Wyczyść plik wynikowy
> "$OUTPUT_FILE"

# Funkcja przetwarzająca katalog w stylu DFS
process_dir() {
  local DIR="$1"

  # Najpierw pliki Markdown w bieżącym katalogu
  for FILE in "$DIR"/*.md; do
    [ -f "$FILE" ] && cat "$FILE" >> "$OUTPUT_FILE" && echo -e "\n\n" >> "$OUTPUT_FILE"
  done

  # Następnie podkatalogi (alfabetycznie)
  for SUBDIR in "$DIR"/*/; do
    [ -d "$SUBDIR" ] && process_dir "$SUBDIR"
  done
}

# Start od katalogu głównego
process_dir "$ROOT_DIR"