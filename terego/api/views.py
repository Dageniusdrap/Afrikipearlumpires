from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RoomSerializers
from terego.models import Rooms

@api_view(['GET'])
def getRoutes(request):
    routs= [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms:id'
    ]
    return Response(routs)


@api_view(['GET'])
def getRooms(request):
    rooms = Rooms.objects.all()
    serializers = RoomSerializers(rooms, many=True)
    return Response(serializers.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Rooms.objects.get(id=pk)
    serializers = RoomSerializers(room, many=False)
    return Response(serializers.data)