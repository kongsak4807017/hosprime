# HosPrime Security Policy

## Supported status

HosPrime is currently a controlled prototype. It must not be used for unrestricted production clinical, legal, financial, workforce, procurement or public-order decisions until the relevant maturity gates pass.

## Reporting a vulnerability

Do not disclose active credentials, personal data, health data or exploit details in a public issue.

Report privately to the repository owner with:

- affected component and version;
- severity and potential impact;
- reproduction steps using non-sensitive data;
- evidence such as logs or screenshots with secrets removed;
- suggested containment if known.

## Immediate incident conditions

Treat the following as P0:

- exposed credential or signing secret;
- unauthorized access to restricted organizational or health information;
- fabricated evidence used for a material decision;
- high-impact action executed without valid approval;
- audit-record loss or tampering;
- data corruption without a verified recovery path.

## Response sequence

1. Contain the affected credential, account, feature or environment.
2. Preserve logs and evidence.
3. Notify the Security Lead and Executive Sponsor.
4. Assess affected data, users, decisions and external systems.
5. Rotate credentials and revoke sessions where required.
6. Restore trusted service or keep the feature disabled.
7. Record root cause, corrective action and prevention.
8. Complete a retrospective within five working days.

## Security design rules

- No real secret in source, documentation, issue, log or build artifact.
- All non-public APIs require authenticated identity.
- Sensitive access follows minimum necessary permissions.
- AI tools use explicit allowlists and validated parameters.
- Human approval identity comes from authentication, not request text.
- Approval does not equal execution.
- Every external action requires an execution receipt and audit event.
- Provider failure must not generate fabricated evidence.
- Production configuration fails closed.

## Dependency and secret management

- Use environment variables or an approved secret manager.
- Rotate credentials by environment and purpose.
- Enable secret scanning and push protection.
- Review dependency alerts and apply risk-based patch timelines.
- Pin production dependencies through controlled lock or build artifacts.

## Data protection

- Classify data and documents before ingestion.
- Log minimum necessary metadata and redact sensitive values.
- Test correction, deletion and retention workflows.
- Separate Person Memory, Role Memory and Organization Memory.
- Do not use sensitive organizational data to train external models without explicit approval and lawful basis.

## Release rule

No release may proceed with an unresolved P0 security or privacy finding.
