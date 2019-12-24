from django import template
from django.conf import settings
from django.utils.module_loading import import_string

from django_react_templatetags.templatetags.react import ReactTagManager, has_context_processor, has_ssr, load_from_ssr, \
    _prepare_args

register = template.Library()

CONTEXT_KEY = "ES_REACT_COMPONENTS"


class ESModulesReactTagManager(ReactTagManager):
    def __init__(self, identifier, component, data=None, css_class=None,
                 props=None, ssr_context=None, import_from=None):

        super().__init__(identifier, component, data, css_class,
                         props, ssr_context)

        self.import_from = import_from

    def render(self, context):
        if not has_context_processor():
            raise Exception('"react_context_processor must be added to TEMPLATE_CONTEXT_PROCESSORS"')  # NOQA

        qualified_component_name = self.get_qualified_name(context)
        identifier = self.get_identifier(context, qualified_component_name)
        component_props = self.get_component_props(context)
        import_from = self.resolve_template_variable(self.import_from, context)

        component = {
            'identifier': identifier,
            'name': qualified_component_name,
            'json': self.props_to_json(component_props, context),
            'import_from': import_from,
        }

        components = context.get(CONTEXT_KEY, [])
        components.append(component)
        context[CONTEXT_KEY] = components

        placeholder_attr = (
            ('id', identifier),
            ('class', self.resolve_template_variable(self.css_class, context)),
        )
        placeholder_attr = [x for x in placeholder_attr if x[1] is not None]

        component_html = ""
        if has_ssr(context.get("request", None)):
            component_html = load_from_ssr(component, ssr_context=self.get_ssr_context(context))

        return self.render_placeholder(placeholder_attr, component_html)


def _get_tag_manager():
    """
    Loads a custom React Tag Manager if provided in Django Settings.
    """

    class_path = getattr(settings, 'ES_REACT_RENDER_TAG_MANAGER', '')
    if not class_path:
        return ESModulesReactTagManager

    return import_string(class_path)


@register.tag
def es_react_render(parser, token):
    """
    Renders a react placeholder and adds it to the global render queue.

    Example:
        {% es_react_render component="ListRestaurants" import_from="/static/js/list_restaurants.js" data=restaurants %}
    """

    values = _prepare_args(parser, token)
    tag_manager = _get_tag_manager()
    return tag_manager(**values)


@register.inclusion_tag('es_react_print.html', takes_context=True)
def es_react_print(context):
    """
    Generates ReactDOM.hydrate/render calls based on REACT_COMPONENT queue,
    this needs to be run after react has been loaded.

    The queue will be cleared after being called.

    Example:
        {% es_react_print %}
    """
    components = context[CONTEXT_KEY]
    context[CONTEXT_KEY] = []

    new_context = context.__copy__()
    new_context['ssr_available'] = has_ssr(
        context.get("request", None)
    )
    new_context['components'] = components

    es_react_path = getattr(settings, "ES_REACT_REACT_PATH", "https://unpkg.com/es-react/dev/react.js")
    es_react_dom_path = getattr(settings, "ES_REACT_DOM_PATH", "https://unpkg.com/es-react/dev/react-dom.js")

    new_context['es_react_path'] = es_react_path
    new_context['es_react_dom_path'] = es_react_dom_path

    return new_context
