from django.db import migrations, models, connection

def check_column_exists(apps, schema_editor):
    cursor = connection.cursor()
    cursor.execute("PRAGMA table_info(api_player);")
    columns = [column[1] for column in cursor.fetchall()]
    return 'image_url' in columns

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_lineupcomparison_user'),
    ]

    operations = [
        migrations.RunPython(
            code=lambda apps, schema_editor: None if check_column_exists(apps, schema_editor) else migrations.AddField(
                model_name='player',
                name='image_url',
                field=models.URLField(blank=True, max_length=500, null=True),
            ).database_forwards('api', schema_editor, None, apps.get_models()[0]),
            reverse_code=migrations.RunPython.noop,
        ),
    ] 