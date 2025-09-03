# LLM-D Comprehensive Monitoring Dashboard

## Overview

This Perses dashboard provides comprehensive monitoring for the llm-d
Kubernetes-native distributed LLM inference platform. It's designed
specifically for Red Hat OpenShift AI environments and follows Google SRE
best practices with a focus on Service Level Objectives (SLOs).

## Dashboard Structure

### 1. System Overview Section

**Purpose**: High-level health and operational status of the llm-d platform.

#### Panels

- **System Overview**:
  - **Query**: `count(up{job=~"llm-d.*", cluster=~"$cluster",
    namespace=~"$namespace"} == 1)`
  - **Meaning**: Number of healthy llm-d services
  - **Thresholds**: Green (≤80), Yellow (81-95), Red (>95)

- **Active Models**:
  - **Query**: `count by (cluster, namespace)
    (llm_model_loaded{cluster=~"$cluster", namespace=~"$namespace",
    model_name=~"$model"} == 1)`
  - **Meaning**: Count of successfully loaded and active LLM models

- **Total Requests/sec**:
  - **Query**: `sum(rate(llm_requests_total{cluster=~"$cluster",
    namespace=~"$namespace", model_name=~"$model"}[5m]))`
  - **Meaning**: Aggregate request throughput across all models

- **System Uptime**:
  - **Query**: `avg(time() - process_start_time_seconds{job=~"llm-d.*",
    cluster=~"$cluster", namespace=~"$namespace"})`
  - **Meaning**: Average uptime of llm-d services

### 2. Performance Metrics Section

**Purpose**: Monitor inference performance, latency, and throughput
characteristics critical for SLO compliance.

#### Panels

- **Inference Latency Percentiles**:
  - **Queries**:
    - P50: `histogram_quantile(0.50,
      rate(llm_inference_duration_seconds_bucket{...}[5m]))`
    - P95: `histogram_quantile(0.95,
      rate(llm_inference_duration_seconds_bucket{...}[5m]))`
    - P99: `histogram_quantile(0.99,
      rate(llm_inference_duration_seconds_bucket{...}[5m]))`
  - **Meaning**: Response time percentiles for inference requests
  - **SRE Value**: Critical for latency SLOs and user experience monitoring

- **Throughput - Requests/sec by Model**:
  - **Query**: `sum by (model_name, instance)
    (rate(llm_requests_total{...}[5m]))`
  - **Meaning**: Request throughput broken down by model and instance
  - **SRE Value**: Capacity planning and load distribution analysis

- **Token Generation Rate**:
  - **Query**: `sum by (model_name)
    (rate(llm_tokens_generated_total{...}[5m]))`
  - **Meaning**: Tokens generated per second by model
  - **SRE Value**: Productivity metric for LLM services

- **Request Queue Depth**:
  - **Query**: `sum by (model_name, instance) (llm_queue_size{...})`
  - **Meaning**: Pending requests waiting for processing
  - **SRE Value**: Early indicator of performance degradation

- **Model Load Time**:
  - **Query**: `llm_model_load_duration_seconds{...}`
  - **Meaning**: Time required to load/reload models
  - **SRE Value**: Service recovery time monitoring

### 3. Resource Utilization Section

**Purpose**: Monitor hardware resource consumption and identify bottlenecks.

#### Panels

- **GPU Utilization**:
  - **Query**: `avg by (node, gpu_id) (DCGM_FI_DEV_GPU_UTIL{...})`
  - **Meaning**: GPU usage percentage by node and GPU
  - **SRE Value**: Resource efficiency and capacity planning

- **GPU Memory Usage**:
  - **Queries**:
    - Used: `DCGM_FI_DEV_FB_USED{...} * 1024 * 1024`
    - Free: `DCGM_FI_DEV_FB_FREE{...} * 1024 * 1024`
  - **Meaning**: GPU memory consumption and availability
  - **SRE Value**: Memory pressure detection and optimization

- **GPU Temperature**:
  - **Query**: `DCGM_FI_DEV_GPU_TEMP{...}`
  - **Meaning**: GPU thermal status
  - **SRE Value**: Hardware health and thermal throttling prevention
  - **Thresholds**: Green (≤70°C), Yellow (71-85°C), Red (>85°C)

- **CPU Usage by Node**:
  - **Query**: `100 - (avg by (node) (irate(node_cpu_seconds_total
    {mode="idle"...}[5m])) * 100)`
  - **Meaning**: CPU utilization across cluster nodes
  - **SRE Value**: Host-level resource monitoring

