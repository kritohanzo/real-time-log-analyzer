from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django import views
import datetime
from logs.forms import LogFileForm, LogTypeForm, SearchPatternForm, DateRangeForm
from logs.models import LogFile, LogType, SearchPattern, AnomalousEvent
from qsstats import QuerySetStats
from django.db.models import Count, F, QuerySet


class MainPageView(views.View):
    def get(self, request, *args, **kwargs):
        form = DateRangeForm()
        start_date = datetime.datetime.now().date()
        end_date = start_date + datetime.timedelta(days=1)
        anomalous_events = AnomalousEvent.objects.filter(datetime__gt=start_date, datetime__lt=end_date)
        qsstats = QuerySetStats(anomalous_events, date_field='datetime')
        logs_metrics = qsstats.time_series(start_date, end_date, interval='minutes')
        logs_metrics = list(filter(lambda x: x[1] > 0 or x[0].minute % 30 == 0, logs_metrics))
        return render(request, template_name="logs/index.html", context={"form": form, "logs_metrics": logs_metrics, "start_date": start_date, "end_date": end_date})
    
    def post(self, request, *args, **kwargs):
        form = DateRangeForm(request.POST)
        if not form.is_valid():
            return self.get(self, request, *args, **kwargs)
        start_date = form.cleaned_data.get("start_date")
        end_date = form.cleaned_data.get("end_date")
        anomalous_events = AnomalousEvent.objects.filter(datetime__gt=start_date, datetime__lt=end_date)
        log_file = form.cleaned_data.get("log_file")
        if log_file:
            anomalous_events = anomalous_events.filter(log_file=log_file)
        log_type = form.cleaned_data.get("log_type")
        if log_type:
            anomalous_events = anomalous_events.filter(log_file__type=log_type)
        search_pattern = form.cleaned_data.get("search_pattern")
        if search_pattern:
            log_types = search_pattern.log_types.all() 
            if log_types:
                anomalous_events = anomalous_events.filter(log_file__type__in=log_types)
        
        qsstats = QuerySetStats(anomalous_events, date_field='datetime')
        logs_metrics = qsstats.time_series(start_date, end_date, interval='minutes')
        logs_metrics = list(filter(lambda x: x[1] > 0 or x[0].minute % 30 == 0, logs_metrics))
        return render(request, template_name="logs/index.html", context={"form": form, "logs_metrics": logs_metrics, "start_date": start_date, "end_date": end_date})


# Log File Views


class LogFileListView(views.View):
    def get(self, request, *args, **kwargs):
        log_files = LogFile.objects.all()
        from random import randint
        AnomalousEvent.objects.create(text="Кто-то чекает файлики", log_file=log_files[randint(0, len(log_files)-1)])
        return render(request, template_name="logs/log-files/log-files-list.html", context={"log_files": log_files})


class LogFileAddView(views.View):
    def get(self, request, *args, **kwargs):
        form = LogFileForm()
        return render(request, template_name="logs/log-files/log-file-form.html", context={"form": form})
    
    def post(self, request, *args, **kwargs):
        form = LogFileForm(request.POST)
        if not form.is_valid():
            return render(request, template_name="logs/log-files/log-file-form.html", context={"form": form})
        LogFile.objects.create(**form.cleaned_data)
        return render(request, template_name="success.html", context={"message": "Вы успеншо добавили лог-файл"})


class LogFileDetailView(views.View):
    def get(self, request, log_file_id, *args, **kwargs):
        log_file = get_object_or_404(LogFile, id=log_file_id)
        return render(request, template_name="logs/log-files/log-files-list.html", context={"log_file": log_file})


class LogFileEditView(views.View):
    def get(self, request, log_file_id, *args, **kwargs):
        log_file = get_object_or_404(LogFile, id=log_file_id)
        form = LogFileForm(instance=log_file)
        return render(request, template_name="logs/log-files/log-file-form.html", context={"form": form, "log_file_id": log_file_id, "is_edit": True})
    
    def post(self, request, log_file_id, *args, **kwargs):
        log_file = get_object_or_404(LogFile, id=log_file_id)
        form = LogFileForm(request.POST, instance=log_file)
        if not form.is_valid():
            return render(request, template_name="logs/log-files/log-file-form.html", context={"form": form, "is_edit": True})
        form.save()
        return render(request, template_name="success.html", context={"message": "Вы успеншо изменили лог-файл"})


class LogFileDeleteView(views.View):
    def get(self, request, log_file_id, *args, **kwargs):
        log_file = get_object_or_404(LogFile, id=log_file_id)
        log_file.delete()
        return render(request, template_name="success.html", context={"message": "Вы успеншо удалили лог-файл"})


# Log Type Views


