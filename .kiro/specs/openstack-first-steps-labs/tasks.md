# Implementation Plan: OpenStack First Steps Labs

## Overview

Incremental implementation of the OpenStack First Steps Labs platform in Python. Each task builds on previous work, starting with core infrastructure (config, credentials, resource limits), then the exercise framework and assessment engine, followed by module content, container packaging, and finally wiring everything together via the Lab Runner.

## Tasks

- [x] 1. Set up project structure and core data models
  - [x] 1.1 Create directory structure and package files
    - Create `labs/` root with subdirectories: `base/`, `modules/` (with 6 module dirs each containing `exercises/`, `solutions/`, `setup/`), `templates/`, `scripts/`, `config/`, `core/`, `tests/`
    - Add `__init__.py` files to `core/`, `templates/`, `scripts/`, `tests/`
    - Add placeholder `README.md` in each module directory
    - _Requirements: 1.1, 1.2, 13.6_

  - [x] 1.2 Define shared data classes and exceptions
    - Create `core/__init__.py` with dataclasses: `LabConfig`, `ResourceLimits`, `Credentials`, `ExerciseStatus`, `ModuleProgress`, `AssessmentResult`
    - Define custom exceptions: `ConfigError`, `CredentialError`, `ResourceLimitError`
    - _Requirements: 2.1, 14.2, 15.3_

- [x] 2. Implement Config Loader
  - [x] 2.1 Implement `core/config_loader.py`
    - Implement `load_config(config_path)` to read and parse YAML with default path `config/lab_config.yaml`
    - Implement `validate_config(raw)` to check required fields (`openstack.endpoint`, `openstack.default_flavor`, `openstack.default_image`, `modules.order`, `session.timeout_minutes`, `session.resource_limits.*`), types, and return a `LabConfig` instance
    - Raise `ConfigError` with descriptive message on missing file, invalid YAML, or missing/wrong-type fields
    - Exit with non-zero code on configuration errors (fail-fast for infrastructure errors)
    - _Requirements: 15.1, 15.2, 15.3_

  - [x] 2.2 Write unit tests for config validation (`tests/test_config_loader.py`)
    - Tests for `validate_config` happy path (returns LabConfig, populates all fields correctly)
    - Tests for missing required fields (parametrized across all 9 required dotted paths)
    - Tests for wrong types (endpoint not string, module_order not list, timeout not int, max_instances not int)
    - Tests for `load_config` file-level errors (missing file, invalid YAML, non-mapping YAML, valid file)
    - _Requirements: 15.1, 15.2, 15.3_

  - [ ]* 2.3 Write property test for config validation (Property 13)
    - **Property 13: Configuration Validation**
    - Test that invalid YAML / missing fields / wrong types always raise `ConfigError` with descriptive message; valid configs always produce a correct `LabConfig`
    - Use Hypothesis strategies for random dicts and malformed YAML strings
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 13: Configuration Validation`
    - **Validates: Requirements 15.3**

  - [x] 2.4 Create `config/lab_config.yaml` and `config/lab_config.example.yaml`
    - Provide default values for all parameters matching the data model in design doc:
      - `openstack.endpoint`, `openstack.default_flavor` (m1.small), `openstack.default_image` (ubuntu-22.04)
      - `modules.order` (first_steps, authentication, compute, networking, storage, security_groups)
      - `session.timeout_minutes` (120)
      - `session.resource_limits` (max_instances: 3, max_networks: 2, max_volumes: 3, max_security_groups: 5)
    - _Requirements: 15.1, 15.4_

- [x] 3. Implement Credential Handler
  - [x] 3.1 Implement `core/credential_handler.py`
    - Implement `load_credentials()` to read from environment variables (`OS_AUTH_URL`, `OS_USERNAME`, `OS_PASSWORD`, `OS_PROJECT_NAME`, `OS_DOMAIN_NAME`), falling back to `~/.openstack/credentials.yaml`
    - Raise `CredentialError` if no source provides all required fields
    - Exit with non-zero code on credential errors (fail-fast for infrastructure errors)
    - Never accept credentials via command-line arguments
    - Implement `mask_value(value)`: return `'****' + last 4 chars` for strings >= 4 chars, `'****'` for shorter strings
    - Never log unmasked credential values — all credential values must be masked before logging
    - _Requirements: 16.1, 16.2_

  - [ ]* 3.2 Write property test for credential masking (Property 14)
    - **Property 14: Credential Masking**
    - For strings >= 4 chars: masked != original, hides all but last 4. For strings < 4 chars: fully masked
    - Use Hypothesis `text()` strategy with varying min/max sizes
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 14: Credential Masking`
    - **Validates: Requirements 16.2**

