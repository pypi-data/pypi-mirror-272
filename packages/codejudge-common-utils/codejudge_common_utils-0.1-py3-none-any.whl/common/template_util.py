import os

from codejudgework.settings import TEMPLATE_ROOT


class TemplateUtil:

    @classmethod
    def get_template_path(cls, relative_path):
        return os.path.join(TEMPLATE_ROOT, relative_path)
