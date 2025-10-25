// Chat Bot JavaScript

let chatOpen = false;
let messageCount = 0;

// Alternar visibilidad del chat
function toggleChat() {
    const chatWindow = document.getElementById('chatWindow');
    const chatBadge = document.getElementById('chatBadge');
    
    chatOpen = !chatOpen;
    
    if (chatOpen) {
        chatWindow.classList.add('show');
        chatBadge.style.display = 'none';
        scrollToBottom();
    } else {
        chatWindow.classList.remove('show');
    }
}

// Enviar mensaje
function enviarMensaje() {
    const input = document.getElementById('chatInput');
    const mensaje = input.value.trim();
    
    if (!mensaje) return;
    
    // Agregar mensaje del usuario
    agregarMensaje(mensaje, 'user');
    input.value = '';
    
    // Mostrar indicador de escritura
    mostrarEscribiendo();
    
    // Simular respuesta del bot después de 1 segundo
    setTimeout(() => {
        ocultarEscribiendo();
        const respuesta = obtenerRespuesta(mensaje);
        agregarMensaje(respuesta, 'bot');
    }, 1000);
}

// Enviar mensaje rápido desde botones de sugerencia
function enviarMensajeRapido(mensaje) {
    // Ocultar sugerencias
    const suggestions = document.querySelector('.chat-suggestions');
    if (suggestions) {
        suggestions.style.display = 'none';
    }
    
    // Agregar mensaje del usuario
    agregarMensaje(mensaje, 'user');
    
    // Mostrar indicador de escritura
    mostrarEscribiendo();
    
    // Simular respuesta del bot
    setTimeout(() => {
        ocultarEscribiendo();
        const respuesta = obtenerRespuesta(mensaje);
        agregarMensaje(respuesta, 'bot');
    }, 1000);
}

// Agregar mensaje al chat
function agregarMensaje(texto, tipo) {
    const chatMessages = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${tipo}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = tipo === 'bot' ? '🤖' : '👤';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    // Permitir HTML básico en las respuestas
    if (texto.includes('<br>')) {
        content.innerHTML = texto;
    } else {
        const p = document.createElement('p');
        p.textContent = texto;
        content.appendChild(p);
    }
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Mostrar indicador de escritura
function mostrarEscribiendo() {
    const chatMessages = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'chat-message bot';
    typingDiv.id = 'typingIndicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
    
    content.appendChild(indicator);
    typingDiv.appendChild(avatar);
    typingDiv.appendChild(content);
    
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

// Ocultar indicador de escritura
function ocultarEscribiendo() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

// Scroll automático al final
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Obtener respuesta del bot (solo visual - respuestas predefinidas)
function obtenerRespuesta(mensaje) {
    const msg = mensaje.toLowerCase();
    
    // Habitaciones
    if (msg.includes('habitacion') || msg.includes('cuarto') || msg.includes('disponible')) {
        return 'Tenemos 3 tipos de habitaciones disponibles:<br><br>🛏️ <strong>Simple</strong> - $50/noche (1 persona)<br>🛏️ <strong>Doble</strong> - $80/noche (2 personas)<br>🏨 <strong>Suite</strong> - $150/noche (4 personas)<br><br>¿Te gustaría ver más detalles?';
    }
    
    // Precios
    if (msg.includes('precio') || msg.includes('costo') || msg.includes('cuanto')) {
        return '💰 Nuestros precios son:<br><br>• Simple: $50 por noche<br>• Doble: $80 por noche<br>• Suite: $150 por noche<br><br>¿Deseas hacer una reserva?';
    }
    
    // Reservas
    if (msg.includes('reserva') || msg.includes('reservar') || msg.includes('booking')) {
        return '📅 Para hacer una reserva:<br><br>1️⃣ Ve a la sección de Habitaciones<br>2️⃣ Selecciona la habitación que te guste<br>3️⃣ Elige tus fechas de entrada y salida<br>4️⃣ Completa el formulario<br><br>¿Necesitas ayuda con algo más?';
    }
    
    // Ayuda
    if (msg.includes('ayuda') || msg.includes('help')) {
        return '🤝 Puedo ayudarte con:<br><br>• Ver habitaciones disponibles<br>• Información de precios<br>• Proceso de reserva<br>• Políticas del hotel<br><br>¿Qué necesitas saber?';
    }
    
    // Políticas
    if (msg.includes('politica') || msg.includes('cancelar') || msg.includes('cancelación')) {
        return '📋 Políticas del hotel:<br><br>• Check-in: 14:00 hrs<br>• Check-out: 12:00 hrs<br>• Puedes cancelar hasta 24 horas antes sin cargo<br>• Se requiere identificación oficial<br><br>¿Tienes otra pregunta?';
    }
    
    // Contacto
    if (msg.includes('contacto') || msg.includes('telefono') || msg.includes('email')) {
        return '📞 Puedes contactarnos:<br><br>• Teléfono: +52 555 123 4567<br>• Email: info@hotelreservas.com<br>• Horario: 24/7<br><br>¿En qué más puedo ayudarte?';
    }
    
    // Ubicación
    if (msg.includes('ubicacion') || msg.includes('direccion') || msg.includes('donde')) {
        return '📍 Nos encontramos en:<br><br>Av. Principal #123<br>Colonia Centro<br>Ciudad, CP 12345<br><br>A 5 minutos del centro y 15 minutos del aeropuerto.<br><br>¿Necesitas indicaciones?';
    }
    
    // Saludos
    if (msg.includes('hola') || msg.includes('buenos') || msg.includes('buenas')) {
        return '¡Hola! 👋 Bienvenido a nuestro hotel. ¿En qué puedo ayudarte hoy?';
    }
    
    // Gracias
    if (msg.includes('gracias') || msg.includes('thank')) {
        return '¡De nada! 😊 Estoy aquí para ayudarte. ¿Hay algo más que quieras saber?';
    }
    
    // Respuesta por defecto
    return '🤔 Interesante pregunta. Por el momento solo puedo ayudarte con:<br><br>• Información de habitaciones<br>• Precios y tarifas<br>• Proceso de reserva<br>• Políticas del hotel<br><br>¿Alguna de estas opciones te interesa?';
}

// Inicializar
document.addEventListener('DOMContentLoaded', function() {
    console.log('🤖 Chatbot inicializado');
    
    // Focus en input cuando se abre el chat
    const chatButton = document.getElementById('chatButton');
    chatButton.addEventListener('click', function() {
        if (chatOpen) {
            setTimeout(() => {
                document.getElementById('chatInput').focus();
            }, 300);
        }
    });
});
