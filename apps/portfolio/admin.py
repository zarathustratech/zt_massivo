from django.contrib import admin, messages
from django.conf import settings
from django.db.models import TextField
from django.forms.widgets import Textarea
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import path, reverse
from django.utils.text import mark_safe
from nested_admin import NestedModelAdmin, NestedTabularInline

from apps.portfolio.models import (CleanedFile, ExtractJob, FileSchemaJob,
                                   JobState, Mapping, MappingRule, PopulateJob,
                                   InferenceJob, Portfolio, SourceColumn, SourceSheet,
                                   TargetField, UploadedFile)
from apps.portfolio.tasks import (enqueue_extract_job, enqueue_file_schema_job,
                                  enqueue_populate_job, enqueue_inference_job)


# -----------------------------------------------------------------------------
# MIXINS
# -----------------------------------------------------------------------------
class DeleteWithNextMixin(object):
    def response_delete(self, request, obj_display, obj_id):
        next_url = request.GET.get('next', None)
        if next_url:
            messages.success(request, '%s deleted.' % obj_display)
            return HttpResponseRedirect(next_url)

        return super(DeleteWithNextMixin, self) \
            .response_delete(request, obj_display, obj_id)


class DeleteBtnMixin(object):
    def delete(self, obj):
        if obj.pk:
            href = self.get_delete_url(obj)
            next_url = self.get_delete_next_url(obj)
            attrs = 'href="%s?next=%s" class="deletelink"' % (href, next_url)
            return mark_safe('<a %s>Delete</a>' % attrs)
        else:
            return '-'


class ModifyBtnMixin(object):
    def modify(self, obj):
        if obj.pk:
            href = obj.get_admin_url()
            attrs = 'href="%s" target="_blank" class="changelink"' % href
            return mark_safe('<a %s>Modify</a >' % attrs)
        else:
            return '-'


class ElapsedJobMixin(object):
    def elapsed(self, obj):
        if obj.started_at and obj.finished_at:
            return obj.finished_at - obj.started_at
        else:
            return '-'


class JobStateMixin(object):
    def job_state(self, obj):
        static_url = settings.STATIC_URL
        crop = 'style="height:15px;width:15px;' \
               'object-fit:cover;object-position: top;"'
        if obj.state == JobState.IDLE:
            icon = '<img src="%sadmin/img/icon-clock.svg" %s">' % \
                (static_url, crop)
            text = 'Waiting'
        if obj.state == JobState.FAILURE:
            icon = '<img src="%sadmin/img/icon-no.svg">' % static_url
            text = 'Failed'
        if obj.state == JobState.RUNNING:
            icon = '<img src="%sadmin/img/icon-alert.svg">' % static_url
            text = 'Running'
        if obj.state == JobState.SUCCESS:
            icon = '<img src="%sadmin/img/icon-yes.svg">' % static_url
            text = 'Success'
        return mark_safe('%s %s' % (icon, text))
    job_state.allow_tags = True


# -----------------------------------------------------------------------------
# PORTFOLIO
# -----------------------------------------------------------------------------
class InferenceJobInline(NestedTabularInline, ModifyBtnMixin,
                        DeleteBtnMixin, ElapsedJobMixin, JobStateMixin):
    model = InferenceJob
    fields = (
        'id',
        'job_state',
        'started_by',
        'n_default_cases',
        'n_paid_cases',
        'elapsed',
        'created_at',
        'modify',
        'delete')
    readonly_fields = fields
    add_form = None
    extra = 0

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_delete_url(self, obj):
        return reverse('admin:portfolio_inferencejob_delete', args=[obj.pk])

    def get_delete_next_url(self, obj):
        return obj.populate_job.extract_job. mapping.file_schema_job.cleaned_file \
            .uploaded_file.portfolio.get_admin_url()


