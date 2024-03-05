from sqlalchemy.orm import Session


class TransactionHandler:
    """
    Handles a DB transaction.
    """

    def __init__(self, session: Session):
        self.session = session

    def __enter__(self):
        if not self.session.is_active:
            return self.session.begin()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
