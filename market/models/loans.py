from enum import Enum
from uuid import UUID

from datetime import datetime

from market.models import DatabaseModel

class LoanRequest(DatabaseModel):
    _type = 'loan_request'

    def __init__(self, user_key, house_id, mortgage_type, banks, description, amount_wanted, status):
        super(LoanRequest, self).__init__()
        assert isinstance(user_key, str)
        assert isinstance(house_id, UUID)
        assert isinstance(mortgage_type, int)
        assert isinstance(banks, list)
        assert isinstance(description, unicode)
        assert isinstance(amount_wanted, int)
        assert isinstance(status, dict)

        self._user_key = user_key
        self._house_id = house_id
        self._mortgage_type = mortgage_type
        self._banks = banks
        self._description = description
        self._amount_wanted = amount_wanted
        self._status = status

    @property
    def user_key(self):
        return self._user_key

    @property
    def house_id(self):
        return self._house_id

    @property
    def mortgage_type(self):
        return self._mortgage_type

    @property
    def banks(self):
        return self._banks

    @property
    def description(self):
        return self._description

    @property
    def amount_wanted(self):
        return self._amount_wanted

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def _is_valid_signer(self, api=None):
        if self._has_signature():
            return self.signer == self.user_key or self.signer in self.banks
        else:
            return False


class Mortgage(DatabaseModel):
    _type = 'mortgage'

    def __init__(self, request_id, house_id, bank, amount, mortgage_type, interest_rate, max_invest_rate, default_rate, duration, risk, investors, status):
        super(Mortgage, self).__init__()
        assert isinstance(request_id, UUID)
        assert isinstance(house_id, UUID)
        assert isinstance(bank, str)
        assert isinstance(amount, int)
        assert isinstance(mortgage_type, int)
        assert isinstance(interest_rate, float)
        assert isinstance(max_invest_rate, float)
        assert isinstance(default_rate, float)
        assert isinstance(duration, int)
        assert isinstance(risk, str)
        assert isinstance(investors, list)
        assert isinstance(status, Enum)

        self._request_id = request_id
        self._house_id = house_id
        self._bank = bank
        self._amount = amount
        self._mortgage_type = mortgage_type
        self._interest_rate = interest_rate
        self._max_invest_rate = max_invest_rate
        self._default_rate = default_rate
        self._duration = duration
        self._risk = risk
        self._investors = investors
        self._status = status

    @property
    def request_id(self):
        return self._request_id

    @property
    def house_id(self):
        return self._house_id

    @property
    def bank(self):
        return self._bank

    @property
    def amount(self):
        return self._amount

    @property
    def mortgage_type(self):
        return self._mortgage_type

    @property
    def interest_rate(self):
        return self._interest_rate

    @property
    def max_invest_rate(self):
        return self._max_invest_rate

    @property
    def default_rate(self):
        return self._default_rate

    @property
    def duration(self):
        return self._duration

    @property
    def risk(self):
        return self._risk

    @property
    def status(self):
        return self._status

    @property
    def investors(self):
        return self._investors

    @status.setter
    def status(self, value):
        self._status = value

    def _is_valid_signer(self, api=None):
        if self._has_signature():
            return self.signer == self.bank
        else:
            return False


class Investment(DatabaseModel):
    _type = 'investment'

    def __init__(self, investor_key, amount, duration, interest_rate, mortgage_id, status):
        super(Investment, self).__init__()
        assert isinstance(investor_key, str)
        assert isinstance(amount, int)
        assert isinstance(duration, int)
        assert isinstance(interest_rate, float)
        assert isinstance(mortgage_id, UUID)
        assert isinstance(status, Enum)

        self._investor_key = investor_key
        self._amount = amount
        self._duration = duration
        self._interest_rate = interest_rate
        self._mortgage_id = mortgage_id
        self._status = status

    @property
    def investor_key(self):
        return self._investor_key

    @property
    def status(self):
        return self._status

    @property
    def amount(self):
        return self._amount

    @property
    def duration(self):
        return self._duration

    @property
    def interest_rate(self):
        return self._interest_rate

    @property
    def mortgage_id(self):
        return self._mortgage_id

    @status.setter
    def status(self, value):
        self._status = value

    def _is_valid_signer(self, api=None):
        if self._has_signature():
            return self.signer == self.investor_key
        else:
            return False


class Campaign(DatabaseModel):
    _type = 'campaign'

    def __init__(self, mortgage_id, amount, end_date, completed):
        super(Campaign, self).__init__()
        assert isinstance(mortgage_id, UUID)
        assert isinstance(amount, int)
        assert isinstance(end_date, datetime)
        assert isinstance(completed, bool)

        self._mortgage_id = mortgage_id
        self._amount = amount
        self._end_date = end_date
        self._completed = completed

    def subtract_amount(self, investment):
        self._amount = self._amount - investment

        if self._amount <= 0:
            self._completed = True

    @property
    def mortgage_id(self):
        return self._mortgage_id

    @property
    def amount(self):
        return self._amount

    @property
    def end_date(self):
        return self._end_date

    @property
    def completed(self):
        return self._completed

    @completed.setter
    def completed(self, value):
        self._completed = value

    def _is_valid_signer(self, api=None):
        if api and self._has_signature():
            mortgage = api.db.get(Mortgage._type, self.mortgage_id)
            if mortgage:
                loan_request = api.db.get(LoanRequest._type, mortgage.request_id)
                if loan_request:
                    return self.signer == loan_request.user_key

        return False

