#Refactored Account
from abc import ABC,abstractmethod
class BankConfig: 
    _instance = None 
    def __new__(cls): 
        if cls._instance is None: 
            cls._instance = super().__new__(cls) 
            cls._instance.interest_rate = 0.05 
            cls._instance.overdraft_limit = 1000 
        return cls._instance 


class SMSAlert: 
    def update(self, event): 
        print(f"[SMS] {event}") 
class AuditLog: 
    def update(self, event): 
        print(f"[Log] {event}") 
   
class Account(ABC): 
    def __init__(self,owner,number,balance):
        self.owner=owner
        self.number=number
        self.balance=balance
        self._observers = [] 

    def subscribe(self, obs): 
        self._observers.append(obs) 

    def _notify(self, event): 
        for obs in self._observers: 
            obs.update(event) 

    def withdraw(self, amount): 
        if amount <= 0:
            self._notify(f"--> Withdrawal Failed: Amount must be greater than 0 ETB.")
        elif self.balance - amount < self.overdraft_limit:
            self._notify(f"--> Withdrawal Failed: withdrawal exceeds overdraft limit.")
        else:
            self._balance -= amount
            self._notify(f"--> {self.owner} withdrew {amount} ETB.succesfully")

    def deposit(self, amount):
        if amount <= 0:
            print(f"--> Deposit Failed: Amount must be greater than 0 ETB.")
        else:
            self.balance += amount
            self._notify(f"--> {self.owner} deposited {amount} ETB.succesfully")


class SavingAccount(Account,BankConfig):

    def Addinterest(self): 
        config = BankConfig()
        interest = self.balance * config.interest_rate
        self.balance +=interest
        self._notify(f"--> Interest of {interest} ETB added.")

    def statement(self):
        print(f"Account Statement (Savings):")
        print(f"  Owner:          {self.owner}")
        print(f"  Account Number: {self.account_number}")
        print(f"  Balance:        {self.balance} ETB")  # Fixed: Use self.balance, not self.__balance
        print(f"  Interest Rate:  {self.rate * 100}%")  # Fixed: Displays interest rate cleanly
        print("-" * 35)

class CurrentAccount(Account,BankConfig): 

    def statement(self):
        print(f"Account Statement (Current):")
        print(f"  Owner:          {self.owner}")
        print(f"  Account Number: {self.account_number}")
        print(f"  Balance:        {self.balance} ETB")  
        print(f"  Overdraft Limit:{self.overdraft} ETB")
        print("-" * 35)



class AccountFactory: 
    @staticmethod 
    def create(kind, owner, number, balance=0): 
        if kind == "saving": 
            return SavingAccount(owner, number, balance) 
        if kind == "current": 
            return CurrentAccount(owner, number, balance) 
            
        raise ValueError(f"The account: {kind} you are trying to create is Unknown.") 



acc1 = AccountFactory.create("saving", "Almaz", "CBE-1", 1500)

acc1.withdraw(5000) 
acc1.Addinterest() 
acc1.subscribe(SMSAlert()) 
acc1.subscribe(AuditLog()) 


acc2 = AccountFactory.create("current", "Abebe", "CBE-2", 5000)

acc2.deposit(500) 
acc2.subscribe(SMSAlert()) 
acc2.subscribe(AuditLog()) 

print()
acc1.statement()
acc2.statement()
print()
config1=BankConfig()
config2=BankConfig()
print("singleton:",config1 is config2)













'''from abc import ABC,abstractmethod 
class Account(ABC):
    def __init__(self, owner, account_number, balance=0):
        self._owner = owner 
        self._account_number = account_number                      
        self._balance = float(balance)                

    @property
    def balance(self):
        return self._balance
    @property
    def owner(self):
        return self._owner
    @property
    def account_number(self):
        return self._account_number

    def deposit(self, amount):
        if amount <= 0:
            print(f"--> Deposit Failed: Amount must be greater than 0 ETB.")
        else:
            self._balance += amount
            print(f"--> Successfully deposited {amount} ETB.")

    @abstractmethod
    def withdraw(self, amount):
       pass
    @abstractmethod
    def statement(self):
        pass

#class AddInterest(Account):
    # @abstractmethod
    # def add_interest(self): 
        # Safely adds interest using the public deposit method
       # interest = self.balance * self.rate
        #self.deposit(interest) 

class SavingsAccount(Account): 
    def __init__(self, owner, account_number, balance=0, rate=0.05):
        super().__init__(owner, account_number, balance) 
        self.rate = float(rate) 

    def Addinterest(self): 
        interest = self.balance * self.rate
        self._balance +=interest
        print(f"--> Interest of {interest} ETB added.")
        return interest

    def withdraw(self, amount):
        if amount <= 0:
            print(f"--> Withdrawal Failed: Amount must be greater than 0 ETB.")
        elif amount > self._balance:
            print(f"--> Withdrawal Failed: Insufficient funds! Overdraft rejected.")
        else:
            self._balance -= amount
            print(f"--> Successfully withdrew {amount} ETB.")


    def statement(self):
        print(f"Account Statement (Savings):")
        print(f"  Owner:          {self._owner}")
        print(f"  Account Number: {self._account_number}")
        print(f"  Balance:        {self._balance} ETB")  # Fixed: Use self.balance, not self.__balance
        print(f"  Interest Rate:  {self.rate * 100}%")  # Fixed: Displays interest rate cleanly
        print("-" * 35)


class CurrentAccount(Account): 
    def __init__(self, owner, account_number, balance=0, overdraft=1000): 
        super().__init__(owner, account_number, balance) 
        self._overdraft = float(overdraft) 

    @property
    def overdraft(self):
        return self._overdraft

    
    
    def withdraw(self, amount):
        if amount <= 0:
            print(f"--> Withdrawal Failed: Amount must be greater than 0 ETB.")
        elif self._balance - amount < self._overdraft:
            print(f"--> Withdrawal Failed: withdrawal exceeds overdraft limit.")
        else:
            self._balance -= amount
            print(f"--> Successfully withdrew {amount} ETB.")

    def statement(self):
        print(f"Account Statement (Current):")
        print(f"  Owner:          {self._owner}")
        print(f"  Account Number: {self._account_number}")
        print(f"  Balance:        {self._balance} ETB")  
        print(f"  Overdraft Limit:{self._overdraft} ETB")
        print("-" * 35)


if __name__ == "__main__":
    account1=SavingsAccount("Dawit", "100012345678", 1000,rate=0.05)         
    account2=CurrentAccount ("Beza", "100087654321", 3000, overdraft=1000) 
      
print( "-----------------------------------" )
print   (" Running Transactions on Savings ---")

account1.deposit(500)
account1.Addinterest() 
account1.statement() 

print("--- Running Transactions on current ---")
account2.withdraw(2500) 
account2.statement()'''

    
    
