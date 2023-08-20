from django.urls import path
from . import views
# from . views import LeavesList

app_name = "hawan"

urlpatterns = [
    # path('add_participant',views.add_participant, name="add_participant" ),
    # path('', views.index, name="index"),
    path('', views.view_page, name='view_page'),
    path('district/', views.district, name='district'),
    # path('add_family_form/<int:participant_id>/',views.add_family_form,name="add_family_form"),
    path('add_family_members/<int:participant_id>/<int:num_family_members>/', views.add_family_members, name='add_family_members'),
    path('letter_hawan_current/<int:participant_id>/', views.letter_hawan_current, name='letter_hawan_current'),
    path('add_participant_with_family_members/', views.add_participant_with_family_members, name='add_participant_with_family_members'),
 ]