- **Memory Usage by Node**:
  - **Queries**:
    - Used: `node_memory_MemTotal_bytes{...} -
      node_memory_MemAvailable_bytes{...}`
    - Available: `node_memory_MemAvailable_bytes{...}`
  - **Meaning**: System memory consumption and availability
  - **SRE Value**: Memory pressure and OOM risk assessment

- **Model Cache Storage**:
  - **Query**: `llm_model_cache_size_bytes{...}`
  - **Meaning**: Storage consumed by model cache
  - **SRE Value**: Storage capacity planning

- **Network Traffic**:
  - **Queries**:
    - RX: `rate(node_network_receive_bytes_total
      {device!~"lo|docker.*|veth.*"...}[5m])`
    - TX: `rate(node_network_transmit_bytes_total
      {device!~"lo|docker.*|veth.*"...}[5m])`
  - **Meaning**: Network I/O between llm-d nodes
  - **SRE Value**: Network bottleneck identification

### 4. Cost & Efficiency Section

**Purpose**: Monitor operational costs and resource efficiency metrics.

#### Panels

- **Token Cost Rate**:
  - **Query**: `sum(rate(llm_tokens_generated_total{...}[5m])) *
    on() group_left() llm_token_cost_per_thousand`
  - **Meaning**: Real-time token generation cost
  - **Business Value**: Operational cost monitoring

- **Resource Cost Breakdown**:
  - **Query**: `sum by (resource_type) (llm_resource_cost_per_hour{...})`
  - **Meaning**: Cost allocation by resource type
  - **Business Value**: Cost optimization and budgeting

- **Efficiency - Tokens per Dollar**:
  - **Query**: `rate(llm_tokens_generated_total{...}[5m]) /
    (rate(llm_resource_cost_total{...}[5m]) / 3600)`
  - **Meaning**: Cost efficiency of token generation
  - **Business Value**: ROI measurement for LLM operations

- **Hardware Utilization Rate**:
  - **Query**: `avg(avg by (node) (DCGM_FI_DEV_GPU_UTIL{...}) +
    avg by (node) (100 - (irate(node_cpu_seconds_total
    {mode="idle"...}[5m]) * 100))) / 2`
  - **Meaning**: Overall hardware utilization efficiency
  - **Thresholds**: Red (<50%), Yellow (50-75%), Green (>75%)
  - **Business Value**: Resource optimization metric

### 5. Quality & Reliability Section

**Purpose**: Monitor service reliability, error rates, and SLA compliance.

#### Panels

- **Error Rate**:
  - **Queries**:
    - 4xx: `sum(rate(llm_requests_total{status_code=~"4.."...}[5m])) /
      sum(rate(llm_requests_total{...}[5m])) * 100`
    - 5xx: `sum(rate(llm_requests_total{status_code=~"5.."...}[5m])) /
      sum(rate(llm_requests_total{...}[5m])) * 100`
  - **Meaning**: HTTP error rates for client and server errors
  - **SRE Value**: Error budget monitoring for reliability SLOs

- **Model Health Status**:
  - **Query**: `sum(llm_model_healthy{...} == 1)`
  - **Meaning**: Count of healthy model instances
  - **SRE Value**: Service health monitoring

- **Service Availability (SLA)**:
  - **Query**: `avg_over_time(up{job=~"llm-d.*"...}[1h]) * 100`
  - **Meaning**: Service uptime percentage
  - **SRE Value**: SLA compliance tracking
  - **Thresholds**: Red (<99%), Yellow (99-99.9%), Green (>99.9%)

- **Mean Time To Recovery (MTTR)**:
  - **Query**: `avg(llm_failure_recovery_time_seconds{...})`
  - **Meaning**: Average recovery time from failures
  - **SRE Value**: Incident response effectiveness

- **Load Balancer Health**:
  - **Query**: `sum by (load_balancer) (llm_lb_healthy_backends{...})`
  - **Meaning**: Number of healthy backend instances per load balancer
  - **SRE Value**: Traffic distribution and failover monitoring

### 6. vLLM Integration Section

**Purpose**: Monitor vLLM-specific metrics and performance characteristics.

#### Panels

- **vLLM Engine Status**:
  - **Query**: `count(vllm_engine_running{...} == 1)`
  - **Meaning**: Number of running vLLM inference engines
  - **vLLM Value**: Engine health monitoring

