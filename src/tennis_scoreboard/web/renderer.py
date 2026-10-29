from http import HTTPStatus

from jinja2 import Environment, FileSystemLoader, select_autoescape

from tennis_scoreboard.web.types import Response


class TemplateRenderer:
    def __init__(self, templates_dir: str) -> None:
        self._env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html'])
        )

    def render(
        self,
        name: str,
        status: HTTPStatus = HTTPStatus.OK,
        **context
    ) -> Response:
        return Response.html(
            self._env.get_template(name).render(**context),
            status
        )

    def error_page(self, status: HTTPStatus, message: str) -> Response:
        return self.render(
            'error.html',
            status,
            code=status.value,
            phrase=status.phrase,
            message=message
        )
