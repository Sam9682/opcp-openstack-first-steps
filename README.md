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
│   ├── modules/       # Exercise modules (first_steps, compute, networking, storage, lacp)
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
2. **Prerequisites** — environment setup and tooling
3. **First Steps** — core OpenStack concepts (projects, services, endpoints)
4. **User Management** — creating users in Keycloak and assigning OPCP roles
5. **Authentication** — authenticating via Keystone with application credentials
6. **Networking** — networks, subnets, and routers (Neutron)
7. **Storage** — volumes and snapshots (Cinder)
8. **Compute** — instances and snapshots (Nova)
9. **LACP Configuration** — link aggregation and bond configuration (Neutron)
10. **Summary & Next Steps** — recap and further learning
11. **Cleanup Resources** — tearing down lab resources

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

   **Option A — Application Credentials (recommended)**
   ```bash
   export OS_AUTH_URL="https://auth.cloud.example.com/v3"
   export OS_AUTH_TYPE="v3applicationcredential"
   export OS_APPLICATION_CREDENTIAL_ID="<your-id>"
   export OS_APPLICATION_CREDENTIAL_SECRET="<your-secret>"
   ```

   **Option B — User / Password**
   ```bash
   export OS_AUTH_URL="https://auth.cloud.example.com/v3"
   export OS_USERNAME="<your-username>"
   export OS_PASSWORD="<your-password>"
   export OS_PROJECT_NAME="<your-project>"
   export OS_DOMAIN_NAME="Default"
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
| lacp | 3 | Create bond, configure LACP, attach to instance |

Each exercise provides a problem statement, step-by-step instructions, automated assessment, and a reference solution under `solutions/`.

### Cleanup

```bash
python3 -m labs.scripts.cleanup_lab --student-id <your-id>
```

## License

See [LICENSE](LICENSE).
