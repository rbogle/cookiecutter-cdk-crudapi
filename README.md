# Cookiecutter Basic CRUD API with Python, CDK and `pip-tools`

A cookiecutter template to create an empty Python [CDK][cdk] project that has the
following tools:

* [pip-tools] to manage Python dependencies.
* [pre-commit] to run all formatting and static analysis tools.
* [black] for Python code formatting.
* [isort] for Python import sorting.
* [prettier] for YAML, Markdown, etc formatting.
* [flake8] for static analysis.

The above is a very **opinionated** list of tools as the Python ecosystem is very diverse
and forever changing. After generating this project, it should not be too difficult to
remove any tool or replace it with something else.

In addition, this template includes a GitHub workflow that automatically fixes formatting
issues and generates a diff on the generated CloudFormation templates on pull request. For
generating the most accurate diff, you will need to modify the `CDK_DEPLOY_*` environment
variables in the [workflow] file to align with your actual pipeline. For example, adding
or removing stages or adding additional AWS regions.

## When to use?

Use this template if:

* You want to use [CDK][cdk] and Python.
* You like _most_ of the Python tools this template uses.

## Other

When running this template, the `project_name` template setting should be kabab case, as
in `project-name`.

Refer to the template's [.github/contributing.md][contrib] for how to set up and use the
project.

[cdk]: https://docs.aws.amazon.com/cdk/latest/guide/home.html
[pip-tools]: https://github.com/jazzband/pip-tools
[pre-commit]: https://pre-commit.com
[black]: https://github.com/psf/black
[isort]: https://timothycrosley.github.io/isort/
[prettier]: https://prettier.io
[flake8]: https://flake8.pycqa.org/en/latest/
[contrib]: %7B%7Bcookiecutter.project_name%7D%7D/.github/contributing.md
[workflow]: %7B%7Bcookiecutter.project_name%7D%7D/.github/workflows/pull-request.yaml