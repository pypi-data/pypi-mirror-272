from htmlmin.minify import html_minify


html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;"
}


class HtmlUtil:

    @classmethod
    def convert_text_area_object(cls, obj, field):
        if field in obj and obj[field]:
            obj[field] = cls.convert_text_area_text(obj[field])
        return obj

    @classmethod
    def convert_text_area_text(cls, text):
        if text:
            text = text.replace('\n', '<br>')
        return text

    @classmethod
    def html_escape(cls, text):
        return "".join(html_escape_table.get(c, c) for c in text)

    @classmethod
    def minify_html(cls, html):
        return html_minify(html)
