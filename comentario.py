import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    bucket_name = os.environ["S3_BUCKET"]
    
    # Generar un UUID para el comentario
    uuidv1 = str(uuid.uuid1())
    
    # Crear el objeto del comentario
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    
    # Guardar el comentario en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)
    
    # Convertir el comentario a JSON para guardarlo en S3
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=bucket_name,
        Key=f'comentarios/{uuidv1}.json',
        Body=json.dumps(comentario),
        ContentType='application/json'
    )
    
    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response
    }
