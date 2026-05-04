from email_validator import validate_email, EmailNotValidError

def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

    
    
def add_valid_mail_column(df):
    _l = []
    for email in df["email"]:
        try:
            _l.append(is_valid_email(email))
        except TypeError:
            _l.append(False)
    df.insert(3, "is_email_valid", _l)
   # df.assign([is_valid_email(email) for email in df["email"]])