from django.contrib import admin
from django.urls import path, include
from logs.views import MainPageView, LogFileListView, LogFileAddView, LogFileEditView, LogFileDeleteView, LogTypeListView, LogTypeAddView, LogTypeEditView, LogTypeDeleteView, SearchPatternListView, SearchPatternAddView, SearchPatternEditView, SearchPatternDeleteView, AnomalousEventListView, AnomalousEventDeleteView, OneTimeScanListView, OneTimeScanAddView, OneTimeScanDeleteView, OneTimeScanAnomalousEventListView
from django.contrib.auth.decorators import login_required

app_name = "logs"

urlpatterns = [
    path("anomalous-events/", login_required(AnomalousEventListView.as_view()), name="anomalous_events_list"),
    path("anomalous-events/<int:anomalous_event_id>/delete", login_required(AnomalousEventDeleteView.as_view()), name="anomalous_event_delete"),

    path("log-files/", login_required(LogFileListView.as_view()), name="log_files_list"),
    path("log-files/add", login_required(LogFileAddView.as_view()), name="log_file_add"),
    path("log-files/<int:log_file_id>/edit", login_required(LogFileEditView.as_view()), name="log_file_edit"),
    path("log-files/<int:log_file_id>/delete", login_required(LogFileDeleteView.as_view()), name="log_file_delete"),

    path("log-types/", login_required(LogTypeListView.as_view()), name="log_types_list"),
    path("log-types/add", login_required(LogTypeAddView.as_view()), name="log_type_add"),
    path("log-types/<int:log_type_id>/edit", login_required(LogTypeEditView.as_view()), name="log_type_edit"),
    path("log-types/<int:log_type_id>/delete", login_required(LogTypeDeleteView.as_view()), name="log_type_delete"),

    path("search-patterns/", login_required(SearchPatternListView.as_view()), name="search_patterns_list"),
    path("search-patterns/add", login_required(SearchPatternAddView.as_view()), name="search_pattern_add"),
    path("search-patterns/<int:search_pattern_id>/edit", login_required(SearchPatternEditView.as_view()), name="search_pattern_edit"),
    path("search-patterns/<int:search_pattern_id>/delete", login_required(SearchPatternDeleteView.as_view()), name="search_pattern_delete"),

    path("one-time-scans/", login_required(OneTimeScanListView.as_view()), name="one_time_scans_list"),
    path("one-time-scans/add", login_required(OneTimeScanAddView.as_view()), name="one_time_scan_add"),
    path("one-time-scans/<int:log_file_id>/delete", login_required(OneTimeScanDeleteView.as_view()), name="one_time_scan_delete"),
    path("one-time-scans/<int:log_file_id>/anomalous-events", login_required(OneTimeScanAnomalousEventListView.as_view()), name="one_time_scan_anomalous_events_list"),

    path("", login_required(MainPageView.as_view()), name="main_page")
]
