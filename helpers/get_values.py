import re
def get_values(result: list) -> list:
    speed_value = None
    speed_unit = None
    for bbox, text, confidence in result:
        cleaned_text = text.strip().upper()

        # Look for a number (int or float)
        if re.fullmatch(r'\d+', cleaned_text):
            speed_value = int(cleaned_text)

        # Look for speed units
        elif cleaned_text in ['MPH', 'KMH']:
            speed_unit = cleaned_text
    return speed_value, speed_unit