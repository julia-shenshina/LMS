# Generated by Django 2.1.4 on 2018-12-13 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='start_year',
            field=models.IntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)]),
        ),
    ]
