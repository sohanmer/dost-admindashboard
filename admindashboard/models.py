from django.db import models
from django.utils.translation import gettext_lazy as _

class Partner(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'partner'
    
    def __str__(self):
        return f'{self.name} - {self.email}'

class User(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address_line_1 = models.TextField(blank=True, null=True)
    address_line_2 = models.TextField(blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    partner_id = models.IntegerField
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)    
    partner = models.ForeignKey(Partner, on_delete=models.DO_NOTHING)
    class Meta:
        db_table = 'user'
    
    def __str__(self):
        return f'{self.name}, {self.phone}'

class Program(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # status = models.CharField(max_length=50)
    class ProgramStatus(models.TextChoices):
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')

    status = models.CharField(
        max_length=50,
        choices=ProgramStatus.choices,
        default=ProgramStatus.ACTIVE,
    )
    version = models.IntegerField
    start_date = models.DateField(blank=True, null=True)
    discontinuation_date = models.DateField(blank=True, null=True)
    program_type = models.CharField(max_length=50, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'program'
    
    def __str__(self):
        return self.name

class Module(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    name = models.CharField(max_length=255)
    # program_id = models.ManyToManyField(Program, through='ProgramModule')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'module'
    
    def __str__(self):
        return self.name

class Content(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    name = models.CharField(max_length=500)
    duration = models.CharField(max_length=50)
    class ContentStatus(models.TextChoices):
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')
    status = models.CharField(
        max_length=50,
        choices=ContentStatus.choices,
        default=ContentStatus.ACTIVE,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 'content'

    def __str__(self):
        return self.name

class ModuleContent(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    module_id = models.IntegerField
    content_id = models.IntegerField
    sequence = models.IntegerField
    is_optional = models.BooleanField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        db_table = 'module_content'

    def __str__(self):
        return f'{self.module.name} - {self.content.name}'

class UserProgram(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    program_id = models.IntegerField
    user_id = models.IntegerField
    preferred_time_slot = models.CharField(max_length=50, blank=True, null=True)
    class UserProgramStatus(models.TextChoices):
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')

    status = models.CharField(
        max_length=50,
        choices=UserProgramStatus.choices,
        default=UserProgramStatus.ACTIVE,
    ) 
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_program'

class ProgramModule(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    program_id = models.IntegerField
    module_id = models.IntegerField
    sequence = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        db_table = 'program_module'
    
    def __str__(self):
        return f'{self.program.name} - {self.module.name}'

class UserModuleContent(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    user_program_id = models.IntegerField
    program_module_id = models.IntegerField
    module_content_id = models.IntegerField
    class UserModuleContentStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        INPROGRESS = 'In-Progress', _('In-Progress')
        COMPLETE = 'Complete', _('Complete')

    status = models.CharField(
        max_length=50,
        choices=UserModuleContentStatus.choices,
        default=UserModuleContentStatus.PENDING,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    user_program = models.ForeignKey(UserProgram, on_delete=models.CASCADE)
    program_module = models.ForeignKey(ProgramModule, on_delete=models.CASCADE)
    module_content = models.ForeignKey(ModuleContent, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_module_content'

class Registration(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    user_phone = models.CharField(max_length=50)
    system_phone = models.CharField(max_length=50)

    # user_id = models.IntegerField(blank=True, null=True)
    # partner_id = models.IntegerField(blank=True, null=True)
    # program_id = models.IntegerField(blank=True, null=True)


    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)

    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    class ParentType(models.TextChoices):
        FATHER = 'Father', _('Father')
        MOTHER = 'Mother', _('Mother')
        GRANDFATHER = 'Grand Father', _('Grand Father')
        GRANDMOTHER = 'Grand Mother', _('Grand Mother')
        OTHER = 'Other', _('Other')
    parent_type = models.CharField(
        max_length=50,
        choices=ParentType.choices,
    )
    area_type = models.CharField(max_length=255, blank=True, null=True)
    is_child_between_0_3 = models.BooleanField(blank=True, null=True)
    is_child_between_3_6 = models.BooleanField(blank=True, null=True)
    is_child_above_6 = models.BooleanField(blank=True, null=True)
    has_no_child = models.BooleanField(blank=True, null=True)
    has_smartphone = models.BooleanField(blank=True, null=True)
    has_dropped_missedcall = models.BooleanField(blank=True, null=True)
    has_received_callback = models.BooleanField(blank=True, null=True)
    class RegistrationStatus(models.TextChoices):
        PENDING = 'Pending', _('Pending')
        INPROGRESS = 'In-Progress', _('In-Progress')
        COMPLETE = 'Complete', _('Complete')

    status = models.CharField(
        max_length=50,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.PENDING,
    )
    signup_date = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'registration'
    
    def __str__(self):
        return self.user_phone

class CallLog(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, blank=True, null=True)
    user_module_content = models.ForeignKey(UserModuleContent, on_delete=models.CASCADE, blank=True, null=True)

    # user_id = models.IntegerField(blank=True, null=True)
    # registration_id = models.IntegerField(blank=True, null=True)
    # user_module_content_id = models.IntegerField(blank=True, null=True)
    
    call_sid = models.IntegerField(blank=True, null=True)
    flow_run_uuid = models.CharField(max_length=255, blank=True, null=True)
    class CallType(models.TextChoices):
        INBOUND = 'Inbound Call', _('Inbound Call')
        OUTBOUNDCALL = 'Outbound Call', _('Outbound Call')
        INBOUNDMISSEDCALL = 'Inbound Missedcall', _('Inbound Missedcall')
        OUTBOUNDLIVECALL = 'Outbound Live Call', _('Outbound Live Call')
    call_type = models.CharField(
        max_length=50,
        choices=CallType.choices,
    )
    scheduled_by = models.CharField(max_length=100, blank=True, null=True)
    user_phone_number = models.CharField(max_length=50)
    system_phone_number = models.CharField(max_length=50)
    circle = models.CharField(max_length=50, blank=True, null=True)
    class CallStatus(models.TextChoices):
        NORESPONSE = 'No Response', _('No Response')
        UNREACHABLE = 'Unreachable', _('Unreachable')
        DND = 'DND', _('DND')
        INVALIDNUMBER = 'Invalid Number', _('Invalid Number')
        REJECTED = 'Rejected', _('Rejected')
        BUSY = 'Busy', _('Busy')
        ANSWERED = 'Answered', _('Answered')

    status = models.CharField(
        max_length=50,
        choices=CallStatus.choices,
    )
    listen_seconds = models.CharField(max_length=50, blank=True, null=True)
    recording_url = models.CharField(max_length=1000, blank=True, null=True)
    dial_time = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'call_log'

class CallbackTracker(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    # missed_call_log_id = models.IntegerField
    # response_call_log_id = models.IntegerField

    missed_call_log = models.ForeignKey(
        CallLog, on_delete=models.CASCADE, 
        related_name="%(app_label)s_%(class)s_related", 
        related_query_name="%(app_label)s_%(class)ss",) 
    response_call_log = models.ForeignKey(CallLog, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'callback_tracker'

class SystemPhone(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    phone = models.CharField(max_length=50)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    class PhoneStatus(models.TextChoices):
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')

    status = models.CharField(
        max_length=50,
        choices=PhoneStatus.choices,
        default=PhoneStatus.ACTIVE,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'system_phone'
    
    def __str__(self):
        return self.phone

class PartnerSystemPhone(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    partner_id = models.IntegerField
    system_phone_id = models.IntegerField
    class PartnerSystemPhoneStatus(models.TextChoices):
        ACTIVE = 'Active', _('Active')
        INACTIVE = 'Inactive', _('Inactive')

    status = models.CharField(
        max_length=50,
        choices=PartnerSystemPhoneStatus.choices,
        default=PartnerSystemPhoneStatus.ACTIVE,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    system_phone = models.ForeignKey(SystemPhone, on_delete=models.CASCADE)

    class Meta:
        db_table = 'partner_system_phone'
    
    def __str__(self):
        return f'{self.partner.name} - {self.system_phone.phone}'

class IvrPrompt(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    # content_id = models.IntegerField(blank=True, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, blank=True, null=True)
    
    prompt_name = models.CharField(max_length=255, blank=True, null=True)
    prompt_question = models.CharField(max_length=1000, blank=True, null=True)
    possible_response = models.CharField(max_length=255, blank=True, null=True)
    class IvrPromptStatus(models.TextChoices):
        ACTIVE = 'Active', _('active')
        INACTIVE = 'Inactive', _('inactive')

    status = models.CharField(
        max_length=50,
        choices=IvrPromptStatus.choices,
        default=IvrPromptStatus.ACTIVE,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'ivr_prompt'

    def __str__(self):
        return self.prompt_name

class IvrPromptResponse(models.Model):
    id = models.AutoField(
        auto_created = True,
        primary_key = True,
        serialize = False,
        verbose_name ='ID'
        )
    content = models.ForeignKey(Content, on_delete=models.CASCADE, blank=True, null=True)
    call_log = models.ForeignKey(CallLog, on_delete=models.CASCADE, blank=True, null=True)

    prompt_name = models.CharField(max_length=255, blank=True, null=True)
    prompt_question = models.CharField(max_length=1000, blank=True, null=True)
    response = models.CharField(max_length=255, blank=True, null=True)
    user_phone = models.CharField(max_length=50)
    is_call_log_processed = models.BooleanField(blank=True, null=True)
    call_sid = models.IntegerField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'ivr_prompt_response'

    def __str__(self):
        return self.prompt_name
    