- [x] 4. Implement Resource Limiter
  - [x] 4.1 Implement `core/resource_limiter.py`
    - Implement `ResourceLimiter.__init__(limits, student_id)`
    - Implement `check_limit(resource_type, current_count)`: raise `ResourceLimitError` (with limit and usage in message, e.g. "Resource limit exceeded: {current}/{limit} {resource_type}") when `current_count >= limit`
    - Implement `get_usage(resource_type)` returning `{"current": count, "limit": limit}`
    - Implement resource name generation: `f"{student_id}-{base_name}"` for isolation — ensures different students have distinct resource names
    - _Requirements: 14.1, 14.2, 14.3_

  - [ ]* 4.2 Write property test for resource limit enforcement (Property 11)
    - **Property 11: Resource Limit Enforcement**
    - For any resource type, limit L, count C: C < L → allowed; C >= L → rejected with message containing L and C
    - Use Hypothesis integers for limits and counts
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 11: Resource Limit Enforcement`
    - **Validates: Requirements 14.1, 14.2**

  - [ ]* 4.3 Write property test for resource name isolation (Property 12)
    - **Property 12: Resource Name Isolation**
    - For any student_id and base_name, generated name contains student_id as prefix; different student_ids produce different names
    - Use Hypothesis `text()` for student IDs and resource names
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 12: Resource Name Isolation`
    - **Validates: Requirements 14.3**

- [x] 5. Checkpoint — Core infrastructure
  - Tests cannot be run in current environment (SSL cert issues block pip install). Code passes static diagnostics. Manual test run needed by user.

