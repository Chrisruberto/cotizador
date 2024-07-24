from rest_framework import serializers

class DolarDataSerializer(serializers.Serializer):
    moneda = serializers.CharField()
    casa = serializers.CharField()
    nombre = serializers.CharField()
    compra = serializers.FloatField()
    venta = serializers.FloatField()
    fechaActualizacion = serializers.DateTimeField()
