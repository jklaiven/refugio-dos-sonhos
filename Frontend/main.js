const API_BASE = "http://127.0.0.1:8000/api";

async function fetchRooms() {
  const res = await fetch(`${API_BASE}/rooms/`);
  const data = await res.json();
  renderRooms(data);
}

function renderRooms(rooms) {
  const container = document.getElementById('roomsList');
  container.innerHTML = '';
  rooms.forEach(room => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <img src="${room.image_url || 'https://via.placeholder.com/400x200'}" alt="Room ${room.number}">
      <h3>Quarto ${room.number} - ${room.type}</h3>
      <p>Capacidade: ${room.capacity} - R$ ${room.price_per_night}</p>
      <button class="reserve-btn" data-room='${JSON.stringify(room)}'>Reservar</button>
    `;
    container.appendChild(card);
  });

  document.querySelectorAll('.reserve-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const room = JSON.parse(e.currentTarget.dataset.room);
      openModal(room);
    });
  });
}

/* modal */
function openModal(room) {
  document.getElementById('modal').classList.remove('hidden');
  document.getElementById('modalRoomNumber').innerText = room.number;
  document.getElementById('roomId').value = room.id;
}

document.getElementById('cancelBtn').addEventListener('click', () => {
  document.getElementById('modal').classList.add('hidden');
});

/* submit reserva */
document.getElementById('reserveForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const clientData = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    phone: document.getElementById('phone').value
  };

  // 1) criar client
  const clientRes = await fetch(`${API_BASE}/clients/`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(clientData)
  });
  const clientJson = await clientRes.json();

  // 2) criar reserva usando o client retornado
  const payload = {
    client: clientJson.id,
    room: Number(document.getElementById('roomId').value),
    check_in: document.getElementById('checkin').value,
    check_out: document.getElementById('checkout').value,
    guests: 1,
    status: 'booked'
  };

  const res = await fetch(`${API_BASE}/reservations/`, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  const msg = document.getElementById('msg');

  if (res.ok) {
    msg.innerText = 'Reserva criada com sucesso!';
    document.getElementById('modal').classList.add('hidden');
  } else {
    msg.innerText = data.detail || 'Erro: ' + (data.detail || JSON.stringify(data));
  }
});

/* inicial */
fetchRooms();
