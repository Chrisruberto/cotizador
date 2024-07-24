from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timezone
import requests
from .models import Dolar


class YourAPIView(APIView):
    def get(self, request, format=None):
        try:
            # Comprueba si ya hay datos en la base de datos
            if not Dolar.objects.exists():
                # Si no hay datos, realiza la solicitud a la API y guarda los datos
                response = requests.get("https://dolarapi.com/v1/dolares")
                response_data = response.json()
                
                # Limpiar datos existentes antes de guardar nuevos datos
                Dolar.objects.all().delete()
                
                # Convertir las fechas a objetos datetime en UTC y guardar en la base de datos
                for item in response_data:
                    if 'fechaActualizacion' in item:
                        fecha_actualizacion = datetime.fromisoformat(item['fechaActualizacion'].replace('Z', '+00:00')).astimezone(timezone.utc)
                        
                        Dolar.objects.create(
                            nombre=item.get('nombre', ''),
                            compra=item.get('compra', 0.0),
                            venta=item.get('venta', 0.0),
                            fecha_actualizacion=fecha_actualizacion
                        )
            
            # Recuperar datos desde la base de datos
            data_from_db = list(Dolar.objects.values())
            
            # Obtener la fecha y valores de la última actualización
            if len(data_from_db) > 1:
                previous_data = data_from_db[0]
                for item in data_from_db:
                    item['is_higher'] = item['compra'] > previous_data['compra']
                    item['is_lower'] = item['compra'] < previous_data['compra']
                    
                    item['is_higher_sale'] = item['venta'] > previous_data['venta']
                    item['is_lower_sale'] = item['venta'] < previous_data['venta']
                previous_date = data_from_db[0]['fecha_actualizacion']
            else:
                previous_date = None
            
            # Verificar si la solicitud espera una respuesta HTML
            if 'text/html' in request.headers.get('Accept', ''):
                return render(request, 'dolar_template.html', {'data': data_from_db, 'previous_date': previous_date})
            
            # Si no, devolver una respuesta JSON
            return JsonResponse(data_from_db, safe=False, status=status.HTTP_200_OK)
        
        except requests.exceptions.RequestException as e:
            error_message = {"error": str(e)}
            
            # Verificar si la solicitud espera una respuesta HTML en caso de error
            if 'text/html' in request.headers.get('Accept', ''):
                return render(request, 'dolar_template.html', {'error': error_message})
            
            # Si no, devolver una respuesta JSON en caso de error
            return JsonResponse(error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
