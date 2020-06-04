# Generated by Django 3.0.6 on 2020-05-29 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('PyTraker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=2000)),
                ('comment_date', models.DateTimeField(verbose_name='commented date')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PyTraker.Profile')),
            ],
        ),
    ]