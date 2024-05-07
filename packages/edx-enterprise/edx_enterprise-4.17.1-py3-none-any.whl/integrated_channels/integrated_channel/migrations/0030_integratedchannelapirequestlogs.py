# Generated by Django 3.2.23 on 2024-01-12 07:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0197_auto_20231130_2239'),
        ('integrated_channel', '0029_genericenterprisecustomerpluginconfiguration_show_course_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntegratedChannelAPIRequestLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('enterprise_customer_configuration_id', models.IntegerField(help_text='ID from the EnterpriseCustomerConfiguration model')),
                ('endpoint', models.TextField()),
                ('payload', models.TextField()),
                ('time_taken', models.DurationField()),
                ('api_record', models.OneToOneField(blank=True, help_text='Data pertaining to the transmissions API request response.', null=True, on_delete=django.db.models.deletion.CASCADE, to='integrated_channel.apiresponserecord')),
                ('enterprise_customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='enterprise.enterprisecustomer')),
            ],
        ),
    ]