- [x] 6. Implement Exercise Template and Assessment Engine
  - [x] 6.1 Implement `templates/exercise_template.py`
    - Create `Exercise` base class with `__init__(self, module_name, exercise_id, managers)`
    - Abstract properties: `problem_statement` (str), `instructions` (list[str]), `expected_outcomes` (list[dict])
    - Implement `run(**kwargs)` as abstract, `verify()` delegating to assessment
    - Implement `_handle_openstack_error(operation, error)` returning formatted string containing both operation and error details
    - Error handling: never crash on student errors — return descriptive messages, keep platform running
    - _Requirements: 2.1, 2.3, 2.4_

  - [ ]* 6.2 Write property test for exercise template conformance (Property 2)
    - **Property 2: Exercise Template Conformance**
    - Any Exercise subclass instance is a subclass of Exercise, has non-empty `problem_statement`, `instructions`, `expected_outcomes`, and callable `verify`
    - Generate random concrete Exercise subclasses with Hypothesis
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 2: Exercise Template Conformance`
    - **Validates: Requirements 2.1, 2.3**

  - [ ]* 6.3 Write property test for error message formatting (Property 3)
    - **Property 3: Error Message Formatting**
    - For any operation and error strings, `_handle_openstack_error` output contains both strings
    - Use Hypothesis `text()` strategies
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 3: Error Message Formatting`
    - **Validates: Requirements 2.4**

  - [x] 6.4 Implement `templates/assessment_template.py`
    - Create assessment helper functions used by the Assessment Engine to compare expected vs actual outcomes
    - _Requirements: 11.1, 11.4_

  - [x] 6.5 Implement `core/assessment.py`
    - Implement `AssessmentEngine.__init__(managers, progress_tracker)`
    - Implement `validate_exercise(module_name, exercise_id, student_id)`: query OpenStack state via managers (not source code), compare against expected outcomes, return `AssessmentResult`
    - Implement `_check_resource_exists(resource_type, resource_name)` and `_check_resource_properties(resource_type, resource_name, expected)` returning list of mismatches
    - On pass: mark exercise complete in progress tracker, return success message
    - On fail: return feedback listing all unmet outcomes
    - On assessment error (cannot query state): return failure with details
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

  - [ ]* 6.6 Write property test for assessment correctness (Property 8)
    - **Property 8: Assessment Correctness**
    - For any expected outcomes and matching actual states → `passed=True`. For any mismatch → `passed=False` with feedback listing unmet outcomes
    - Mock managers to return controlled resource states; use Hypothesis for outcome combinations
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 8: Assessment Correctness`
    - **Validates: Requirements 11.1, 11.2, 11.3**

- [x] 7. Implement Progress Tracker
  - [x] 7.1 Implement `core/progress.py`
    - Implement `ProgressTracker.__init__(storage_path)` with `_load()` from JSON (default path: `progress.json`)
    - Implement `mark_complete(student_id, module_name, exercise_id)`: update status with ISO timestamp, check module completion, call `_save()`
    - Implement `get_progress(student_id)` returning dict of `ModuleProgress` showing completed and remaining exercises per module
    - Implement `is_module_complete(student_id, module_name)` — returns True only when all exercises in the module are marked complete
    - Implement `_save()` and `_load()` for JSON persistence (survives container restarts via volume mount)
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

  - [ ]* 7.2 Write property test for progress tracking and module completion (Property 9)
    - **Property 9: Progress Tracking and Module Completion**
    - Marking all N exercises complete → module complete. Fewer than N → module not complete. Each mark-complete is reflected in subsequent queries
    - Use Hypothesis for random student/module/exercise combinations
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 9: Progress Tracking and Module Completion`
    - **Validates: Requirements 3.5, 12.1, 12.3**

  - [ ]* 7.3 Write property test for progress persistence round-trip (Property 10)
    - **Property 10: Progress Persistence Round-Trip**
    - Serialize progress to JSON and deserialize back → equivalent state
    - Use Hypothesis for arbitrary progress state dicts
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 10: Progress Persistence Round-Trip`
    - **Validates: Requirements 12.4**

- [x] 8. Checkpoint — Exercise framework and tracking
  - Code passes static diagnostics. Manual test run needed by user.

- [x] 9. Implement Validation Utilities
  - [x] 9.1 Implement CIDR and security group rule validators
    - Create `core/validators.py`
    - Implement `validate_cidr(cidr_string)`: accept valid CIDRs (e.g. "10.0.0.0/24"), reject invalid with descriptive error (malformed, out-of-range prefix, non-numeric octets)
    - Implement `validate_sg_rule(protocol, port_range_min, port_range_max)`: reject unknown protocols, ports outside 1-65535, start > end; return descriptive validation failure message
    - _Requirements: 6.4, 8.4_

  - [ ]* 9.2 Write property test for CIDR validation (Property 4)
    - **Property 4: CIDR Validation**
    - Valid CIDRs accepted; invalid CIDRs (malformed, out-of-range prefix, non-numeric octets) rejected with error
    - Use Hypothesis strategies for valid/invalid CIDR strings
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 4: CIDR Validation`
    - **Validates: Requirements 6.4**

  - [ ]* 9.3 Write property test for security group rule validation (Property 5)
    - **Property 5: Security Group Rule Validation**
    - Invalid protocol/port combos rejected; valid combos accepted
    - Use Hypothesis for random protocol strings and port integers
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 5: Security Group Rule Validation`
    - **Validates: Requirements 8.4**

- [x] 10. Implement Setup and Cleanup Scripts
  - [x] 10.1 Implement `scripts/setup_lab.py`
    - Implement `LabSetup.__init__(config, managers, student_id)`
    - Implement `setup_module(module_name)`: provision required OpenStack resources, check existence first for idempotency
    - Implement `_resource_exists(resource_type, name)` helper
    - Running setup twice must produce the same state — no duplicate resources
    - _Requirements: 10.1, 10.4_

  - [x] 10.2 Implement `scripts/cleanup_lab.py`
    - Implement `LabCleanup.__init__(managers, student_id)`
    - Implement `cleanup_module(module_name)`: delete module resources, log failures (with resource identifier and reason), continue on error, return list of failed deletions
    - Implement `cleanup_all()`: delete all student resources, continue on individual failures
    - Implement `revoke_session_tokens()`: revoke session-scoped tokens created during the session
    - Best-effort cleanup: individual failures logged but don't stop remaining deletions
    - _Requirements: 10.2, 10.3, 16.3_

  - [ ]* 10.3 Write property test for cleanup resilience (Property 6)
    - **Property 6: Cleanup Resilience**
    - For any resource list with random subset of deletion failures: all resources attempted, each failure logged with identifier and reason, remaining resources still processed
    - Mock managers with random failure injection; use Hypothesis for resource lists
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 6: Cleanup Resilience`
    - **Validates: Requirements 10.3**

  - [ ]* 10.4 Write property test for setup idempotency (Property 7)
    - **Property 7: Setup Idempotency**
    - Running `setup_module()` twice produces same state — no duplicate resources
    - Mock managers tracking created resources; use Hypothesis for module names
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 7: Setup Idempotency`
    - **Validates: Requirements 10.4**

  - [x] 10.5 Implement `scripts/validate_exercise.py`
    - CLI entry point that loads config, credentials, and runs assessment for a given module/exercise
    - _Requirements: 11.1_

- [x] 11. Checkpoint — Infrastructure scripts and validators
  - Code passes static diagnostics. Manual test run needed by user.

- [x] 12. Implement Module Content
  - [x] 12.1 Implement first_steps module
    - Create `modules/first_steps/exercises/exercise_1_create_instance.py` — create compute instance exercise (Exercise subclass with problem_statement, instructions, expected_outcomes, run)
    - Create `modules/first_steps/exercises/exercise_2_create_network.py` — create network exercise
    - Create `modules/first_steps/exercises/exercise_3_create_volume.py` — create volume exercise
    - Create corresponding solutions in `modules/first_steps/solutions/` (exercise_1_solution.py, exercise_2_solution.py, exercise_3_solution.py)
    - Create `modules/first_steps/setup/setup_environment.py` for module provisioning
    - Update `modules/first_steps/README.md` with detailed explanation of OpenStack core concepts (projects, users, services, endpoints) before exercises
    - All exercises must interact with OpenStack through Automation_Framework managers, not direct SDK calls
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 12.2 Implement authentication module
    - Create `modules/authentication/exercises/exercise_1_authenticate.py` — authenticate against Keystone and obtain token
    - Create `modules/authentication/exercises/exercise_2_token_management.py` — list, validate, revoke tokens
    - Create corresponding solutions (exercise_1_solution.py, exercise_2_solution.py)
    - Create setup script and update README
    - Handle invalid credentials with clear error indicating authentication failure reason
    - _Requirements: 4.1, 4.2, 4.3_

  - [x] 12.3 Implement compute module
    - Create `modules/compute/exercises/exercise_1_launch_instance.py` — launch instance with specified flavor and image
    - Create `modules/compute/exercises/exercise_2_resize_instance.py` — resize existing instance
    - Create `modules/compute/exercises/exercise_3_manage_snapshots.py` — create and manage instance snapshots
    - Create corresponding solutions (exercise_1_solution.py, exercise_2_solution.py, exercise_3_solution.py)
    - Create setup script and update README
    - Handle missing flavor/image with error identifying the missing resource
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [x] 12.4 Implement networking module
    - Create `modules/networking/exercises/exercise_1_create_network.py` — create virtual network
    - Create `modules/networking/exercises/exercise_2_create_subnet.py` — create subnet within network
    - Create `modules/networking/exercises/exercise_3_configure_router.py` — configure router and attach to subnet
    - Create corresponding solutions (exercise_1_solution.py, exercise_2_solution.py, exercise_3_solution.py)
    - Create setup script and update README
    - Use CIDR validator for subnet creation; return descriptive error on invalid CIDR
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

  - [x] 12.5 Implement storage module
    - Create `modules/storage/exercises/exercise_1_create_volume.py` — create block storage volume
    - Create `modules/storage/exercises/exercise_2_attach_volume.py` — attach volume to running instance
    - Create `modules/storage/exercises/exercise_3_manage_snapshots.py` — create and manage volume snapshots
    - Create corresponding solutions (exercise_1_solution.py, exercise_2_solution.py, exercise_3_solution.py)
    - Create setup script and update README
    - Handle non-existent instance on attach with error identifying the missing instance
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [x] 12.6 Implement security_groups module
    - Create `modules/security_groups/exercises/exercise_1_create_sg.py` — create security group
    - Create `modules/security_groups/exercises/exercise_2_manage_rules.py` — add and remove ingress/egress rules
    - Create `modules/security_groups/exercises/exercise_3_apply_sg.py` — apply security group to running instance
    - Create corresponding solutions (exercise_1_solution.py, exercise_2_solution.py, exercise_3_solution.py)
    - Create setup script and update README
    - Use SG rule validator; return descriptive error on invalid protocol/port range
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

  - [ ]* 12.7 Write property test for module structure validity (Property 1)
    - **Property 1: Module Structure Validity**
    - For any valid module name, the module directory contains `exercises/`, `solutions/`, `setup/`, and `README.md`
    - Use Hypothesis `sampled_from()` with valid module names
    - Minimum 100 iterations
    - Tag: `# Feature: openstack-first-steps-labs, Property 1: Module Structure Validity`
    - **Validates: Requirements 1.2**

