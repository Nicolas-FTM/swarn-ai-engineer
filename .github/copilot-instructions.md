# Copilot instructions for swarn-ai-engineer

Purpose
--
Provide concise, project-aware guidance to GitHub Copilot for making changes in this repository.

Repository overview
--
- Python-based multi-agent swarm system using LangGraph and LangChain.
- Infrastructure manifests for Docker Compose and Kubernetes live under `infra/`.

Priorities when producing changes
--
- Keep changes minimal and focused to satisfy the user's request.
- Prefer fixes at the root cause rather than superficial patches.
- Preserve public APIs and existing configs unless the user asks to alter them.

Style & conventions
--
- Language: English (use Spanish comments only when the author leaves Spanish notes).
- Python formatting: follow existing project style; avoid unrelated reformatting.
- Use clear, descriptive names; avoid one-letter variables.
- Do not add license headers or unrelated files.

Testing & verification
--
- When editing runnable code, run the project's tests or a minimal local run to verify behavior if possible.
- For infra changes, validate YAML structure and keep semantics compatible with current k8s/docker-compose layout.

Files & locations of interest
--
- Infrastructure: `infra/docker-compose/` and `infra/k8s/`.
- Agent docs: `.github/agents/`.

Collaboration rules
--
- When a change is larger than a few lines, propose a short plan and ask for confirmation.
- Explain assumptions and highlight any manual steps needed to validate changes locally.

When asked about the model
--
If explicitly asked what model is used, state: "GPT-5 mini".

Contact
--
When unsure about repository conventions, ask the repository maintainer before making large design changes.
