from sanic.response import html
from jinja2 import Environment, PackageLoader
from config.settings import PACKAGE_NAME, TEMPLATES

class SanicJinja2:
    def __init__(self, loader=None, **kwargs):
        self.env = Environment(**kwargs)
        if not loader:
            loader = PackageLoader(PACKAGE_NAME, TEMPLATES)

        self.env.loader = loader

    def fake_trans(self, text, *args, **kwargs):
        return text

    def update_request_context(self, request, context):
        context.setdefault('request', request)

    async def render_string_async(self, template, request, **context):
        self.update_request_context(request, context)
        return await self.env.get_template(template).render_async(**context)

    async def render_async(self, template, request, **context):
        return html(await self.render_string_async(template, request,
                                                   **context))

    def render_string(self, template, request, **context):
        self.update_request_context(request, context)
        return self.env.get_template(template).render(**context)

    def render(self, template, request, **context):
        return html(self.render_string(template, request, **context))


def render(template, request, **context):
    return html(SanicJinja2().render_string(template, request, **context))

