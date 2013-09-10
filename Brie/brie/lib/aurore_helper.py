from brie.config import ldap_config
import datetime

class Residences:
    
    @staticmethod
    def get_dn_by_name(user_session, name):
        result = user_session.ldap_bind.search_first(ldap_config.liste_residence_dn, "(cn=" + name + ")")

        if result is None:
            return None
        #end if

        return result.uniqueMember.first()
    #end def

    @staticmethod
    def get_name_by_dn(user_session, dn):
        result = user_session.ldap_bind.search_first(ldap_config.liste_residence_dn, "(uniqueMember=" + dn + ")")

        if result is None:
            return None
        #end if
        
        return result.cn.first()
    #end def
    
    @staticmethod
    def get_residences(user_session):
        return user_session.ldap_bind.search(ldap_config.liste_residence_dn, "(objectClass=groupOfUniqueNames)")
    #end def
#end class

class CotisationComputes:
   
    @staticmethod
    def current_year():
       now = datetime.datetime.now()
       if now.year > 8:
           return now.year + 1

       return now.year
    #end def

    @staticmethod
    def get_available_months(start, end, paid_months = []):
        next_months_available = []

        if start > 12 or end > 12:
            raise Exception("invalid start or end")

        if start > 8 and end > 8:
            next_months_available = range(start, end + 1)
        elif start > 8:
            next_months_available =  range(start, 13) + range(1, end + 1 )
        elif start <= 8 and end < 9:
            next_months_available = range(start, 9)
        else:
            raise Exception("invalid start and end")
        #end if

        if paid_months == []:
            return next_months_available

        print next_months_available
        available_months = [
            month
            for month in next_months_available
            if month not in paid_months
        ]

        return available_months

    #end def

    @staticmethod
    def is_valid_month(month):
        now = datetime.datetime.now()
        if now.month > 8:
            return (month >= now.month and month < 13) or (month >= 1 and month < 9)
        else:
            return month >= now.month and month < 9
        #end if
    #end def

    @staticmethod
    def price_to_pay(year_price, month_price, already_paid, number_months_to_pay):
        
        months_price = number_months_to_pay * month_price
        print "already paid : " + str(already_paid)
        print "months price : " + str(months_price)
        if already_paid + months_price > 50:
            months_price = max(0, 50 - already_paid)

        return months_price
    #end def

#end class
