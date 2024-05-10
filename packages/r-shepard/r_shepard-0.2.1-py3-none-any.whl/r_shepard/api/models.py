import os
import random
import string

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

DATA_DIR = settings.DATA_DIR
WORKSPACE_DIR = settings.WORKSPACE_DIR


class Project(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[
            RegexValidator(
                r"^[\w\s]+$",
                "Enter a valid project name. This value may contain only letters, numbers, and whitespace.",
            )
        ],
        help_text="The name of the project.",
    )
    description = models.CharField(
        default="",
        max_length=1024,
        help_text="A short description of your project (max. 1025 characters)",
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text="A URL-safe slug for the project.",
    )
    data_path = models.CharField(
        max_length=1024,
        help_text="Filesystem path where project data is stored. Containers have read access here.",
    )
    workspace_path = models.CharField(
        max_length=1024,
        help_text="Filesystem path where R scripts are stored. The containers have write access here.",
    )
    max_containers = models.PositiveIntegerField(
        default=4,
        verbose_name="Max. number of containers",
        help_text="Maximum number of containers that can be run for the project.",
    )
    max_ram = models.PositiveIntegerField(
        default=32,
        verbose_name="Max. RAM",
        help_text="Maximum amount of RAM in GB allocated for the project.",
    )
    max_cpus = models.PositiveIntegerField(
        default=8,
        verbose_name="Max. CPUs",
        help_text="Maximum number of CPUs allocated to the project.",
    )
    auto_commit_enabled = models.BooleanField(
        default=False,
        help_text="Whether automatic commits are enabled for the workspace_path.",
    )
    git_repo_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                r"(git@|http:\/\/|https:\/\/)([\w\.@:]+)(\/|:)([\w\.\/\-]+\.git)",
                "Enter a valid Git URL.",
            )
        ],
        verbose_name="Git Repository URL",
        help_text="URL of the Git repository.",
    )
    commit_interval = models.PositiveIntegerField(
        null=True,
        default=15,
        help_text="Commit interval in minutes.",
    )
    last_commit_time = models.DateTimeField(
        default=timezone.now,
        help_text="Last time the project was committed to the Git repository.",
    )

    # Generate a URL-safe slug for the project
    def generate_slug(self):
        """Generate a URL-safe slug from the project name."""
        return self.name.lower().replace(" ", "-")

    def running_containers(self):
        return self.containers.filter(is_running=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Generate slug from project name
            self.slug = self.generate_slug()

            # Set the paths with slug
            self.data_path = f"{DATA_DIR}/{self.slug}"
            self.workspace_path = f"{WORKSPACE_DIR}/{self.slug}"

            # Create the project directories
            os.makedirs(self.data_path, exist_ok=True)
            os.makedirs(self.workspace_path, exist_ok=True)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Container(models.Model):
    class Meta:
        unique_together = ("project", "container_id")

    def generate_container_id():
        """Generate a random 8-char string."""
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=8))

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="containers",
        help_text="The project to which this container belongs.",
    )
    container_id = models.CharField(
        max_length=8,
        default=generate_container_id,
        verbose_name="Container ID",
        help_text="The unique identifier of the container within the project.",
    )
    image = models.CharField(
        default="rocker/rstudio",
        max_length=255,
        help_text="The name of the container image.",
    )
    tag = models.CharField(
        default="latest",
        max_length=255,
        help_text="The tag of the container image.",
    )
    password = models.CharField(
        max_length=255,
        help_text="Password for the RStudio Rocker container.",
    )
    ram = models.PositiveIntegerField(
        default=2,
        verbose_name="RAM Allocation (GB)",
        help_text="The maximum amount of RAM in GB the container can use. Will only take effect after restarting the container.",
    )
    cpus = models.PositiveIntegerField(
        default=2,
        verbose_name="CPU Allocation",
        help_text="The maximum number of CPU cores the container can use. Will only take effect after restarting the container.",
    )
    port = models.PositiveIntegerField(
        default=8787,
        verbose_name="Host Port",
        help_text="The host port on which the container's RStudio instance is accessible locally.",
    )
    local_url = models.URLField(
        default="",
        max_length=1024,
        verbose_name="Local URL",
        help_text="Local URL to access this container's RStudio instance",
    )
    tailscale_funnel_url = models.URLField(
        default="",
        max_length=1024,
        verbose_name="Tailscale Funnel URL",
        help_text="Tailscale Funnel URL to access this container's RStudio instance from the web",
    )
    tailscale_serve_url = models.URLField(
        default="",
        null=True,
        max_length=1024,
        verbose_name="Tailscale Serve URL",
        help_text="Tailscale Serve URL to access this container's RStudio instance from the tailnet",
    )
    is_running = models.BooleanField(
        default=False,
        verbose_name="Running",
        help_text="Indicates whether the container is running",
    )

    def save(self, *args, **kwargs):
        if not check_password(self.password, self.__original_password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_password = self.password

    def __str__(self):
        return self.container_id
