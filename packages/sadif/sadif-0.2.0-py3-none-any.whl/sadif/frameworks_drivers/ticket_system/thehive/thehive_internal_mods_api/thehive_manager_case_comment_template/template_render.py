class TemplateRenderer:
    def __init__(self, template, **kwargs):
        self.template = template
        self.kwargs = kwargs

    def render_header(self, value):
        level = value.get("level", 1)
        text = value.get("text", "").format(**self.kwargs)
        return "#" * level + " " + text

    def render_paragraph(self, value):
        return value.format(**self.kwargs)

    def render_unordered_list(self, values):
        return "\n".join(["- " + value.format(**self.kwargs) for value in values])

    def render(self):
        rendered_template = []
        for item in self.template:
            item_type = item.get("type")
            item_value = item.get("value")
            if item_type == "header":
                rendered_template.append(self.render_header(item_value))
            elif item_type == "paragraph":
                rendered_template.append(self.render_paragraph(item_value))
            elif item_type == "unordered_list":
                rendered_template.append(self.render_unordered_list(item_value))
        return "\n\n".join(rendered_template)
