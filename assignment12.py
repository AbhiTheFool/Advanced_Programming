from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import uuid, json, os


class OrderStatus(Enum):
    PENDING   = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED    = "FAILED"


# ── ORDERS ────────────────────────────────────────────────────────────────────

class Order(ABC):
    def __init__(self, customer: str, items: list[dict]):
        self.order_id  = str(uuid.uuid4())[:8].upper()
        self.customer  = customer
        self.items     = items
        self.status    = OrderStatus.PENDING
        self.created   = datetime.now().isoformat()

    def base_total(self):
        return sum(i["price"] for i in self.items)

    @abstractmethod
    def final_price(self): pass

    @abstractmethod
    def order_type(self): pass

    def to_dict(self):
        return {
            "order_id"   : self.order_id,
            "type"       : self.order_type(),
            "customer"   : self.customer,
            "items"      : self.items,
            "total"      : self.final_price(),
            "status"     : self.status.value,
            "created"    : self.created,
        }

    def __str__(self):
        return f"[{self.order_type()}] #{self.order_id} | {self.customer} | ₹{self.final_price():.2f}"


class RegularOrder(Order):
    def final_price(self): return self.base_total()
    def order_type(self):  return "Regular"


class DiscountedOrder(Order):
    def __init__(self, customer, items, discount_pct):
        super().__init__(customer, items)
        self.discount_pct = discount_pct

    def final_price(self): return self.base_total() * (1 - self.discount_pct / 100)
    def order_type(self):  return f"Discounted ({self.discount_pct}% off)"


class PriorityOrder(Order):
    def final_price(self): return self.base_total() + 49
    def order_type(self):  return "Priority (+₹49 express fee)"


# ── PAYMENT METHODS ───────────────────────────────────────────────────────────

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, order: Order) -> bool: pass
    @abstractmethod
    def name(self) -> str: pass


class CreditCardPayment(PaymentProcessor):
    def __init__(self, card_number, cvv):
        self.last4 = card_number[-4:]

    def process(self, order):
        print(f"  💳  Charging ₹{order.final_price():.2f} to card ****{self.last4}")
        return True

    def name(self): return f"Credit Card (****{self.last4})"


class UPIPayment(PaymentProcessor):
    def __init__(self, upi_id):
        self.upi_id = upi_id

    def process(self, order):
        print(f"  📲  UPI request of ₹{order.final_price():.2f} sent to {self.upi_id}")
        return True

    def name(self): return f"UPI ({self.upi_id})"


class WalletPayment(PaymentProcessor):
    def __init__(self, wallet_id, balance):
        self.wallet_id = wallet_id
        self.balance   = balance

    def process(self, order):
        if self.balance >= order.final_price():
            self.balance -= order.final_price()
            print(f"  👛  Wallet debited ₹{order.final_price():.2f}. Remaining: ₹{self.balance:.2f}")
            return True
        print(f"  ❌  Wallet balance ₹{self.balance:.2f} is less than ₹{order.final_price():.2f}")
        return False

    def name(self): return f"Wallet ({self.wallet_id})"


class NetBankingPayment(PaymentProcessor):
    def __init__(self, bank, account_suffix):
        self.bank = bank
        self.acct = account_suffix

    def process(self, order):
        print(f"  🏦  Net Banking transfer of ₹{order.final_price():.2f} via {self.bank}")
        return True

    def name(self): return f"Net Banking ({self.bank} ...{self.acct})"


# ── NOTIFICATION CHANNELS ─────────────────────────────────────────────────────

class Notifier(ABC):
    @abstractmethod
    def send(self, order: Order, message: str): pass
    @abstractmethod
    def channel(self) -> str: pass


class EmailNotifier(Notifier):
    def __init__(self, email): self.email = email
    def send(self, order, message):
        print(f"  📧  Email → {self.email} | {message}")
    def channel(self): return f"Email ({self.email})"


class SMSNotifier(Notifier):
    def __init__(self, phone): self.phone = phone
    def send(self, order, message):
        print(f"  📱  SMS → {self.phone} | {message[:100]}")
    def channel(self): return f"SMS ({self.phone})"


class PushNotifier(Notifier):
    def __init__(self, token): self.token = token[:8] + "..."
    def send(self, order, message):
        print(f"  🔔  Push → {self.token} | {message}")
    def channel(self): return f"Push ({self.token})"


# ── STORAGE ───────────────────────────────────────────────────────────────────

