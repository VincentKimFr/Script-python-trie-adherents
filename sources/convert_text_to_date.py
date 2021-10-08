# ==============================================================================
# Python 3.9 (64 bits)
# -Vincent Kim-
# V 2.0
# ==============================================================================
import datetime
# ==============================================================================
def ft_convert_text_to_date(date) :
    
    #VAR
    conv = 0

    if (date == "") :
        conv = ft_convert_text_to_date("01/01/2100") + datetime.timedelta(days = 36500)
        return (conv)

    conv = date.split("/")
    conv = datetime.datetime(int(conv[2]), int(conv[1]), int(conv[0]))

    return (conv)
# ==============================================================================