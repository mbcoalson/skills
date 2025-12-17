# Skills

A collection of Claude Code skills and automation tools for building energy consulting workflows.

## Overview

This repository contains specialized Claude Code skills for energy modeling, building commissioning, and project management automation. Each skill provides domain-specific knowledge and tooling to streamline workflows in building energy consulting.

## Claude Code Skills

16 specialized skills organized by domain, orchestrated by the work-command-center skill for seamless workflow integration.

### Energy Modeling & Simulation

**[energyplus-assistant](.claude/skills/energyplus-assistant/)** - EnergyPlus IDF analysis, QA/QC validation, HVAC topology analysis, and ECM testing. Fast validation without Docker and comprehensive analysis with MCP tools.

**[diagnosing-energy-models](.claude/skills/diagnosing-energy-models/)** - Troubleshooting for OpenStudio/EnergyPlus models including geometry errors, HVAC validation, LEED Appendix G baseline generation, and systematic diagnostics.

**[energy-efficiency](.claude/skills/energy-efficiency/)** - Comprehensive energy analysis using EnergyPlus, commissioning best practices, and ASHRAE standards for building energy modeling and code compliance.

**[running-openstudio-models](.claude/skills/running-openstudio-models/)** - Work with OpenStudio 3.10 .osm models to adjust HVAC systems, run simulations, apply measures, and validate changes. Includes BCL measure search and download.

**[writing-openstudio-model-measures](.claude/skills/writing-openstudio-model-measures/)** - Write OpenStudio ModelMeasures (Ruby scripts) for programmatic .osm file modifications. Targets OpenStudio 3.9+ with NREL best practices.

### Building Systems & Operations

**[skyspark-analysis](.claude/skills/skyspark-analysis/)** - SkySpark analytics for building automation systems including Axon queries, trend analysis, fault detection, and performance optimization using haystack tagging standards.

**[commissioning-reports](.claude/skills/commissioning-reports/)** - Building commissioning workflows including MBCx procedures, testing protocols, and report generation following ASHRAE Guideline 0 and NEBB standards.

**[writing-oprs](.claude/skills/writing-oprs/)** - Create Owner Project Requirements (OPR) documents for commissioning projects following ASHRAE Standard 202 and Guideline 0. Includes templates, measurable criteria guidance, and system-specific checklists.

**[hvac-specifications](.claude/skills/hvac-specifications/)** - Look up HVAC equipment specifications (capacity, efficiency, dimensions, electrical requirements) by brand and model number. Searches manufacturer websites and processes PDF spec sheets.

**[n8n-automation](.claude/skills/n8n-automation/)** - n8n workflow automation for building analytics including SkySpark multi-agent systems, FastAPI tool servers, and automated building system alert triage.

### Business Development

**[energize-denver-proposals](.claude/skills/energize-denver-proposals/)** - Create Energize Denver compliance proposals including benchmarking, energy audits, compliance pathways, and performance target analysis. Handles cost estimation and timeline planning for Denver Article XIV requirements.

### Project Documentation & Development Tools

**[work-command-center](.claude/skills/work-command-center/)** - Orchestrate work management including deliverables tracking, deadline management, team coordination, priority coaching, and work-life balance. Provides structured task management and delegates to all 16 specialized skills with intelligent decision tree.

**[work-documentation](.claude/skills/work-documentation/)** - Company-specific procedures, standards, templates, and best practices for engineering documentation and professional communication in building energy consulting.

**[skill-builder](.claude/skills/skill-builder/)** - Create and edit Claude Code skills from scratch, design skill workflows, write SKILL.md files, and organize supporting files with intention-revealing names.

**[converting-markdown-to-word](.claude/skills/converting-markdown-to-word/)** - Convert Markdown (.md) files to Microsoft Word (.docx) format for sharing with colleagues. Supports single file or batch conversion.

**[git-pushing](.claude/skills/git-pushing/)** - Automated git workflows with conventional commit messages, staging, and smart push handling with Claude Code footer.

## Additional Tools

### EnergyPlus MCP Server

[EnergyPlus-MCP-main/](./EnergyPlus-MCP-main/) - Python MCP server for EnergyPlus IDF file manipulation, analysis, and HVAC system diagram generation. Provides programmatic access to EnergyPlus functionality through the Model Context Protocol.

## Repository Structure

This repository contains **only** the public-facing Claude Code skills and supporting documentation. Sensitive company data, client projects, and proprietary information are protected by comprehensive `.gitignore` patterns and never committed to this repository.

**What's included:**

- `.claude/skills/` - All 16 Claude Code skills with SKILL.md files and supporting docs
- Documentation, templates, and reference materials
- Scripts and automation tools (Node.js, Ruby, Python)

**What's excluded:**

- Company data and internal documentation
- Client-specific projects and deliverables
- Proprietary spreadsheets and reports
- Local configuration files

## Installation

### Prerequisites

- [Claude Code](https://claude.com/claude-code) - Anthropic's official CLI for Claude
- Node.js (for JavaScript-based tools)
- Python 3.8+ (for Python-based scripts)
- Ruby 2.7+ (for OpenStudio measures)

### Setup

1. Clone this repository to your Claude Code workspace:

   ```bash
   git clone https://github.com/mbcoalson/skills.git
   cd skills
   ```

2. Skills are automatically available in Claude Code when placed in `.claude/skills/`

3. Activate skills by mentioning relevant keywords in conversation with Claude

## Usage

Skills activate automatically based on conversation context. For example:

- "Analyze this EnergyPlus IDF file" → activates `energyplus-assistant`
- "Create a commissioning test procedure" → activates `commissioning-reports`
- "What's my priority today?" → activates `work-command-center`
- "Push these changes to GitHub" → activates `git-pushing`

Each skill directory contains a `SKILL.md` file with detailed usage instructions, activation patterns, and examples.

## Contributing

These skills are tailored for building energy consulting workflows but can be adapted for other domains. Feel free to fork and modify for your own use cases.

## License

Skills and tools in this repository are provided as-is for personal and professional use.

---

**Built with [Claude Code](https://claude.com/claude-code)**