class OrderStorage(ABC):
    @abstractmethod
    def save(self, order: Order): pass
    @abstractmethod
    def retrieve(self, order_id: str): pass
    @abstractmethod
    def name(self) -> str: pass


class DatabaseStorage(OrderStorage):
    def __init__(self): self._db = {}
    def save(self, order):
        self._db[order.order_id] = order.to_dict()
        print(f"  🗄️   Saved #{order.order_id} to Database")
    def retrieve(self, order_id): return self._db.get(order_id)
    def name(self): return "Database"


class FileStorage(OrderStorage):
    def __init__(self, path="/tmp/orders"):
        self.path = path
        os.makedirs(path, exist_ok=True)

    def save(self, order):
        file = os.path.join(self.path, f"{order.order_id}.json")
        with open(file, "w") as f:
            json.dump(order.to_dict(), f, indent=2)
        print(f"  📁  Saved #{order.order_id} to {file}")

    def retrieve(self, order_id):
        file = os.path.join(self.path, f"{order_id}.json")
        return json.load(open(file)) if os.path.exists(file) else None

    def name(self): return f"File ({self.path})"


# ── ORDER SERVICE (orchestrator) ──────────────────────────────────────────────

class OrderService:
    def __init__(self, payment: PaymentProcessor, notifiers: list[Notifier], storage: OrderStorage):
        self.payment   = payment
        self.notifiers = notifiers
        self.storage   = storage

    def place_order(self, order: Order) -> bool:
        print(f"\n{'─'*55}")
        print(f"  🛒  {order}")
        print(f"{'─'*55}")

        print(f"\n  [1] Payment via {self.payment.name()}")
        if not self.payment.process(order):
            order.status = OrderStatus.FAILED
            print(f"  ❌  Payment failed. Order cancelled.\n")
            return False

        order.status = OrderStatus.CONFIRMED
        print(f"  ✅  Payment successful!")

        msg = f"Order #{order.order_id} confirmed! Total: ₹{order.final_price():.2f}. Thank you, {order.customer}!"
        print(f"\n  [2] Notifications ({len(self.notifiers)} channel/s)")
        for n in self.notifiers:
            n.send(order, msg)

        print(f"\n  [3] Storage via {self.storage.name()}")
        self.storage.save(order)

        print(f"\n  🎉  Done! Order #{order.order_id} placed.\n")
        return True


# ── DEMO ──────────────────────────────────────────────────────────────────────

def main():
    print("\n  ══ E-Commerce Order System (SOLID) ══\n")

    print("  ▶ Demo 1: Regular | Credit Card | Email + SMS | Database")
    OrderService(
        payment   = CreditCardPayment("4111111111111234", "123"),
        notifiers = [EmailNotifier("riya@example.com"), SMSNotifier("+91-98765-43210")],
        storage   = DatabaseStorage()
    ).place_order(RegularOrder("Riya Sharma", [{"name": "Python Book", "price": 599}, {"name": "USB Hub", "price": 899}]))

    print("  ▶ Demo 2: Discounted 20% | UPI | Push | File")
    OrderService(
        payment   = UPIPayment("arjun@okaxis"),
        notifiers = [PushNotifier("device_token_ABC123XYZ")],
        storage   = FileStorage()
    ).place_order(DiscountedOrder("Arjun Mehta", [{"name": "Keyboard", "price": 1499}, {"name": "Mouse", "price": 799}], discount_pct=20))

    print("  ▶ Demo 3: Priority | Wallet with LOW balance (should fail)")
    OrderService(
        payment   = WalletPayment("sneha_wallet", balance=500),
        notifiers = [EmailNotifier("sneha@example.com")],
        storage   = DatabaseStorage()
    ).place_order(PriorityOrder("Sneha Patel", [{"name": "Smartwatch", "price": 5999}]))

    print("  ▶ Demo 4: Discounted 10% | Net Banking | All 3 Notifiers | File")
    OrderService(
        payment   = NetBankingPayment("HDFC", "7890"),
        notifiers = [EmailNotifier("v@co.com"), SMSNotifier("+91-91234-56789"), PushNotifier("device_XYZ_789")],
        storage   = FileStorage()
    ).place_order(DiscountedOrder("Vikram Singh", [{"name": "Laptop Stand", "price": 1299}, {"name": "Desk Lamp", "price": 649}], discount_pct=10))


if __name__ == "__main__":
    main()
