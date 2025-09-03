# LLM-D Perses Monitoring Dashboard

A comprehensive Perses dashboard for monitoring the llm-d Kubernetes-native
distributed LLM inference platform, designed specifically for Red Hat
OpenShift AI environments.

## Overview

This project provides production-ready monitoring for llm-d deployments with:

- **Comprehensive metrics coverage** - System health, performance, resources,
  cost, and reliability
- **SRE-focused design** - Built around Google SRE principles with SLO
  monitoring
- **vLLM integration** - Specialized panels for vLLM engine metrics
- **Dynamic filtering** - Multi-dimensional variables for flexible analysis
- **OpenShift AI optimized** - Tailored for Red Hat OpenShift AI environments

## Features

### Six Monitoring Sections

1. **System Overview** - High-level health and operational status
2. **Performance Metrics** - Inference latency, throughput, and queue
   monitoring
3. **Resource Utilization** - GPU, CPU, memory, and storage monitoring
4. **Cost & Efficiency** - Token costs, resource optimization, and ROI tracking
5. **Quality & Reliability** - Error rates, SLA compliance, and MTTR monitoring
6. **vLLM Integration** - Engine-specific performance and memory management

### Key Capabilities

- **Real-time monitoring** with 30-second refresh intervals
- **Multi-cluster support** with cascading variable filters
- **Cost tracking** and efficiency optimization metrics
- **SLO compliance** monitoring with error budget tracking
- **Hardware health** monitoring including GPU temperature and utilization
- **Load balancer** and traffic distribution monitoring

### NEW v0.51.1 Features

- **Datasource Variables** - Dynamic datasource selection for
  multi-environment support
- **Panel Zoom Controls** - Interactive zoom in/out/reset functionality on
  time series charts
- **Table Pagination** - Efficient handling of large datasets with
  customizable page sizes
- **OAuth Authentication** - Enhanced security with OAuth2 support for
  datasources
- **Custom Lint Rules** - Dashboard validation with custom linting
  capabilities

## Quick Start

### Prerequisites

- Perses v0.51.1 or later (includes latest features)
- Prometheus with llm-d metrics collection
- Required tools: `curl`, `jq`, `yq` (recommended for validation)

### 1. Deploy Dashboard

```bash
# Clone or download the dashboard files
git clone <repository-url>
cd perses-llm-d

# Deploy to local Perses instance
./deploy-dashboard.sh

# Deploy to remote Perses instance
PERSES_URL=https://perses.example.com ./deploy-dashboard.sh
```

### 2. Configure Prometheus

Ensure your Prometheus instance collects the required metrics:

- Standard `node_exporter` metrics for system monitoring
- DCGM GPU metrics for hardware monitoring
- llm-d custom metrics for application monitoring
- vLLM engine metrics for specialized monitoring

### 3. Access Dashboard

Navigate to your Perses instance:

```text
https://your-perses-instance/projects/llm-d-monitoring/dashboards/llm-d-comprehensive-monitoring
```

## Configuration

### Environment Variables

- `PERSES_URL` - Perses server URL (default: `http://localhost:8080`)

### Datasource Configuration

Update `datasource.yaml` for your environment:

```yaml
# For OpenShift AI
directUrl: https://thanos-querier-openshift-monitoring.apps.cluster.example.com

# For development
directUrl: http://localhost:9090

# For production with authentication
proxy:
  kind: HTTPProxy
  spec:
    headers:
      Authorization: "Bearer ${PROMETHEUS_TOKEN}"
```

### Variable Customization

The dashboard includes four dynamic variables:

- **cluster** - Filter by Kubernetes cluster
- **namespace** - Filter by namespace
- **model** - Filter by LLM model name
- **instance** - Filter by model instance

## Metrics Reference

### Required Prometheus Metrics

#### Core llm-d Metrics

```prometheus
# Request metrics
llm_requests_total{cluster, namespace, model_name, status_code}
llm_inference_duration_seconds_bucket{cluster, namespace, model_name}
llm_tokens_generated_total{cluster, namespace, model_name}
llm_queue_size{cluster, namespace, model_name, instance}

# Model metrics
llm_model_loaded{cluster, namespace, model_name}
llm_model_healthy{cluster, namespace, model_name}
llm_model_load_duration_seconds{cluster, namespace, model_name}
llm_model_cache_size_bytes{cluster, namespace}

# Cost metrics
llm_token_cost_per_thousand
llm_resource_cost_per_hour{cluster, namespace, resource_type}
llm_resource_cost_total{cluster, namespace, model_name}

# Reliability metrics
llm_failure_recovery_time_seconds{cluster, namespace}
llm_lb_healthy_backends{cluster, namespace, load_balancer}
```

#### vLLM-Specific Metrics

```prometheus
# Engine metrics
vllm_engine_running{cluster, namespace}
vllm_cache_size_bytes{cluster, namespace, model_name}
vllm_memory_pool_size_bytes{cluster, namespace, model_name}
vllm_batch_size{cluster, namespace, model_name}
vllm_tokens_generated_total{cluster, namespace, model_name}
```

#### System Metrics (node_exporter)

```prometheus
# CPU and memory
node_cpu_seconds_total{mode, node}
node_memory_MemTotal_bytes{node}
node_memory_MemAvailable_bytes{node}

# Network
node_network_receive_bytes_total{device, node}
node_network_transmit_bytes_total{device, node}

# Process metrics
process_start_time_seconds{job}
up{job, cluster, namespace}
```

#### GPU Metrics (DCGM)

```prometheus
# GPU utilization and memory
DCGM_FI_DEV_GPU_UTIL{cluster, namespace, node, gpu_id}
DCGM_FI_DEV_FB_USED{cluster, namespace, node, gpu}
DCGM_FI_DEV_FB_FREE{cluster, namespace, node, gpu}
DCGM_FI_DEV_GPU_TEMP{cluster, namespace, node, gpu}
```

