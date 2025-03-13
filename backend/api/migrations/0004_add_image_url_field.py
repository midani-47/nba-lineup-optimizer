from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_lineupcomparison_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ] 