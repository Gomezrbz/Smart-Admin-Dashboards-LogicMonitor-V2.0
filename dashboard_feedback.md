<div class="azure-cost-section">
	<style>
		.azure-cost-section {
			font-family: Arial, Helvetica, sans-serif; background: linear-gradient(135deg, #0f172a 0%, #1e293b 55%, #0f766e 100%); color: #ffffff; border-radius: 14px; padding: 22px; box-sizing: border-box; box-shadow: 0 6px 18px rgba(15, 23, 42, 0.25);
		}
		
		.azure-cost-header {
			display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; margin-bottom: 22px;
		}
		
		.azure-cost-title h2 {
			margin: 0 0 6px 0; font-size: 24px; font-weight: 700; letter-spacing: 0.2px;
		}
		
		.azure-cost-title p {
			margin: 0; font-size: 14px; color: #cbd5e1; max-width: 760px; line-height: 1.5;
		}
		
		.azure-cost-badge {
			background: rgba(255, 255, 255, 0.14); border: 1px solid rgba(255, 255, 255, 0.22); border-radius: 999px; padding: 8px 14px; font-size: 13px; white-space: nowrap; color: #e0f2fe;
		}
		
		.azure-cost-grid {
			display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-bottom: 18px;
		}
		
		.azure-cost-card {
			background: rgba(15, 23, 42, 0.72); border: 1px solid rgba(148, 163, 184, 0.32); border-radius: 12px; padding: 16px; min-height: 130px; box-sizing: border-box;
		}
		
		.azure-cost-card h3 {
			margin: 0 0 10px 0; font-size: 15px; color: #ffffff;
		}
		
		.azure-cost-card p {
			margin: 0; font-size: 13px; line-height: 1.5; color: #cbd5e1;
		}
		
		.azure-cost-icon {
			width: 34px; height: 34px; border-radius: 10px; background: rgba(56, 189, 248, 0.18); display: flex; align-items: center; justify-content: center; margin-bottom: 12px; font-size: 18px;
		}
		
		.azure-cost-footer {
			display: grid; grid-template-columns: 1.2fr 1fr; gap: 14px; margin-top: 14px;
		}
		
		.azure-cost-panel {
			background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 16px;
		}
		
		.azure-cost-panel h3 {
			margin: 0 0 10px 0; font-size: 15px; color: #ffffff;
		}
		
		.azure-cost-panel ul {
			margin: 0; padding-left: 18px; color: #dbeafe; font-size: 13px; line-height: 1.6;
		}
		
		.azure-cost-note {
			font-size: 13px; line-height: 1.5; color: #dbeafe; margin: 0;
		}
		
		.severity-row {
			display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;
		}
		
		.severity-pill {
			border-radius: 999px; padding: 6px 10px; font-size: 12px; font-weight: 600;
		}
		
		.critical {
			background: #dc2626; color: #ffffff;
		}
		
		.error {
			background: #f97316; color: #ffffff;
		}
		
		.warning {
			background: #eab308; color: #111827;
		}
		
		@media (max-width: 900px) {
			.azure-cost-header,
			.azure-cost-footer {
				grid-template-columns: 1fr; display: block;
			}
			.azure-cost-grid {
				grid-template-columns: 1fr;
			}
			.azure-cost-badge {
				display: inline-block; margin-top: 12px;
			}
		}

	</style>
	<div class="azure-cost-header">
		<div class="azure-cost-title">

			<h2>Azure Cost Management Overview</h2>

			<p>This section provides visibility into Azure billing, cost-related alerts, and Azure Advisor recommendations. It helps teams identify spend risks, optimization opportunities, and impacted Azure resources from a single LogicMonitor dashboard view.</p>
		</div>
		<div class="azure-cost-badge">Azure Billing &amp; Advisor Monitoring</div></div>
	<div class="azure-cost-grid">
		<div class="azure-cost-card">
			<div class="azure-cost-icon">
				<br>
			</div>

			<h3>Cost Management Alerts</h3>

			<p>Shows active Azure billing and cost-related alerts, including severity, reported time, monitored Azure account, LogicModule, instance, and alert detail.</p>
		</div>
		<div class="azure-cost-card">
			<div class="azure-cost-icon">
				<br>
			</div>

			<h3>Advisor Recommendations</h3>

			<p>Displays Azure Advisor recommendations related to cost, security, availability, performance, and operational improvement. Each alert identifies the impacted Azure resource and recommendation impact.</p>
		</div>
		<div class="azure-cost-card">
			<div class="azure-cost-icon">
				<br>
			</div>

			<h3>Subscriptions Monitored</h3>

			<p>Provides a quick count of Azure subscriptions currently monitored for billing and cost visibility. This confirms the scope of Azure cost monitoring currently represented in the dashboard.</p>
		</div></div>
	<div class="azure-cost-footer">
		<div class="azure-cost-panel">

			<h3>How to Use This Section</h3>

			<ul>
				<li>Review Error and Warning alerts first to prioritize active cost or Advisor recommendations.</li>
				<li>Use the impacted resource name to identify the Azure object requiring review.</li>
				<li>Validate recommendations in Azure before making production changes.</li>
				<li>Track recurring Advisor recommendations to identify optimization trends.</li>
			</ul>
		</div>
		<div class="azure-cost-panel">

			<h3>Alert Prioritization</h3>

			<p class="azure-cost-note">Severity indicators help identify which Azure billing or Advisor findings should be reviewed first.</p>
			<div class="severity-row"><span class="severity-pill critical">Critical</span> <span class="severity-pill error">Error</span> <span class="severity-pill warning">Warning</span></div></div></div></div>
