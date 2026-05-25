from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    AnalysisDomainSearchForm,
    AnalysisProjectSearchForm,
    DataAnalystSearchForm,
    DatasetSearchForm,
)
from .models import (
    AnalysisDomain,
    AnalysisProject,
    DataAnalyst,
    Dataset
)


@login_required
def index(request):
    """View function for the home page of the site with dashboard metrics."""
    num_analysts = DataAnalyst.objects.count()
    num_domains = AnalysisDomain.objects.count()
    num_datasets = Dataset.objects.count()
    num_projects = AnalysisProject.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_analysts": num_analysts,
        "num_domains": num_domains,
        "num_datasets": num_datasets,
        "num_projects": num_projects,
        "num_visits": num_visits,
    }

    return render(request, "hub/index.html", context=context)


# ---- ANALYSIS DOMAIN VIEWS ----


class AnalysisDomainListView(LoginRequiredMixin, generic.ListView):
    model = AnalysisDomain
    context_object_name = "domain_list"
    template_name = "hub/domain_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = AnalysisDomainSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = AnalysisDomainSearchForm(self.request.GET)
        if form.is_valid():
            return AnalysisDomain.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return AnalysisDomain.objects.all()


class AnalysisDomainCreateView(LoginRequiredMixin, generic.CreateView):
    model = AnalysisDomain
    fields = "__all__"
    template_name = "hub/domain_form.html"
    success_url = reverse_lazy("hub:domain-list")


class AnalysisDomainUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = AnalysisDomain
    fields = "__all__"
    template_name = "hub/domain_form.html"
    success_url = reverse_lazy("hub:domain-list")


class AnalysisDomainDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = AnalysisDomain
    template_name = "hub/domain_confirm_delete.html"
    success_url = reverse_lazy("hub:domain-list")


# ---- DATASET VIEWS ----


class DatasetListView(LoginRequiredMixin, generic.ListView):
    model = Dataset
    context_object_name = "dataset_list"
    template_name = "hub/dataset_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DatasetSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        form = DatasetSearchForm(self.request.GET)
        if form.is_valid():
            return Dataset.objects.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return Dataset.objects.all()


class DatasetCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dataset
    fields = "__all__"
    template_name = "hub/dataset_form.html"
    success_url = reverse_lazy("hub:dataset-list")


class DatasetUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dataset
    fields = "__all__"
    template_name = "hub/dataset_form.html"
    success_url = reverse_lazy("hub:dataset-list")


class DatasetDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dataset
    template_name = "hub/dataset_confirm_delete.html"
    success_url = reverse_lazy("hub:dataset-list")


# ---- ANALYSIS PROJECT VIEWS ---


class AnalysisProjectListView(LoginRequiredMixin, generic.ListView):
    model = AnalysisProject
    context_object_name = "project_list"
    template_name = "hub/project_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = AnalysisProjectSearchForm(initial={"title": title})
        return context

    def get_queryset(self):
        queryset = AnalysisProject.objects.select_related("domain")
        form = AnalysisProjectSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset


class AnalysisProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = AnalysisProject
    template_name = "hub/project_detail.html"


class AnalysisProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = AnalysisProject
    fields = "__all__"
    template_name = "hub/project_form.html"
    success_url = reverse_lazy("hub:project-list")


class AnalysisProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = AnalysisProject
    fields = "__all__"
    template_name = "hub/project_form.html"
    success_url = reverse_lazy("hub:project-list")


class AnalysisProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = AnalysisProject
    template_name = "hub/project_confirm_delete.html"
    success_url = reverse_lazy("hub:project-list")


@login_required
def toggle_assign_to_project(request, pk):
    """Allows the logged-in analyst to join or leave a specific data project."""
    analyst = DataAnalyst.objects.get(id=request.user.id)
    project = AnalysisProject.objects.get(id=pk)

    if analyst in project.assignees.all():
        project.assignees.remove(analyst)
    else:
        project.assignees.add(analyst)

    return HttpResponseRedirect(reverse_lazy("hub:project-detail", args=[pk]))


# ---- DATA ANALYST VIEWS ----


class DataAnalystListView(LoginRequiredMixin, generic.ListView):
    model = DataAnalyst
    context_object_name = "analyst_list"
    template_name = "hub/analyst_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = DataAnalystSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        form = DataAnalystSearchForm(self.request.GET)
        if form.is_valid():
            return DataAnalyst.objects.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return DataAnalyst.objects.all()


class DataAnalystDetailView(LoginRequiredMixin, generic.DetailView):
    model = DataAnalyst
    template_name = "hub/analyst_detail.html"


class DataAnalystCreateView(LoginRequiredMixin, generic.CreateView):
    model = DataAnalyst
    fields = [
        "username", "email", "password", "first_name", "last_name", "position"
    ]
    template_name = "hub/analyst_form.html"
    success_url = reverse_lazy("hub:analyst-list")


class DataAnalystUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DataAnalyst
    fields = [
        "username", "email", "first_name", "last_name", "position"
    ]
    template_name = "hub/analyst_form.html"
    success_url = reverse_lazy("hub:analyst-list")


class DataAnalystDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DataAnalyst
    template_name = "hub/analyst_confirm_delete.html"
    success_url = reverse_lazy("hub:analyst-list")
