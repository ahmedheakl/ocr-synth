# Configuration Guide

This project uses multiple configuration files to control various stages of the pipeline.

| Config Type             | Format | Path                                 | Purpose                             |
|------------------------|--------|--------------------------------------|-------------------------------------|
| Synthetic Data Config  | `.json`| `synthetic_data_generation/config/` | Defines document generation options |
| Template Selection     | `.json`| `synthetic_data_generation/templates/templates/` | Defines visual/layout style using json         |
| Layout style    | `.json`| `synthetic_data_generation/templates/template_settings/` | Defines in detail the layout style using json + chart generation flag         |