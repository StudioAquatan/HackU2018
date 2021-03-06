# Generated by Django 2.1 on 2018-08-30 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=256)),
                ('comment_time', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='RoomTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('num_listener', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SlideTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slide_no', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField(verbose_name='slide start time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='slide end time')),
                ('room_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.RoomTable')),
            ],
        ),
        migrations.CreateModel(
            name='VoteTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_type', models.IntegerField()),
                ('vote_time', models.DateTimeField(verbose_name='date published')),
                ('slide_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.SlideTable')),
            ],
        ),
        migrations.AddField(
            model_name='commenttable',
            name='slide_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.SlideTable'),
        ),
    ]
