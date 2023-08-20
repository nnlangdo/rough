from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Event,EventManager,District,Province,Participant,FamilyMember

admin.site.register(Event)
admin.site.register(EventManager)

class ProvinceResource(resources.ModelResource):
   class Meta:
      model = Province
class ProvinceAdmin(ImportExportModelAdmin):
   resource_class = ProvinceResource
   list_display = ('id','name',)
   search_fields = ('name',)
admin.site.register(Province,ProvinceAdmin)

class DistrictResource(resources.ModelResource):
   class Meta:
      model = District
class DistrictAdmin(ImportExportModelAdmin):
   resource_class = DistrictResource
   list_display = ('id','name',)
   search_fields = ('name',)
admin.site.register(District,DistrictAdmin)


class FamilyMemberResource(resources.ModelResource):
   class Meta:
      model = FamilyMember
class FamilyMemberAdmin(ImportExportModelAdmin):
   resource_class = FamilyMemberResource
   list_display = ('participant','name','age','gender')
   search_fields = ('name',)
class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember

admin.site.register(FamilyMember,FamilyMemberAdmin)

# class ParticipantResource(resources.ModelResource):
#    class Meta:
#       model = Participant
# class ParticipantAdmin(ImportExportModelAdmin):
#    resource_class = ParticipantResource
#    list_display = ('date_entry','name','phone','village','district','state','id_type','id_number','status','registered_by')
#    search_fields = ('name','id_number')
#    inlines = [FamilyMemberAdmin]
# admin.site.register(Participant,ParticipantAdmin)

# from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin
# from .models import Event, Participant, FamilyMember, EventManager, Id_Type

# Register Event, EventManager, and Id_Type as before
# admin.site.register(Event)
# admin.site.register(EventManager)
# admin.site.register(Id_Type)

# class FamilyMemberResource(resources.ModelResource):
#     class Meta:
#         model = FamilyMember

# class FamilyMemberInline(admin.TabularInline):
#     model = FamilyMember

class ParticipantResource(resources.ModelResource):
    class Meta:
        model = Participant

class ParticipantAdmin(ImportExportModelAdmin):
    resource_class = ParticipantResource
    list_display = ('date_entry', 'event','position','name','age','gender', 'phone', 'state','district','village','type_id','number_id', 'status', 'registered_by')
    search_fields = ('name', 'number_id')
    inlines = [FamilyMemberInline]  # Use FamilyMemberInline here

admin.site.register(Participant, ParticipantAdmin)