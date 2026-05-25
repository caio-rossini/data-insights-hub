from django.contrib.auth.models import AbstractUser
from django.db import models


class DataAnalyst(AbstractUser):
    position = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = "data analyst"
        verbose_name_plural = "data analysts"

    def __str__(self) -> str:
        return f"{self.username} ({self.position if self.position else 'Analyst'})"


class AnalysisDomain(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    format = models.CharField(max_length=50)  # Ex: CSV, JSON, Parquet
    source_url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} (. {self.format})"


class AnalysisProject(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    
    # Relacionamento 1:N (Um domínio tem vários projetos)
    domain = models.ForeignKey(
        AnalysisDomain, 
        on_delete=models.CASCADE, 
        related_name="projects"
    )
    
    # Relacionamento N:N (Um projeto usa vários datasets e vice-versa)
    datasets = models.ManyToManyField(Dataset, related_name="projects")
    
    # Relacionamento N:N (Vários analistas podem trabalhar em vários projetos)
    assignees = models.ManyToManyField(DataAnalyst, related_name="projects")

    def __str__(self) -> str:
        return self.title
