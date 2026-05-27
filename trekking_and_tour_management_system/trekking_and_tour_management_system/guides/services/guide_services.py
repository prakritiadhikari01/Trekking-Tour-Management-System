def send_customer_trip_details(booking):

    guide = booking.assigned_guide

    payload = {
        "to": booking.email,
        "subject": "Your Trip Details",
        "message": {
            "packing_list": [
                "Trekking shoes",
                "Warm jacket",
                "Water bottle"
            ],
            "meeting_point": "Thamel Tourism Office - 7:00 AM",
            "guide_name": guide.full_name,
            "guide_phone": guide.phone_number,
        }
    }

    print("EMAIL SENT:", payload)