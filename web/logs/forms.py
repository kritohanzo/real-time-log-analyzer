import datetime

from django import forms

from logs.models import (
    LogFile,
    LogType,
    NotificationType,
    SearchPattern,
    SearchPatternTypeChoices,
)


class LogFileForm(forms.ModelForm):
    name = forms.CharField(
        label="Краткое название или описание лог-файла",
        max_length=64,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите краткое название или описание лог-файла",
                "class": "form-control",
            }
        ),
    )
    path = forms.CharField(
        label="Путь до файла",
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите путь до файла", "class": "form-control"}
        ),
    )
    type = forms.ModelChoiceField(
        queryset=LogType.objects.all(),
        label="Тип протокола / ПО",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="—",
    )

    class Meta:
        model = LogFile
        fields = ("name", "path", "type")


class LogTypeForm(forms.ModelForm):
    name = forms.CharField(
        label="Краткое название или описание протокола / ПО",
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите краткое название или описание протокола / ПО",
                "class": "form-control",
            }
        ),
    )
    search_patterns = forms.ModelMultipleChoiceField(
        queryset=SearchPattern.objects.all(),
        label="Поиксовые паттерны",
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-check form-check-inline"}
        ),
    )

    class Meta:
        model = LogType
        fields = ("name", "search_patterns")


class SearchPatternForm(forms.ModelForm):
    name = forms.CharField(
        label="Краткое название или описание поискового паттерна",
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите краткое название или описание поискового паттерна",
                "class": "form-control",
            }
        ),
    )
    pattern = forms.CharField(
        label="Поисковый паттерн",
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите поисковый паттерн", "class": "form-control"}
        ),
    )
    search_type = forms.ChoiceField(
        choices=SearchPatternTypeChoices.choices(),
        label="Тип поиска",
        required=True,
        widget=forms.Select(
            attrs={"placeholder": "Выберите тип поиска", "class": "form-select"}
        ),
    )
    counter = forms.BooleanField(
        label="Повторяющееся событие с одного IP-адреса",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "placeholder": "Повторяющееся событие с одного IP-адреса",
                "class": "form-check form-switch form-check-input",
            }
        ),
    )
    coefficient = forms.FloatField(
        label="Коэффициент вхождения",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите коэффициент вхождения",
                "class": "form-control",
            }
        ),
    )
    count_of_events = forms.IntegerField(
        label="Количество событий до оповещения",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите количество событий до оповещения",
                "class": "form-control",
            }
        ),
    )
    period_of_events = forms.TimeField(
        label="Период для подсчёта количества событий до оповещения",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Введите период для подсчёта количества событий до оповещения",
                "class": "form-control",
                "type": "time",
                "step": "1",
            }
        ),
    )
    notification_types = forms.ModelMultipleChoiceField(
        queryset=NotificationType.objects.all(),
        label="Типы оповещений",
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "form-check form-check-inline"}
        ),
        initial=NotificationType.objects.filter(method="websocket"),
    )

    class Meta:
        model = SearchPattern
        fields = (
            "name",
            "pattern",
            "search_type",
            "counter",
            "coefficient",
            "count_of_events",
            "period_of_events",
            "notification_types",
        )


class AnomalousEventBaseSearchForm(forms.Form):
    text = forms.CharField(
        label="Текст события",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите текст события", "class": "form-control"}
        ),
    )
    log_file = forms.ModelChoiceField(
        queryset=LogFile.objects.filter(one_time_scan=False),
        required=False,
        label="Лог-файл",
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Любой",
    )
    log_type = forms.ModelChoiceField(
        queryset=LogType.objects.all(),
        required=False,
        label="Тип протокола / ПО",
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Любой",
    )
    search_pattern = forms.ModelChoiceField(
        queryset=SearchPattern.objects.all(),
        required=False,
        label="Поисковый паттерн",
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Любой",
    )


class AnomalousEventMainPageSearchForm(AnomalousEventBaseSearchForm):
    start_datetime = forms.DateTimeField(
        label="Начало периода",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Выберите начала периода",
                "class": "form-control",
                "type": "datetime-local",
                "value": datetime.datetime.now().strftime("%Y-%m-%d 00:00"),
            }
        ),
    )
    end_datetime = forms.DateTimeField(
        label="Конец периода",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Выберите начала периода",
                "class": "form-control",
                "type": "datetime-local",
                "value": (
                    datetime.datetime.now() + datetime.timedelta(days=1)
                ).strftime("%Y-%m-%d 00:00"),
            }
        ),
    )


class AnomalousEventSearchForm(AnomalousEventBaseSearchForm):
    start_datetime = forms.DateTimeField(
        label="Начало периода",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Выберите начала периода",
                "class": "form-control",
                "type": "datetime-local",
                "step": "1",
            }
        ),
    )
    end_datetime = forms.DateTimeField(
        label="Конец периода",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Выберите конец периода",
                "class": "form-control",
                "type": "datetime-local",
                "step": "1",
            }
        ),
    )


class LogFileSearchForm(forms.Form):
    name = forms.CharField(
        label="Описание",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите описание", "class": "form-control"}
        ),
    )
    path = forms.CharField(
        label="Путь",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите путь", "class": "form-control"}
        ),
    )
    log_type = forms.ModelChoiceField(
        queryset=LogType.objects.all(),
        required=False,
        label="Тип протокола / ПО",
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Любой",
    )
    search_pattern = forms.ModelChoiceField(
        queryset=SearchPattern.objects.all(),
        required=False,
        label="Поисковый паттерн",
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Любой",
    )


class LogTypeSearchForm(forms.Form):
    name = forms.CharField(
        label="Описание",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите описание", "class": "form-control"}
        ),
    )
    search_pattern = forms.ModelChoiceField(
        queryset=SearchPattern.objects.all(),
        required=False,
        label="Поисковый паттерн",
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Любой",
    )


class SearchPatternSearchForm(forms.Form):
    name = forms.CharField(
        label="Описание",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите описание", "class": "form-control"}
        ),
    )
    pattern = forms.CharField(
        label="Паттерн",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите паттерн", "class": "form-control"}
        ),
    )
    search_type = forms.ChoiceField(
        choices=SearchPatternTypeChoices.choices_with_none(),
        label="Тип поиска",
        required=False,
        widget=forms.Select(
            attrs={"placeholder": "Выберите тип поиска", "class": "form-select"}
        ),
    )
    notification_type = forms.ModelChoiceField(
        queryset=NotificationType.objects.all(),
        label="Тип оповещений",
        required=False,
        widget=forms.Select(
            attrs={"placeholder": "Выберите тип оповещений", "class": "form-select"}
        ),
        empty_label="Любой",
    )


class OneTimeScanAnomalousEventSearchForm(forms.Form):
    text = forms.CharField(
        label="Текст события",
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Введите текст события", "class": "form-control"}
        ),
    )
    search_pattern = forms.ModelChoiceField(
        queryset=SearchPattern.objects.none(),
        required=False,
        label="Поисковый паттерн",
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="Любой",
    )

    def __init__(self, *args, **kwargs):
        log_file_id = kwargs.pop("log_file_id")
        self.declared_fields.get("search_pattern").queryset = LogFile.objects.get(
            id=log_file_id
        ).type.search_patterns.all()
        super().__init__(*args, **kwargs)
