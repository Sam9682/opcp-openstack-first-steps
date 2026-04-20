# opcp-openstack-first-steps

Hands-on training framework for learning OpenStack fundamentals on the OPCP (OpenStack Rack Platform). The project combines an interactive web-based course (**SkillHub**) with a containerised lab environment where students practice real API calls against a live OpenStack deployment.

## Repository Structure

```
├── skillhub/          # Static HTML training site (EN + FR)
│   ├── en/            # English lessons
│   ├── fr/            # French lessons
│   └── assets/        # CSS, JS (navigation, i18n, progress tracking)
├── labs/              # Python lab framework
│   ├── base/          # Dockerfile, entrypoint, pip requirements
│   ├── core/          # Runner, config loader, assessment, progress, resource limiter
│   ├── modules/       # Exercise modules (first_steps, compute, networking, storage, security_groups)
│   ├── templates/     # Base classes for exercises and assessments
│   ├── scripts/       # Setup, cleanup, and validation scripts
│   ├── config/        # lab_config.yaml (OpenStack endpoint, limits, module order)
│   └── tests/         # Unit tests
├── Specs/             # Design documents and specifications
└── docs/              # Additional operational documentation
```

## SkillHub — Web Training

SkillHub is a static, multi-language (EN/FR) site that guides learners through the following path:

1. **Introduction** — overview and setup validation
2. **First Steps** — core OpenStack concepts (projects, services, endpoints)
3. **User Management** — creating users in Keycloak and assigning OPCP roles
4. **Authentication** — authenticating via Keystone with application credentials
5. **Networking** — networks, subnets, and routers (Neutron)
6. **Security Groups** — firewall rules (Neutron)
7. **Storage** — volumes and snapshots (Cinder)
8. **Compute** — instances and snapshots (Nova)

Open `skillhub/index.html` in a browser to start. The site auto-detects the browser language and redirects to the appropriate locale.

## Labs — Hands-on Exercises

The lab framework runs inside a Docker container and connects to a real OpenStack endpoint.

### Prerequisites

- Python 3.9+
- Docker
- Access to an OPCP / OpenStack environment

### Quick Start

1. Copy and edit the configuration:
   ```bash
   cp labs/config/lab_config.example.yaml labs/config/lab_config.yaml
   # Edit endpoint, flavor, image to match your environment
   ```

2. Set your credentials:
   ```bash
   export OS_AUTH_URL="https://auth.cloud.example.com/v3"
   export OS_AUTH_TYPE="v3applicationcredential"
   export OS_APPLICATION_CREDENTIAL_ID="<your-id>"
   export OS_APPLICATION_CREDENTIAL_SECRET="<your-secret>"
   ```

3. Build and run the lab container:
   ```bash
   docker build -t opcp-labs -f labs/base/Dockerfile labs/
   docker run --env-file .env opcp-labs --module first_steps --student-id <your-id>
   ```

### Module Overview

| Module | Exercises | Topics |
|--------|-----------|--------|
| first_steps | 3 | Create instance, network, volume |
| compute | 3 | Launch, resize, snapshots |
| networking | 3 | Network, subnet, router |
| storage | 3 | Volume, attach, snapshots |
| security_groups | 3 | Create SG, manage rules, apply to instance |

Each exercise provides a problem statement, step-by-step instructions, automated assessment, and a reference solution under `solutions/`.

### Cleanup

```bash
python -m labs.scripts.cleanup_lab --student-id <your-id>
```

## License

See [LICENSE](LICENSE).
