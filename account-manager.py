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
        self._config=BankConfig()

    def subscribe(self, obs): 
        self._observers.append(obs) 

    def _notify(self, event): 
        for obs in self._observers: 
            obs.update(event) 

    def withdraw(self, amount): 
        if amount <= 0:
            self._notify(f"--> Withdrawal Failed: Amount must be greater than 0 ETB.")
        elif self.balance - amount < self._config.overdraft_limit:
            self._notify(f"--> Withdrawal Failed: withdrawal exceeds overdraft limit.")
        else:
            self.balance -= amount
            self._notify(f"--> {self.owner} withdrew {amount} ETB.succesfully")
            

    def deposit(self, amount):
        if amount <= 0:
            print(f"--> Deposit Failed: Amount must be greater than 0 ETB.")
        else:
            self.balance += amount
            self._notify(f"--> {self.owner} deposited {amount} ETB.succesfully")
@abstractmethod
def statement (self):
    pass


class SavingAccount(Account):

    def Addinterest(self): 
        config = BankConfig()
        interest = self.balance * self._config.interest_rate
        self.balance +=interest
        self._notify(f"--> Interest of {interest} ETB added.")

    def statement(self):
        print(f"Account Statement (Savings):")
        print(f"  Owner:          {self.owner}")
        print(f"  Account Number: {self.number}")
        print(f"  Balance:        {self.balance} ETB")  # Fixed: Use self.balance, not self.__balance
        print(f"  Interest Rate:  {self._config.interest_rate * 100}%")  # Fixed: Displays interest rate cleanly
        print(f"  Overdraft Limit:{self._config.overdraft_limit} ETB")
        print("-" * 35)

class CurrentAccount(Account): 

    def statement(self):
        print(f"Account Statement (Current):")
        print(f"  Owner:          {self.owner}")
        print(f"  Account Number: {self.number}")
        print(f"  Balance:        {self.balance} ETB")  
        print(f"  Overdraft Limit:{self._config.overdraft_limit} ETB")
        print("-" * 35)



class AccountFactory: 
    @staticmethod 
    def create(kind, owner, number, balance=0): 
        if kind == "saving": 
            return SavingAccount(owner, number, balance) 
        if kind == "current": 
            return CurrentAccount(owner, number, balance) 
            
        raise ValueError(f"The account: {kind} you are trying to create is Unknown.") 



acc1 = AccountFactory.create("saving", "Almaz", "1000123456789", 1500)
acc1.subscribe(SMSAlert()) 
acc1.subscribe(AuditLog()) 

acc1.withdraw(3000) 
acc1.Addinterest() 



acc2 = AccountFactory.create("current", "Abebe", "1000987654321", 5000)
acc2.subscribe(SMSAlert()) 
acc2.subscribe(AuditLog()) 

acc2.deposit(500) 


print()
acc1.statement()
acc2.statement()

print()
config1=BankConfig()
config2=BankConfig()
print("singleton:",config1 is config2)