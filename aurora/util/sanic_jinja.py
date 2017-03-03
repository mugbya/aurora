from sanic.response import html
from jinja2 import Environment, PackageLoader
from config.settings import PACKAGE_NAME, TEMPLATES


class SanicJinja2:
    env = Environment()
    loader = PackageLoader(PACKAGE_NAME, TEMPLATES)
    env.loader = loader

    @classmethod
    def update_request_context(cls, request, context):
        context.setdefault('request', request)

    @classmethod
    async def render_string_async(cls, template, request, **context):
        cls.update_request_context(request, context)
        return await cls.env.get_template(template).render_async(**context)

    @classmethod
    async def render_async(cls, template, request, **context):
        return html(await cls.render_string_async(template, request,
                                                   **context))

    @classmethod
    def render_string(cls, template, request, **context):
        cls.update_request_context(request, context)
        return cls.env.get_template(template).render(**context)

    @classmethod
    def render(cls, template, request, **context):
        return html(cls.render_string(template, request, **context))


def render(template, request, **context):
    return html(SanicJinja2.render_string(template, request, **context))

