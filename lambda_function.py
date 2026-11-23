import boto3
import csv
import json
import logging
import io
import os

# Configuración del logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Cliente de S3
s3_client = boto3.client('s3')

# Configuración de los buckets
INPUT_BUCKET = 'bld-tseed-workshop-input-semillero-2026-q4'
INPUT_KEY = 'andres-jimenez/users_dataset_100.csv'

OUTPUT_BUCKET = 'bld-tseed-workshop-output-semillero-2026-q4-d'
OUTPUT_PREFIX = 'andres-jimenez/data/'


def read_csv_from_s3(bucket, key):
    """
    Descarga y lee el archivo CSV desde S3.
    """

    logger.info(f"Leyendo archivo: s3://{bucket}/{key}")

    response = s3_client.get_object(
        Bucket=bucket,
        Key=key
    )

    csv_content = io.TextIOWrapper(
        response['Body'],
        encoding='utf-8-sig'
    )

    csv_reader = csv.DictReader(csv_content)

    return csv_reader


def convert_row_to_json(row):
    """
    Convierte una fila del CSV en un objeto JSON.
    """

    return json.dumps(
        row,
        ensure_ascii=False
    )


def upload_json_to_s3(json_data, filename):
    """
    Sube un archivo JSON al bucket de destino.
    """

    output_key = f"{OUTPUT_PREFIX}{filename}"

    s3_client.put_object(
        Bucket=OUTPUT_BUCKET,
        Key=output_key,
        Body=json_data.encode('utf-8'),
        ContentType='application/json'
    )

    logger.info(
        f"Archivo generado: s3://{OUTPUT_BUCKET}/{output_key}"
    )


def lambda_handler(event, context):
    """
    Función principal de AWS Lambda.
    """

    try:

        logger.info("Iniciando procesamiento del CSV")

        # 1. Leer archivo CSV desde S3
        csv_reader = read_csv_from_s3(
            INPUT_BUCKET,
            INPUT_KEY
        )

        # 2. Procesar cada registro
        total_records = 0

        for row_number, row in enumerate(csv_reader, start=1):

            # 3. Convertir registro a JSON
            json_data = convert_row_to_json(row)

            # 4. Generar nombre del archivo
            filename = f"users_dataset_100_{row_number}.json"

            # 5. Subir JSON al bucket de destino
            upload_json_to_s3(
                json_data,
                filename
            )

            total_records += 1

        logger.info(
            f"Procesamiento finalizado. "
            f"Total de registros: {total_records}"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Procesamiento exitoso',
                'total_records': total_records,
                'output_bucket': OUTPUT_BUCKET,
                'output_prefix': OUTPUT_PREFIX
            })
        }

    except Exception as e:

        logger.exception(
            f"Error durante el procesamiento: {str(e)}"
        )

        raise
