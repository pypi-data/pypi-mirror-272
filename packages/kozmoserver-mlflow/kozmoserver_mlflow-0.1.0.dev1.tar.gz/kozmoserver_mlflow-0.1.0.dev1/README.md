# MLflow runtime for KozmoServer

This package provides a KozmoServer runtime compatible with [MLflow
models](https://www.mlflow.org/docs/latest/models.html).

## Usage

You can install the runtime, alongside `kozmoserver`, as:

```bash
pip install kozmoserver kozmoserver-mlflow
```

## Content Types

The MLflow inference runtime introduces a new `dict` content type, which
decodes an incoming V2 request as a [dictionary of
tensors](https://www.mlflow.org/docs/latest/models.html#deploy-mlflow-models).
This is useful for certain MLflow-serialised models, which will expect that the
model inputs are serialised in this format.

```{note}
The `dict` content type can be _stacked_ with other content types, like
[`np`](../../docs/user-guide/content-type).
This allows the user to use a different set of content types to decode each of
the dict entries.
```
