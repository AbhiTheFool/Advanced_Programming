import java.util.*;

class BankProfile {
    private String idNumber;
    private String holderName;
    private double amount;

    // Default Constructor
    public BankProfile() {
        this("XXXX", "Guest", 0.0);
    }

    // Parameterized Constructor
    public BankProfile(String idNumber, String holderName, double amount) {
        this.idNumber = idNumber;
        this.holderName = holderName;
        setAmount(amount);
    }

    public String getIdNumber() {
        return idNumber;
    }

    public void setIdNumber(String idNumber) {
        if (idNumber == null || idNumber.isEmpty()) {
            throw new IllegalArgumentException("Invalid ID");
        }
        this.idNumber = idNumber;
    }

    public String getHolderName() {
        return holderName;
    }

    public void setHolderName(String holderName) {
        if (holderName == null || holderName.isEmpty()) {
            throw new IllegalArgumentException("Invalid Name");
        }
        this.holderName = holderName;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        this.amount = amount;
    }

    public void addMoney(double value) {
        if (value <= 0) {
            throw new IllegalArgumentException("Enter valid amount");
        }
        amount += value;
    }

    public void deductMoney(double value) {
        if (value <= 0) {
            throw new IllegalArgumentException("Enter valid amount");
        }
        if (value > amount) {
            throw new IllegalArgumentException("Low balance");
        }
        amount -= value;
    }

    public void showDetails() {
        System.out.println("ID: " + idNumber);
        System.out.println("Name: " + holderName);
        System.out.println("Balance: " + amount);
    }
}

// Fixed Deposit Account
class FixedDeposit extends BankProfile {
    private double rate;

    public FixedDeposit(String id, String name, double amt, double rate) {
        super(id, name, amt);
        this.rate = rate;
    }

    public double computeReturn() {
        return getAmount() * rate / 100;
    }

    @Override
    public void showDetails() {
        super.showDetails();
        System.out.println("Interest Rate: " + rate + "%");
        System.out.println("Return: " + computeReturn());
    }
}

// Business Account
class BusinessAccount extends BankProfile {
    private double creditLimit;

    public BusinessAccount(String id, String name, double amt, double creditLimit) {
        super(id, name, amt);
        this.creditLimit = creditLimit;
    }

    @Override
    public void deductMoney(double value) {
        if (value <= 0) {
            throw new IllegalArgumentException("Enter valid amount");
        }

        if (value > (getAmount() + creditLimit)) {
            throw new IllegalArgumentException("Limit exceeded");
        }

        setAmount(getAmount() - value);
    }

    @Override
    public void showDetails() {
        super.showDetails();
        System.out.println("Credit Limit: " + creditLimit);
    }
}

public class FinanceApp {
    public static void main(String[] args) {

        List<BankProfile> list = new ArrayList<>();

        list.add(new FixedDeposit("FDclass500", "Rahul", 2000, 6));
        list.add(new BusinessAccount("BA900", "Neha", 800, 1500));
        list.add(new BusinessAccount("BA400", "Rohan", 700, 9500));

        for (BankProfile bp : list) {
            System.out.println("\n=== Profile Info ===");
            bp.showDetails();
        }

        try {
            list.get(0).deductMoney(5000);
        } catch (Exception e) {
            System.out.println("\nException: " + e.getMessage());
        }
    }
}
