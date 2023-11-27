import sys
sys.path.append('./user_account')
import access_enum

""" Access Control Policy function to set the permissions of each resource """
def access_control_policy():
    policy = {
        access_enum.UserRole.CLIENT: {
            access_enum.AccessControl.VIEW: [access_enum.FinancialInstrument.BALANCE, 
                                             access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO, 
                                             access_enum.FinancialInstrument.CONTACT_DETAILS],
            access_enum.AccessControl.MODIFY: []  # no modifying access
        },
        access_enum.UserRole.PREMIUM_CLIENT: {
            access_enum.AccessControl.VIEW: [access_enum.FinancialInstrument.BALANCE, 
                                             access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO, 
                                             access_enum.FinancialInstrument.CONTACT_DETAILS],
            access_enum.AccessControl.MODIFY: [access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO] 
        },
        access_enum.UserRole.FINANCIAL_PLANNER: {
            access_enum.AccessControl.VIEW: [access_enum.FinancialInstrument.BALANCE, 
                                             access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO,
                                             access_enum.FinancialInstrument.CLIENT_INFO,
                                             access_enum.FinancialInstrument.MONEY_MARKET_INSTRUMENTS,
                                             access_enum.FinancialInstrument.PRIV_CONSUMER_INSTRUMENTS],
            access_enum.AccessControl.MODIFY: [access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO] 
        },
        access_enum.UserRole.FINANCIAL_ADVISOR: {
            access_enum.AccessControl.VIEW: [access_enum.FinancialInstrument.BALANCE, 
                                             access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO,
                                             access_enum.FinancialInstrument.CLIENT_INFO,
                                             access_enum.FinancialInstrument.MONEY_MARKET_INSTRUMENTS,
                                             access_enum.FinancialInstrument.PRIV_CONSUMER_INSTRUMENTS],
            access_enum.AccessControl.MODIFY: [access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO] 
        },
        access_enum.UserRole.INVESTMENT_ANALYST: {
            access_enum.AccessControl.VIEW: [access_enum.FinancialInstrument.BALANCE, 
                                             access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO,
                                             access_enum.FinancialInstrument.CLIENT_INFO,
                                             access_enum.FinancialInstrument.PRIV_CONSUMER_INSTRUMENTS,
                                             access_enum.FinancialInstrument.MONEY_MARKET_INSTRUMENTS,
                                             access_enum.FinancialInstrument.DERIVATIVES_TRADING,
                                             access_enum.FinancialInstrument.INTEREST_INSTRUMENTS],
            access_enum.AccessControl.MODIFY: [access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO] 
        },
        access_enum.UserRole.TECH_SUPPORT: {
            access_enum.AccessControl.VIEW: [access_enum.FinancialInstrument.CLIENT_INFO,
                                             access_enum.FinancialInstrument.CLIENT_ACCOUNT],
            access_enum.AccessControl.MODIFY: [access_enum.FinancialInstrument.CLIENT_ACCOUNT] 
        },
        access_enum.UserRole.TELLER: {
            access_enum.AccessControl.VIEW: [access_enum.FinancialInstrument.BALANCE, 
                                             access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO,
                                             access_enum.FinancialInstrument.CLIENT_INFO],
            access_enum.AccessControl.MODIFY: []  # no modifying access
        },
        access_enum.UserRole.COMPLIANCE_OFFICER: {
            access_enum.AccessControl.VIEW: [access_enum.FinancialInstrument.BALANCE, 
                                             access_enum.FinancialInstrument.INVESTMENT_PORTFOLIO,
                                             access_enum.FinancialInstrument.CLIENT_INFO],
            access_enum.AccessControl.MODIFY: []  # no modifying access
        }
    }
    
    return policy

""" Helper function to state the permissions """
def set_role_permission(user_role):
    access = access_control_policy().get(user_role, {})
    view_access = access.get(access_enum.AccessControl.VIEW, [])
    modify_access = access.get(access_enum.AccessControl.MODIFY, [])
    
    print("---------------------------------------")
    print(f"Role Permissions for {user_role.value} ")
    print("---------------------------------------")
    print(f"* VIEW PERMISSIONS: {', '.join(map(lambda x: x.name, view_access))}")
    if modify_access:
        print(f"* MODIFY PERMISSIONS: {', '.join(map(lambda x: x.name, modify_access))}")
    else:
        print("* MODIFY PERMISSIONS: No modify permissions.")