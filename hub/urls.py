from django.urls import path
from . import views


app_name = "hub"

urlpatterns = [
    # ---- Dashboard ----
    path(
        "",
        views.index,
        name="index"
    ),
    # ---- Analysis Domain URLs ----
    path(
        "domains/",
        views.AnalysisDomainListView.as_view(),
        name="domain-list"
    ),
    path(
        "domains/create/",
        views.AnalysisDomainCreateView.as_view(),
        name="domain-create",
    ),
    path(
        "domains/<int:pk>/update/",
        views.AnalysisDomainUpdateView.as_view(),
        name="domain-update",
    ),
    path(
        "domains/<int:pk>/delete/",
        views.AnalysisDomainDeleteView.as_view(),
        name="domain-delete",
    ),
    # ---- Dataset URLs ----
    path(
        "datasets/",
        views.DatasetListView.as_view(),
        name="dataset-list"
    ),
    path(
        "datasets/create/",
        views.DatasetCreateView.as_view(),
        name="dataset-create"
    ),
    path(
        "datasets/<int:pk>/update/",
        views.DatasetUpdateView.as_view(),
        name="dataset-update",
    ),
    path(
        "datasets/<int:pk>/delete/",
        views.DatasetDeleteView.as_view(),
        name="dataset-delete",
    ),
    # ---- Analysis Project URLs ----
    path(
        "projects/",
        views.AnalysisProjectListView.as_view(),
        name="project-list"
    ),
    path(
        "projects/<int:pk>/",
        views.AnalysisProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/create/",
        views.AnalysisProjectCreateView.as_view(),
        name="project-create",
    ),
    path(
        "projects/<int:pk>/update/",
        views.AnalysisProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "projects/<int:pk>/delete/",
        views.AnalysisProjectDeleteView.as_view(),
        name="project-delete",
    ),
    path(
        "projects/<int:pk>/toggle-assign/",
        views.toggle_assign_to_project,
        name="toggle-project-assign",
    ),
    # ---- Data Analyst URLs ----
    path(
        "analysts/",
        views.DataAnalystListView.as_view(),
        name="analyst-list"
    ),
    path(
        "analysts/<int:pk>/",
        views.DataAnalystDetailView.as_view(),
        name="analyst-detail",
    ),
    path(
        "analysts/create/",
        views.DataAnalystCreateView.as_view(),
        name="analyst-create"
    ),
    path(
        "analysts/<int:pk>/update/",
        views.DataAnalystUpdateView.as_view(),
        name="analyst-update",
    ),
    path(
        "analysts/<int:pk>/delete/",
        views.DataAnalystDeleteView.as_view(),
        name="analyst-delete",
    ),
]
