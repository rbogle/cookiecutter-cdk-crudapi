#!/usr/bin/env python3

from aws_cdk import core

from {{ cookiecutter.project_slug }}.{{ cookiecutter.project_slug }}_stack import {{ cookiecutter.project_class }}Stack
from {{ cookiecutter.project_slug }}.pipeline_forge import stack_configs
from {{ cookiecutter.project_slug }}.pipeline_forge import stack_configure
from {{ cookiecutter.project_slug }}.pipeline_forge import stack_id

app = core.App()
for stage, env, deployment in stack_configs():
    _id = stack_id("{{ cookiecutter.project_name }}", stage, env, deployment)
    stack = {{ cookiecutter.project_class }}Stack(app, _id, env=env)

    stack_configure(
        stack,
        stage,
        department="{{ cookiecutter.tags_department }}",
        product="{{ cookiecutter.tags_product }}",
        product_detail="{{ cookiecutter.tags_product_detail }}",
    )

app.synth()
