# How to List Bare Metal Servers in OPCP

In the OPCP (OpenStack Rack Platform) environment, bare metal servers are managed through OpenStack's Ironic service. Here's how to list these physical servers using the OpenStack CLI.

## Prerequisites

Before listing bare metal servers, ensure you have:
1. OpenStack credentials configured
2. OpenStack CLI installed and properly configured
3. Access to the OPCP environment

## Listing Bare Metal Servers

### Basic Command

To list all bare metal nodes in the OPCP environment:

```bash
openstack baremetal node list
```

### Detailed Listing

For more detailed information including node states:

```bash
openstack baremetal node list --fields id name power_state provision_state driver
```

### Filtering by Status

To list only nodes in a specific state (e.g., active):

```bash
openstack baremetal node list --provision-state active
```

## Understanding Ironic Service

The Ironic service is critical in OPCP because it provides:
- Bare metal provisioning capabilities
- Direct management of physical hardware
- Integration with OpenStack's compute service (Nova)
- Hardware inventory management

## Common Node States

- **enroll**: Node is registered but not yet manageable
- **manageable**: Node is ready to be inspected
- **inspect**: Node is being inspected for hardware details
- **active**: Node is ready for use
- **error**: Node encountered an error during provisioning

## Additional Useful Commands

Get detailed information about a specific node:

```bash
openstack baremetal node show <node-id>
```

List nodes with their hardware details:

```bash
openstack baremetal node list --fields id name driver_info
```

## Troubleshooting

If you encounter issues:
1. Verify your OpenStack credentials are correctly configured
2. Ensure you're connecting to the correct OpenStack endpoint
3. Check that the Ironic service is running in your OPCP environment
4. Confirm you have appropriate permissions to view bare metal nodes

## Security Note

Always handle OpenStack credentials securely and never share them publicly. In OPCP environments, credentials should be obtained from your system administrator.