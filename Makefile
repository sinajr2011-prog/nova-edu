.PHONY: help install normalize extract demo-sft validate pipeline

help:
	@echo "Nova-Edu development helpers"
	@echo ""
	@echo "  make install       Install basic requirements"
	@echo "  make normalize     Test Persian normalization"
	@echo "  make extract       Show PDF extraction help"
	@echo "  make demo-sft      Generate a demo SFT example"
	@echo "  make pipeline      Run normalize → SFT → save demo"
	@echo "  make validate      Validate sample SFT files"

install:
	pip install -r requirements.txt

normalize:
	python scripts/normalize_persian.py

extract:
	python scripts/extract_pdf_text.py --help

demo-sft:
	python scripts/build_sft_example.py

pipeline:
	python scripts/pipeline_demo.py

validate:
	python scripts/validate_sft.py data/examples/sample_sft.jsonl data/examples/sets_grade9.jsonl
