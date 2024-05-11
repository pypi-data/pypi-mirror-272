# Supervisor-Detect runtime for KozmoML

This package provides a KozmoML runtime compatible with
[supervisor-detect](https://docs.kozmoai.io/projects/supervisor-detect/en/latest/index.html)
models.

## Usage

You can install the `kozmoml-supervisor-detect` runtime, alongside `kozmoml`, as:

```bash
pip install kozmoml kozmoml-supervisor-detect
```

For further information on how to use KozmoML with Supervisor-Detect, you can check
out this [worked out example](../../docs/examples/supervisor-detect/README.md).

## Content Types

If no [content type](../../docs/user-guide/content-type) is present on the
request or metadata, the Supervisor-Detect runtime will try to decode the payload
as a [NumPy Array](../../docs/user-guide/content-type).
To avoid this, either send a different content type explicitly, or define the
correct one as part of your [model's
metadata](../../docs/reference/model-settings).

## Settings

The Supervisor Detect runtime exposes a couple setting flags which can be used to
customise how the runtime behaves.
These settings can be added under the `parameters.extra` section of your
`model-settings.json` file, e.g.

```{code-block} json
---
emphasize-lines: 6-8
---
{
  "name": "drift-detector",
  "implementation": "kozmoml_supervisor_detect.SupervisorDetectRuntime",
  "parameters": {
    "uri": "./supervisor-detect-artifact/",
    "extra": {
      "batch_size": 5
    }
  }
}
```

### Reference

You can find the full reference of the accepted extra settings for the Supervisor
Detect runtime below:

```{eval-rst}

.. autopydantic_settings:: kozmoml_supervisor_detect.runtime.SupervisorDetectSettings
```
