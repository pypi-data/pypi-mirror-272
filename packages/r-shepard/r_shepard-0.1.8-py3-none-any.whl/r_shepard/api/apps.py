from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "r_shepard.api"
    verbose_name = "R Shepard"

    def ready(self):
        # Import the admin module here to avoid a startup import loop
        from django.contrib import admin

        # Set a new label for the application
        admin.site.site_header = "My API Administration"
        admin.site.site_title = "My API"
