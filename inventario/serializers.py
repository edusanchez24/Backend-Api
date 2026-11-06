from rest_framework import serializers

from .models import Cliente, Producto, ProductoTalla, Venta, VentaDetalle


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'


class ProductoTallaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductoTalla
        fields = '__all__'

    def validate(self, attrs):
        producto = attrs.get('producto', getattr(self.instance, 'producto', None))
        talla = attrs.get('talla', getattr(self.instance, 'talla', None))
        if producto and producto.tallas.exclude(pk=getattr(self.instance, 'pk', None)).filter(
            talla=talla
        ).exists():
            raise serializers.ValidationError(
                {'talla': 'Ya existe esta talla para el producto seleccionado.'}
            )
        return attrs


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'
        read_only_fields = ('total', 'fecha')


class VentaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaDetalle
        fields = '__all__'
        read_only_fields = ('subtotal',)

    def validate(self, attrs):
        producto = attrs.get('producto', getattr(self.instance, 'producto', None))
        talla = attrs.get('talla', getattr(self.instance, 'talla', None))
        cantidad = attrs.get('cantidad', getattr(self.instance, 'cantidad', None))

        if talla and producto and talla.producto_id != producto.pk:
            raise serializers.ValidationError(
                {'talla': 'La talla seleccionada no pertenece al producto.'}
            )
        if cantidad is not None and cantidad < 1:
            raise serializers.ValidationError(
                {'cantidad': 'La cantidad debe ser al menos 1.'}
            )
        return attrs
