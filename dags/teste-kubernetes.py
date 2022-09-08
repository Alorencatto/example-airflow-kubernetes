# [START pre_requisites]

# [END pre_requisites]

# [START import_module]
from os import getenv
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
# [END import_module]



# [START default_args]
default_args = {
    'owner': 'alorencatto',
    'start_date': datetime(2022, 8, 25),
    'depends_on_past': False,
    'email': ['lorencattoaugusto@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    }
# [END default_args]

# [START instantiate_dag]
with DAG(
    'teste-kubernetes',
    default_args=default_args,
    schedule_interval='@daily',
    tags=['development', 's3', 'sensor', 'minio', 'spark', 'operator', 'k8s']
) as dag:
# [END instantiate_dag]

    transformation = SparkKubernetesOperator(
        task_id='spark_transform_frete_new',
        namespace='spark',
        application_file='spark.yml',
        kubernetes_conn_id='kube-local',
        do_xcom_push=True,
    )
    
    monitor_spark_app_status = SparkKubernetesSensor(
        task_id='monitor_spark_app_status',
        namespace="spark",
        application_name="{{ task_instance.xcom_pull(task_ids='spark_transform_frete_new')['metadata']['name'] }}",
        kubernetes_conn_id="kube-local",
        attach_log=True
    )


    # [START task_sequence]
    transformation >> monitor_spark_app_status
    # [END task_sequence]
