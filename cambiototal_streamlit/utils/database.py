import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import relationship
import datetime

# --- Configuration ---
# Use an absolute path for the database file to avoid ambiguity.
# The database will be created in the project's root directory.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(PROJECT_ROOT, 'cambiototal.db')}"

# --- SQLAlchemy Setup ---
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --- ORM Models ---

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False, default="operator") # 'operator' or 'admin'

    fiat_transactions = relationship("TransactionFiat", back_populates="operator")
    crypto_transactions = relationship("TransactionCrypto", back_populates="operator")

class TransactionFiat(Base):
    __tablename__ = "transactions_fiat"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    type = Column(String, nullable=False) # "compra" (we buy USD) or "venta" (we sell USD)
    amount_usd = Column(Float, nullable=False)
    amount_ars = Column(Float, nullable=False)
    rate_applied = Column(Float, nullable=False)
    commission_spread_applied = Column(Float, nullable=False)

    operator_username = Column(String, ForeignKey("users.username"))
    operator = relationship("User", back_populates="fiat_transactions")

class TransactionCrypto(Base):
    __tablename__ = "transactions_crypto"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    type = Column(String, nullable=False) # "compra" or "venta"
    crypto_name = Column(String, nullable=False)
    crypto_amount = Column(Float, nullable=False)
    total_ars = Column(Float, nullable=False)
    usd_rate_applied = Column(Float, nullable=False)
    commission_applied = Column(Float, nullable=False)

    operator_username = Column(String, ForeignKey("users.username"))
    operator = relationship("User", back_populates="crypto_transactions")

class SystemSetting(Base):
    __tablename__ = "system_settings"
    key = Column(String, primary_key=True, index=True)
    value = Column(String, nullable=False)


# --- Database Initialization ---

def init_db():
    """
    Creates the database and all tables if they don't exist.
    """
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")

if __name__ == "__main__":
    # This allows running the script directly to initialize the database
    init_db()
    print("Tables created successfully in cambiototal.db")
