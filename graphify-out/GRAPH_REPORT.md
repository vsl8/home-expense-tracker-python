# Graph Report - .  (2026-06-26)

## Corpus Check
- Corpus is ~22,924 words - fits in a single context window. You may not need a graph.

## Summary
- 252 nodes · 298 edges · 15 communities (12 shown, 3 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 10 edges (avg confidence: 0.7)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Data Models & Testing|Data Models & Testing]]
- [[_COMMUNITY_Expense Type API Tests|Expense Type API Tests]]
- [[_COMMUNITY_Expense API Tests|Expense API Tests]]
- [[_COMMUNITY_Report Tests|Report Tests]]
- [[_COMMUNITY_Core API Routes|Core API Routes]]
- [[_COMMUNITY_Report Export Tests|Report Export Tests]]
- [[_COMMUNITY_Build Scripts (Shell)|Build Scripts (Shell)]]
- [[_COMMUNITY_Documentation & Docker|Documentation & Docker]]
- [[_COMMUNITY_Build Scripts (PowerShell)|Build Scripts (PowerShell)]]
- [[_COMMUNITY_Application Factory|Application Factory]]
- [[_COMMUNITY_Graphify Skill|Graphify Skill]]
- [[_COMMUNITY_Reports Module|Reports Module]]
- [[_COMMUNITY_Routes Init|Routes Init]]
- [[_COMMUNITY_Tests Init|Tests Init]]
- [[_COMMUNITY_Project Package|Project Package]]

