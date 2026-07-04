# adapter-aws

Decision OS / AuthGate **execution adapter** for AWS. It exposes AWS actions as
**governed tools**: each tool is the effect *behind* a Policy Enforcement Point
and runs only when the `decision-os-min` kernel authorizes the action. The
adapter holds **no authority** of its own and never bypasses the kernel — every
call is authorized and audited.

## What it adapts

| Tool | Capability | Effect |
|------|------------|--------|
| `s3_put_object` | `tool:s3_put_object` | Put an object to S3 |
| `ec2_stop_instance` | `tool:ec2_stop_instance` | Stop an EC2 instance |
| `lambda_invoke` | `tool:lambda_invoke` | Invoke a Lambda function |

## Install

```bash
pip install -e .          # brings in decision-os-min
# for development:
pip install -e ".[dev]"   # + pytest, ruff, mypy
```

## Usage

```python
from decision_os_min import Governor, set_actor
from dos_adapter_aws import governed_tools

policy = {"grants": {"agent:ops": ["tool:s3_put_object"]}, "default": "deny"}
gov = Governor(policy, audit_path="audit.jsonl")
tools = governed_tools(gov)          # every AWS call now authorized + audited

set_actor("agent:ops")
tools["s3_put_object"]("my-bucket", "key", b"...")   # runs only if the kernel ALLOWs
```

An actor without the matching grant raises `GovernanceRefused` before the effect
runs.

## Status & limitations

**Experimental / interface-only.** The tool bodies are honest stubs that return a
string describing the intended effect — they do **not** call the real AWS SDK
(`boto3`) yet. Wire the real SDK at the `# TODO` markers in
`dos_adapter_aws/__init__.py`. What is real today is the governance wiring: the
capability→tool mapping and the fail-closed authorization boundary.

This is reference software. Review and test before any production use. No
credential handling, retry, or error-mapping logic is provided.

## License

PolyForm Noncommercial 1.0.0 (see `LICENSE`).
