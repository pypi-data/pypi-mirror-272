from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from express.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = "__all__"

class STKCheckoutSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()
    amount = serializers.IntegerField(min_value=1)
    reference = serializers.CharField()
    description = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.pop("phone_number")
        attrs["phone_number"] = str(phone_number)[1:]
        return attrs

