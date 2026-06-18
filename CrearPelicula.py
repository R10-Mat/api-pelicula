import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        # Entrada (json)
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]
        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        # Salida (json)
        
        respuesta_validada = {
            "tipo": "INFO",
            "log_datos": {
                "pelicula": pelicula,
                "dynamo_response": response
            }
        }
        print(json.dumps(respuesta_validada))
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    except Exception as e:
        respuesta_errada = {
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Hubo un error al registrar los datos",
                "Detalle": str(e) 
            }
        }
        print(json.dumps(e))
        return {
            'statusCode': 500,
            'error': 'error interno',
            'detalle': str(e)
        }
