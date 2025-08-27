from django.db import models

class Room(models.Model):
    ROOM_TYPES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    )

    number = models.CharField(max_length=10, unique=True)   # número/identificador do quarto
    type = models.CharField(max_length=10, choices=ROOM_TYPES)
    capacity = models.PositiveIntegerField(default=1)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)  # se o quarto está disponível para venda

    def __str__(self):
        return f"{self.number} - {self.get_type_display()}"


class Client(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Reservation(models.Model):
    STATUS = (
        ('booked', 'Booked'),
        ('checked_in', 'Checked-in'),
        ('cancelled', 'Cancelled'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS, default='booked')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Resv {self.id} - {self.client.name} - {self.room.number}"