class PopulateJobInline(NestedTabularInline, ModifyBtnMixin,
                        DeleteBtnMixin, ElapsedJobMixin, JobStateMixin):
    model = PopulateJob
    fields = (
        'id',
        'job_state',
        'started_by',
        'n_borrowers',
        'n_loans',
        'n_payments',
        'elapsed',
        'created_at',
        'actions',
        'modify',
        'delete')
    readonly_fields = fields
    add_form = None
    extra = 0
    inlines = (InferenceJobInline,)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_delete_url(self, obj):
        return reverse('admin:portfolio_populatejob_delete', args=[obj.pk])

    def get_delete_next_url(self, obj):
        return obj.extract_job.mapping.file_schema_job.cleaned_file.uploaded_file.portfolio.get_admin_url()

    def actions(self, obj):
        if obj.pk:
            portfolio_id = obj.extract_job.mapping.file_schema_job.cleaned_file.uploaded_file.portfolio.pk
            href = reverse('admin:portfolio_populatejob_inference',
                           args=[portfolio_id, obj.pk])
            attrs = 'href="%s" class="button" style="white-space:nowrap"' % href
            return mark_safe('<a %s>Start inference job</a>' % attrs)
        else:
            return '-'


class ExtractJobInline(NestedTabularInline, ModifyBtnMixin,
                       DeleteBtnMixin, ElapsedJobMixin, JobStateMixin):
    model = ExtractJob
    fields = (
        'id',
        'job_state',
        'started_by',
        'n_extracted_data_points',
        'elapsed',
        'created_at',
        'actions',
        'modify',
        'delete',)
    readonly_fields = fields
    add_form = None
    extra = 0
    inlines = (PopulateJobInline, )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_delete_url(self, obj):
        return reverse('admin:portfolio_extractjob_delete', args=[obj.pk])

    def get_delete_next_url(self, obj):
        return obj.mapping.file_schema_job.cleaned_file.uploaded_file \
            .portfolio.get_admin_url()

    def actions(self, obj):
        if obj.pk and obj.n_extracted_data_points > 0:
            portfolio_id = obj.mapping.file_schema_job.cleaned_file \
                .uploaded_file.portfolio.pk
            href = reverse('admin:portfolio_extractjob_populate',
                           args=[portfolio_id, obj.pk])
            attrs = 'href="%s" class="button" style="white-space:nowrap"' % href
            return mark_safe('<a %s>Start populate job</a>' % attrs)
        else:
            return '-'


class MappingInline(NestedTabularInline, ModifyBtnMixin, DeleteBtnMixin):
    model = Mapping
    fields = (
        'id',
        'n_rules',
        'created_at',
        'updated_at',
        'modify',
        'actions',
        'delete')
    readonly_fields = fields
    add_form = None
    inlines = (ExtractJobInline, )

    def n_rules(self, obj):
        return obj.mappingrule_set.count()

    def has_delete_permission(self, request, obj=None):
        return False

    def get_delete_url(self, obj):
        return reverse('admin:portfolio_mapping_delete', args=[obj.pk])

    def get_delete_next_url(self, obj):
        return obj.file_schema_job.cleaned_file.uploaded_file \
            .portfolio.get_admin_url()

    def actions(self, obj):
        if obj.pk:
            portfolio_id = obj.file_schema_job.cleaned_file \
                .uploaded_file.portfolio.pk
            href = reverse('admin:portfolio_mapping_extract',
                           args=[portfolio_id, obj.pk])
            attrs = 'href="%s" class="button" style="white-space:nowrap"' % href
            return mark_safe('<a %s>Start extract job</a>' % attrs)
        else:
            return '-'


