from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import ShiftAssignment, ProcessHistory
from .forms import ProcessHistoryForm


class HomePageView(TemplateView):
    template_name = 'process_history/home.html'


class ShiftAssignmentView(LoginRequiredMixin, TemplateView):
    template_name = 'process_history/shift_assignments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments'] = ShiftAssignment.objects.filter(operator=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        return redirect('process_history:history_process_create')  # Перенаправление на страницу создания истории процесса


class HistoryProcessCreateView(LoginRequiredMixin, FormView):
    template_name = 'process_history/history_process_create.html'
    form_class = ProcessHistoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment_id = self.kwargs.get('assignment_id')
        context['assignment'] = ShiftAssignment.objects.get(id=assignment_id)
        return context

    def form_valid(self, form):
        process_history = form.save(commit=False)
        process_history.user = self.request.user
        process_history.assignment = self.get_context_data()['assignment']
        process_history.save()

        # Логика для создания модальных окон для ввода параметров
        # Это может быть реализовано через JavaScript на клиентской стороне

        return super().form_valid(form)


class CompleteProcessHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'process_history/complete_process_history.html'

    def post(self, request, *args, **kwargs):
        # Логика завершения истории процесса
        return redirect('process_history:shift_assignments_update')


class ShiftAssignmentsUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'process_history/shift_assignments_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assignment_id = self.kwargs.get('assignment_id')
        context['assignment'] = ShiftAssignment.objects.get(id=assignment_id)
        return context

    def post(self, request, *args, **kwargs):
        # Логика обновления сменного задания и ввода количества брака
        assignment_id = self.kwargs.get('assignment_id')
        assignment = ShiftAssignment.objects.get(id=assignment_id)

        # Обновление полей задания на основе введенных данных
        assignment.broken_count = request.POST.get('broken_count')
        assignment.save()

        return redirect('process_history:shift_assignments')  # Перенаправление на страницу со сменными заданиями