## God Nodes (most connected - your core abstractions)
1. `build.sh script` - 17 edges
2. `ExpenseType` - 14 edges
3. `TestExpenseAPI` - 13 edges
4. `Expense` - 12 edges
5. `TestExpenseTypeAPI` - 11 edges
6. `TestReportsSummary` - 11 edges
7. `TestExpenseModel` - 8 edges
8. `TestExpenseTypeModel` - 7 edges
9. `get_date_range()` - 6 edges
10. `graphify Skill` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Report Export UI` --semantically_similar_to--> `Expense Reports`  [INFERRED] [semantically similar]
  app/templates/index.html → README.md
- `Docker Multi-Stage Build Guidance` --semantically_similar_to--> `Multi-Stage Docker Build`  [INFERRED] [semantically similar]
  docs/DOCKER.md → .github/copilot-instructions.md
- `Azure App Service Setup` --semantically_similar_to--> `Azure Web App Deployment`  [INFERRED] [semantically similar]
  docs/GITHUB_ACTIONS_SETUP.md → .github/workflows/ci-cd.yml
- `TestExpenseModel` --uses--> `ExpenseType`  [INFERRED]
  tests/test_models.py → app/models.py
- `TestExpenseTypeModel` --uses--> `ExpenseType`  [INFERRED]
  tests/test_models.py → app/models.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Graphify Reference Documents** — references_query_query_reference, references_extraction_spec_extraction_prompt, references_update_incremental_update_reference, references_add_watch_add_watch_reference, references_exports_export_reference, references_hooks_hook_integration [EXTRACTED 1.00]
- **Progressive Delivery Stack** — workflows_ci_cd_ci_cd_pipeline, workflows_ci_cd_azure_web_app_deployment, workflows_ci_cd_progressive_deployment, docs_github_actions_setup_environment_setup_guide, docs_github_actions_setup_azure_app_service [INFERRED 0.85]
- **Expense Reporting Surface** — readme_home_expense_tracker, readme_expense_reports, templates_index_home_expense_tracker_spa, templates_index_report_export_ui, requirements_python_dependencies [INFERRED 0.85]

## Communities (15 total, 3 thin omitted)

### Community 0 - "Data Models & Testing"
Cohesion: 0.07
Nodes (26): Expense, ExpenseType, Database models for the Expense Tracker application., Model for expense categories/types., Convert model to dictionary., Model for individual expense records., Convert model to dictionary., create_expense() (+18 more)

### Community 1 - "Expense Type API Tests"
Cohesion: 0.06
Nodes (19): Unit tests for API endpoints., Test deleting (soft delete) an expense type., Tests for expense type API endpoints., Test getting expense types when none exist., Test getting all expense types., Tests for dashboard API endpoints., Test dashboard stats with no data., Test dashboard stats with data. (+11 more)

### Community 2 - "Expense API Tests"
Cohesion: 0.08
Nodes (13): Tests for expense API endpoints., Test getting expenses when none exist., Test getting all expenses., Test getting a single expense., Test getting a non-existent expense., Test creating a new expense., Test creating expense without amount fails., Test creating expense with invalid type fails. (+5 more)

### Community 3 - "Report Tests"
Cohesion: 0.09
Nodes (14): Unit tests for reports API endpoints., Tests for chart data endpoint., Test getting pie chart data., Test getting bar chart data., Test getting line chart data., Tests for Excel export endpoint., Test exporting to Excel., Test exporting to Excel with custom date range. (+6 more)

### Community 4 - "Core API Routes"
Cohesion: 0.10
Nodes (19): create_expense_type(), delete_expense(), delete_expense_type(), get_dashboard_stats(), get_expense(), get_expense_type(), get_expense_types(), get_expenses() (+11 more)

### Community 5 - "Report Export Tests"
Cohesion: 0.10
Nodes (11): Tests for reports summary endpoint., Test getting monthly report summary., Test getting daily report summary., Test getting weekly report summary., Test getting quarterly report summary., Test getting half-yearly report summary., Test getting yearly report summary., Test getting report with custom date range. (+3 more)

### Community 6 - "Build Scripts (Shell)"
Cohesion: 0.23
Nodes (17): invoke_clean_all(), invoke_dev_build(), invoke_local_dev(), invoke_local_test(), invoke_build(), invoke_clean(), invoke_dev(), invoke_lint() (+9 more)

### Community 7 - "Documentation & Docker"
Cohesion: 0.18
Nodes (17): Home Expense Tracker Copilot Instructions, Multi-Stage Docker Build, Docker Compose Container Stack, Development Expense Tracker Service, Production Expense Tracker Service, Docker Deployment Guide, Docker Multi-Stage Build Guidance, Azure App Service Setup (+9 more)

### Community 8 - "Build Scripts (PowerShell)"
Cohesion: 0.13
Nodes (3): Invoke-Build(), Invoke-Prod(), Invoke-Run()

### Community 9 - "Application Factory"
Cohesion: 0.14
Nodes (11): create_app(), Home Expense Tracker - Flask Application A single-page application for managing, Application factory for creating Flask app instances., health(), index(), Main routes for serving the SPA., Serve the main single-page application., Health check endpoint. (+3 more)

### Community 10 - "Graphify Skill"
Cohesion: 0.17
Nodes (12): graphify Skill, Add and Watch Reference, Watch Mode, Export Reference, MCP Server Export, Extraction Subagent Prompt, Hook Integration Reference, Post-Commit Hook (+4 more)

### Community 11 - "Reports Module"
Cohesion: 0.23
Nodes (11): export_to_excel(), export_to_pdf(), get_chart_data(), get_date_range(), get_report_summary(), Reports API routes for generating expense reports and exports., Export expense report to Excel spreadsheet., Calculate date range based on period type. (+3 more)

## Knowledge Gaps
- **6 isolated node(s):** `home-expense-tracker`, `Extraction Subagent Prompt`, `Incremental Re-Extraction`, `Watch Mode`, `MCP Server Export` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ExpenseType` connect `Data Models & Testing` to `Reports Module`, `Core API Routes`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Why does `TestExpenseAPI` connect `Expense API Tests` to `Expense Type API Tests`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Why does `Expense` connect `Data Models & Testing` to `Reports Module`, `Core API Routes`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `ExpenseType` (e.g. with `TestExpenseModel` and `TestExpenseTypeModel`) actually correct?**
  _`ExpenseType` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Expense` (e.g. with `TestExpenseModel` and `TestExpenseTypeModel`) actually correct?**
  _`Expense` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Home Expense Tracker - Flask Application A single-page application for managing`, `Application factory for creating Flask app instances.`, `Database models for the Expense Tracker application.` to the rest of the system?**
  _100 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Data Models & Testing` be split into smaller, more focused modules?**
  _Cohesion score 0.07254623044096728 - nodes in this community are weakly interconnected._