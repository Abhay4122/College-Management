# Generated by Django 2.2.1 on 2019-06-28 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cit', '0003_std_registration'),
    ]

    operations = [
        migrations.CreateModel(
            name='std_exm_marks',
            fields=[
                ('exm_id', models.AutoField(primary_key=True, serialize=False)),
                ('exm_std_id', models.CharField(max_length=10)),
                ('exm_frm_no', models.CharField(max_length=10)),
                ('exm_enroll_no', models.CharField(max_length=20)),
                ('exm_certi_no', models.CharField(max_length=20)),
                ('exm_std_nam', models.CharField(max_length=50)),
                ('exm_fat_nam', models.CharField(max_length=50)),
                ('exm_location', models.CharField(max_length=150)),
                ('exm_cors', models.CharField(max_length=50)),
                ('exm_det', models.DateField()),
                ('exm_award_det', models.DateField()),
                ('exm_session', models.CharField(max_length=50)),
                ('exm_theory', models.CharField(max_length=10)),
                ('exm_prect', models.CharField(max_length=10)),
                ('exm_oral', models.CharField(max_length=10)),
                ('exm_total', models.CharField(max_length=10)),
            ],
        ),
    ]