from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from django import forms
from django.template import RequestContext
import django_excel as excel
from django import forms
from .models import Module, ProgramModule, Program, Content, IvrPrompt, ModuleContent
from django.contrib import messages
from django.db import IntegrityError
from upload_validator import FileTypeValidator
from django.core.exceptions import ValidationError

validator = FileTypeValidator(
    allowed_types=["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"],
    allowed_extensions=['.xlsx', '.xls']
)

# Function to handle import of programs.
def add_program(request):
    if request.method == "POST":
        try:
            validator(request.FILES["import_form_program"])
        except:
            messages.add_message(request, 40, 'Error uploading file, please upload .xlsx file.')
            return  HttpResponseRedirect('/admindashboard/program/')
        try:
            if request.FILES["import_form_program"]:
                programs = request.FILES["import_form_program"].get_records()
                import_count = 0
                skipped_count = 0
                update_count = 0
                error_count = 0
                msg = ''  
                for program in programs:
                    if 'id' in program and 'name' in program and 'description' in program and 'status' in program and 'start_date' in program and 'discontinuation_date' in program and 'program_type' in program and program['id'] != '':
                        try:
                            update_count += 1
                            update_program = Program.objects.get(id = program['id'])
                            update_program.name = program['name']
                            update_program.description = program['description']
                            update_program.status = program['status']
                            update_program.start_date = program['start_date']
                            update_program.discontinuation_date = program['discontinuation_date']
                            update_program.program_type = program['program_type']
                            update_program.save()
                        except:
                            error_count += 1
                    elif 'name' in program and 'description' in program and 'status' in program and 'start_date' in program and 'discontinuation_date' in program and 'program_type' in program and not 'id' in program and program['name'] != '':
                        print(program)
                        if not Program.objects.all().filter(name = program['name']):
                                new_program = Program(name = program['name'], description = program['description'], status = program['status'], start_date = program['start_date'], discontinuation_date = program['discontinuation_date'], program_type = program['program_type'])

                                new_program.save()
                                import_count +=1
                        else:
                            skipped_count += 1
                    elif  ('id' in program and program['id'] == '') or program['name'] == '':
                        pass
                    else:
                        messages.add_message(request, 40, 'Some column(s) are missing! Please download a sample file and upload a xlsx file with correct format.')
                        return  HttpResponseRedirect('/admindashboard/program/')
                msg = str(import_count) + ' program(s) import successfully. '+ str(update_count) +' program(s) updated.' + str(skipped_count) + ' existing program(s) skipped.' 
                messages.add_message(request, 25, msg)
                return HttpResponseRedirect('/admindashboard/program/')
        except Exception as e:
            messages.add_message(request, 40, 'Error uploading file! Please check your file and try again.')
            return  HttpResponseRedirect('/admindashboard/program/')
    else:
        messages.add_message(request, 40, 'Error! Please try again later')
        return  HttpResponseRedirect('/admindashboard/program/')


def program_format(request):
    if int(request.POST['format']) == 1:
        column_names = [["name", "description", "status", "start_date", "discontinuation_date", "program_type"]]
        return excel.make_response_from_array(
            column_names, "xlsx", file_name="Add Program"
        )
    elif int(request.POST['format']) == 2:
        column_names = [["id", "name", "description", "status", "start_date", "discontinuation_date", "program_type"]]
        return excel.make_response_from_array(
                column_names, "xlsx", file_name="Update Program"
            )
        

