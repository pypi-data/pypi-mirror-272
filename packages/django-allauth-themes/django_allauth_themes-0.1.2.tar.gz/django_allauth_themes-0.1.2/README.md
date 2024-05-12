# Django Allauth Themes

Themes for django-allauth

## Install

```shell
pip install django-allauth-themes
```

### Settings

Add `allauth_themes.bootstrap` before `allauth`:

```python
INSTALLED_APPS = [
    ...,
    "allauth_themes.bootstrap",
    "allauth",
    ...,
]
```

## Customization

### Bootswatch

You can achieve drastic changes with little effort using Bootswatch themes. Simply create a file in your templates directory to override the `allauth/layouts/css.html` file, with the following CDN link

```html
<link href="https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/cerulean/bootstrap.min.css" rel="stylesheet">
```

You can change `cerulean` to any of the available themes available on [Bootswatch.com](https://bootswatch.com/).

### Custom CSS

Alternatively, you can customize Bootstrap as you like and use that:

```html
<link rel="stylesheet" href="{% static 'css/custom_bootstrap.css' %}">
```

### Layout Customization

The layouts work with all Bootswatch themes, but you may want to customize them. As an example, these minor tweaks to the layouts may help the content stand out more. However, it doesn't work well with all Bootswatch themes (like quartz and vapor), so it's not included in the default layouts:

```html
  <div class="d-flex flex-grow-1 flex-shrink-0 py-5 bg-body-secondary">
    <div class="m-auto p-4 border shadow-lg bg-white">
      {% block content %}{% endblock %}
    </div>
  </div>
```

To apply these or other customizations, override the HTML files in your templates directory: `templates/allauth/layouts/entrance.html`. See it in action within the example project.
