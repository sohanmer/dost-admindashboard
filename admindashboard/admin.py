from django.contrib import admin
from .models import Partner, User, Program, Module, Content, ModuleContent, ProgramModule, Registration, SystemPhone, PartnerSystemPhone, IvrPrompt, IvrPromptResponse, CallLog, CallbackTracker, UserModuleContent, UserProgram, CallLogEvent, IvrPromptMapping, KookooCallLog, UserCustomField, UserGroup
from django import forms

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email',)
admin.site.register(Partner, PartnerAdmin)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'address_line_1', 'address_line_2', 'postal_code', 'city', 'district', 'state', 'partner_id',)
admin.site.register(User, UserAdmin)

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'status', 'start_date', 'discontinuation_date', 'program_type',)
    list_filter = ('status', 'start_date', 'discontinuation_date', 'program_type',)
    change_list_template = 'imports/import_form_program_change_list.html'

admin.site.register(Program, ProgramAdmin)

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'program_id',)
    list_filter = ('program_id',)
    change_list_template = 'imports/import_form_module_change_list.html'    

admin.site.register(Module, ModuleAdmin)

class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration', 'status',)
    list_filter = ('duration', 'status',)
    change_list_template = 'imports/import_form_content_change_list.html'

admin.site.register(Content, ContentAdmin)

# admin.site.register(ModuleContent)
class ModuleContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'module_id', 'content_id', 'is_optional',)
    list_filter = ('module_id', 'content_id',)
admin.site.register(ModuleContent, ModuleContentAdmin)

# admin.site.register(ProgramModule)
class ProgramModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'program_id', 'module_id', 'sequence',)
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
class IvrPromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_id', 'prompt_name', 'prompt_question', 'possible_response', 'status',)
    list_filter = ('content_id', 'prompt_name', 'prompt_question', 'status',)
    change_list_template = 'imports/import_form_prompt_change_list.html'
admin.site.register(IvrPrompt, IvrPromptAdmin)

# admin.site.register(IvrPromptResponse)
class IvrPromptResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_phone', 'content_id', 'prompt_name', 'prompt_question', 'response', 'is_call_log_processed', 'call_sid', 'call_log_id',)
admin.site.register(IvrPromptResponse, IvrPromptResponseAdmin)

class CallLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'call_sid', 'flow_run_uuid', 'call_type', 'user_phone_number', 'system_phone_number', )
admin.site.register(CallLog, CallLogAdmin)

class CallbackTrackerAdmin(admin.ModelAdmin):
    list_display = ('id', 'missed_call_log', 'response_call_log',)
admin.site.register(CallbackTracker, CallbackTrackerAdmin)

class UserModuleContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_program_id', 'program_module_id',)
admin.site.register(UserModuleContent, UserModuleContentAdmin)

class CallLogEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'telco_code', 'call_sid', 'account_sid', 'from_number', 'to_number', 'call_status', 'dial_time', 'pick_time', 'end_time', 'duration', )
admin.site.register(CallLogEvent, CallLogEventAdmin)

class IvrPromptMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'mapped_table_name', 'mapped_table_column_name', 'default_value', )
admin.site.register(IvrPromptMapping, IvrPromptMappingAdmin)

class KookooCallLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_call_sid', 'log_session_id', 'log_called_id', 'log_date', 'log_time', 'log_message', 'event_created_on', )
admin.site.register(KookooCallLog, KookooCallLogAdmin)

class UserCustomFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'registration_id', 'user_phone', 'flow_run_uuid', 'field_name', 'field_value', )
admin.site.register(UserCustomField, UserCustomFieldAdmin)

class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('id',  'user_phone', 'user_id', 'registration_id', 'group_name', 'group_uuid', 'status', )
admin.site.register(UserGroup, UserGroupAdmin)