# Generated by Django 2.1.4 on 2018-12-18 14:16

from django.db import migrations, models
import django.db.models.deletion
import lms.models.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('description', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('level', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])),
                ('faculty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='lms.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('text', models.CharField(max_length=512)),
                ('updated_at', models.DateField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='lms.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('token', models.CharField(blank=True, default=uuid.uuid4, max_length=64, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=128, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=12, null=True, unique=True, validators=[lms.models.validators.phone_number_validation])),
                ('password', models.CharField(blank=True, max_length=64, null=True)),
                ('secret_key', models.CharField(blank=True, max_length=64, null=True)),
                ('vk_link', models.CharField(blank=True, default='', max_length=64, validators=[lms.models.validators.vk_link_validation])),
                ('fb_link', models.CharField(blank=True, default='', max_length=64, validators=[lms.models.validators.fb_link_validation])),
                ('linkedin_link', models.CharField(blank=True, default='', max_length=64, validators=[lms.models.validators.linkedin_link_validation])),
                ('insta_link', models.CharField(blank=True, default='', max_length=64, validators=[lms.models.validators.insta_link_validation])),
                ('city', models.CharField(blank=True, default='', max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=512)),
                ('created_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('token', models.CharField(blank=True, default=uuid.uuid4, max_length=64, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=128, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=12, null=True, unique=True, validators=[lms.models.validators.phone_number_validation])),
                ('password', models.CharField(blank=True, max_length=64, null=True)),
                ('secret_key', models.CharField(blank=True, max_length=64, null=True)),
                ('vk_link', models.CharField(blank=True, default='', max_length=64, validators=[lms.models.validators.vk_link_validation])),
                ('fb_link', models.CharField(blank=True, default='', max_length=64, validators=[lms.models.validators.fb_link_validation])),
                ('linkedin_link', models.CharField(blank=True, default='', max_length=64, validators=[lms.models.validators.linkedin_link_validation])),
                ('insta_link', models.CharField(blank=True, default='', max_length=64, validators=[lms.models.validators.insta_link_validation])),
                ('city', models.CharField(blank=True, default='', max_length=64)),
                ('start_year', models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)])),
                ('degree', models.CharField(choices=[('bach', 'бакалавр'), ('mag', 'магистр'), ('spec', 'специалист')], max_length=64)),
                ('study_form', models.CharField(choices=[('full', 'очная'), ('ext', 'заочная'), ('nig', 'вечерняя')], max_length=64)),
                ('study_base', models.CharField(choices=[('bg', 'бюджетная'), ('cnt', 'контрактная')], max_length=64)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='lms.Group')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('text', models.CharField(max_length=512)),
                ('start_time', models.DateField()),
                ('finish_time', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='lms.Course')),
            ],
        ),
        migrations.AddField(
            model_name='solution',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='lms.Student'),
        ),
        migrations.AddField(
            model_name='solution',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='lms.Task'),
        ),
        migrations.AddField(
            model_name='course',
            name='groups',
            field=models.ManyToManyField(blank=True, null=True, related_name='courses', to='lms.Group'),
        ),
        migrations.AddField(
            model_name='course',
            name='headmen',
            field=models.ManyToManyField(blank=True, related_name='driven_courses', to='lms.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='professor',
            field=models.ManyToManyField(blank=True, null=True, related_name='courses', to='lms.Professor'),
        ),
    ]
