#!/usr/bin/env python3
"""
Generate a professional Perses dashboard mockup for llm-d monitoring.
Creates a realistic-looking dashboard with sample metrics and data.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch
import numpy as np
from datetime import datetime, timedelta
import random

# Set up the figure with dark theme
plt.style.use('dark_background')
fig = plt.figure(figsize=(20, 14))
fig.patch.set_facecolor('#1a1a1a')

# Dashboard title and header with version info
plt.suptitle('llm-d Platform Monitoring Dashboard v0.51.1', 
             fontsize=24, fontweight='bold', color='#ffffff', y=0.95)

# Add timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
plt.figtext(0.85, 0.92, f'Last Updated: {timestamp}', 
            fontsize=10, color='#888888')

# Define colors
red_hat_red = '#ee0000'
panel_bg = '#2d2d2d'
text_color = '#ffffff'
metric_green = '#28a745'
metric_yellow = '#ffc107' 
metric_red = '#dc3545'

# Create 6x5 grid layout for panels
gs = fig.add_gridspec(6, 5, hspace=0.3, wspace=0.2, 
                      left=0.05, right=0.95, top=0.88, bottom=0.05)

# Panel 1: System Overview - Active Models
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(panel_bg)
ax1.text(0.5, 0.8, 'Active Models', ha='center', va='center', 
         fontsize=14, fontweight='bold', color=text_color)
ax1.text(0.5, 0.4, '12', ha='center', va='center', 
         fontsize=36, fontweight='bold', color=metric_green)
ax1.text(0.5, 0.1, '+2 from last hour', ha='center', va='center', 
         fontsize=10, color=metric_green)
ax1.set_xlim(0, 1)
ax1.set_ylim(0, 1)
ax1.axis('off')

# Panel 2: Total RPS
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(panel_bg)
ax2.text(0.5, 0.8, 'Requests/sec', ha='center', va='center', 
         fontsize=14, fontweight='bold', color=text_color)
ax2.text(0.5, 0.4, '1,247', ha='center', va='center', 
         fontsize=32, fontweight='bold', color=metric_green)
ax2.text(0.5, 0.1, '↗ 15% increase', ha='center', va='center', 
         fontsize=10, color=metric_green)
ax2.set_xlim(0, 1)
ax2.set_ylim(0, 1)
ax2.axis('off')

# Panel 3: System Uptime
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_facecolor(panel_bg)
ax3.text(0.5, 0.8, 'System Uptime', ha='center', va='center', 
         fontsize=14, fontweight='bold', color=text_color)
ax3.text(0.5, 0.4, '99.97%', ha='center', va='center', 
         fontsize=32, fontweight='bold', color=metric_green)
ax3.text(0.5, 0.1, '47 days, 13h', ha='center', va='center', 
         fontsize=10, color='#888888')
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')

# Panel 4: Error Rate
ax4 = fig.add_subplot(gs[0, 3])
ax4.set_facecolor(panel_bg)
ax4.text(0.5, 0.8, 'Error Rate', ha='center', va='center', 
         fontsize=14, fontweight='bold', color=text_color)
ax4.text(0.5, 0.4, '0.03%', ha='center', va='center', 
         fontsize=32, fontweight='bold', color=metric_green)
ax4.text(0.5, 0.1, 'Within SLO', ha='center', va='center', 
         fontsize=10, color=metric_green)
ax4.set_xlim(0, 1)
ax4.set_ylim(0, 1)
ax4.axis('off')

# Panel 5: GPU Utilization
ax5 = fig.add_subplot(gs[0, 4])
ax5.set_facecolor(panel_bg)
ax5.text(0.5, 0.8, 'GPU Utilization', ha='center', va='center', 
         fontsize=14, fontweight='bold', color=text_color)
ax5.text(0.5, 0.4, '78%', ha='center', va='center', 
         fontsize=32, fontweight='bold', color=metric_yellow)
ax5.text(0.5, 0.1, '8/10 GPUs active', ha='center', va='center', 
         fontsize=10, color='#888888')
ax5.set_xlim(0, 1)
ax5.set_ylim(0, 1)
ax5.axis('off')

# Panel 6: Inference Latency Graph (Large panel spanning 2x2)
ax6 = fig.add_subplot(gs[1:3, 0:2])
ax6.set_facecolor(panel_bg)
ax6.set_title('Inference Latency (P50, P95, P99)', fontsize=14, 
              fontweight='bold', color=text_color, pad=20)

# Generate sample latency data
hours = np.arange(0, 24, 0.5)
p50 = 45 + 10 * np.sin(hours/4) + np.random.normal(0, 2, len(hours))
p95 = 120 + 20 * np.sin(hours/4) + np.random.normal(0, 5, len(hours))
p99 = 280 + 40 * np.sin(hours/4) + np.random.normal(0, 10, len(hours))

ax6.plot(hours, p50, color=metric_green, linewidth=2, label='P50', alpha=0.8)
ax6.plot(hours, p95, color=metric_yellow, linewidth=2, label='P95', alpha=0.8)
ax6.plot(hours, p99, color=metric_red, linewidth=2, label='P99', alpha=0.8)
ax6.fill_between(hours, p50, alpha=0.2, color=metric_green)
ax6.fill_between(hours, p95, p50, alpha=0.1, color=metric_yellow)
ax6.fill_between(hours, p99, p95, alpha=0.1, color=metric_red)

ax6.set_xlabel('Hours Ago', color=text_color)
ax6.set_ylabel('Latency (ms)', color=text_color)
ax6.tick_params(colors=text_color)
ax6.legend(loc='upper left')
ax6.grid(True, alpha=0.3)
ax6.set_xlim(0, 24)
ax6.set_ylim(0, 400)

# Add NEW v0.51.1 zoom control indicators
ax6.text(0.95, 0.95, '🔍+ 🔍- ⟲', ha='right', va='top', 
         transform=ax6.transAxes, fontsize=12, color='#888888',
         bbox=dict(boxstyle="round,pad=0.3", facecolor='#3d3d3d', alpha=0.7))

# Panel 7: Token Cost Tracking
ax7 = fig.add_subplot(gs[1:3, 2])
ax7.set_facecolor(panel_bg)
ax7.set_title('Token Costs', fontsize=14, fontweight='bold', 
              color=text_color, pad=20)

# Generate cost data for different time periods
periods = ['Last Hour', 'Last Day', 'Last Week', 'Last Month']
costs = [12.47, 298.50, 2156.78, 8734.25]
colors = [metric_green, metric_green, metric_yellow, metric_red]

bars = ax7.bar(periods, costs, color=colors, alpha=0.8)
ax7.set_ylabel('Cost ($)', color=text_color)
ax7.tick_params(colors=text_color, rotation=45)

# Add value labels on bars
for bar, cost in zip(bars, costs):
    height = bar.get_height()
    ax7.text(bar.get_x() + bar.get_width()/2., height,
             f'${cost:.2f}', ha='center', va='bottom', color=text_color)

# Panel 8: GPU Temperature Gauge
ax8 = fig.add_subplot(gs[1, 3])
ax8.set_facecolor(panel_bg)
ax8.text(0.5, 0.85, 'GPU Temp (Max)', ha='center', va='center', 
         fontsize=12, fontweight='bold', color=text_color)

# Create a simple gauge visualization
theta = np.linspace(0, np.pi, 100)
r = 0.4
x_outer = r * np.cos(theta)
y_outer = r * np.sin(theta)

ax8.plot(x_outer, y_outer, color='#555555', linewidth=8)

# Temperature indicator (72°C out of 90°C max)
temp_angle = np.pi * (72/90)
x_temp = r * np.cos(temp_angle)
y_temp = r * np.sin(temp_angle)
ax8.plot([0, x_temp], [0, y_temp], color=metric_yellow, linewidth=6)

ax8.text(0, -0.1, '72°C', ha='center', va='center', 
         fontsize=20, fontweight='bold', color=metric_yellow)
ax8.text(0, -0.25, 'Safe Range', ha='center', va='center', 
         fontsize=10, color=metric_green)
ax8.set_xlim(-0.6, 0.6)
ax8.set_ylim(-0.4, 0.6)
ax8.axis('off')

# Panel 9: Queue Depth
ax9 = fig.add_subplot(gs[1, 4])
ax9.set_facecolor(panel_bg)
ax9.text(0.5, 0.8, 'Queue Depth', ha='center', va='center', 
         fontsize=12, fontweight='bold', color=text_color)
ax9.text(0.5, 0.4, '23', ha='center', va='center', 
         fontsize=28, fontweight='bold', color=metric_green)
ax9.text(0.5, 0.1, 'Avg wait: 45ms', ha='center', va='center', 
         fontsize=10, color='#888888')
ax9.set_xlim(0, 1)
ax9.set_ylim(0, 1)
ax9.axis('off')

# Panel 10: Memory Usage
ax10 = fig.add_subplot(gs[2, 3])
ax10.set_facecolor(panel_bg)
ax10.text(0.5, 0.8, 'Memory Usage', ha='center', va='center', 
          fontsize=12, fontweight='bold', color=text_color)
ax10.text(0.5, 0.4, '67%', ha='center', va='center', 
          fontsize=28, fontweight='bold', color=metric_yellow)
ax10.text(0.5, 0.1, '42.7GB / 64GB', ha='center', va='center', 
          fontsize=10, color='#888888')
ax10.set_xlim(0, 1)
ax10.set_ylim(0, 1)
ax10.axis('off')

# Panel 11: vLLM Engine Status
ax11 = fig.add_subplot(gs[2, 4])
ax11.set_facecolor(panel_bg)
ax11.text(0.5, 0.8, 'vLLM Engines', ha='center', va='center', 
          fontsize=12, fontweight='bold', color=text_color)
ax11.text(0.5, 0.5, '✓', ha='center', va='center', 
          fontsize=32, fontweight='bold', color=metric_green)
ax11.text(0.5, 0.2, '6/6 Healthy', ha='center', va='center', 
          fontsize=10, color=metric_green)
ax11.text(0.5, 0.05, 'v0.2.1', ha='center', va='center', 
          fontsize=8, color='#888888')
ax11.set_xlim(0, 1)
ax11.set_ylim(0, 1)
ax11.axis('off')

# Panel 12: Throughput Over Time (Large panel)
ax12 = fig.add_subplot(gs[3:5, 0:3])
ax12.set_facecolor(panel_bg)
ax12.set_title('Throughput Metrics', fontsize=14, fontweight='bold', 
               color=text_color, pad=20)

# Generate throughput data
time_points = np.arange(0, 24, 0.25)
base_rps = 800 + 400 * np.sin((time_points - 8) * np.pi / 12)  # Daily pattern
rps = np.maximum(200, base_rps + np.random.normal(0, 50, len(time_points)))

base_tps = rps * 45  # ~45 tokens per request average
tps = base_tps + np.random.normal(0, 1000, len(time_points))

ax12_twin = ax12.twinx()

line1 = ax12.plot(time_points, rps, color=metric_green, linewidth=2, 
                  label='Requests/sec', alpha=0.9)
line2 = ax12_twin.plot(time_points, tps, color=red_hat_red, linewidth=2, 
                       label='Tokens/sec', alpha=0.9)

ax12.fill_between(time_points, rps, alpha=0.2, color=metric_green)
ax12_twin.fill_between(time_points, tps, alpha=0.1, color=red_hat_red)

ax12.set_xlabel('Hours Ago', color=text_color)
ax12.set_ylabel('Requests/sec', color=metric_green)
ax12_twin.set_ylabel('Tokens/sec', color=red_hat_red)

ax12.tick_params(colors=text_color)
ax12_twin.tick_params(colors=text_color)

# Combine legends
lines1, labels1 = ax12.get_legend_handles_labels()
lines2, labels2 = ax12_twin.get_legend_handles_labels()
ax12.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

ax12.grid(True, alpha=0.3)
ax12.set_xlim(0, 24)

# Panel 13: Model Distribution
ax13 = fig.add_subplot(gs[3:5, 3:5])
ax13.set_facecolor(panel_bg)
ax13.set_title('Active Model Distribution', fontsize=14, fontweight='bold', 
               color=text_color, pad=20)

# Pie chart of model types
models = ['Llama-2-7B', 'Llama-2-13B', 'CodeLlama-7B', 'Mistral-7B', 'GPT-3.5-Turbo']
sizes = [35, 25, 15, 15, 10]
colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']

wedges, texts, autotexts = ax13.pie(sizes, labels=models, colors=colors, 
                                    autopct='%1.1f%%', startangle=90)

# Improve text visibility
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

for text in texts:
    text.set_color('white')
    text.set_fontsize(10)

# Panel 14: SLA Status
ax14 = fig.add_subplot(gs[5, 0])
ax14.set_facecolor(panel_bg)
ax14.text(0.5, 0.8, 'SLA Status', ha='center', va='center', 
          fontsize=12, fontweight='bold', color=text_color)
ax14.text(0.5, 0.45, '✓', ha='center', va='center', 
          fontsize=24, fontweight='bold', color=metric_green)
ax14.text(0.5, 0.15, 'All targets met', ha='center', va='center', 
          fontsize=10, color=metric_green)
ax14.set_xlim(0, 1)
ax14.set_ylim(0, 1)
ax14.axis('off')

# Panel 15: Cost per Token
ax15 = fig.add_subplot(gs[5, 1])
ax15.set_facecolor(panel_bg)
ax15.text(0.5, 0.8, 'Cost/1K Tokens', ha='center', va='center', 
          fontsize=12, fontweight='bold', color=text_color)
ax15.text(0.5, 0.4, '$0.0023', ha='center', va='center', 
          fontsize=24, fontweight='bold', color=metric_green)
ax15.text(0.5, 0.1, '12% under budget', ha='center', va='center', 
          fontsize=10, color=metric_green)
ax15.set_xlim(0, 1)
ax15.set_ylim(0, 1)
ax15.axis('off')

# Panel 16: Load Balancer Health
ax16 = fig.add_subplot(gs[5, 2])
ax16.set_facecolor(panel_bg)
ax16.text(0.5, 0.8, 'Load Balancer', ha='center', va='center', 
          fontsize=12, fontweight='bold', color=text_color)
ax16.text(0.5, 0.4, '98.2%', ha='center', va='center', 
          fontsize=24, fontweight='bold', color=metric_green)
ax16.text(0.5, 0.1, 'Distribution eff.', ha='center', va='center', 
          fontsize=10, color='#888888')
ax16.set_xlim(0, 1)
ax16.set_ylim(0, 1)
ax16.axis('off')

# Panel 17: MTTR
ax17 = fig.add_subplot(gs[5, 3])
ax17.set_facecolor(panel_bg)
ax17.text(0.5, 0.8, 'MTTR', ha='center', va='center', 
          fontsize=12, fontweight='bold', color=text_color)
ax17.text(0.5, 0.4, '2.3m', ha='center', va='center', 
          fontsize=24, fontweight='bold', color=metric_green)
ax17.text(0.5, 0.1, 'Target: <5m', ha='center', va='center', 
          fontsize=10, color=metric_green)
ax17.set_xlim(0, 1)
ax17.set_ylim(0, 1)
ax17.axis('off')

# Panel 18: NEW v0.51.1 Table with Pagination
ax18 = fig.add_subplot(gs[5, 4])
ax18.set_facecolor(panel_bg)
ax18.text(0.5, 0.85, 'Model Summary', ha='center', va='center', 
          fontsize=12, fontweight='bold', color=text_color)

# Mini table visualization
table_data = [
    ['Model', 'RPS', 'Latency'],
    ['Llama-2-7B', '245', '95ms'],
    ['Mistral-7B', '189', '87ms'], 
    ['CodeLlama', '156', '102ms']
]

for i, row in enumerate(table_data):
    y_pos = 0.7 - i * 0.15
    if i == 0:  # Header
        ax18.text(0.1, y_pos, ' | '.join(row), ha='left', va='center', 
                  fontsize=8, fontweight='bold', color=text_color)
    else:
        ax18.text(0.1, y_pos, ' | '.join(row), ha='left', va='center', 
                  fontsize=8, color=text_color)

# Pagination indicator
ax18.text(0.5, 0.05, 'Page 1 of 3 (10/page)', ha='center', va='center', 
          fontsize=8, color='#888888')
ax18.set_xlim(0, 1)
ax18.set_ylim(0, 1)
ax18.axis('off')

# Add Red Hat branding
plt.figtext(0.02, 0.02, '© 2024 Red Hat, Inc. | OpenShift AI + llm-d', 
            fontsize=10, color='#888888', alpha=0.7)

# Add Perses logo text and datasource selector
plt.figtext(0.02, 0.92, 'Perses', fontsize=16, fontweight='bold', 
            color=red_hat_red)
plt.figtext(0.15, 0.92, 'Datasource: prometheus-llm-d', fontsize=12, 
            color='#888888')

plt.tight_layout()
plt.savefig('/Users/jeder/repos/perses-llm-d/dashboard-mockup.png', 
            dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
plt.close()

print("Dashboard mockup generated successfully: dashboard-mockup.png")
print("Resolution: 6000x4200 pixels (300 DPI)")
print("File size: ~2-3MB")