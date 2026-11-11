---
name: codebase-memory
description: >-
  Query the codebase knowledge graph instead of reading files one by one.
  Use when exploring an unfamiliar codebase, finding where a feature lives,
  tracing who calls a function or what it calls, hunting dead code, doing
  impact analysis before a change, or answering where is X, who calls Y, and
  what breaks if I change Z. Structural search, call tracing, Cypher graph
  queries, diff impact, and architecture overviews over an indexed repo.
---

# codebase-memory

A local MCP server (`codebase-memory-mcp`, native C binary) that indexes a repo
into a persistent knowledge graph — functions, classes, call chains, routes,
imports, infra — and answers structural questions in one call instead of
dozens of file reads. 17 tools. No LLM inside it: it is the index, you are
the intelligence. No network calls, no telemetry, no API key. (Per the project's own docs — not independently verifiable from this plugin; the binary is neither bundled nor audited here.)

## When to query the graph

- **Onboarding to unfamiliar code:** where does this feature live, what does
  this subsystem do, what are the entry points.
- **Tracing:** who calls `X`, what does `X` call, full call context both ways,
  cross-service and data-flow paths.
- **Dead-code hunts:** functions nothing calls, unused exports.
- **Impact analysis before a change:** what breaks if I change `Z`, what does
  this diff touch, which tests cover it.
- **Architecture questions:** languages, packages, routes, hotspots, cycles,
  how services connect.

## When NOT to use it

- **Tiny repos or a single known file:** just read the file. Indexing a
  20-file project to answer one question is slower than opening it.
- **A single known symbol:** read the file or grep once; don't index first.
- **A bug with an unknown root cause:** that's `systematic-debugging`, not
  graph exploration. Use the graph to map the suspect area, then debug.
- **Runtime behavior:** the graph is static analysis. It cannot tell you what
  happens at runtime, what a value is, or why a live request failed. For
  observed calls, record them first with `ingest_traces`.

## Setup — the binary is NOT bundled in the plugin

Install it once on your machine, then the plugin's `mcp.json` entry points
at the installed binary (`command: "codebase-memory-mcp"`, `args: []`).

Windows (PowerShell):

```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/v0.12.1/install.ps1 -OutFile install.ps1
Unblock-File .\install.ps1
.\install.ps1
```

This downloads the release binary to
`%LOCALAPPDATA%\Programs\codebase-memory-mcp\codebase-memory-mcp.exe`, puts
that folder on your user PATH, and writes the MCP entry plus a
`codebase-memory` skill into `~/.cursor/`. Note: the skill the installer
plants is stale — it says 15 MCP tools and omits `compare_graphs` and
`get_file_outline` — so this plugin's skill (17 tools) wins: if Cursor loads the stale one, verify the tool list against this plugin's skill and use this plugin's list (`compare_graphs` and `get_file_outline` included). Which one Cursor prefers is a live smoke-test item. Restart your terminal
and Cursor afterwards. If PowerShell blocks the script, run
`Set-ExecutionPolicy -Scope Process Bypass` first. (Defender may flag the
binary as `Trojan:Script/Wacatac.B!ml`; the project documents this as a known
false positive — see its `SECURITY.md`.)

macOS / Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/v0.12.1/install.sh | bash
```

That installs to `~/.local/bin/codebase-memory-mcp`. Verify with
`codebase-memory-mcp --version`, then restart Cursor. If the server doesn't
appear, check the MCP entry points at the binary on your PATH.

**If the binary is absent:** if `codebase-memory-mcp` is not installed or not on PATH, do not stop — fall back to grep-and-read for the question at hand and note the fallback in the final report.

## Workflow

1. `list_projects` — pick the project whose `root_path` contains your working
   directory. Pass its `name`, or the absolute directory itself, as `project`
   — never guess a repo or folder name.
2. `index_repository` if the project isn't indexed yet (async for big repos,
   then poll with `status: true` every ~30s, up to 5 minutes). If it has not succeeded by then, stop polling, fall back to grep-and-read, and note it in the final report.
3. `get_graph_schema` — learn the node labels and edge types before querying.
4. `search_graph` to find symbols, `trace_path` for callers/callees,
   `get_code_snippet` to read the exact source.
5. `check_index_coverage` on every path you cite for a negative or exhaustive
   claim ("nothing calls X", "this change affects only Y"). A clean result
   means "no recorded gap", never proof of completeness — if coverage is
   partial, skipped, or stale, read/grep the reported ranges directly.

## Tool reference — indexing (5)

- `index_repository` — Index a repo into the graph. Waits by default; use
  async for large repos.
  `index_repository(repo_path="/abs/path/to/repo")`
  `index_repository(repo_path="/abs/path", async=true)` then
  `index_repository(repo_path="/abs/path", status=true)` until `succeeded` — poll every ~30s, up to 5 minutes, then stop polling and fall back to grep-and-read (and note it)
  `index_repository(repo_path="/abs/path", mode="cross-repo-intelligence", target_projects=["api", "web"])`
- `list_projects` — List indexed projects; `detail: "stats"` adds node/edge
  counts and database sizes.
  `list_projects()`
  `list_projects(detail="stats")`
- `delete_project` — Remove a project and all its graph data (including its
  ADR store). Destructive — only when the project is gone or stale.
  `delete_project(project="old-prototype")`
- `index_status` — Readiness, counts, root, watch state, coverage gaps for a
  project. Best-effort; verify cited paths with `check_index_coverage`.
  `index_status(project="my-app")`
  `index_status(project="my-app", diagnostics="full")`
- `check_index_coverage` — Check whether exact paths or a scope are indexed
  and fresh. Run it before any absence or exhaustive claim.
  `check_index_coverage(project="my-app", paths=["src/api/routes.py"])`
  `check_index_coverage(project="my-app", paths=["src/"])`

## Tool reference — querying (12)

- `search_graph` — Structural, BM25, and semantic search over symbols.
  Page with `offset`/`limit`; semantic rows page separately.
  `search_graph(project="my-app", label="Function", name_pattern=".*Handler.*")`
  `search_graph(project="my-app", max_degree=0, exclude_entry_points=true)` (dead-code candidates)
  `search_graph(project="my-app", min_degree=10, relationship="CALLS")` (high-degree nodes)
- `trace_path` — Trace callers, callees, data flow, or cross-service paths.
  Needs exact names — run `search_graph` first. Depth 1–15. Alias:
  `trace_call_path`.
  `trace_path(project="my-app", function_name="checkout", direction="inbound", depth=3)`
  `trace_path(project="my-app", function_name="checkout", direction="both", depth=3)`
  `trace_path(project="my-app", function_name="handleWebhook", mode="cross_service")`
- `detect_changes` — Map the git diff to affected symbols and blast radius,
  with risk classification. `scope: "tests"` reports test impact.
  `detect_changes(project="my-app")`
  `detect_changes(project="my-app", scope="tests")`
  `detect_changes(project="my-app", scope="files")`
- `query_graph` — Read-only openCypher subset over the graph. Add a `LIMIT`;
  broad queries hit a 100k-row ceiling.
  `query_graph(project="my-app", query="MATCH (f:Function) WHERE NOT EXISTS { (f)<-[:CALLS]-() } RETURN f.name, f.file_path LIMIT 20")`
  `query_graph(project="my-app", query="MATCH (a)-[r:HTTP_CALLS]->(b) RETURN a.name, b.name, r.url_path LIMIT 20")`
- `get_graph_schema` — Node/edge counts, relationship patterns, property
  definitions per label. Run this first on an unfamiliar project.
  `get_graph_schema(project="my-app")`
  `get_graph_schema(project="my-app", diagnostics="full")`
- `compare_graphs` — Node/edge additions and removals between two indexed
  snapshots (base vs target project).
  `compare_graphs(base_project="my-app-main", target_project="my-app-feature")`
  `compare_graphs(base_project="my-app-main", target_project="my-app-feature", limit=100)`
- `get_code_snippet` — Read source for a function by qualified name
  (`<project>.<path_parts>.<name>`). Discover the name with `search_graph`
  first.
  `get_code_snippet(project="my-app", qualified_name="my-app.src.api.routes.checkout")`
  `get_code_snippet(project="my-app", qualified_name="my-app.src.api.routes.checkout", source_mode="full")`
- `get_file_outline` — Declaration outline of one repo-relative file, in
  source order, with optional label filter and paging.
  `get_file_outline(project="my-app", file_path="src/api/routes.py")`
  `get_file_outline(project="my-app", file_path="src/api/routes.py", labels=["Function", "Class"])`
- `get_architecture` — Codebase overview: languages, packages, routes,
  hotspots, clusters, entry points, cycles.
  `get_architecture(project="my-app")`
  `get_architecture(project="my-app", aspects=["routes", "hotspots"])`
  `get_architecture(project="my-app", path="src/api")`
- `search_code` — Grep-like text search within indexed files, graph-ranked.
  `search_code(project="my-app", pattern="TODO.*auth")`
  `search_code(project="my-app", pattern="stripe", file_pattern="**/*.py", mode="files")`
- `manage_adr` — CRUD for Architecture Decision Records stored beside the
  graph. `get` reads, `update` replaces the whole document, `set_sections`
  rewrites only named sections.
  `manage_adr(project="my-app", mode="get")`
  `manage_adr(project="my-app", mode="set_sections", section_updates={"DECISION": "Use Postgres, not SQLite, for the queue."})`
- `ingest_traces` — Store observed runtime call paths under a run label, so
  the graph can distinguish observed paths from merely possible ones. Both
  endpoints must resolve to indexed symbols.
  `ingest_traces(project="my-app", label="pytest 2026-11-10", traces=[{"caller": "my-app.src.api.routes.checkout", "callee": "my-app.src.billing.charge", "count": 12}])`

## Gotchas

- `trace_path` needs exact symbol names. `search_graph` with a
  `name_pattern` first, or the trace returns nothing.
- `search_graph` defaults to 50 rows per page — check `has_more` and page
  with `offset` before claiming something doesn't exist.
- A clean `check_index_coverage` is not proof of completeness, and
  `search_graph(relationship="HTTP_CALLS")` filters nodes by degree — use
  `query_graph` with Cypher to see the actual edges.
- Ignored by the indexer: hardcoded patterns (`.git`, `node_modules`, …),
  your `.gitignore` hierarchy, and `.cbmignore` (project-specific, gitignore
  syntax). Symlinks are always skipped. PDF text is indexed, but there is no
  OCR.
- The graph is static analysis with tree-sitter (163 languages) plus Hybrid
  LSP type resolution for Python, TypeScript/JavaScript, PHP, C#, Go, C,
  C++, Java, Kotlin, Rust, and Perl. Everything else resolves by name only.
- `query_graph` is read-only: writes, `MERGE`, and `CALL` fail with an
  `unsupported …` error rather than returning empty results.
- Indexes live in SQLite under `~/.cache/codebase-memory-mcp/` (or
  `$CBM_CACHE_DIR`). To reset: `rm -rf ~/.cache/codebase-memory-mcp/`.
- Cursor gets no CBM hooks: the installer withholds them because session
  injection races and `readonly` blocks MCP. Skills and the read-only
  Scout/Verify/Auditor agent profiles are the durable surfaces.
