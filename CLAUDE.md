# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Repository Purpose

This is a Perses dashboard configuration repository for monitoring the llm-d
Kubernetes-native distributed LLM inference platform. The repository contains
production-ready monitoring configurations designed specifically for Red Hat
OpenShift AI environments following SRE best practices.

## Core Architecture

**Configuration-First Approach**: This is primarily a YAML configuration
repository with supporting deployment and visualization tools. The main
deliverables are Perses dashboard definitions, not application code.

**Component Structure**:

- **dashboard.yaml** - Main 29-panel Perses dashboard with 6 monitoring
  sections (System Overview, Performance, Resources, Cost, Quality, vLLM
  Integration)
- **datasource.yaml** - Prometheus datasource configuration with OAuth
  v0.51.1 support
- **project.yaml** - Project-level configuration with security and integration
  settings
- **deploy-dashboard.sh** - Comprehensive deployment script with validation,
  error handling, and verification
- **generate_mockup.py** - Python script for creating realistic dashboard
  visualizations

## Essential Commands

### Deployment Operations

```bash
# Deploy dashboard (primary command)
./deploy-dashboard.sh

# Deploy to remote Perses instance
PERSES_URL=https://perses.example.com ./deploy-dashboard.sh

# Validate configurations without deploying
./deploy-dashboard.sh --dry-run

# Verify existing deployment
./deploy-dashboard.sh --verify
```

### YAML Validation

```bash
# Validate individual files
yq eval '.' dashboard.yaml
yq eval '.' datasource.yaml  
yq eval '.' project.yaml

# Batch validate all YAML files
for file in *.yaml; do yq eval '.' "$file" > /dev/null && \
echo "$file: ✓ Valid" || echo "$file: ✗ Invalid"; done
```

### Mockup Generation

```bash
# Generate dashboard visualization
python3 generate_mockup.py

# Using virtual environment (recommended)
source /Users/jeder/.venv/bin/activate && python generate_mockup.py
```

### Documentation Maintenance

```bash
# Lint markdown files (required before commits)
markdownlint README.md
markdownlint dashboard-documentation.md
```

## Configuration Architecture

### Perses v0.51.1 Features

- **Datasource Variables**: Dynamic datasource selection with `$datasource`
  variable
- **Panel Zoom Controls**: Interactive zoom functionality on TimeSeriesChart
  panels
- **Table Pagination**: 10 items per page for large datasets
- **OAuth Authentication**: Enhanced security for datasource connections

### Variable Hierarchy

```yaml
datasource (StaticListVariable) → cluster → namespace → model → instance
```

All PrometheusLabelValuesVariable queries reference `datasource: name:
"$datasource"` for v0.51.1 compatibility.

### Monitoring Sections Architecture

1. **System Overview** (4 panels) - Health indicators, model counts,
   throughput
2. **Performance Metrics** (5 panels) - Latency percentiles, queue depth,
   load times  
3. **Resource Utilization** (7 panels) - GPU/CPU/memory/network monitoring
4. **Cost & Efficiency** (4 panels) - Token costs, ROI metrics, resource
   optimization
5. **Quality & Reliability** (5 panels) - Error rates, SLA compliance, MTTR
6. **vLLM Integration** (4 panels) - Engine status, memory management, batch
   processing

## Prometheus Metrics Dependencies

The dashboard expects specific metric naming conventions:

- **llm_*** - Core application metrics (requests, latency, costs)
- **vllm_*** - vLLM engine-specific metrics  
- **DCGM_FI_DEV_*** - GPU monitoring via DCGM
- **node_*** - System metrics via node_exporter

## Development Workflow

### Making Dashboard Changes

1. Edit YAML configurations
2. Run `./deploy-dashboard.sh --dry-run` for validation
3. Test deployment in development environment
4. Update mockup with `python3 generate_mockup.py` if visual changes made
5. Run `markdownlint` on any updated documentation

### Environment Requirements

- **Perses**: v0.51.1 or later for full feature compatibility
- **Python**: 3.13+ with matplotlib, numpy for mockup generation
- **Tools**: curl, jq, yq for deployment operations

### Deployment Script Features

- Automatic YAML validation with yq
- HTTP response code handling (200/201 for create, 409 for update conflicts)
- Comprehensive error reporting with colored output
- Resource verification after deployment
- Support for multiple Perses environments via PERSES_URL

## Testing Strategy

**Configuration Testing**: Uses `--dry-run` mode for pre-deployment validation
without side effects

**YAML Validation**: Comprehensive syntax checking with yq before any
deployment

**Integration Testing**: Full deployment cycle with verification of created
resources

**Visual Testing**: Mockup generation ensures dashboard layouts render
correctly

## Critical Configuration Notes

- All TimeSeriesChart panels support zoom controls in v0.51.1
- Table panels include pagination for performance with large datasets  
- OAuth configuration is commented but ready for production deployment
- Variable cascading ensures efficient Prometheus query performance
- Rate limiting configured to prevent Prometheus overload (100 req/s, 200
  burst)

## Production Deployment Considerations

- Update `directUrl` in datasource.yaml for target Prometheus instance
- Configure authentication (OAuth or Bearer tokens) for production
- Verify all required Prometheus metrics are being collected
- Test variable cascading with actual cluster/namespace/model labels
- Ensure RBAC permissions for dashboard project access