class LogTypeListView(views.View):
    def get(self, request, *args, **kwargs):
        log_types = LogType.objects.all()
        return render(request, template_name="logs/log-types/log-types-list.html", context={"log_types": log_types})
    

class LogTypeAddView(views.View):
    def get(self, request, *args, **kwargs):
        form = LogTypeForm()
        return render(request, template_name="logs/log-types/log-type-form.html", context={"form": form})
    
    def post(self, request, *args, **kwargs):
        form = LogTypeForm(request.POST)
        if not form.is_valid():
            return render(request, template_name="logs/log-types/log-type-form.html", context={"form": form})
        search_patterns = form.cleaned_data.pop("search_patterns")
        log_type = LogType.objects.create(**form.cleaned_data)
        log_type.search_patterns.set(search_patterns)
        return render(request, template_name="success.html", context={"message": "Вы успешно добавили протокол / ПО"})


class LogTypeDetailView(views.View):
    def get(self, request, log_type_id, *args, **kwargs):
        log_type = get_object_or_404(LogType, id=log_type_id)
        return render(request, template_name="logs/log-types/log-type-detail.html", context={"log_type": log_type})


class LogTypeEditView(views.View):
    def get(self, request, log_type_id, *args, **kwargs):
        log_type = get_object_or_404(LogType, id=log_type_id)
        form = LogTypeForm(instance=log_type)
        return render(request, template_name="logs/log-types/log-type-form.html", context={"form": form, "log_type_id": log_type_id, "is_edit": True})
    
    def post(self, request, log_type_id, *args, **kwargs):
        log_type = get_object_or_404(LogType, id=log_type_id)
        form = LogTypeForm(request.POST, instance=log_type)
        if not form.is_valid():
            return render(request, template_name="logs/log-types/log-type-form.html", context={"form": form, "is_edit": True})
        form.save()
        search_patterns = form.cleaned_data.pop("search_patterns")
        log_type.search_patterns.set(search_patterns)
        return render(request, template_name="success.html", context={"message": "Вы успешно изменили протокол / ПО"})


class LogTypeDeleteView(views.View):
    def get(self, request, log_type_id, *args, **kwargs):
        log_type = get_object_or_404(LogType, id=log_type_id)
        log_type.delete()
        return render(request, template_name="success.html", context={"message": "Вы успеншо удалили протокол / ПО"})
    

# Search Patterns Views


class SearchPatternListView(views.View):
    def get(self, request, *args, **kwargs):
        search_patterns = SearchPattern.objects.all()
        return render(request, template_name="logs/search-patterns/search-patterns-list.html", context={"search_patterns": search_patterns})
    

class SearchPatternAddView(views.View):
    def get(self, request, *args, **kwargs):
        form = SearchPatternForm()
        return render(request, template_name="logs/search-patterns/search-pattern-form.html", context={"form": form})
    
    def post(self, request, *args, **kwargs):
        form = SearchPatternForm(request.POST)
        if not form.is_valid():
            return render(request, template_name="logs/search-patterns/search-pattern-form.html", context={"form": form})
        SearchPattern.objects.create(**form.cleaned_data)
        return render(request, template_name="success.html", context={"message": "Вы успешно добавили поисковый паттерн"})


class SearchPatternDetailView(views.View):
    def get(self, request, search_pattern_id, *args, **kwargs):
        search_pattern = get_object_or_404(SearchPattern, id=search_pattern_id)
        return render(request, template_name="logs/search-patterns/search-pattern-detail.html", context={"search_pattern": search_pattern})


class SearchPatternEditView(views.View):
    def get(self, request, search_pattern_id, *args, **kwargs):
        search_pattern = get_object_or_404(SearchPattern, id=search_pattern_id)
        form = SearchPatternForm(instance=search_pattern)
        return render(request, template_name="logs/search-patterns/search-pattern-form.html", context={"form": form, "search_pattern_id": search_pattern_id, "is_edit": True})
    
    def post(self, request, search_pattern_id, *args, **kwargs):
        search_pattern = get_object_or_404(SearchPattern, id=search_pattern_id)
        form = SearchPatternForm(request.POST, instance=search_pattern)
        if not form.is_valid():
            return render(request, template_name="logs/search-patterns/search-pattern-form.html", context={"form": form, "is_edit": True})
        form.save()
        return render(request, template_name="success.html", context={"message": "Вы успешно изменили поисковый паттерн"})


class SearchPatternDeleteView(views.View):
    def get(self, request, search_pattern_id, *args, **kwargs):
        search_pattern = get_object_or_404(SearchPattern, id=search_pattern_id)
        search_pattern.delete()
        return render(request, template_name="success.html", context={"message": "Вы успеншо удалили поисковый паттерн"})