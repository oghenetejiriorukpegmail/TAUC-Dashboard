# Repository Guidelines

## Project Structure & Module Organization
The Streamlit UI entrypoint is `app.py`, which wires pages, API helpers, and theming. Feature-specific views live under `pages/` (for example `pages/inventory.py` and `pages/network_management.py`), while reusable UI and API logic sits in `utils/`. `port_helper.py` resolves an open port for local runs, and `theme_css.py` centralizes custom styling. Any certificates or `.env` credentials should sit alongside the parent SDK checkout referenced in `README.md`.

## Build, Run & Development Commands
- `pip install -e ..`: Install the TAUC Python SDK from the repository root one level up.
- `pip install -r requirements.txt`: Install Streamlit UI dependencies for this app.
- `streamlit run app.py` or `./run.sh`: Launch the dashboard (the script auto-selects an available port and sets defaults from `.streamlit/config.toml`).
- `./setup_env.sh`: Optional helper to copy `.env.example` into place and prompt for credentials.

## Coding Style & Naming Conventions
Use Python 3.7+ with 4-space indentation. Follow `snake_case` for functions and variables, `CamelCase` for classes, and keep module names descriptive (e.g., `inventory.py`, `api_helpers.py`). Organize new Streamlit pages under `pages/` and reusable widgets or request code under `utils/`. Maintain concise functions with clear docstrings when behavior is not obvious, and prefer explicit imports over wildcards.

## Testing Guidelines
Automated tests are not yet part of this app; rely on manual verification. Before opening a PR, run the dashboard locally, exercise the flows touched (inventory listings, NAT control, device lookup), and confirm API calls succeed using the credentials detailed in `TEST_RESULTS.md`. Capture console output for authentication or signature errors when relevant.

## Commit & Pull Request Guidelines
Commits should follow the existing history’s imperative style (e.g., "Add comprehensive MAC address normalization across all inputs"). Group related changes together and include succinct bodies when configuration or migration steps are required. PRs should describe the feature or fix, link any relevant issues, list manual test steps, and attach screenshots or terminal captures for UI-facing changes. Mention required credentials or setup changes so reviewers can reproduce quickly.

## Security & Configuration Tips
Never commit real credentials or certificates—keep secrets in `.env` and the `certs/` directory outside version control. Verify `setup_env.sh` and `.streamlit/secrets.toml` remain ignored. When sharing troubleshooting logs, redact access tokens and X-Authorization signatures.
