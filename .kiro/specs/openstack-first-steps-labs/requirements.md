# Requirements Document

## Introduction

This document defines the requirements for the OpenStack First Steps Labs platform — a customer-hosted, hands-on learning environment where students learn OpenStack fundamentals through progressive, interactive exercises. The platform integrates with the existing `opcp-openstack-automation` framework (reusing its auth, compute, network, volume, and security group managers) and follows the same modular directory conventions (skillhub pattern). Labs are containerized for deployment consistency and include automated assessment and progress tracking.

## Glossary

- **Lab_Platform**: The overall system that hosts, orchestrates, and delivers OpenStack first-steps lab modules to students.
- **Lab_Module**: A self-contained unit of learning content covering a specific OpenStack topic (e.g., first_steps, authentication, compute, networking, storage, security_groups). Each module contains exercises, solutions, setup scripts, and a README.
- **Exercise**: A single hands-on task within a Lab_Module that a student must complete. Each exercise has a problem statement, step-by-step instructions, expected outcomes, and a verification mechanism.
- **Solution**: A reference implementation for an Exercise, stored in the `solutions/` directory of a Lab_Module.
- **Assessment_Engine**: The subsystem responsible for automatically validating student exercise submissions against expected outcomes and generating feedback.
- **Progress_Tracker**: The subsystem that records which exercises and modules a student has completed and exposes completion status.
- **Setup_Script**: An automated script within a Lab_Module's `setup/` directory that provisions the required OpenStack resources and environment for that module's exercises.
- **Cleanup_Script**: An automated script that tears down all OpenStack resources created during a lab session.
- **Lab_Container**: A Docker container image that packages the lab environment, dependencies, and tooling for consistent cross-platform deployment.
- **Automation_Framework**: The existing `opcp-openstack-automation` codebase, including its auth_manager, compute_manager, network_manager, volume_manager, and security_group_manager components.
- **Student**: A person using the Lab_Platform to learn OpenStack fundamentals.
- **Customer**: An organization that deploys and hosts the Lab_Platform for its students.
- **Lab_Config**: A YAML configuration file (`lab_config.yaml`) that defines module ordering, resource limits, and environment parameters.
- **Resource_Limit**: A configurable cap on the OpenStack resources (instances, networks, volumes) a single student session may consume.

## Requirements

### Requirement 1: Modular Lab Structure

**User Story:** As a Customer, I want the lab content organized into independent, topic-specific modules, so that I can deploy selected modules and students can follow a clear learning path.

#### Acceptance Criteria

1. THE Lab_Platform SHALL organize content into the following Lab_Modules: first_steps, authentication, compute, networking, storage, and security_groups.
2. WHEN a Lab_Module is deployed, THE Lab_Module SHALL contain an `exercises/` directory, a `solutions/` directory, a `setup/` directory, and a `README.md` file.
3. THE Lab_Platform SHALL allow each Lab_Module to be deployed independently without requiring other Lab_Modules to be present.
4. THE Lab_Platform SHALL define a recommended module progression order in the Lab_Config file.

### Requirement 2: Exercise Framework

**User Story:** As a Student, I want each exercise to have clear instructions and expected outcomes, so that I can learn OpenStack concepts step by step.

#### Acceptance Criteria

1. THE Exercise SHALL include a problem statement, step-by-step instructions, expected outcomes, and a solution verification hook.
2. WHEN a Student executes an Exercise, THE Exercise SHALL interact with OpenStack services through the Automation_Framework managers (auth_manager, compute_manager, network_manager, volume_manager, security_group_manager).
3. THE Lab_Platform SHALL provide a standardized exercise template that all exercises follow.
4. WHEN an Exercise encounters an OpenStack API error, THE Exercise SHALL display a descriptive error message that includes the operation attempted and the error details.

### Requirement 3: First Steps Module Content

**User Story:** As a Student, I want a first-steps module that introduces basic OpenStack operations, so that I can build foundational skills before moving to advanced topics.

#### Acceptance Criteria

1. THE first_steps Lab_Module SHALL include an exercise for creating a compute instance.
2. THE first_steps Lab_Module SHALL include an exercise for creating a network.
3. THE first_steps Lab_Module SHALL include an exercise for creating a volume.
4. THE first_steps Lab_Module SHALL include a README.md that explains OpenStack core concepts (projects, users, services, endpoints) before the exercises begin.
5. WHEN a Student completes all exercises in the first_steps Lab_Module, THE Assessment_Engine SHALL report the module as complete.

