from database import SessionLocal, User, SystemSetting, engine
from sqlalchemy.orm import Session

def seed_data():
    """
    Seeds the database with initial users and system settings.
    """
    db: Session = SessionLocal()

    try:
        # --- Check if users already exist ---
        admin = db.query(User).filter(User.username == "agustin_admin").first()
        operator = db.query(User).filter(User.username == "juan_operador").first()

        if not admin:
            print("Creating admin user...")
            admin_user = User(
                username="agustin_admin",
                name="Agustín (Admin)",
                role="admin"
            )
            db.add(admin_user)
        else:
            print("Admin user already exists.")

        if not operator:
            print("Creating operator user...")
            operator_user = User(
                username="juan_operador",
                name="Juan (Operador)",
                role="operator"
            )
            db.add(operator_user)
        else:
            print("Operator user already exists.")

        # --- Initial System Settings ---
        default_settings = {
            "fiat_buy_commission_percent": "0.5",
            "fiat_sell_spread_percent": "0.5",
            "crypto_buy_commission_percent": "1.0",
            "crypto_sell_commission_percent": "1.0",
            "crypto_usd_rate": "1000.0" # Default "dólar cripto" rate
        }

        for key, value in default_settings.items():
            setting = db.query(SystemSetting).filter(SystemSetting.key == key).first()
            if not setting:
                print(f"Creating setting: {key} = {value}")
                new_setting = SystemSetting(key=key, value=value)
                db.add(new_setting)
            else:
                print(f"Setting '{key}' already exists.")

        db.commit()
        print("Database seeding completed successfully.")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting database seeding process...")
    seed_data()
