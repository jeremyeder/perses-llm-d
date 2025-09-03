#!/bin/bash

# LLM-D Perses Dashboard Deployment Script
# This script deploys the llm-d monitoring dashboard to a Perses instance

set -euo pipefail

# Configuration variables
PERSES_URL="${PERSES_URL:-http://localhost:8080}"
PROJECT_NAME="llm-d-monitoring"
DASHBOARD_NAME="llm-d-comprehensive-monitoring"
DATASOURCE_NAME="prometheus-llm-d"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if required tools are installed
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v curl &> /dev/null; then
        log_error "curl is required but not installed"
        exit 1
    fi
    
    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed"
        exit 1
    fi
    
    if ! command -v yq &> /dev/null; then
        log_warning "yq not found. Install with: pip install yq"
    fi
    
    log_success "Prerequisites check completed"
}

# Function to validate YAML files
validate_yaml_files() {
    log_info "Validating YAML configuration files..."
    
    local files=("project.yaml" "datasource.yaml" "dashboard.yaml")
    
    for file in "${files[@]}"; do
        if [[ ! -f "$file" ]]; then
            log_error "Required file $file not found"
            exit 1
        fi
        
        # Basic YAML validation
        if command -v yq &> /dev/null; then
            if ! yq eval '.' "$file" > /dev/null 2>&1; then
                log_error "Invalid YAML syntax in $file"
                exit 1
            fi
        fi
        
        log_success "Validated $file"
    done
}

# Function to check Perses connectivity
check_perses_connectivity() {
    log_info "Checking Perses connectivity at $PERSES_URL..."
    
    if ! curl -s -o /dev/null -w "%{http_code}" "$PERSES_URL/api/health" | grep -q "200"; then
        log_error "Cannot connect to Perses at $PERSES_URL"
        log_error "Please check the PERSES_URL environment variable and ensure Perses is running"
        exit 1
    fi
    
    log_success "Successfully connected to Perses"
}

# Function to create or update project
deploy_project() {
    log_info "Deploying project configuration..."
    
    local response_code
    response_code=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST \
        -H "Content-Type: application/yaml" \
        --data-binary @project.yaml \
        "$PERSES_URL/api/v1/projects")
    
    case $response_code in
        200|201)
            log_success "Project $PROJECT_NAME deployed successfully"
            ;;
        409)
            log_info "Project already exists, updating..."
            response_code=$(curl -s -o /dev/null -w "%{http_code}" \
                -X PUT \
                -H "Content-Type: application/yaml" \
                --data-binary @project.yaml \
                "$PERSES_URL/api/v1/projects/$PROJECT_NAME")
            
            if [[ "$response_code" == "200" ]]; then
                log_success "Project $PROJECT_NAME updated successfully"
            else
                log_error "Failed to update project (HTTP $response_code)"
                exit 1
            fi
            ;;
        *)
            log_error "Failed to deploy project (HTTP $response_code)"
            exit 1
            ;;
    esac
}

# Function to create or update datasource
deploy_datasource() {
    log_info "Deploying datasource configuration..."
    
    local response_code
    response_code=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST \
        -H "Content-Type: application/yaml" \
        --data-binary @datasource.yaml \
        "$PERSES_URL/api/v1/projects/$PROJECT_NAME/datasources")
    
    case $response_code in
        200|201)
            log_success "Datasource $DATASOURCE_NAME deployed successfully"
            ;;
        409)
            log_info "Datasource already exists, updating..."
            response_code=$(curl -s -o /dev/null -w "%{http_code}" \
                -X PUT \
                -H "Content-Type: application/yaml" \
                --data-binary @datasource.yaml \
                "$PERSES_URL/api/v1/projects/$PROJECT_NAME/datasources/$DATASOURCE_NAME")
            
            if [[ "$response_code" == "200" ]]; then
                log_success "Datasource $DATASOURCE_NAME updated successfully"
            else
                log_error "Failed to update datasource (HTTP $response_code)"
                exit 1
            fi
            ;;
        *)
            log_error "Failed to deploy datasource (HTTP $response_code)"
            exit 1
            ;;
    esac
}