### Requirement 4: Authentication Module Content

**User Story:** As a Student, I want to learn how OpenStack authentication works, so that I understand identity management and token-based access.

#### Acceptance Criteria

1. THE authentication Lab_Module SHALL include an exercise for authenticating against the Keystone identity service and obtaining a token.
2. THE authentication Lab_Module SHALL include an exercise for managing tokens (listing, validating, and revoking).
3. WHEN a Student provides invalid credentials in an authentication exercise, THE Exercise SHALL return a clear error indicating the authentication failure reason.

### Requirement 5: Compute Module Content

**User Story:** As a Student, I want to practice compute operations, so that I can manage virtual machine instances in OpenStack.

#### Acceptance Criteria

1. THE compute Lab_Module SHALL include an exercise for launching a new instance with specified flavor and image.
2. THE compute Lab_Module SHALL include an exercise for resizing an existing instance.
3. THE compute Lab_Module SHALL include an exercise for creating and managing instance snapshots.
4. WHEN a Student attempts to launch an instance and the requested flavor or image does not exist, THE Exercise SHALL return an error identifying the missing resource.

### Requirement 6: Networking Module Content

**User Story:** As a Student, I want to practice network configuration, so that I can manage virtual networks, subnets, and routers in OpenStack.

#### Acceptance Criteria

1. THE networking Lab_Module SHALL include an exercise for creating a virtual network.
2. THE networking Lab_Module SHALL include an exercise for creating a subnet within a network.
3. THE networking Lab_Module SHALL include an exercise for configuring a router and attaching it to a subnet.
4. WHEN a Student creates a subnet with an invalid CIDR, THE Exercise SHALL return an error describing the CIDR validation failure.

### Requirement 7: Storage Module Content

**User Story:** As a Student, I want to practice storage operations, so that I can manage block storage volumes in OpenStack.

#### Acceptance Criteria

1. THE storage Lab_Module SHALL include an exercise for creating a block storage volume.
2. THE storage Lab_Module SHALL include an exercise for attaching a volume to a running instance.
3. THE storage Lab_Module SHALL include an exercise for creating and managing volume snapshots.
4. WHEN a Student attempts to attach a volume to a non-existent instance, THE Exercise SHALL return an error identifying the missing instance.

### Requirement 8: Security Groups Module Content

**User Story:** As a Student, I want to practice security group management, so that I can control network access to instances.

#### Acceptance Criteria

1. THE security_groups Lab_Module SHALL include an exercise for creating a security group.
2. THE security_groups Lab_Module SHALL include an exercise for adding and removing ingress and egress rules.
3. THE security_groups Lab_Module SHALL include an exercise for applying a security group to a running instance.
4. WHEN a Student creates a rule with an invalid protocol or port range, THE Exercise SHALL return an error describing the validation failure.

### Requirement 9: Container-Based Deployment

**User Story:** As a Customer, I want the lab environment packaged as a container, so that I can deploy it consistently across different infrastructure.

#### Acceptance Criteria

1. THE Lab_Platform SHALL provide a Dockerfile that builds a Lab_Container containing all lab dependencies, the Automation_Framework, and lab modules.
2. THE Lab_Container SHALL include a requirements.txt listing all Python dependencies with pinned versions.
3. THE Lab_Container SHALL include an entrypoint script that initializes the lab environment and validates connectivity to the target OpenStack cloud.
4. WHEN the Lab_Container starts and cannot reach the configured OpenStack endpoint, THE Lab_Container SHALL exit with a non-zero exit code and log a descriptive connectivity error.
5. THE Lab_Container SHALL run on Linux, macOS, and Windows hosts that support Docker.

### Requirement 10: Automated Environment Setup and Cleanup

**User Story:** As a Student, I want the lab environment to be set up and cleaned up automatically, so that I can focus on learning rather than infrastructure management.

#### Acceptance Criteria

1. WHEN a Student starts a Lab_Module, THE Setup_Script SHALL provision all required OpenStack resources for that module's exercises.
2. WHEN a Student finishes a Lab_Module or the lab session ends, THE Cleanup_Script SHALL delete all OpenStack resources created during that session.
3. IF the Cleanup_Script fails to delete a resource, THEN THE Cleanup_Script SHALL log the resource identifier and the failure reason, and continue deleting remaining resources.
4. THE Setup_Script SHALL be idempotent: running the Setup_Script multiple times SHALL produce the same environment state.

