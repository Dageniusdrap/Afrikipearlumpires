from rest_framework.serializers import ModelSerializer
from terego.models import Rooms


class RoomSerializers(ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'