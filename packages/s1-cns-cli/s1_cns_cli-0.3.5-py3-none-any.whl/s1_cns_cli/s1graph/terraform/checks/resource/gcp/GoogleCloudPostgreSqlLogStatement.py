from s1_cns_cli.s1graph.common.models.enums import CheckCategories
from s1_cns_cli.s1graph.terraform.checks.resource.gcp.AbsGooglePostgresqlDatabaseFlags import AbsGooglePostgresqlDatabaseFlags

FLAG_NAME = 'log_statement'
FLAG_VALUES = [
    'ddl',
    'mod',
    'all'
]


class GoogleCloudPostgreSqlLogStatement(AbsGooglePostgresqlDatabaseFlags):
    def __init__(self):
        name = "Ensure GCP PostgreSQL logs SQL statements"
        check_id = "CKV_GCP_111"
        supported_resources = ['google_sql_database_instance']
        categories = [CheckCategories.LOGGING]
        super().__init__(
            name=name,
            id=check_id,
            categories=categories,
            supported_resources=supported_resources,
            flag_name=FLAG_NAME,
            flag_values=FLAG_VALUES
        )


check = GoogleCloudPostgreSqlLogStatement()