# Function to create or update dashboard
deploy_dashboard() {
    log_info "Deploying dashboard configuration..."
    
    local response_code
    response_code=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST \
        -H "Content-Type: application/yaml" \
        --data-binary @dashboard.yaml \
        "$PERSES_URL/api/v1/projects/$PROJECT_NAME/dashboards")
    
    case $response_code in
        200|201)
            log_success "Dashboard $DASHBOARD_NAME deployed successfully"
            ;;
        409)
            log_info "Dashboard already exists, updating..."
            response_code=$(curl -s -o /dev/null -w "%{http_code}" \
                -X PUT \
                -H "Content-Type: application/yaml" \
                --data-binary @dashboard.yaml \
                "$PERSES_URL/api/v1/projects/$PROJECT_NAME/dashboards/$DASHBOARD_NAME")
            
            if [[ "$response_code" == "200" ]]; then
                log_success "Dashboard $DASHBOARD_NAME updated successfully"
            else
                log_error "Failed to update dashboard (HTTP $response_code)"
                exit 1
            fi
            ;;
        *)
            log_error "Failed to deploy dashboard (HTTP $response_code)"
            exit 1
            ;;
    esac
}

# Function to verify deployment
verify_deployment() {
    log_info "Verifying deployment..."
    
    # Check if project exists
    if curl -s "$PERSES_URL/api/v1/projects/$PROJECT_NAME" | jq -e '.metadata.name' > /dev/null; then
        log_success "Project verification passed"
    else
        log_error "Project verification failed"
        return 1
    fi
    
    # Check if datasource exists
    if curl -s "$PERSES_URL/api/v1/projects/$PROJECT_NAME/datasources/$DATASOURCE_NAME" | jq -e '.metadata.name' > /dev/null; then
        log_success "Datasource verification passed"
    else
        log_error "Datasource verification failed"
        return 1
    fi
    
    # Check if dashboard exists
    if curl -s "$PERSES_URL/api/v1/projects/$PROJECT_NAME/dashboards/$DASHBOARD_NAME" | jq -e '.metadata.name' > /dev/null; then
        log_success "Dashboard verification passed"
    else
        log_error "Dashboard verification failed"
        return 1
    fi
    
    log_success "All components deployed and verified successfully!"
}

# Function to display access information
display_access_info() {
    log_info "Dashboard Access Information:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Dashboard URL: $PERSES_URL/projects/$PROJECT_NAME/dashboards/$DASHBOARD_NAME"
    echo "  Project: $PROJECT_NAME"
    echo "  Dashboard: $DASHBOARD_NAME"
    echo "  Datasource: $DATASOURCE_NAME"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Next Steps:"
    echo "1. Configure Prometheus to expose llm-d metrics"
    echo "2. Update datasource URL in Perses UI if needed"
    echo "3. Set up alerting rules for critical metrics"
    echo "4. Configure authentication and RBAC as needed"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Deploy LLM-D monitoring dashboard to Perses"
    echo ""
    echo "Environment Variables:"
    echo "  PERSES_URL    Perses server URL (default: http://localhost:8080)"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verify   Only verify deployment without deploying"
    echo "  -d, --dry-run  Validate files without deploying"
    echo ""
    echo "Examples:"
    echo "  # Deploy to local Perses instance"
    echo "  $0"
    echo ""
    echo "  # Deploy to remote Perses instance"
    echo "  PERSES_URL=https://perses.example.com $0"
    echo ""
    echo "  # Dry run to validate files"
    echo "  $0 --dry-run"
}

# Main execution function
main() {
    local dry_run=false
    local verify_only=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            -d|--dry-run)
                dry_run=true
                shift
                ;;
            -v|--verify)
                verify_only=true
                shift
                ;;
            *)
                log_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    echo "🚀 LLM-D Perses Dashboard Deployment"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Always check prerequisites and validate files
    check_prerequisites
    validate_yaml_files
    
    if [[ "$dry_run" == true ]]; then
        log_success "Dry run completed successfully - all files are valid"
        exit 0
    fi
    
    if [[ "$verify_only" == true ]]; then
        check_perses_connectivity
        verify_deployment
        exit 0
    fi
    
    # Full deployment
    check_perses_connectivity
    deploy_project
    deploy_datasource
    deploy_dashboard
    verify_deployment
    display_access_info
    
    log_success "LLM-D dashboard deployment completed successfully! 🎉"
}

# Execute main function with all arguments
main "$@"