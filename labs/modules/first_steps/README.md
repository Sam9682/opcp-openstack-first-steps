# First Steps Module

## OpenStack Core Concepts

Before starting the exercises, review these foundational concepts:

### Projects
A project (also called a tenant) is an organizational unit in OpenStack.
Resources such as instances, networks, and volumes belong to a project.
Each student session operates within a single project.

### Users
A user is an identity that authenticates against the Keystone identity
service. Users are assigned roles within projects that determine what
operations they can perform.

### Services
OpenStack is composed of independent services, each responsible for a
domain:
- **Nova** — Compute (virtual machine instances)
- **Neutron** — Networking (virtual networks, subnets, routers)
- **Cinder** — Block Storage (volumes, snapshots)
- **Keystone** — Identity (authentication, authorization, service catalog)
- **Glance** — Image (virtual machine images)

### Endpoints
Each service exposes one or more HTTP endpoints listed in the Keystone
service catalog. Clients discover service URLs by querying the catalog
after authentication.

## Exercises

| # | Exercise | Objective |
|---|----------|-----------|
| 1 | Create Instance | Launch a compute instance via Nova |
| 2 | Create Network | Create a virtual network via Neutron |
| 3 | Create Volume | Create a block storage volume via Cinder |

Complete all three exercises to finish this module.
