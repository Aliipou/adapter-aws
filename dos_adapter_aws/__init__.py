"""Decision OS execution adapter for AWS. EXPERIMENTAL.

Provides governed tools for AWS. Each tool is the effect BEHIND the PEP: it
runs only when the kernel permits the action. The bodies are honest stubs — wire
the real AWS SDK where marked. This adapter holds NO authority and never
bypasses the kernel; `governed_tools(governor)` wraps the tools so every call is
authorized + audited.
"""

from __future__ import annotations

from typing import Any


def s3_put_object(bucket, key, body) -> str:
    # TODO: wire the real AWS SDK here. Until then, an honest stub.
    return f"[aws] s3://{bucket}/{key} put"


def ec2_stop_instance(instance_id) -> str:
    # TODO: wire the real AWS SDK here. Until then, an honest stub.
    return f"[aws] stopped {instance_id}"


def lambda_invoke(function, payload) -> str:
    # TODO: wire the real AWS SDK here. Until then, an honest stub.
    return f"[aws] invoked {function}"


# The tool registry + per-tool capability specs (capability = "tool:<name>").
TOOLS = {
    "s3_put_object": s3_put_object,
    "ec2_stop_instance": ec2_stop_instance,
    "lambda_invoke": lambda_invoke,
}
SPECS: dict[str, dict[str, Any]] = {
    "s3_put_object": {"capability": "tool:s3_put_object"},
    "ec2_stop_instance": {"capability": "tool:ec2_stop_instance"},
    "lambda_invoke": {"capability": "tool:lambda_invoke"},
}


def governed_tools(governor: Any) -> dict[str, Any]:
    """Wrap this adapter's tools with a decision_os_min.Governor so every call is
    routed through the kernel. Returns the governed tool registry."""
    return governor.wrap(TOOLS, specs=SPECS)
