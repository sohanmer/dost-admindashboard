from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django import forms
from django.template import RequestContext
import django_excel as excel
from django import forms
from .models import Module, ProgramModule, Program, Content, IvrPromptResponse

def upload(request):
    if request.method == "POST":
        # request.FILES["import_form"].save_book_to_database(
        #     models=[Module],
        #     mapdicts=[
        #         {"name" : "name", "program" : "program_id"},
        #     ],
        # )
        # record_length = len(request.FILES["import_form"].get_array(
        #     sheet_name = 'module'
        # ))
        # modules = Module.objects.all().values('id','program_id').order_by('-id')[:record_length-1]
        # for module in modules:
        #     if not ProgramModule.objects.all().filter(module_id = list(module.values())[0]).filter(program_id = list(module.values())[1]):
                
        #         program_module = ProgramModule(module_id = list(module.values())[0], program_id = list(module.values())[1])
                
        #         program_module.save()
        #     print(list(module.values()))
        importFile = request.FILES["import_form"].get_records()

        for record in importFile:
            if not Program.objects.all().filter(name = list(record.values())[0]):
                program = Program(name=list(record.values())[0])
            # print(list(record.values())[0])

        return HttpResponse(importFile)