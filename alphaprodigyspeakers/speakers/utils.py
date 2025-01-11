from django.core.mail import send_mail

def send_booking_confirmation_email(user, booking):
    subject = 'Booking Confirmation'
    message = f'Dear {user.username},\n\nYour booking for {booking.service.name} on {booking.date} has been confirmed.\n\nThank you for choosing Alpha Prodigy Speakers!'
    send_mail(subject, message, 'annetdaisymm@gmail.com', [user.email])
