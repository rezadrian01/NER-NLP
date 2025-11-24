#!/bin/bash

# ==============================================================================
# NLP Knowledge Graph Pipeline - Complete Setup and Execution Script
# ==============================================================================
# This script automates the entire pipeline:
# 1. Environment setup (virtual environment + dependencies)
# 2. NER model training
# 3. Model evaluation and comparison
# 4. Knowledge graph construction
# 5. Results logging and reporting
# ==============================================================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Project paths
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_DIR}/venv"
OUTPUT_DIR="${PROJECT_DIR}/output"
MODELS_DIR="${PROJECT_DIR}/models"
LOG_FILE="${OUTPUT_DIR}/pipeline_execution.log"

# Create output directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}"

# ==============================================================================
# Logging Functions
# ==============================================================================

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "${LOG_FILE}"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "${LOG_FILE}"
}

log_warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "${LOG_FILE}"
}

log_info() {
    echo -e "${CYAN}[$(date +'%Y-%m-%d %H:%M:%S')] INFO:${NC} $1" | tee -a "${LOG_FILE}"
}

log_section() {
    echo -e "\n${MAGENTA}======================================================================${NC}" | tee -a "${LOG_FILE}"
    echo -e "${MAGENTA}  $1${NC}" | tee -a "${LOG_FILE}"
    echo -e "${MAGENTA}======================================================================${NC}\n" | tee -a "${LOG_FILE}"
}

# ==============================================================================
# Environment Setup
# ==============================================================================

setup_environment() {
    log_section "STEP 1: Environment Setup"
    
    # Check if virtual environment exists
    if [ -d "${VENV_DIR}" ]; then
        log_info "Virtual environment found at: ${VENV_DIR}"
    else
        log "Creating new virtual environment..."
        python3 -m venv "${VENV_DIR}"
        log "✓ Virtual environment created successfully"
    fi
    
    # Activate virtual environment
    log "Activating virtual environment..."
    source "${VENV_DIR}/bin/activate"
    log "✓ Virtual environment activated"
    
    # Upgrade pip
    log "Upgrading pip..."
    pip install --upgrade pip --quiet
    log "✓ pip upgraded"
    
    # Install dependencies
    log "Installing dependencies from requirements.txt..."
    pip install -r "${PROJECT_DIR}/requirements.txt" --quiet
    log "✓ Dependencies installed"
    
    # Check if spaCy model is installed
    log "Checking spaCy multilingual model..."
    if python3 -c "import spacy; spacy.load('xx_ent_wiki_sm')" 2>/dev/null; then
        log "✓ spaCy multilingual model found"
    else
        log "Downloading spaCy multilingual model (xx_ent_wiki_sm)..."
        python3 -m spacy download xx_ent_wiki_sm
        log "✓ spaCy model downloaded"
    fi
    
    log_info "Environment setup completed successfully!"
}

# ==============================================================================
# NER Model Training
# ==============================================================================

train_ner_model() {
    log_section "STEP 2: NER Model Training"
    
    log "Starting NER model training..."
    log_info "Training data: ${MODELS_DIR}/train_data.json"
    log_info "Test data: ${MODELS_DIR}/test_data.json"
    log_info "Output model: ${MODELS_DIR}/custom_ner_model/"
    
    python3 "${PROJECT_DIR}/ner_trainer.py" 2>&1 | tee -a "${LOG_FILE}"
    
    if [ -d "${MODELS_DIR}/custom_ner_model" ]; then
        log "✓ NER model training completed successfully!"
        log_info "Model saved to: ${MODELS_DIR}/custom_ner_model/"
    else
        log_error "Model training failed - model directory not found"
        exit 1
    fi
}

# ==============================================================================
# NER Model Evaluation
# ==============================================================================

evaluate_ner_model() {
    log_section "STEP 3: NER Model Evaluation & Comparison"
    
    log "Evaluating and comparing NER models..."
    log_info "Custom model: ${MODELS_DIR}/custom_ner_model/"
    log_info "Baseline model: xx_ent_wiki_sm (multilingual)"
    
    python3 "${PROJECT_DIR}/compare_ner_models.py" 2>&1 | tee -a "${LOG_FILE}"
    
    if [ -f "${OUTPUT_DIR}/ner_evaluation_comparison.html" ]; then
        log "✓ Model evaluation completed successfully!"
        log_info "HTML Report: ${OUTPUT_DIR}/ner_evaluation_comparison.html"
        log_info "JSON Report: ${OUTPUT_DIR}/ner_evaluation_comparison.json"
    else
        log_error "Model evaluation failed - output files not found"
        exit 1
    fi
}

# ==============================================================================
# Knowledge Graph Construction
# ==============================================================================

build_knowledge_graph() {
    log_section "STEP 4: Knowledge Graph Construction"
    
    log "Building knowledge graph with custom NER model..."
    log_info "Input data: ${MODELS_DIR}/full_data.json"
    log_info "NER model: ${MODELS_DIR}/custom_ner_model/"
    log_info "Extraction methods: Regex (42 patterns) + Dependency Parsing + Co-occurrence Statistics"
    
    python3 "${PROJECT_DIR}/build_knowledge_graph.py" 2>&1 | tee -a "${LOG_FILE}"
    
    if [ -f "${OUTPUT_DIR}/knowledge_graph.html" ]; then
        log "✓ Knowledge graph construction completed successfully!"
        log_info "Interactive Graph: ${OUTPUT_DIR}/knowledge_graph.html"
        log_info "Graph Data: ${OUTPUT_DIR}/knowledge_graph.json"
    else
        log_error "Knowledge graph construction failed - output files not found"
        exit 1
    fi
}