- **vLLM Memory Management**:
  - **Queries**:
    - KV Cache: `vllm_cache_size_bytes{...}`
    - Memory Pool: `vllm_memory_pool_size_bytes{...}`
  - **Meaning**: vLLM-specific memory usage patterns
  - **vLLM Value**: Memory optimization and capacity planning

- **vLLM Batch Processing**:
  - **Query**: `avg by (model_name) (vllm_batch_size{...})`
  - **Meaning**: Average batch sizes processed by vLLM
  - **vLLM Value**: Throughput optimization monitoring

- **vLLM Serving Efficiency**:
  - **Query**: `sum by (model_name)
    (rate(vllm_tokens_generated_total{...}[5m]))`
  - **Meaning**: Token generation rate specifically for vLLM engines
  - **vLLM Value**: vLLM performance comparison and optimization

## Variables Configuration

### Dynamic Filtering Variables

- **cluster**: Select Kubernetes cluster(s) for multi-cluster deployments
- **namespace**: Filter by Kubernetes namespace(s)
- **model**: Select specific LLM model(s) for focused monitoring
- **instance**: Filter by model instance(s) for granular analysis

All variables support:

- Multi-selection for comparative analysis
- "All" option for comprehensive views
- Cascading dependencies (namespace depends on cluster, etc.)

## Datasource Configuration

### Prometheus Integration

- **Default URL**: `http://prometheus:9090`
- **Query Timeout**: 300 seconds for complex queries
- **Connection Timeout**: 30 seconds
- **Health Checks**: Enabled with 30-second intervals
- **Rate Limiting**: 100 requests/second with 200 burst capacity

### Environment-Specific Configurations

- **OpenShift AI**: Use Thanos Querier endpoint
- **Development**: Local Prometheus instance
- **Production**: Authenticated endpoints with TLS

## SRE Integration

This dashboard is designed around key SRE principles:

### Service Level Indicators (SLIs)

- **Latency**: P95/P99 inference response times
- **Availability**: Service uptime percentage
- **Error Rate**: 4xx/5xx error percentages
- **Throughput**: Requests and tokens per second

### Service Level Objectives (SLOs)

- **Latency SLO**: 95% of requests < 2 seconds
- **Availability SLO**: 99.9% uptime
- **Error Budget**: <1% error rate
- **Efficiency SLO**: >75% hardware utilization

### Error Budget Monitoring

- Real-time error rate tracking
- Historical SLO compliance
- Automated alerting on budget burn rate

## Usage Guidelines

### For Site Reliability Engineers

1. Monitor the **Quality & Reliability** section for SLO compliance
2. Use **Performance Metrics** for capacity planning
3. Watch **Resource Utilization** for optimization opportunities
4. Track **Cost & Efficiency** for budget management

### For Platform Engineers

1. Focus on **System Overview** for operational status
2. Use **vLLM Integration** for engine-specific optimization
3. Monitor **Resource Utilization** for infrastructure scaling
4. Analyze **Performance Metrics** for configuration tuning

### For Business Stakeholders

1. Review **Cost & Efficiency** for ROI analysis
2. Monitor **System Overview** for service health
3. Track **Quality & Reliability** for customer impact
4. Use efficiency metrics for investment decisions

## Alert Integration

The dashboard is designed to integrate with Perses alerting rules:

### Critical Alerts

- Service availability < 99%
- Error rate > 5%
- GPU temperature > 85°C
- Queue depth > 1000

### Warning Alerts

- P95 latency > 2 seconds
- GPU utilization > 90%
- Memory usage > 85%
- Cost burn rate > budget

## Maintenance and Updates

### Regular Reviews

- Weekly SLO compliance assessment
- Monthly cost optimization review
- Quarterly dashboard configuration audit
- Annual metric relevance evaluation

### Version Control

- All dashboard configurations are version controlled
- Changes require peer review
- Rollback procedures documented
- Change log maintained

## Technical Requirements

### Prometheus Metrics Required

- Standard node_exporter metrics
- DCGM GPU metrics
- llm-d custom metrics
- vLLM engine metrics
- Kubernetes cluster metrics

### Perses Version

- Minimum Perses v0.40.0
- Prometheus datasource plugin enabled
- TimeSeriesChart, StatChart, GaugeChart plugins

### OpenShift AI Integration

- Service Monitor configurations
- RBAC permissions for metric collection
- Network policies for Prometheus access
- Storage for historical data retention

This dashboard provides comprehensive monitoring coverage for llm-d
deployments, ensuring operational excellence through data-driven insights
and proactive monitoring capabilities.