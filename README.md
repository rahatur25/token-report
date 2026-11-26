# Token Report

A Python tool to analyze text files using the cl100k_base tokenizer.

## Features

- Character count
- Byte count
- Token count
- Bytes per token ratio
- Unicode canonicalization
- Before and after token comparison
- Estimated input cost

## Installation

pip install -r requirements.txt

## Usage

python3 token_report.py report.txt

## Custom price

python3 token_report.py report.txt --price 2.50
