from django.contrib import admin
from .models import Partner, User, Program, Module, Content, ModuleContent, ProgramModule, Registration, SystemPhone, PartnerSystemPhone, IvrPrompt, IvrPromptResponse
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget


class ModuleResource(resources.ModelResource):
    
    class Meta:
        model = Module
        skip_unchanged = True
        report_skipped = True
        use_transaction = True
        import_fields = ('name', 'program')
        import_id_fields = ('name',)    
    
class ContentResource(resources.ModelResource):

    class Meta:
        model = Content
        exclude = ('id','created_on', 'updated_on',)
        import_id_fields = ('name',)

class IvrPromotResource(resources.ModelResource):

    class Meta:
        model = IvrPrompt
        exclude = ('id',)

class ProgramResource(resources.ModelResource):

    class Meta:
        model = Program
        exclude = ('id',)

class ProgramModuleResource(resources.ModelResource):
    id = fields.Field(column_name="module_id")

    class Meta:
        model = ProgramModule
        skip_unchanged = True
        report_skipped = True
        use_transaction = True
        import_fields = ('module_id', 'program')
        import_id_fields = ('id',)
        

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email',)
admin.site.register(Partner, PartnerAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'address_line_1', 'address_line_2', 'postal_code', 'city', 'district', 'state', 'partner_id',)
admin.site.register(User, UserAdmin)

class ProgramAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'description', 'status', 'start_date', 'discontinuation_date', 'program_type',)
    list_filter = ('status', 'start_date', 'discontinuation_date', 'program_type',)
admin.site.register(Program, ProgramAdmin)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'program_id',)
    list_filter = ('program_id',)
    change_list_template = 'imports/import_form_change_list.html'
    resource_class = ModuleResource
admin.site.register(Module, ModuleAdmin)

class ContentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'duration', 'status',)
    list_filter = ('duration', 'status',)
    resource_class = ContentResource
admin.site.register(Content, ContentAdmin)

# admin.site.register(ModuleContent)
class ModuleContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'module_id', 'content_id', 'is_optional',)
    list_filter = ('module_id', 'content_id',)
admin.site.register(ModuleContent, ModuleContentAdmin)

# admin.site.register(ProgramModule)
class ProgramModuleAdmin(ImportExportModelAdmin):
    list_display = ('id', 'program_id', 'module_id', 'sequence',)
    resource_class = ProgramModuleResource
admin.site.register(ProgramModule, ProgramModuleAdmin)

# admin.site.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_phone', 'system_phone', 'district', 'state', 'parent_type', 'area_type', 'is_child_between_0_3', 'is_child_between_3_6', 'is_child_above_6', 'has_no_child', 'has_smartphone', 'has_dropped_missedcall', 'has_received_callback', 'status', 'signup_date', 'partner_id', 'program_id', 'user_id',)
admin.site.register(Registration, RegistrationAdmin)

# admin.site.register(SystemPhone)
class SystemPhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'district', 'state', 'status',)
admin.site.register(SystemPhone, SystemPhoneAdmin)

# admin.site.register(PartnerSystemPhone)
class PartnerSystemPhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'partner_id', 'system_phone_id', 'status',)
admin.site.register(PartnerSystemPhone, PartnerSystemPhoneAdmin)

# admin.site.register(IvrPrompt)
class IvrPromptAdmin(ImportExportModelAdmin):
    list_display = ('id', 'content_id', 'prompt_name', 'prompt_question', 'possible_response', 'status',)
    list_filter = ('content_id', 'prompt_name', 'prompt_question', 'status',)
admin.site.register(IvrPrompt, IvrPromptAdmin)

# admin.site.register(IvrPromptResponse)
class IvrPromptResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_phone', 'content_id', 'prompt_name', 'prompt_question', 'response', 'is_call_log_processed', 'call_sid', 'call_log_id',)
admin.site.register(IvrPromptResponse, IvrPromptResponseAdmin)

