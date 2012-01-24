from team.models import Runner
from team.models import Race
from team.models import RaceType
from team.models import RaceRunner

#django contrib
from django.contrib import admin

class RaceRunnerInline(admin.TabularInline):
    model = RaceRunner
    extra = 3

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.attname == 'time':
            kwargs['widget'] = admin.widgets.AdminTextInputWidget()
        #     return db_field.formfield(**kwargs)
        return super(RaceRunnerInline, self).formfield_for_dbfield(db_field, **kwargs) 

class RaceAdmin(admin.ModelAdmin):
	
	model = Race
	inlines = (RaceRunnerInline,)
	
	list_display = ['name', 'url', 'date', 'location', 'racetype']
	list_display_links = ['name']
	list_filter = ['name', 'racetype']
	search_fields = ['name']
	date_hierarchy = 'date'
	
class RaceTypeAdmin(admin.ModelAdmin):
	
	model = RaceType
	
	list_display = ['name', 'is_maintype']
	
class RunnerAdmin(admin.ModelAdmin):
	
	model = Runner
	
	list_display = ['name', 'user', 'nickname', 'gender', 'birthdate', 'phone']
	list_display_links = ['name']
	list_filter = ['gender']
	search_fields = ['name']
	date_hierarchy = 'birthdate'
	
admin.site.register(Runner, RunnerAdmin)
admin.site.register(RaceType, RaceTypeAdmin)
admin.site.register(Race, RaceAdmin)



