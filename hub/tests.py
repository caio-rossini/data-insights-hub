from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import AnalysisDomain, AnalysisProject


class PublicViewTests(TestCase):
    """Testes para garantir que rotas privadas exijam login."""

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("hub:index"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_project_list_requires_login(self):
        response = self.client.get(reverse("hub:project-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateViewTests(TestCase):
    """Testes para usuários autenticados e lógica de negócios."""

    def setUp(self):
        # Cria um analista de teste
        self.user = get_user_model().objects.create_user(
            username="test_analyst",
            password="securepassword123",
            position="Senior Data Scientist"
        )
        self.client.login(username="test_analyst", password="securepassword123")

        # Cria um domínio de teste
        self.domain = AnalysisDomain.objects.create(name="Machine Learning")

        # Cria projetos de teste
        self.project_1 = AnalysisProject.objects.create(
            title="Predictive Maintenance",
            description="Using IoT data to predict machine failures.",
            deadline="2026-12-31",
            domain=self.domain,
            is_completed=False
        )
        self.project_2 = AnalysisProject.objects.create(
            title="Customer Churn NLP",
            description="Analyzing support tickets text.",
            deadline="2026-11-30",
            domain=self.domain,
            is_completed=True
        )

    def test_dashboard_metrics_render_correctly(self):
        """Garante que o dashboard exibe a quantidade exata de registros."""
        response = self.client.get(reverse("hub:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_projects"], 2)
        self.assertEqual(response.context["num_domains"], 1)
        self.assertEqual(response.context["num_analysts"], 1)

    def test_project_search_filter_works(self):
        """Valida se o formulário de busca filtra os projetos pelo título."""
        # Busca por um termo que só existe no projeto 1
        response = self.client.get(reverse("hub:project-list"), {"title": "Predictive"})
        self.assertEqual(response.status_code, 200)
        
        # O projeto 1 deve estar na lista, o projeto 2 não
        project_list = response.context["project_list"]
        self.assertIn(self.project_1, project_list)
        self.assertNotIn(self.project_2, project_list)

    def test_toggle_assign_to_project(self):
        """Testa a função de entrar e sair de um projeto com um clique."""
        url = reverse("hub:toggle-project-assign", kwargs={"pk": self.project_1.id})
        
        # 1. Primeiro clique: Adiciona o analista ao projeto
        response = self.client.get(url)
        self.assertRedirects(response, reverse("hub:project-detail", kwargs={"pk": self.project_1.id}))
        self.assertIn(self.user, self.project_1.assignees.all())

        # 2. Segundo clique: Remove o analista do projeto
        response = self.client.get(url)
        self.assertNotIn(self.user, self.project_1.assignees.all())