### Requirement 11: Automated Assessment and Feedback

**User Story:** As a Student, I want automated validation of my exercise solutions, so that I receive immediate feedback on my work.

#### Acceptance Criteria

1. WHEN a Student submits an Exercise solution, THE Assessment_Engine SHALL validate the solution against the expected outcomes defined for that Exercise.
2. WHEN a solution passes validation, THE Assessment_Engine SHALL return a success message and mark the Exercise as completed in the Progress_Tracker.
3. WHEN a solution fails validation, THE Assessment_Engine SHALL return a feedback message describing which expected outcomes were not met.
4. THE Assessment_Engine SHALL validate solutions by querying actual OpenStack resource state (not by comparing source code).

### Requirement 12: Progress Tracking

**User Story:** As a Student, I want to see my progress across modules and exercises, so that I know what I have completed and what remains.

#### Acceptance Criteria

1. THE Progress_Tracker SHALL record the completion status of each Exercise for each Student.
2. WHEN a Student queries progress, THE Progress_Tracker SHALL return a summary showing completed and remaining exercises per Lab_Module.
3. WHEN all exercises in a Lab_Module are marked complete, THE Progress_Tracker SHALL mark that Lab_Module as complete.
4. THE Progress_Tracker SHALL persist progress data so that it survives Lab_Container restarts.

### Requirement 13: Automation Framework Integration

**User Story:** As a developer, I want the labs to reuse the existing automation framework managers, so that lab exercises use proven, maintained OpenStack client code.

#### Acceptance Criteria

1. THE Lab_Platform SHALL import and use auth_manager from the Automation_Framework for all authentication operations.
2. THE Lab_Platform SHALL import and use compute_manager from the Automation_Framework for all compute operations.
3. THE Lab_Platform SHALL import and use network_manager from the Automation_Framework for all networking operations.
4. THE Lab_Platform SHALL import and use volume_manager from the Automation_Framework for all storage operations.
5. THE Lab_Platform SHALL import and use security_group_manager from the Automation_Framework for all security group operations.
6. THE Lab_Platform SHALL preserve the existing skillhub directory structure from the Automation_Framework repository.

### Requirement 14: Resource Limits and Isolation

**User Story:** As a Customer, I want resource usage limits per student session, so that a single student cannot exhaust the OpenStack cloud capacity.

#### Acceptance Criteria

1. THE Lab_Platform SHALL enforce configurable Resource_Limits per student session as defined in the Lab_Config.
2. WHEN a Student attempts to create a resource that would exceed the configured Resource_Limit, THE Lab_Platform SHALL reject the operation and return a message stating the limit and current usage.
3. THE Lab_Platform SHALL isolate each Student's resources using dedicated OpenStack projects or naming conventions so that one Student's resources do not interfere with another Student's resources.

### Requirement 15: Configuration Management

**User Story:** As a Customer, I want a central configuration file to control lab behavior, so that I can customize the platform for my environment.

#### Acceptance Criteria

1. THE Lab_Platform SHALL read deployment parameters (OpenStack endpoint URL, default flavor, default image, module order) from the Lab_Config file.
2. THE Lab_Platform SHALL read per-student session parameters (resource limits, timeout durations) from the Lab_Config file.
3. WHEN the Lab_Config file is missing or contains invalid YAML, THE Lab_Platform SHALL exit with a non-zero exit code and log a descriptive configuration error.
4. THE Lab_Platform SHALL provide a documented example Lab_Config file with default values for all configurable parameters.

### Requirement 16: Security and Credential Handling

**User Story:** As a Customer, I want credentials handled securely, so that student and admin OpenStack credentials are protected.

#### Acceptance Criteria

1. THE Lab_Platform SHALL accept OpenStack credentials through environment variables or a secure configuration file, not through command-line arguments.
2. THE Lab_Platform SHALL mask credential values in all log output.
3. WHEN a Student session ends, THE Cleanup_Script SHALL revoke any session-scoped tokens created during that session.
4. THE Lab_Platform SHALL use HTTPS for all communication with the OpenStack endpoint when the endpoint supports TLS.