# Function to handle import of module.
def add_module(request):
    if request.method == "POST":
        try:
            validator(request.FILES["import_form_module"])
        except:
            messages.add_message(request, 40, 'Error uploading file, please upload .xlsx file.')
            return  HttpResponseRedirect('/admindashboard/module/')
        try:
            if request.FILES["import_form_module"]:
                modules = request.FILES["import_form_module"].get_records()
                import_count = 0
                skipped_count = 0
                error_count = 0
                update_count = 0
                msg = ''
                for module in modules:
                    if 'id' in module and 'name' in module and 'program_id' in module and module['id'] != '':
                        try:
                            update_module = Module.objects.get(id = module['id'])
                            update_module.name = module['name']
                            update_module.program_id = module['program_id']
                            update_module.save()

                            update_program_module = ProgramModule.objects.get(module_id = module['id'])
                            update_program_module.program_id = module['program_id']
                            update_program_module.save()
                            
                            update_count += 1
                        except IntegrityError:
                            error_count += 1
                    elif 'name' in module and 'program_id' in module and not 'id' in module and module['name'] != '':
                        if not Module.objects.all().filter(name = module['name']).filter(program_id = module['program_id']):
                            try:
                                new_module = Module(name = module['name'], program_id = module['program_id'])
                                new_module.save()
                                import_count += 1

                                program_module = ProgramModule(module_id = new_module.id, program_id = new_module.program_id)
                            
                                program_module.save()
                            except IntegrityError:
                                error_count += 1
                                
                        else:
                            skipped_count += 1
                    elif ('id' in module and module['id'] =='') or module['name'] == '':
                        pass
                    else:
                        messages.add_message(request, 40, 'Some column(s) are missing! Please download a sample file and upload a xlsx file with correct format.')
                        return  HttpResponseRedirect('/admindashboard/module/')
                msg = str(import_count) + ' module(s) import successfully. '+ str(skipped_count) + ' existing module(s) skipped. ' + str(update_count) + ' module(s) updated. ' + str(error_count) + ' error(s) occured.'
                messages.add_message(request, 25, msg)
                return HttpResponseRedirect('/admindashboard/module/')
        except:
            messages.add_message(request, 40, 'Error uploading file! Please check your file and try again.')
            return  HttpResponseRedirect('/admindashboard/module/')
    else:
        messages.add_message(request, 40, 'Error! Please try again later')
        return  HttpResponseRedirect('/admindashboard/module/')


def module_format(request):
    if int(request.POST['format']) == 1:
        try:
            column_names = [["name", "program_id"]]
            return excel.make_response_from_array(
                    column_names, "xlsx", file_name="Add Module"
                )
        except:
            messages.add_message(request, 40, "Error! Please try again later" )
            return HttpResponseRedirect('/admindashboard/module/')
    elif int(request.POST['format']) == 2:
        try:
            column_names = [["id", "name", "program_id"]]
            return excel.make_response_from_array(
                column_names, "xlsx", file_name="Update Module"
            )
        except:
            messages.add_message(request, 40, "Error! Please try again later" )
            return HttpResponseRedirect('/admindashboard/module/')



   