# ==============================================================================
# Results Summary
# ==============================================================================

show_results() {
    log_section "PIPELINE EXECUTION COMPLETED!"
    
    echo -e "\n${GREEN}╔════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                          RESULTS SUMMARY                               ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════════════╝${NC}\n"
    
    echo -e "${CYAN}📊 NER Model Evaluation Results:${NC}"
    echo -e "   └─ HTML Report: ${BLUE}${OUTPUT_DIR}/ner_evaluation_comparison.html${NC}"
    echo -e "   └─ JSON Data:   ${BLUE}${OUTPUT_DIR}/ner_evaluation_comparison.json${NC}"
    
    echo -e "\n${CYAN}🕸️  Knowledge Graph Results:${NC}"
    echo -e "   └─ Interactive Visualization: ${BLUE}${OUTPUT_DIR}/knowledge_graph.html${NC}"
    echo -e "   └─ Graph JSON Data:           ${BLUE}${OUTPUT_DIR}/knowledge_graph.json${NC}"
    
    echo -e "\n${CYAN}🤖 Trained NER Model:${NC}"
    echo -e "   └─ Model Files: ${BLUE}${MODELS_DIR}/custom_ner_model/${NC}"
    
    echo -e "\n${CYAN}📝 Execution Log:${NC}"
    echo -e "   └─ Full Log: ${BLUE}${LOG_FILE}${NC}"
    
    echo -e "\n${CYAN}🎨 Entity-specific Visualizations:${NC}"
    if [ -d "${OUTPUT_DIR}/entity_visualizations" ]; then
        ENTITY_COUNT=$(ls -1 "${OUTPUT_DIR}/entity_visualizations"/*.html 2>/dev/null | wc -l)
        echo -e "   └─ ${ENTITY_COUNT} entity visualizations in: ${BLUE}${OUTPUT_DIR}/entity_visualizations/${NC}"
    fi
    
    echo -e "\n${GREEN}╔════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                     HOW TO VIEW RESULTS                                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════════════╝${NC}\n"
    
    echo -e "${YELLOW}🌐 To view the interactive visualizations:${NC}"
    echo -e "   1. Open in browser:"
    echo -e "      ${BLUE}file://${OUTPUT_DIR}/knowledge_graph.html${NC}"
    echo -e "      ${BLUE}file://${OUTPUT_DIR}/ner_evaluation_comparison.html${NC}"
    echo -e "\n   2. Or use command:"
    echo -e "      ${CYAN}xdg-open ${OUTPUT_DIR}/knowledge_graph.html${NC}"
    echo -e "      ${CYAN}xdg-open ${OUTPUT_DIR}/ner_evaluation_comparison.html${NC}"
    
    echo -e "\n${YELLOW}📊 Quick Stats:${NC}"
    if [ -f "${OUTPUT_DIR}/knowledge_graph.json" ]; then
        echo -e "   └─ Knowledge Graph Statistics:"
        python3 -c "
import json
with open('${OUTPUT_DIR}/knowledge_graph.json', 'r') as f:
    data = json.load(f)
    print(f'      • Entities: {len(data.get(\"nodes\", []))}')
    print(f'      • Relations: {len(data.get(\"edges\", []))}')
" 2>/dev/null || echo "      (Run complete to see stats)"
    fi
    
    echo -e "\n${GREEN}✨ All pipeline steps completed successfully!${NC}\n"
}

# ==============================================================================
# Main Execution
# ==============================================================================

main() {
    clear
    echo -e "${MAGENTA}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║          NLP KNOWLEDGE GRAPH PIPELINE - AUTOMATED EXECUTION               ║
║                                                                           ║
║  This script will:                                                        ║
║  • Set up Python virtual environment                                     ║
║  • Install all required dependencies                                     ║
║  • Train custom NER model                                                ║
║  • Evaluate and compare models                                           ║
║  • Build knowledge graph with 3 extraction methods                       ║
║  • Generate interactive visualizations                                   ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}\n"
    
    # Record start time
    START_TIME=$(date +%s)
    
    # Initialize log file
    echo "Pipeline Execution Log - Started at $(date)" > "${LOG_FILE}"
    echo "========================================" >> "${LOG_FILE}"
    
    # Execute pipeline steps
    setup_environment
    train_ner_model
    evaluate_ner_model
    build_knowledge_graph
    
    # Calculate execution time
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    MINUTES=$((DURATION / 60))
    SECONDS=$((DURATION % 60))
    
    log_section "Execution Time: ${MINUTES}m ${SECONDS}s"
    
    # Show results
    show_results
}

# ==============================================================================
# Error Handling
# ==============================================================================

trap 'log_error "Pipeline failed at step: $BASH_COMMAND"; exit 1' ERR

# ==============================================================================
# Run Main Function
# ==============================================================================

main "$@"
