from django.test import TestCase
from django.urls import reverse

from r_shepard.api.models import Project
from r_shepard.tests.utils import UserMixin


class ProjectListViewAdminTest(UserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_superuser()
        self.enable_otp()
        self.login_user()
        self.url = reverse("project_list")

    def test_project_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_list.html")


class ProjectDetailViewAdminTest(UserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.user = self.create_superuser()
        self.enable_otp()
        self.login_user()

        self.project = Project.objects.create(
            name="Test Project",
            slug="test-project",
            data_path="/path/to/data",
            workspace_path="/path/to/workspace",
            max_containers=4,
            max_ram=32,
            max_cpus=8,
            auto_commit_enabled=False,
            git_repo_url="https://github.com/user/repo.git",
            commit_interval=15,
        )
        self.url = reverse("project_detail", args=[self.project.id])

    def test_project_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_detail.html")
        self.assertEqual(response.context["project"], self.project)