#  Function to handle import of content.               
def add_content(request):
    if request.method == "POST":
        try:
            validator(request.FILES["import_form_content"])
        except:
            messages.add_message(request, 40, 'Error uploading file, please upload .xlsx file.')
            return  HttpResponseRedirect('/admindashboard/content/')
        try:
            if request.FILES["import_form_content"]:
                contents = request.FILES["import_form_content"].get_records()
                import_count = 0
                skipped_count = 0
                error_count = 0
                update_count = 0
                msg = ''
                if 'id' in contents[0] and 'name' in contents[0] and 'duration' in contents[0] and 'status' in contents[0]:
                    # if "module" in contents[0] and "program_id" in contents[0]:
                    #     for content in contents:
                    #         if content['id'] == '':
                    #             pass
                    #         elif not Program.objects.all().filter(id = content['program_id']):
                    #             error_count += 1
                    #         elif content['id'] != '':
                    #             if not Module.objects.all().filter(name = content['module']).filter(program_id = content['program_id']):
                    #                 try:
                    #                     new_module = Module(name = content['module'], program_id = content['program_id'])
                    #                     new_module.save()

                    #                     new_program_module = ProgramModule(module_id = new_module.id, program_id = content['program_id'])
                    #                     new_program_module.save()

                    #                     update_content = Content.objects.get(id = content['id'])
                    #                     update_content.name = content['name']
                    #                     update_content.duration = content['duration']
                    #                     update_content.status = content['status']
                    #                     update_content.save()

                    #                     update_module_content = ModuleContent.objects.get(content_id = content['id'])
                    #                     update_module_content.module_id = new_module.id
                    #                     update_module_content.save()

                    #                     update_count += 1
                    #                 except:
                    #                     error_count += 1
                    #             else:
                    #                 try:
                    #                     update_content = Content.objects.get(id = content['id'])
                    #                     update_content.name = content['name']
                    #                     update_content.duration = content['duration']
                    #                     update_content.status = content['status']
                    #                     update_content.save()
                                        
                    #                     updated_module = Module.objects.get(name = content['module'])
                    #                     update_module_content = ModuleContent.objects.get(content_id = content['id'])
                    #                     update_module_content.module_id = updated_module.id 
                    #                     update_module_content.save()

                    #                     update_count += 1
                    #                 except:
                    #                     error_count += 1
                    # elif not 'module' in contents[0]:
                    try:
                        for content in contents:
                            if ('id' in content and content['id'] != ''):
                                update_content = Content.objects.get(id = content['id'])
                                update_content.name =  content['name']
                                update_content.duration = content['duration']
                                update_content.status = content['status']
                                update_content.save()

                                update_count += 1
                    except:
                        error_count += 1
                    
                    msg = str(import_count) + ' content(s) import successfully. '+ str(skipped_count) + ' existing content(s) skipped. '+ str(update_count) + ' content(s) updated.' + str(error_count) + ' error occured.' 
                    messages.add_message(request, 25, msg)
                    return HttpResponseRedirect('/admindashboard/content/')

                elif 'name' in contents[0] and 'duration' in contents[0] and 'status' in contents[0]:
                    if "module" in contents[0]:
                        for content in contents:
                            if content['name'] == '':
                                    pass
                            elif not Content.objects.all().filter(name = content['name'])  and not 'id' in content and content['name'] != '':
                                if not Module.objects.all().filter(name = content['module']).filter(program_id = content['program_id']):
                                    try:
                                        new_module = Module(name = content['module'], program_id = content['program_id'])
                                        new_module.save()

                                        new_program_module = ProgramModule(module_id = new_module.id, program_id = content['program_id'])
                                        new_program_module.save()

                                        new_content = Content(name = content['name'], duration = content['duration'], status = content['status'])
                                        new_content.save()

                                        module_content = ModuleContent(module_id = new_module.id, content_id = new_content.id)
                                        module_content.save()
                                        import_count += 1
                                    except IntegrityError:
                                        error_count += 1
                                else:
                                    try:
                                        new_content = Content(name = content['name'], duration = content['duration'], status = content['status'])
                                        new_content.save()
                                        import_count += 1

                                        module_id = Module.objects.get(name = content['module'], program_id = content['program_id']).id
                                        print(module_id)

                                        module_content = ModuleContent(module_id = module_id, content_id = new_content.id)
                                        module_content.save()
                                    except Exception as e:
                                        error_count += 1
                            else:
                                skipped_count += 1
                    else:
                        for content in contents:
                            if content['name'] == '':
                                pass
                            elif not Content.objects.all().filter(name = content['name'])  and not 'id' in content:
                                new_content = Content(name = content['name'], duration = content['duration'], status = content['status'])
                                new_content.save()
                                import_count += 1
                            else:
                                skipped_count += 1
                    
                    msg = str(import_count) + ' content(s) import successfully. '+ str(skipped_count) + ' existing content(s) skipped. '+ str(update_count) + ' content(s) updated. ' + str(error_count) + ' error occured.' 
                    messages.add_message(request, 25, msg)
                    return HttpResponseRedirect('/admindashboard/content/')
                else:
                    messages.add_message(request, 40, 'Some column(s) are missing! Please download a sample file and upload a xlsx file with correct format.')
                    return HttpResponseRedirect('/admindashboard/content/')
        except:
            messages.add_message(request, 40, 'Error uploading file! Please check your file and try again.')
            return HttpResponseRedirect('/admindashboard/content/')
    
    messages.add_message(request, 40, "Error! Please try again later" )
    return HttpResponseRedirect('/admindashboard/content/')


def content_format(request):
    if int(request.POST['format']) == 1:
        try:
            column_names = [["name", "duration", "status"]]
            return excel.make_response_from_array(
                   column_names, "xlsx", file_name="Add Content"
                )
        except:
            messages.add_message(request, 40, "Error! Please try again later" )
            return HttpResponseRedirect('/admindashboard/content/')
    elif int(request.POST['format']) == 2:
        try:
            column_names = [["name", "duration", "status","module", "program_id"]]
            return excel.make_response_from_array(
                    column_names, "xlsx", file_name="Add Content"
                )
        except:
            messages.add_message(request, 40, "Error! Please try again later" )
            return HttpResponseRedirect('/admindashboard/content/')
    elif int(request.POST['format']) == 3:
        try:
            column_names = [["id", "name", "duration", "status"]]
            return excel.make_response_from_array(
                    column_names, "xlsx", file_name="Update Content"
                )
        except:
            messages.add_message(request, 40, "Error! Please try again later" )
            return HttpResponseRedirect('/admindashboard/content/')

    # elif int(request.POST['format']) == 4:
    #     try:
    #         column_names = [["id", "name", "duration", "status","module", "program_id"]]
    #         return excel.make_response_from_array(
    #                 column_names, "xlsx", file_name="Update Content"
    #             )
    #     except:
    #         messages.add_message(request, 40, "Error! Please try again later" )
    #         return HttpResponseRedirect('/admindashboard/content/')
        
