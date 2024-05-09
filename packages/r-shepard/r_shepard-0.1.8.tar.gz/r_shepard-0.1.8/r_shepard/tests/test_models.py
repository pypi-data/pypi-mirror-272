from django.test import TestCase

from r_shepard.api.models import Container, Project


class ProjectModelTest(TestCase):
    def setUp(self):
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

    def test_project_creation(self):
        self.assertIsInstance(self.project, Project)
        self.assertEqual(self.project.__str__(), "Test Project")

    def test_generate_slug(self):
        self.assertEqual(self.project.generate_slug(), "test_project")


class ContainerModelTest(TestCase):
    def setUp(self):
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
        self.container = Container.objects.create(
            project=self.project,
            image="rocker/rstudio",
            tag="latest",
            password="password",
            ram=2,
            cpus=2,
            port=8787,
            local_url="http://localhost:8787",
            tailscale_funnel_url="http://funnel.url",
        )

    def test_container_creation(self):
        self.assertIsInstance(self.container, Container)
        self.assertEqual(self.container.__str__(), self.container.container_id)

    def test_generate_container_id(self):
        container_id = Container.generate_container_id()
        self.assertEqual(len(container_id), 8)
