import unittest
from uuid import UUID

from market.api.api import STATUS
from market.api.api import MarketAPI
from market.database.backends import MemoryBackend
from market.database.database import MockDatabase
from market.dispersy.crypto import ECCrypto
from market.models.loans import LoanRequest, Mortgage
from market.models.profiles import BorrowersProfile
from market.models.profiles import Profile
from market.models.user import User
from market.models.loans import Investment
from market.models.role import Role


class APITestSuite(unittest.TestCase):
    def setUp(self):
        self.database = MockDatabase(MemoryBackend())
        self.api = MarketAPI(self.database)
        self.ec = ECCrypto()

        self.payload = {'role': 1, 'first_name': 'Bob', 'last_name': 'Saget', 'email': 'example@example.com', 'iban': 'NL53 INGBB 04027 30393', 'phonenumber': '+3170253719234',
                        'current_postalcode': '2162CD', 'current_housenumber': '22', 'documents_list': []}
        self.payload_investor = {'role': 2, 'first_name': 'Ruby', 'last_name': 'Cue', 'email': 'example1@example.com', 'iban': 'NL53 INGB 04097 30393', 'phonenumber': '+3170253719290'}
        self.payload_bank = {'role': 3}
        self.payload_loan_offer1 = {'role': 1, 'user_key': 'rfghiw98594pio3rjfkhs', 'amount': 1000, 'duration': 24, 'interest_rate': 2.5,
                         'mortgage_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'status': STATUS.PENDING}
        self.payload_loan_offer2 = {'role': 1, 'user_key': 'rfghiw93iuedij3565534', 'amount': 20000, 'duration': 36, 'interest_rate': 3.5,
                         'mortgage_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'status': STATUS.ACCEPTED}
        self.payload_loan_offer3 = {'role': 1, 'user_key': 'r98iw98594p09eikhs', 'amount': 500, 'duration': 12, 'interest_rate': 7.0,
                         'mortgage_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'status': STATUS.REJECTED}
        self.payload_mortgage1 = {'request_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c') , 'bank': '387-sfe4r-ffrw3r-sfew4',
                                  'amount': 150000, 'mortgage_type': 1, 'interest_rate': 5.5, 'max_invest_rate': 10.5, 'default_rate': 2.5,
                                  'duration': 600, 'risk': 'B', 'investors': [], 'status': STATUS.PENDING}
        self.payload_mortgage2 = {'request_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'bank': '89rui-434y-r7y3wf-5ty',
                                  'amount': 140000, 'mortgage_type': 1, 'interest_rate': 4.5, 'max_invest_rate': 8.5,
                                  'default_rate': 6.5, 'duration': 588, 'risk': 'A', 'investors': [], 'status': STATUS.PENDING}
        self.payload_mortgage3 = {'request_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c') , 'bank': '093ru-crh8tyh3-drw8',
                                  'amount': 150000, 'mortgage_type': 0, 'interest_rate': 6.5, 'max_invest_rate': 9.5,
                                  'default_rate': 3.5, 'duration': 360, 'risk': 'A', 'investors': [], 'status': STATUS.ACCEPTED}
        self.payload_investment1 = {'user_key': '67ee-fwr4t-4ewdw3', 'amount': 2000, 'duration': 48, 'interest_rate': 2.5, 'mortgage_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c') , 'status': STATUS.PENDING}
        self.payload_investment2 = {'user_key': '67903dwiejf3', 'amount': 3000, 'duration': 60, 'interest_rate': 4.5, 'mortgage_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'status': STATUS.PENDING}
        self.payload_investment3 = {'user_key': 'kfee-f9874uwe', 'amount': 1000, 'duration': 72, 'interest_rate': 7.5, 'mortgage_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'status': STATUS.PENDING}
        self.payload_loan_request1 = {'postal_code': '1210 BV', 'house_number': '89', 'price': 150000, 'role': 1, 'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c') , 'mortgage_type': 1, 'banks' : [], 'description': unicode('La la la'),
                                      'amount_wanted': 200000}
        self.payload_loan_request2 = {'postal_code': '1011 TV', 'house_number': '55', 'price': 160000, 'role': 1, 'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c') , 'mortgage_type': 1, 'banks': [], 'description': unicode('Ho ho ho merry christmas'),
                                      'amount_wanted': 250000}
        self.payload_loan_request = {'house_id': UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c') , 'mortgage_type': 1, 'banks': [],
                                     'description': unicode('I want to buy a house'), 'amount_wanted': 123456, 'postal_code' : '1111AA', 'house_number' : '11', 'price' : 123456}
        self.payload_mortgage = {'house_id' : UUID('b97dfa1c-e125-4ded-9b1a-5066462c520c'), 'mortgage_type': 1, 'amount' : 123000, 'interest_rate' : 5.5, 'max_invest_rate' : 7.0, 'default_rate' : 9.0, 'duration' : 30, 'risk' : 'hi', 'investors' : []}

    def test_create_user(self):
        user, pub, priv = self.api.create_user()

        # Check if the user object is returned
        self.assertIsInstance(user, User)

        # Check if the public and private keys are valid
        self.assertTrue(self.ec.is_valid_public_bin(pub.decode("HEX")))
        self.assertTrue(self.ec.is_valid_private_bin(priv.decode("HEX")))

    def test_login_user(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Login the user using his private key
        user_login = self.api.login_user(priv)

        # Confirm is the user returned is equal to the user created.
        self.assertEqual(user, user_login)

    def test_create_borrower_profile(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create a borrowers profile
        self.payload['role'] = 1  # borrower
        profile = self.api.create_profile(user, self.payload)

        # Check if the BorrowersProfile object is returned
        self.assertIsInstance(profile, BorrowersProfile)

        # Check if the profile id is saved in the user.
        self.assertEqual(user.profile_id, profile.id)

    def test_create_investor_profile(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create an investors profile
        self.payload['role'] = 2  # investor
        profile = self.api.create_profile(user, self.payload)

        # Check if the Profile object is returned
        self.assertIsInstance(profile, Profile)

        # Check if the profile id is saved in the user.
        self.assertEqual(user.profile_id, profile.id)

    def test_create_bank_profile(self):
        # Create an user
        bank, _, _ = self.api.create_user()

        # Create a bank profile
        self.payload['role'] = 3  # bank
        profile = self.api.create_profile(bank, self.payload)

        # Check if the Profile object is returned
        self.assertTrue(profile)

        # Check if the profile id is empty in the user
        self.assertIsNone(bank.profile_id)

        # Check if the role was set correctly.
        self.assertEqual(self.api.check_role(bank).role, self.payload['role'])

    def test_create_profile_keyerror(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Delete an essential key in the payload
        del self.payload['role']
        profile = self.api.create_profile(user, self.payload)

        # Check if the Profile object is returned
        self.assertFalse(profile)

    def test_load_profile_borrower(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create a borrowers profile
        self.payload['role'] = 1  # borrower
        profile = self.api.create_profile(user, self.payload)

        # Get the profile
        loaded_profile = self.api.load_profile(user)

        # Check if the returned profile is the profile in the database
        self.assertEqual(profile, loaded_profile)
        self.assertIsInstance(profile, BorrowersProfile)

    def test_load_profile_investor(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create a borrowers profile
        self.payload['role'] = 2  # investor
        profile = self.api.create_profile(user, self.payload)

        # Get the profile
        loaded_profile = self.api.load_profile(user)

        # Check if the returned profile is the profile in the database
        self.assertEqual(profile, loaded_profile)
        self.assertIsInstance(profile, Profile)

    def test_load_profile_bank(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create a bank profile
        self.payload['role'] = 3  # bank
        profile = self.api.create_profile(user, self.payload)
        # Get the profile
        loaded_profile = self.api.load_profile(user)

        # Check if the Profile object is returned
        self.assertTrue(profile)
        self.assertIsNone(loaded_profile)
        # Check if the profile id is empty in the user
        self.assertIsNone(user.profile_id)

    # TODO: Fix the test. Fails due to place_loan_offer function
    def test_place_loan_offer_investor(self):
        # Create an user
        investor, pub0, priv0 = self.api.create_user()
        borrower, pub1, priv1 = self.api.create_user()
        bank, pub2, priv2 = self.api.create_user()

        # Create an investor profile
        self.payload['role'] = 2  # investor
        profile = self.api.create_profile(investor, self.payload)
        # Create a borrower profile
        self.payload['role'] = 1 # borrower
        profile2 = self.api.create_profile(borrower, self.payload)
        # Create a bank profile
        self.payload['role'] = 3  # bank
        profile3 = self.api.create_profile(bank, self.payload_bank)

        # Create loan request
        loan_request = self.api.create_loan_request(borrower, self.payload_loan_request2)

        # Set payload
        self.payload_mortgage3['request_id'] = loan_request.id
        self.payload_mortgage3['user_key'] = borrower.id
        self.payload_mortgage3['house_id'] = loan_request.house_id
        self.payload_mortgage3['bank'] = bank.id

        # Let the bank accept the request
        loan_request, mortgage = self.api.accept_loan_request(bank, self.payload_mortgage3)

        # Create loan offer
        self.payload_loan_offer1['user_key'] = borrower.id # set user_key to the investor's public key
        self.payload_loan_offer1['mortgage_id'] = mortgage.id
        loan_offer = self.api.place_loan_offer(investor, self.payload_loan_offer1)

        # Reload borrower
        borrower = self.api._get_user(borrower)

        # Check if the Investment object is returned
        self.assertIsInstance(loan_offer, Investment)

        # Check if the investment id is saved in the user's investment ids list (for borrower ditto)
        self.assertIn(loan_offer.id, investor.investment_ids)
        self.assertIn(loan_offer.id, borrower.investment_ids)

    def test_place_loan_offer_borrower(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create an borrower profile
        self.payload['role'] = 1  # borrower
        self.payload_loan_offer1['role'] = 1 # borrower
        profile = self.api.create_profile(user, self.payload)

        # Create loan offer
        self.payload_loan_offer1['user_key'] = user.id  # set user_key to the borrower's public key
        loan_offer = self.api.place_loan_offer(user, self.payload_loan_offer1)

        # Check if the Profile object is returned
        self.assertIsInstance(profile, Profile)
        # Check if the Investment object is returned
        self.assertFalse(loan_offer)
        # Check if the investment ids list is empty
        self.assertEqual(user.investment_ids, [])

    def test_place_loan_offer_bank(self):
        # Create an user
        user, pub, priv = self.api.create_user()

        # Create an borrower profile
        self.payload['role'] = 3  # bank
        self.payload_loan_offer1['role'] = 3 # bank
        profile = self.api.create_profile(user, self.payload)

        # Create loan offer
        self.payload_loan_offer1['user_key'] = user.id  # set user_key to the bank's public key
        loan_offer = self.api.place_loan_offer(user, self.payload_loan_offer1)

        # Check if True is returned as in role is set.
        self.assertTrue(profile)
        # Check if False is returned from the loan_offer.
        self.assertFalse(loan_offer)
        # Check if the investment ids list is empty
        self.assertEqual(user.investment_ids, [])

    #def test_create_loan_request_borrower(self):
        # Create a user

    # TODO: Fix the test. Fails due to place_loan_offer function
    def test_load_investments(self):
        # Create an user
        investor, _, _ = self.api.create_user()
        borrower, _, _ = self.api.create_user()
        bank, _, _ = self.api.create_user()

        # Create an investor's profile
        self.payload['role'] = 2  # investor
        self.api.create_profile(investor, self.payload)
        # Create a borrower profile
        self.payload['role'] = 1  # borrower
        self.api.create_profile(borrower, self.payload)
        # Create a bank profile
        self.payload['role'] = 3  # bank
        self.api.create_profile(bank, self.payload_bank)

        # Create loan request
        loan_request = self.api.create_loan_request(borrower, self.payload_loan_request2)

        # Set payload
        self.payload_mortgage3['request_id'] = loan_request.id
        self.payload_mortgage3['user_key'] = borrower.id
        self.payload_mortgage3['house_id'] = loan_request.house_id
        self.payload_mortgage3['bank'] = bank.id

        # Let the bank accept the request
        loan_request, mortgage = self.api.accept_loan_request(bank, self.payload_mortgage3)

        # the borrower accepts the mortgage offer
        self.api.accept_mortgage_offer(borrower, {'mortgage_id': mortgage.id})

        # Create loan offers
        self.payload_loan_offer1['user_key'] = borrower.id # set user_key to the investor's public key
        self.payload_loan_offer1['mortgage_id'] = mortgage.id
        loan_offer1 = self.api.place_loan_offer(investor, self.payload_loan_offer1)
        loan_offer2 = self.api.place_loan_offer(investor, self.payload_loan_offer1)
        loan_offer3 = self.api.place_loan_offer(investor, self.payload_loan_offer1)

        # Accept investment 2
        self.api.accept_investment_offer(borrower, {'investment_id': loan_offer2.id})

        # Get the investments
        current_investment, pending_investment = self.api.load_investments(investor)

        # Check if the returned objects are Lists
        self.assertIsInstance(current_investment, list)
        self.assertIsInstance(pending_investment, list)
        # Check if the elements of the lists are Investment-objects
        for investment in current_investment:
            self.assertIsInstance(investment, Investment)
        for investment in pending_investment:
            self.assertIsInstance(investment, Investment)

        # Check if the Investment-objects are saved in the correct list
        self.assertIn(loan_offer1, pending_investment)
        self.assertIn(loan_offer2, current_investment)
        self.assertIn(loan_offer3, pending_investment)

    def test_load_borrowers_offers_mortgage_pending(self):
        # create users
        user, _, _ = self.api.create_user()
        bank1, _, _ = self.api.create_user()
        bank2, _, _ = self.api.create_user()

        # Create a borrower profile
        self.payload['role'] = 1  # borrower
        self.api.create_profile(user, self.payload)

        # Create bank profiles
        self.api.create_profile(bank1, self.payload_bank)
        self.api.create_profile(bank2, self.payload_bank)

        # Create a loan request
        loan_request = self.api.create_loan_request(user, self.payload_loan_request2) # loan request accepted, mortgage pending

        # Set payload
        self.payload_mortgage1['request_id'] = loan_request.id
        self.payload_mortgage2['request_id'] = loan_request.id
        self.payload_mortgage1['user_key'] = user.id
        self.payload_mortgage2['user_key'] = user.id
        self.payload_mortgage1['house_id'] = loan_request.house_id
        self.payload_mortgage2['house_id'] = loan_request.house_id
        self.payload_mortgage1['bank'] = bank1.id
        self.payload_mortgage2['bank'] = bank2.id

        # Let the bank accept the request
        loan_request1, mortgage1 = self.api.accept_loan_request(bank1, self.payload_mortgage1)
        loan_request2, mortgage2 = self.api.accept_loan_request(bank2, self.payload_mortgage2)

        # Get the offers from the database
        offers = self.api.load_borrowers_offers(user)

        # Check if the objects in the returned list are Mortgage-objects
        self.assertIsInstance(offers[0], Mortgage)
        self.assertIsInstance(offers[1], Mortgage)

        # Check if the mortgages in the list are the right ones
        self.assertEqual(offers[0], mortgage1)
        self.assertEqual(offers[1], mortgage2)

    # TODO: Fix the test. Fails due to place_loan_offer function
    def test_load_borrowers_offers_mortgage_accepted(self):
        # create users
        user, _, _ = self.api.create_user()
        investor1, _, _ = self.api.create_user()
        investor2, _, _ = self.api.create_user()
        bank, _, _ = self.api.create_user()

        # Create a borrower's profile
        self.payload['role'] = 1  # borrower
        self.api.create_profile(user, self.payload)
        # Create investors their profiles
        self.payload_investor['role'] = 2  # investor
        self.api.create_profile(investor1, self.payload_investor)
        self.api.create_profile(investor2, self.payload_investor)
        # Create bank's profile
        self.payload['role'] = 3  # bank
        self.api.create_profile(bank, self.payload_bank)

        # Create the loan request
        self.payload_loan_request1['banks'] = [bank.id]
        loan_request = self.api.create_loan_request(user, self.payload_loan_request1)

        # Set payload
        self.payload_mortgage3['request_id'] = loan_request.id
        self.payload_mortgage3['investors'] = [investor1.id, investor2.id]
        self.payload_mortgage3['user_key'] = user.id

        # Let the bank accept the request
        loan_request, mortgage = self.api.accept_loan_request(bank, self.payload_mortgage3)

        # And the borrower accepts the offer
        self.api.accept_mortgage_offer(user, {'mortgage_id': mortgage.id})

        # Create the actual investments.
        self.payload_investment1['mortgage_id'] = mortgage.id
        self.payload_investment2['mortgage_id'] = mortgage.id
        self.payload_investment1['user_key'] = user.id
        self.payload_investment2['user_key'] = user.id
        investment1 = self.api.place_loan_offer(investor1, self.payload_investment1)
        investment2 = self.api.place_loan_offer(investor2, self.payload_investment2)

        # The borrower now accepts the offers.
        #self.api.accept_investment_offer(user, {'investment_id': investment1.id})
        #self.api.accept_investment_offer(user, {'investment_id': investment2.id})

        # Get the offers from the database
        offers = self.api.load_borrowers_offers(user)

        # Check if the objects in the returned list are Mortgage-objects
        self.assertIsInstance(offers[0], Investment)
        self.assertIsInstance(offers[1], Investment)

        # Check if the mortgages in the list are the right ones
        self.assertEqual(offers[0], investment1)
        self.assertEqual(offers[1], investment2)

    def test_check_role_borrower(self):
        # create a user
        user, pub, priv = self.api.create_user()

        # Create a borrower profile
        self.payload['role'] = 1  # borrower
        self.api.create_profile(user, self.payload)

        # Get the role of the user
        role = self.api.check_role(user)

        # Check whether the returned role is indeed the user's role
        self.assertEqual(role.id, user.role_id)
        self.assertEqual(role.role_name, "BORROWER")

    def test_check_role_investor(self):
        # create a user
        user, pub, priv = self.api.create_user()

        # Create a borrower profile
        self.payload['role'] = 2  # investor
        self.api.create_profile(user, self.payload)

        # Get the role of the user
        role = self.api.check_role(user)

        # Check whether the returned role is indeed the user's role
        self.assertEqual(role.id, user.role_id)
        self.assertEqual(role.role_name, "INVESTOR")

    def test_check_role_bank(self):
        # create a user
        user, pub, priv = self.api.create_user()

        # Create a borrower profile
        self.payload['role'] = 3  # bank/financial institution
        self.api.create_profile(user, self.payload)

        # Get the role of the user
        role = self.api.check_role(user)

        # Check whether the returned role is indeed the user's role
        self.assertEqual(role.id, user.role_id)
        self.assertEqual(role.role_name, "FINANCIAL_INSTITUTION")

    def test_load_open_market(self):
        # TODO
        # Clear the database as a start.
        self.database.backend.clear()

        open_market = self.api.load_open_market()
        self.assertFalse(open_market)

    def test_create_loan_request_borrower(self):
        # Create a borrower
        user, pub, priv = self.api.create_user()
        role_id = self.api.db.post('role', Role(user.id, 1))
        user.role_id = role_id
        self.api.db.put('users', user.id, user)

        # Create banks
        bank1, pub1, priv1 = self.api.create_user()
        bank2, pub2, priv2 = self.api.create_user()

        # Create loan request
        self.payload_loan_request['user_key'] = user.id  # Set user_key to the borrower's public key
        self.payload_loan_request['banks'] = [bank1.id, bank2.id]   # Add banks to list
        loan_request_1 = self.api.create_loan_request(user, self.payload_loan_request)

        # Check if the LoanRequest object is returned
        self.assertIsInstance(loan_request_1, LoanRequest)
        # Check if the loan request id is saved in the user's loan_request_id
        self.assertEqual(user.loan_request_ids, [loan_request_1.id])
        # Check if the status is set to pending
        for bank in loan_request_1.status:
            self.assertEqual(loan_request_1.status[bank], STATUS.PENDING)
        # Check if the loan request has been added to the banks' lists
        updated_bank1 = self.api.db.get('users', bank1.id)
        updated_bank2 = self.api.db.get('users', bank2.id)
        self.assertIn(loan_request_1.id, updated_bank1.loan_request_ids)
        self.assertIn(loan_request_1.id, updated_bank2.loan_request_ids)

        # Create another loan request; should not be possible
        self.payload['user_key'] = user.id  # set user_key to the borrower's public key
        loan_request_2 = self.api.create_loan_request(user, self.payload_loan_request)
        self.assertFalse(loan_request_2)

    def test_create_loan_request_investor(self):
        # Create a investor
        user, pub, priv = self.api.create_user()
        role_id = self.api.db.post('role', Role(user.id, 2))
        user.role_id = role_id
        self.api.db.put('users', user.id, user)

        # Create loan request
        self.payload['user_key'] = user.id  # set user_key to the investor's public key
        loan_request = self.api.create_loan_request(user, self.payload_loan_request)

        # Check if the LoanRequest object is returned
        self.assertFalse(loan_request)
        # Check if the loan_request_id is empty
        self.assertEquals(user.loan_request_ids, [])

    def test_create_loan_request_bank(self):
        # Create a bank
        user, pub, priv = self.api.create_user()
        role_id = self.api.db.post('role', Role(user.id, 3))
        user.role_id = role_id
        self.api.db.put('users', user.id, user)

        # Create loan request
        self.payload['user_key'] = user.id  # set user_key to the bank's public key
        self.payload['banks'] = [user]
        loan_request = self.api.create_loan_request(user, self.payload_loan_request)

        # Check if the LoanRequest object is returned
        self.assertFalse(loan_request)
        # Check if the loan_request_id is empty
        self.assertEquals(user.loan_request_ids, [])

    def test_load_all_loan_requests(self):
        # Create borrowers
        borrower1, pub, priv = self.api.create_user()
        role_id = self.api.db.post('role', Role(borrower1.id, 1))
        borrower1.role_id = role_id
        self.api.db.put('users', borrower1.id, borrower1)

        borrower2, pub, priv = self.api.create_user()
        role_id = self.api.db.post('role', Role(borrower2.id, 1))
        borrower2.role_id = role_id
        self.api.db.put('users', borrower2.id, borrower2)

        borrower3, pub, priv = self.api.create_user()
        role_id = self.api.db.post('role', Role(borrower3.id, 1))
        borrower3.role_id = role_id
        self.api.db.put('users', borrower3.id, borrower3)

        # Create a bank
        bank, pub, priv = self.api.create_user()
        role_id = self.api.db.post('role', Role(bank.id, 3))
        bank.role_id = role_id
        self.api.db.put('users', bank.id, bank)

        # Create loan requests
        loan_request_1 = self.api.create_loan_request(borrower1, self.payload_loan_request)
        self.payload_loan_request['banks'] = [bank.id]
        loan_request_2 = self.api.create_loan_request(borrower2, self.payload_loan_request)
        loan_request_3 = self.api.create_loan_request(borrower3, self.payload_loan_request)

        # Accept one loan request TODO Check this
        #self.payload_mortgage['user_key'] = borrower3.id
        #self.payload_mortgage['request_id'] = loan_request_3.id
        #self.api.accept_loan_request(bank, self.payload_mortgage)

        # Check if the loan requests are (not) in the list
        updated_bank = self.api.db.get('users', bank.id)
        pending_loan_requests = self.api.load_all_loan_requests(updated_bank)
        self.assertIsInstance(pending_loan_requests, list)
        self.assertNotIn(loan_request_1.id, pending_loan_requests)
        self.assertIn(loan_request_2.id, pending_loan_requests)
        self.assertIn(loan_request_3.id, pending_loan_requests)

    def test_load_single_loan_request(self):
        # Create a borrower
        borrower, pub0, priv0 = self.api.create_user()
        role_id = self.api.db.post('role', Role(borrower.id, 1))
        borrower.role_id = role_id
        self.api.db.put('users', borrower.id, borrower)

        # Create loan request
        self.payload['user_key'] = borrower.id  # set user_key to the borrower's public key
        loan_request = self.api.create_loan_request(borrower, self.payload_loan_request)
        self.assertIsInstance(loan_request, LoanRequest)
        self.payload_loan_request['loan_request_id'] = loan_request.id

        # Check if the correct loan request has been returned
        loaded_loan_request = self.api.load_single_loan_request(self.payload_loan_request)
        self.assertIsInstance(loaded_loan_request, LoanRequest)
        self.assertEqual(loan_request.id, loaded_loan_request.id)

    def test_accept_loan_request(self):
        # Create a borrower
        borrower, pub0, priv0 = self.api.create_user()
        role_id = self.api.db.post('role', Role(borrower.id, 1))
        borrower.role_id = role_id
        self.api.db.put('users', borrower.id, borrower)

        # Create a bank
        bank, pub1, priv1 = self.api.create_user()
        role_id = self.api.db.post('role', Role(bank.id, 3))
        bank.role_id = role_id
        self.api.db.put('users', bank.id, bank)

        # Create loan request
        self.payload_loan_request['user_key'] = borrower.id  # set user_key to the borrower's public key
        self.payload_loan_request['banks'] = [bank.id, bank.id]
        loan_request = self.api.create_loan_request(borrower, self.payload_loan_request)
        self.assertIsInstance(loan_request, LoanRequest)

        # Set payload
        self.payload_mortgage['user_key'] = borrower.id
        self.payload_mortgage['request_id'] = loan_request.id
        self.payload_mortgage['house_id'] = self.payload_loan_request['house_id']
        self.payload_mortgage['mortgage_type'] = self.payload_loan_request['mortgage_type']

        # Accept the loan request
        accepted_loan_request, mortgage = self.api.accept_loan_request(bank, self.payload_mortgage)

        # Check if the status has changed to accepted
        self.assertEqual(accepted_loan_request.status[bank.id], STATUS.ACCEPTED)
        # Check if the mortgage has been added to the borrower
        updated_borrower = self.api.db.get('users', borrower.id)
        self.assertIn(mortgage.id, updated_borrower.mortgage_ids)
        # Check if the mortgage has been added to the bank
        updated_bank = self.api.db.get('users', bank.id)
        self.assertIn(mortgage.id, updated_bank.mortgage_ids)

    def test_reject_loan_request(self):
        # Create a borrower
        borrower, pub0, priv0 = self.api.create_user()
        role_id = self.api.db.post('role', Role(borrower.id, 1))
        borrower.role_id = role_id
        self.api.db.put('users', borrower.id, borrower)

        # Create banks
        bank1, pub1, priv1 = self.api.create_user()
        bank2, pub2, priv2 = self.api.create_user()

        # Create loan request
        self.payload_loan_request['user_key'] = borrower.id  # set user_key to the borrower's public key
        self.payload_loan_request['banks'] = [bank1.id, bank2.id]
        loan_request = self.api.create_loan_request(borrower, self.payload_loan_request)
        self.assertIsInstance(loan_request, LoanRequest)
        # Check if the loan request has been added to the borrower
        self.assertNotEqual(borrower.loan_request_ids, [])

        self.payload_loan_request['request_id'] = loan_request.id

        # Reject the loan request
        rejected_loan_request1 = self.api.reject_loan_request(bank1, self.payload_loan_request)
        # Check if the status has changed to rejected
        self.assertEqual(rejected_loan_request1.status[bank1.id], STATUS.REJECTED)
        # Check if the loan request hasn't been removed from borrower
        updated_borrower = self.api.db.get('users', borrower.id)
        self.assertTrue(updated_borrower.loan_request_ids)

        rejected_loan_request2 = self.api.reject_loan_request(bank2, self.payload_loan_request)
        # Check if the status has changed to rejected
        self.assertEqual(rejected_loan_request2.status[bank2.id], STATUS.REJECTED)
        # Check if the loan request has been removed from borrower
        updated_borrower = self.api.db.get('users', borrower.id)
        self.assertFalse(updated_borrower.loan_request_ids)