class FileSchemaJobInline(NestedTabularInline, ModifyBtnMixin,
                          DeleteBtnMixin, ElapsedJobMixin, JobStateMixin):
    model = FileSchemaJob
    extra = 0
    fields = (
        'job_state',
        'n_sheets',
        'n_columns',
        'started_by',
        'created_at',
        'elapsed',
        'modify',
        'delete')
    readonly_fields = fields
    add_form = None
    inlines = (MappingInline, )

    def has_add_permission(self, request):
        """
        The add functionality is disabled so they are added by launching
        the file processing job using the button provided in CleanedFileInline.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_delete_url(self, obj):
        return reverse('admin:portfolio_fileschemajob_delete', args=[obj.pk])

    def get_delete_next_url(self, obj):
        return obj.cleaned_file.uploaded_file.portfolio.get_admin_url()


class CleanedFileInline(NestedTabularInline, DeleteBtnMixin):
    model = CleanedFile
    extra = 0
    fields = (
        'file',
        'remarks',
        'uploaded_by',
        'created_at',
        'updated_at',
        'actions',
        'delete')
    readonly_fields = fields[2:]
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 30})}
    }
    inlines = (FileSchemaJobInline, )

    def has_delete_permission(self, request, obj=None):
        return False

    def actions(self, obj):
        if obj.pk:
            href = reverse(
                'admin:portfolio_uploadedfile_scanschema',
                args=[obj.uploaded_file.portfolio.pk, obj.pk])
            attrs = 'href="%s" class="button" style="white-space:nowrap"' \
                % href
            return mark_safe('<a %s>Start File Schema Parsing Job</a>' % attrs)
        else:
            return '-'

    def get_delete_url(self, obj):
        return reverse('admin:portfolio_cleanedfile_delete', args=[obj.pk])

    def get_delete_next_url(self, obj):
        return obj.uploaded_file.portfolio.get_admin_url()


class UploadedFileInline(NestedTabularInline, DeleteBtnMixin):
    model = UploadedFile
    extra = 0
    fields = (
        'file',
        'uploaded_by',
        'created_at',
        'updated_at',
        'delete')
    readonly_fields = fields[1:]
    inlines = (CleanedFileInline, )

    def has_delete_permission(self, request, obj=None):
        return False

    def get_delete_url(self, obj):
        return reverse('admin:portfolio_uploadedfile_delete', args=[obj.pk])

    def get_delete_next_url(self, obj):
        return obj.portfolio.get_admin_url()


@admin.register(Portfolio)
class PortfolioAdmin(NestedModelAdmin):
    # List
    list_display = (
        'id',
        'code',
        'name',
        'created_at',
        'updated_at')
    search_fields = ('code', 'name')
    list_filter = ('created_at', )

    # Detail
    readonly_fields = ('created_at', 'updated_at')
    inlines = (UploadedFileInline, )

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ('code', )
        return super(PortfolioAdmin, self) \
            .add_view(request, form_url, extra_context)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk:
                # This is the same for UploadedFile & CleanedFile
                instance.uploaded_by = request.user
            instance.save()
        formset.save_m2m()

    def start_file_schema_scanning(self, request, *args, **kwargs):
        portfolio = Portfolio.objects.get(id=kwargs['portfolio_id'])
        cleaned_file_id = kwargs['cleaned_file_id']
        cleaned_file = get_object_or_404(
            CleanedFile,
            pk=cleaned_file_id,
            uploaded_file__portfolio=portfolio)

        enqueue_file_schema_job(cleaned_file, request.user)
        messages.success(request, 'A file schema parsing job has started.')
        return HttpResponseRedirect(portfolio.get_admin_url())

    def start_extract_job(self, request, *args, **kwargs):
        portfolio = Portfolio.objects.get(id=kwargs['portfolio_id'])
        mapping = Mapping.objects.get(id=kwargs['mapping_id'])
        enqueue_extract_job(
            mapping=mapping,
            account=request.user)
        messages.success(request, 'An extract job has started.')
        return HttpResponseRedirect(portfolio.get_admin_url())

    def start_populate_job(self, request, *args, **kwargs):
        portfolio = Portfolio.objects.get(id=kwargs['portfolio_id'])
        extract_job = ExtractJob.objects.get(id=kwargs['extract_job_id'])
        enqueue_populate_job(
            extract_job=extract_job,
            account=request.user
        )
        messages.success(request, 'A populate job has started.')
        return HttpResponseRedirect(portfolio.get_admin_url())

    def start_inference_job(self, request, *args, **kwargs):
        portfolio = Portfolio.objects.get(id=kwargs['portfolio_id'])
        populate_job = PopulateJob.objects.get(id=kwargs['populate_job_id'])
        enqueue_inference_job(
            populate_job=populate_job,
            account=request.user
        )
        messages.success(request, 'An inference job has started.')
        return HttpResponseRedirect(portfolio.get_admin_url())

    def get_urls(self):
        urls = super(PortfolioAdmin, self).get_urls()
        curstom_urls = [
            path(
                '<int:portfolio_id>/scan-schema/<int:cleaned_file_id>/',
                self.admin_site.admin_view(self.start_file_schema_scanning),
                name='portfolio_uploadedfile_scanschema',
            ),
            path(
                '<int:portfolio_id>/mapping-extract/<int:mapping_id>/',
                self.admin_site.admin_view(self.start_extract_job),
                name='portfolio_mapping_extract',
            ),
            path(
                '<int:portfolio_id>/populate/<int:extract_job_id>/',
                self.admin_site.admin_view(self.start_populate_job),
                name='portfolio_extractjob_populate',
            ),
            path(
                '<int:portfolio_id>/inference/<int:populate_job_id>/',
                self.admin_site.admin_view(self.start_inference_job),
                name='portfolio_populatejob_inference',
            ),
        ]
        return curstom_urls + urls


# -----------------------------------------------------------------------------
# CLEANED FILE
# -----------------------------------------------------------------------------
@admin.register(CleanedFile)
class CleanedFileAdmin(DeleteWithNextMixin, NestedModelAdmin):
    # List
    list_display = (
        'id',
        'portfolio',
        'file',
        'uploaded_by',
        'remarks',
        'created_at',
        'updated_at')

    def portfolio(self, instance):
        return instance.uploaded_file.portfolio

    # Update
    readonly_fields = ('uploaded_by', 'created_at', 'updated_at')


# -----------------------------------------------------------------------------
# UPLOADED FILE
# -----------------------------------------------------------------------------
@admin.register(UploadedFile)
class UploadedFileAdmin(DeleteWithNextMixin, NestedModelAdmin):
    # List
    list_display = (
        'id',
        'portfolio',
        'file',
        'uploaded_by',
        'created_at',
        'updated_at')

    # Update
    readonly_fields = ('uploaded_by', 'created_at', 'updated_at')


# -----------------------------------------------------------------------------
# FILE SCHEMA JOB
# -----------------------------------------------------------------------------
class SourceColumnInlineAdmin(NestedTabularInline):
    model = SourceColumn
    extra = 0
    readonly_fields = ('id', 'source_sheet_name', 'created_at', 'updated_at')


class SourceSheetInlineAdmin(NestedTabularInline):
    model = SourceSheet
    extra = 0
    inlines = (SourceColumnInlineAdmin, )
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(FileSchemaJob)
class FileSchemaJobAdmin(DeleteWithNextMixin, NestedModelAdmin):
    readonly_fields = (
        'state',
        'cleaned_file',
        'n_sheets',
        'n_columns',
        'logs',
        'started_by',
        'started_at',
        'finished_at',
        'created_at',
        'updated_at')
    inlines = (SourceSheetInlineAdmin, )


# -----------------------------------------------------------------------------
# MAPPING
# -----------------------------------------------------------------------------
class MappingRuleInline(NestedTabularInline):
    model = MappingRule
    readonly_fields = ('mapped_by', 'created_at', 'updated_at')
    formfield_overrides = {
        TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 30})}
    }

    def get_extra(self, request, obj=None, **kwargs):
        if obj and obj.pk and obj.mappingrule_set.count() > 0:
            return 0
        else:
            return TargetField.objects.count()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'source_column':
            mapping_id = request.resolver_match[2]['object_id']
            mapping = Mapping.objects.get(id=mapping_id)
            kwargs['queryset'] = SourceColumn.objects \
                .filter(source_sheet__file_schema_job=mapping.file_schema_job)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Mapping)
class MappingAdmin(DeleteWithNextMixin, NestedModelAdmin):
    inlines = (MappingRuleInline, )
    readonly_fields = ('file_schema_job', )

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.mapped_by = request.user
            instance.save()
        formset.save_m2m()


# -----------------------------------------------------------------------------
# EXTRACT JOB
# -----------------------------------------------------------------------------
def delete_selected(modeladmin, request, queryset):
    queryset.delete()


@admin.register(ExtractJob)
class ExtractJobAdmin(DeleteWithNextMixin, NestedModelAdmin):
    actions = (delete_selected,)


# -----------------------------------------------------------------------------
# POPULATE JOB
# -----------------------------------------------------------------------------
@admin.register(PopulateJob)
class PopulateJobAdmin(DeleteWithNextMixin, NestedModelAdmin):
    actions = (delete_selected,)


# -----------------------------------------------------------------------------
# INFERENCE JOB
# -----------------------------------------------------------------------------
@admin.register(InferenceJob)
class InferenceJobAdmin(DeleteWithNextMixin, NestedModelAdmin):
    actions = (delete_selected,)