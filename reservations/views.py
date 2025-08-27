from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Room, Client, Reservation
from .serializers import RoomSerializer, ClientSerializer, ReservationSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        """
        Ao criar uma reserva, verificamos se o quarto já está reservado (status booked/checked_in)
        para o intervalo de datas solicitado. Se houver interseção, retornamos 400.
        """
        room_id = request.data.get('room')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')

        if not room_id or not check_in or not check_out:
            return Response({'detail': 'room, check_in e check_out são obrigatórios.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # buscar conflitos: reservas para o mesmo quarto com status ativo (booked/checked_in)
        conflicts = Reservation.objects.filter(
            room_id=room_id,
            status__in=['booked', 'checked_in']
        ).filter(
            Q(check_in__lte=check_out) & Q(check_out__gte=check_in)
        )

        if conflicts.exists():
            return Response({'detail': 'Quarto indisponível nestas datas.'},
                             status=status.HTTP_400_BAD_REQUEST)

        # tudo ok, cria a reserva
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # opcional: calcular total_price antes de salvar (por exemplo, price_per_night * nights)
        room = Room.objects.get(pk=room_id)
        from datetime import datetime
        ci = datetime.fromisoformat(check_in)
        co = datetime.fromisoformat(check_out)
        nights = (co - ci).days
        if nights <= 0:
            return Response({'detail': 'check_out deve ser após check_in.'},
                            status=status.HTTP_400_BAD_REQUEST)
        total = room.price_per_night * nights
        serializer.save(total_price=total)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