# Function to handle import of IvrPrompt
def add_ivr_prompt(request):
    try:
        validator(request.FILES["import_form_ivrprompt"])
    except:
        messages.add_message(request, 40, 'Error uploading file, please upload .xlsx file.')
        return  HttpResponseRedirect('/admindashboard/ivrprompt/')
    if request.method == "POST":
        try:
            if request.FILES['import_form_ivrprompt']:
                prompts = request.FILES['import_form_ivrprompt'].get_records()
                import_count = 0
                skipped_count = 0
                error_count = 0
                update_count = 0
                msg = ''
                for prompt in prompts:
                    try:
                        if 'id' in prompt and 'content_id' in prompt and 'prompt_name' in prompt and 'prompt_question' in prompt and 'possible_response' in prompt and 'status' in prompt:
                            if prompt['id'] != '':
                                update_prompt = IvrPrompt.objects.get(id = prompt['id'])
                                update_prompt.content_id = prompt['content_id']
                                update_prompt.name = prompt['prompt_name']
                                update_prompt.prompt_question = prompt['prompt_question']
                                update_prompt.possible_response = prompt['possible_response']
                                update_prompt.status = prompt['status']

                                update_prompt.save()
                                update_count += 1
                            else:
                                pass
                        elif 'content_id' in prompt and 'prompt_name' in prompt and 'prompt_question' in prompt and 'possible_response' in prompt and 'status' in prompt:
                            if prompt['content_id']!='':
                                if not IvrPrompt.objects.all().filter(prompt_name = prompt['prompt_name']).filter(content = prompt['content_id']):
                                    new_prompt = IvrPrompt(content_id = prompt['content_id'], prompt_name = prompt['prompt_name'], prompt_question = prompt['prompt_question'], possible_response = prompt['possible_response'], status = prompt['status'])
                                    new_prompt.save()
                                    import_count += 1
                                    print(prompt)
                                else:
                                    skipped_count += 1
                            else:
                                pass                
                        else:
                            messages.add_message(request, 40, 'Some column(s) are missing! Please download a sample file and upload a xlsx file with correct format.')
                            return HttpResponseRedirect('/admindashboard/ivrprompt/')
                    except:
                        error_count += 1
                        
                msg = str(import_count) + ' IvrPrompt(s) imported successfully. ' + str(skipped_count) + ' existing IvrPrompt(s) skipped. ' + str(update_count) + ' ivrprompt(s) updated.' + str(error_count) + ' error occured.' 
                messages.add_message(request, 25, msg)
                return HttpResponseRedirect('/admindashboard/ivrprompt/')
        except:
            messages.add_message(request, 40, 'Error uploading file! Please check your file and try again.')
            return  HttpResponseRedirect('/admindashboard/ivrprompt/')

    messages.add_message(request, 40, "Error! Please try again later" )
    return HttpResponseRedirect('/admindashboard/ivrprompt/')


def ivrprompt_format(request):
    if int(request.POST['format']) == 1:
        try:
            column_names = [["content_id", "prompt_name", "prompt_question", "possible_response", "status"]]
            return excel.make_response_from_array(
                column_names, "xlsx", file_name="Add IVRPrompt"
            )
        except:
            messages.add_message(request, 40, "Error! Please try again later" )
            return HttpResponseRedirect('/admindashboard/ivrprompt/') 
    elif int(request.POST['format']) == 2:
        try:
            column_names = [["id", "content_id", "prompt_name", "prompt_question", "possible_response", "status"]]
            return excel.make_response_from_array(
                    column_names, "xlsx", file_name="Update IVRprompt"
            )
        except:
            messages.add_message(request, 40, "Error! Please try again later" )
            return HttpResponseRedirect('/admindashboard/ivrprompt/')
