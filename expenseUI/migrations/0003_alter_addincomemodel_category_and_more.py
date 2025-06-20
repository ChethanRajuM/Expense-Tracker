# Generated by Django 5.2.1 on 2025-05-28 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("expenseUI", "0002_alter_addincomemodel_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="addincomemodel",
            name="Category",
            field=models.CharField(
                choices=[
                    ("health", "Health"),
                    ("shopping", "Shopping"),
                    ("salary", "Salary"),
                    ("food", "Food"),
                    ("entertainment", "Entertainment"),
                    ("other income", "Other Income"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="addincomemodel",
            name="Payment_Method",
            field=models.CharField(
                choices=[
                    ("online", "Online"),
                    ("offline", "Offline"),
                    ("cash", "Cash"),
                    ("card", "Card"),
                    ("upi", "UPI"),
                    ("other income", "Other Income"),
                ],
                max_length=20,
            ),
        ),
    ]
