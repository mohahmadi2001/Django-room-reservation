from django.core.mail import send_mass_mail

def send_reminder_email(recipient_list, room, start_time, end_time):
    """
    Send a reminder email to a list of recipients about a room reservation.
    This function sends a reminder email to a list of recipients to notify them about a room reservation. The email includes information about the reserved room and its scheduled time.
    """
    email_messages = []
    subject = 'Room Reservation Reminder'
    message = f'Room {room} has been reserved for you from {start_time} to {end_time}.'
    from_email = 'admin@reservationapp.com'
    email_messages.append((subject, message, from_email, recipient_list))
    
    send_mass_mail(email_messages, fail_silently=False)