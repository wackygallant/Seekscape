from datetime import datetime
import secrets

def generate_trip_id(trip_instance):
    # 1. Get Trek Prefix
    title_parts = trip_instance.trek.title.split()
    if len(title_parts) > 1:
        prefix = "".join([word[0] for word in title_parts]).upper()
    else:
        prefix = trip_instance.trek.title[:3].upper()

    # 2. Get Formatted Date
    date_str = trip_instance.start_date.strftime('%Y%m%d')

    # 3. Calculate the NNNN
    day_count = trip_instance.__class__.objects.filter(
        trek=trip_instance.trek,
        start_date=trip_instance.start_date
    ).count()

    sequence = str(day_count + 1).zfill(4)

    return f"{prefix}-{date_str}-{sequence}"#

def generate_booking_id(prefix="BOOK", length=5):
    """
    Generates a human-readable unique code.
    Example output: BOOK-KJ928
    """
    # We remove 0, O, I, L, 1, S, 5 to prevent user errors
    allowed_chars = "ABCDEFGHJKMNPQRTUVWXY2346789"
    
    # Generate the random part
    random_part = ''.join(secrets.choice(allowed_chars) for _ in range(length))
    
    return f"{prefix}-{random_part}"