## Deployment Options

### Manual Deployment

1. **Project Setup**

   ```bash
   curl -X POST -H "Content-Type: application/yaml" \
     --data-binary @project.yaml \
     http://localhost:8080/api/v1/projects
   ```

2. **Datasource Creation**

   ```bash
   curl -X POST -H "Content-Type: application/yaml" \
     --data-binary @datasource.yaml \
     http://localhost:8080/api/v1/projects/llm-d-monitoring/datasources
   ```

3. **Dashboard Deployment**

   ```bash
   curl -X POST -H "Content-Type: application/yaml" \
     --data-binary @dashboard.yaml \
     http://localhost:8080/api/v1/projects/llm-d-monitoring/dashboards
   ```

### GitOps Deployment

For GitOps workflows, include the YAML files in your Perses configuration
repository:

```text
perses-config/
├── projects/
│   └── llm-d-monitoring.yaml
├── datasources/
│   └── prometheus-llm-d.yaml
└── dashboards/
    └── llm-d-comprehensive-monitoring.yaml
```

## Customization

### Adding Custom Panels

1. Edit `dashboard.yaml`
2. Add new panel to the `panels` array
3. Update the `layouts` section to position the panel
4. Redeploy using `./deploy-dashboard.sh`

### Modifying Queries

Common customizations:

```yaml
# Change time window
rate(metric_name[5m])  # 5-minute rate
rate(metric_name[1m])  # 1-minute rate

# Add label filters
metric_name{environment="production"}

# Aggregate across dimensions
sum by (cluster) (metric_name)
avg by (model_name) (metric_name)
```

### Custom Variables

Add new variables to the dashboard:

```yaml
variables:
  - kind: ListVariable
    spec:
      name: environment
      display:
        name: "Environment"
      plugin:
        kind: PrometheusLabelValuesVariable
        spec:
          labelName: environment
          matchers:
            - __name__=~"llm_.*"
```

## Alerting Integration

The dashboard is designed to work with Perses alerting rules. Example alert
configurations:

### Critical Alerts

```yaml
# High error rate alert
- alert: LLMDHighErrorRate
  expr: |
    sum(rate(llm_requests_total{status_code=~"5.."}[5m])) /
    sum(rate(llm_requests_total[5m])) * 100 > 5
  for: 2m
  severity: critical

# Service down alert  
- alert: LLMDServiceDown
  expr: up{job=~"llm-d.*"} == 0
  for: 1m
  severity: critical

# GPU overheating alert
- alert: GPUOverheating
  expr: DCGM_FI_DEV_GPU_TEMP > 85
  for: 5m
  severity: critical
```

### Warning Alerts

```yaml
# High latency alert
- alert: LLMDHighLatency
  expr: |
    histogram_quantile(0.95,
      rate(llm_inference_duration_seconds_bucket[5m])) > 2
  for: 5m
  severity: warning

# High queue depth alert
- alert: LLMDHighQueueDepth
  expr: llm_queue_size > 1000
  for: 5m
  severity: warning
```

## Troubleshooting

### Common Issues

1. **Dashboard not loading**
   - Check Perses connectivity: `curl $PERSES_URL/api/health`
   - Verify project exists:
     `curl $PERSES_URL/api/v1/projects/llm-d-monitoring`

2. **No data in panels**
   - Verify Prometheus connectivity in datasource settings
   - Check if metrics are being collected:
     `curl $PROMETHEUS_URL/api/v1/label/__name__/values | grep llm_`

3. **Variables not working**
   - Ensure label values exist in metrics
   - Check metric naming conventions match queries

### Debugging Commands

```bash
# Validate YAML syntax
yq eval '.' dashboard.yaml

# Check Perses API
curl -s $PERSES_URL/api/v1/projects/llm-d-monitoring | jq .

# Test Prometheus queries
curl -s "$PROMETHEUS_URL/api/v1/query?query=up{job=~\"llm-d.*\"}"

# Verify deployment
./deploy-dashboard.sh --verify
```

## SRE Best Practices

### Service Level Objectives (SLOs)

The dashboard supports monitoring these SLOs:

- **Availability SLO**: 99.9% uptime
- **Latency SLO**: 95% of requests < 2 seconds
- **Error Budget**: < 1% error rate
- **Efficiency SLO**: > 75% hardware utilization

### Error Budget Monitoring

Use the Quality & Reliability section to track:

- Error rate over time
- SLA compliance percentage
- Mean time to recovery (MTTR)

### Capacity Planning

Use the Resource Utilization section for:

- Hardware scaling decisions
- Cost optimization opportunities
- Performance bottleneck identification

## Contributing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes to YAML configurations
4. Test with `./deploy-dashboard.sh --dry-run`
5. Deploy to test environment
6. Submit pull request

### Code Standards

- Use consistent YAML formatting
- Follow Perses naming conventions
- Document all custom queries
- Include panel descriptions
- Validate with linters before submission

## Support

### Documentation

- [Dashboard Documentation](./dashboard-documentation.md) - Detailed panel
  explanations
- [Perses Documentation](https://perses.dev/docs) - Official Perses
  documentation
- [PromQL Guide](https://prometheus.io/docs/prometheus/latest/querying/basics/)
  - Prometheus query language

### Getting Help

- Check the troubleshooting section above
- Review Perses logs for deployment issues
- Validate Prometheus metric collection
- Test queries in Prometheus UI before adding to dashboard

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file
for details.

## Acknowledgments

- llm-d project team for the inference platform
- Red Hat OpenShift AI team for integration support  
- Perses community for the observability platform
- SRE community for monitoring best practices
