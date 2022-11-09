from django.db import models


# Create your models here.
class Menu(models.Model):
    title       =  models.TextField(blank=False, null=False)
    flag        =  models.CharField(max_length=50, blank=False, null=False)
    label       =  models.CharField(max_length=50, blank=True, null=True)
    pull        =  models.IntegerField(default=0, null=False)
    pull_url    =  models.URLField(blank=True, null=True)
    post_url    =  models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'dt_menus'
        verbose_name_plural = 'Menu'

    def __str__(self):
        return self.title


class SubMenu(models.Model):
    menu        =  models.ForeignKey(Menu, on_delete=models.CASCADE)
    view_id     =  models.CharField(max_length=10, blank=False, null=False)
    title       =  models.TextField(blank=False, null=False)
    

    class Meta:
        db_table = 'dt_sub_menus'
        verbose_name_plural = 'Sub Menus'

    def __str__(self):
        return self.title    


class MenuLink(models.Model):
    menu        =  models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu')
    sub_menu    =  models.ForeignKey(SubMenu, on_delete=models.DO_NOTHING, blank=True, null=True)
    link        =  models.ForeignKey(Menu, on_delete=models.DO_NOTHING, related_name='link')

    class Meta:
        db_table = 'dt_menu_links'
        verbose_name_plural = 'Menu Links'     


class MenuSession(models.Model):
    code        =  models.CharField(max_length=100, blank=True, null=True)
    phone       =  models.CharField(max_length=100, blank=True, null=True)
    message_id  =  models.CharField(max_length=100, blank=True, null=True)
    channel     =  models.CharField(max_length=100, blank=False, null=False, default='whatsapp')  
    menu        =  models.ForeignKey(Menu, on_delete=models.CASCADE)
    values      =  models.TextField(blank=True, null=True)
    active      =  models.IntegerField(blank=False, null=False, default=0)
    sent        =  models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        db_table = 'dt_menu_sessions'
        verbose_name_plural = 'Menu Sessions' 