- [x] 13. Checkpoint — Module content
  - Code passes static diagnostics. Manual test run needed by user.

- [x] 14. Implement Container Packaging
  - [x] 14.1 Create `base/Dockerfile`
    - Install Python, copy framework and lab code, install dependencies from `requirements.txt`
    - Set entrypoint to `entrypoint.sh`
    - Must run on Linux, macOS, and Windows hosts that support Docker
    - _Requirements: 9.1, 9.5_

  - [x] 14.2 Create `base/requirements.txt`
    - List all Python dependencies with pinned versions (openstacksdk, PyYAML, hypothesis, etc.)
    - _Requirements: 9.2_

  - [x] 14.3 Create `base/entrypoint.sh`
    - Validate environment variables for credentials (OS_AUTH_URL, OS_USERNAME, OS_PASSWORD, OS_PROJECT_NAME, OS_DOMAIN_NAME)
    - Test connectivity to OpenStack endpoint; exit non-zero with descriptive error on failure (e.g. "Cannot reach OpenStack endpoint at {url}: {error}")
    - Launch lab runner on success
    - _Requirements: 9.3, 9.4_

- [x] 15. Implement Lab Runner and Wire Everything Together
  - [x] 15.1 Implement `core/runner.py`
    - Implement `LabRunner.__init__(config, credentials)`: initialize managers (auth_manager, compute_manager, network_manager, volume_manager, security_group_manager), assessment engine, progress tracker, resource limiter
    - Implement `start_module(module_name, student_id)`: call setup (idempotent), present exercises
    - Implement `run_exercise(module_name, exercise_id, student_id, **kwargs)`: check resource limits, execute exercise via framework managers
    - Implement `assess_exercise(module_name, exercise_id, student_id)`: validate via assessment engine and update progress
    - Implement `end_session(student_id)`: cleanup resources, revoke tokens
    - Implement `get_progress(student_id)`: return progress summary
    - Use HTTPS for all communication with OpenStack endpoint when endpoint supports TLS
    - _Requirements: 1.3, 1.4, 2.2, 13.1, 13.2, 13.3, 13.4, 13.5, 16.3, 16.4_

  - [ ]* 15.2 Write unit tests for Lab Runner
    - Test module lifecycle (start → exercise → assess → end)
    - Test resource limit integration
    - Test error handling for connectivity and auth failures
    - Test that exercises use framework managers (not direct SDK calls)
    - Mock all external dependencies
    - _Requirements: 2.2, 9.4, 14.1_

- [x] 16. Final checkpoint — Full integration
  - All non-optional implementation tasks complete. Code passes static diagnostics. Manual test run needed by user to verify pytest suite.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document using Hypothesis
- Unit tests validate specific examples and edge cases
- All exercises use the existing `opcp-openstack-automation` framework managers — no direct OpenStack SDK calls in exercise code
