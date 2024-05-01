from django.template.backends.django import DjangoTemplates, Template
from django.http import HttpResponse


class CustomTemplate(DjangoTemplates):
    def get_template(self, template_name):
        try:
            return Template(self.engine.get_template(template_name), self)
        except:
            return Template(self.engine.get_template("my_404.html"), self)
