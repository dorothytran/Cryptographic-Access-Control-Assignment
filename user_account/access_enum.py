from enum import *

class UserRole(Enum):
    CLIENT = "CLIENT"
    PREMIUM_CLIENT = "PREMIUM CLIENT"
    FINANCIAL_PLANNER = "FINANCIAL PLANNER"
    FINANCIAL_ADVISOR = "FINANCIAL ADVISOR"
    INVESTMENT_ANALYST = "INVESTMENT ANALYST"
    TECH_SUPPORT = "TECHNICAL SUPPORT"
    TELLER = "TELLER"
    COMPLIANCE_OFFICER = "COMPLIANCE OFFICER"

class AccessControl(Enum):
    VIEW = 1
    MODIFY = 2

class FinancialInstrument(Enum):
    BALANCE = 1
    CLIENT_INFO = 2
    INVESTMENT_PORTFOLIO = 3
    CONTACT_DETAILS = 4
    MONEY_MARKET_INSTRUMENTS = 5
    PRIV_CONSUMER_INSTRUMENTS = 6
    DERIVATIVES_TRADING = 7
    INTEREST_INSTRUMENTS = 8
    CLIENT_ACCOUNT = 9