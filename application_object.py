from config import (
    FSAFIL,
    AGENCY,
    DISCOVERY,
    ERROR_FINDING,
    ELEMENT_VARIANCE,
    NATURE_VARIANCE,
    VARIANCE_VERIFICATION
)


class SnapApplication(object):

    def __init__(self, application):

        self.app = application

        kwargs = {
            "number_of_individuals_listed": self.app.iloc[0:16].count(),
            "applicant_status": [
                f"one person is a(n) {FSAFIL[status]}"
                for status in self.app.loc["FSAFIL1":"FSAFIL16"]
                if status > 0
            ],
            "over_under": [
                ERROR_FINDING[error_type]
                for error_type in self.app.loc["E_FINDG1":"E_FINDG9"]
                if error_type > 0
            ]
            or ["did not state if dollar amount was an over or under issuance"],
            "responsibility_of_error": [
                f"{AGENCY[error]}"
                for error in self.app.loc["AGENCY1":"AGENCY9"]
                if error > 0
            ]
            or ["not listed by QC reviewer"],
            "variance_dollar_amount": [
                f"${str(variance)}"
                for variance in self.app.loc["AMOUNT1":"AMOUNT9"]
                if variance != 0
            ]
            or ["none of the variances were listed"],
            "error_discovered_by": [
                DISCOVERY[discov]
                for discov in self.app.loc["DISCOV1":"DISCOV9"]
                if discov > 0
            ]
            or ["not listed"],
            "element_driving_variance": [
                ELEMENT_VARIANCE[element]
                for element in self.app.loc["ELEMENT1":"ELEMENT9"]
                if element > 0
            ]
            or ["not given"],
            "nature_of_variance": [
                NATURE_VARIANCE[nature]
                for nature in self.app.loc["NATURE1":"NATURE9"]
                if nature > 0
            ]
            or ["the nature of variance is not given"],
            "date_of_occurence": [
                str(date) for date in self.app.loc["OCCDATE1":"OCCDATE9"] if date > 0
            ]
            or ["an unknown date"],
            "variance_verification": [
                VARIANCE_VERIFICATION[verify]
                for verify in self.app.loc["VERIF1":"VERIF9"]
                if verify > 0
            ]
            # or ["if error finding verified reviewer did not state how"]

            or ['demographics'], 
            'tanf_status' : ['Household is categorically eligible for SNAP through TANF categorical eligiblity.' if self.app.loc['TANF_IND'] == 1 else 'Household is not categorically eligible through TANF'][0],
            'num_with_disability' : self.app.loc['DIS1': 'DIS16'].sum(),
            'num_over_60': len([age for age in self.app.loc['AGE1': 'AGE16'] if age >= 60]),
            'homeless': ['Household is homeless' if self.app.loc['HOMEDED'] > 1 else 'Household is not homeless'],
            'shelter_expenses': self.app.loc['FSSLTEXP'],
            'dependent_care_expenses': self.app.loc['FSDEPDED'],
            'child_support_payment': self.app.loc['EXCL_FSCSDED'],
            'utility_amount': self.app.loc['UTIL'],
            'rent' : self.app.loc['RENT'],


            # benefit
            "final_calculated_benefit": self.app.loc["FSBEN"],
            # income
            "countable_unit_income_from_contributions": self.app.loc["FSCONT"],
            "countable_unit_child_support_payment_income": self.app.loc["FSCSUPRT"],
            "countable_unit_deemed_income": self.app.loc["FSDEEM"],
            "countable_unit_state_diversion_payments": self.app.loc["FSDIVER"],
            "countable_unit_earned_income": self.app.loc["FSEARN"],
            "countable_unit_income_from_educational_grants_and_loans": self.app.loc[
                "FSEDLOAN"
            ],
            "countable_unit_income_from_earned_income_tax_credit": self.app.loc[
                "FSEITC"
            ],
            "countable_unit_energy_assistance_income": self.app.loc["FSENERGY"],
            "countable_unit_foster_care_income": self.app.loc["FSFOSTER"],
            "countable_unit_general_assistance_benefits": self.app.loc["FSGA"],
            "final_gross_countable_unit_income": self.app.loc[
                "FSGRINC"
            ],  # if we do regression this might lead to multicollinearity
            "final_net_countable_unit_income": self.app.loc[
                "FSNETINC"
            ],  # if we do regression this might lead to multicollinearity
            "countable_unit_other_earned_income": self.app.loc["FSOTHERN"],
            "countable_unit_income_from_other_government_benefits": self.app.loc[
                "FSOTHGOV"
            ],
            "countable_unit_other_unearned_income": self.app.loc["FSOTHUN"],
            "countable_unit_self_employment_income": self.app.loc["FSSLFEMP"],
            "countable_unit_social_security_income": self.app.loc["FSSOCSEC"],
            "countable_unit_ssi_benefits": self.app.loc["FSSSI"],
            "countable_unit_tanf_payments": self.app.loc["FSTANF"],
            "countable_unit_unearned_income": self.app.loc["FSUNEARN"],
            "countable_unit_unemployment_compensation_benefits": self.app.loc["FSUNEMP"],
            "countable_unit_veterans_benefits": self.app.loc["FSVET"],
            "countable_unit_wages_and_salaries": self.app.loc["FSWAGES"],
            "countable_unit_workers_compensation_benefits": self.app.loc["FSWCOMP"],
            "countable_unit_wage_supplementation_income": self.app.loc["FSWGESUP"],
            "reported_gross_countable_unit_income": self.app.loc["RAWGROSS"],
            "reported_net_countable_unit_income": self.app.loc["RAWNET"],
            # assets
            "total_countable_assets_under_state_rules": self.app.loc["FSASSET"],
            "countable_non_excluded_vehicles_values_under_state_rules": self.app.loc[
                "FSVEHAST"
            ],
            "countable_liquid_assets_under_state_rules": self.app.loc["LIQRESOR"],
            "countable_other_nonliquid_assets_under_state_rules": self.app.loc[
                "OTHNLRES"
            ],
            "reported_liquid_assets": self.app.loc["RAWLQRES"],
            "reported_other_nonliquid_assets": self.app.loc["RAWOTRES"],
            "reported_real_property": self.app.loc["RAWRPROP"],
            "reported_non_excluded_vehicles_value": self.app.loc["RAWVHAST"],
            "countable_real_property_under_state_rules": self.app.loc["REALPROP"],
            # DC often doesn't complete this line item
            # "impact_of_error": [f"the impact was an {impact}" for impact in self.app.loc["E_FINDG1":"E_FINDG9"], if impact>0

        }

        self.application_story = self.generate_text_story(**kwargs)

    def generate_text_story(
        self,
        number_of_individuals_listed,
        applicant_status,
        num_over_60,
        num_with_disability,
        tanf_status,
        homeless,
        shelter_expenses,
        dependent_care_expenses,
        child_support_payment, 
        utility_amount,
        rent,

        responsibility_of_error,
        over_under,
        variance_dollar_amount,
        error_discovered_by,
        element_driving_variance,
        nature_of_variance,
        date_of_occurence,
        variance_verification,
        final_calculated_benefit,
        # income
        countable_unit_income_from_contributions,  # michael
        countable_unit_child_support_payment_income,
        countable_unit_deemed_income,  # michael
        countable_unit_state_diversion_payments,  # one-time payment for families eligible for tanf
        countable_unit_earned_income,
        countable_unit_income_from_educational_grants_and_loans,
        countable_unit_income_from_earned_income_tax_credit,
        countable_unit_energy_assistance_income,
        countable_unit_foster_care_income,
        countable_unit_general_assistance_benefits,
        final_gross_countable_unit_income,
        final_net_countable_unit_income,
        countable_unit_other_earned_income,
        countable_unit_income_from_other_government_benefits,
        countable_unit_other_unearned_income,
        countable_unit_self_employment_income,
        countable_unit_social_security_income,
        countable_unit_ssi_benefits,
        countable_unit_tanf_payments,
        countable_unit_unearned_income,
        countable_unit_unemployment_compensation_benefits,
        countable_unit_veterans_benefits,
        countable_unit_wages_and_salaries,
        countable_unit_workers_compensation_benefits,
        countable_unit_wage_supplementation_income,
        reported_gross_countable_unit_income,
        reported_net_countable_unit_income,
        # assets
        total_countable_assets_under_state_rules,
        countable_non_excluded_vehicles_values_under_state_rules,  # michael, how is this different from below
        countable_liquid_assets_under_state_rules,
        countable_other_nonliquid_assets_under_state_rules,
        reported_liquid_assets,
        reported_other_nonliquid_assets,
        reported_real_property,
        reported_non_excluded_vehicles_value,
        countable_real_property_under_state_rules,
        # impact_of_error,
        # dollar_amount_of_error,
    ):

        story = [
            f"{number_of_individuals_listed} individual(s) listed in this SNAP application. ",

            # comment out code for irrelevant story sections 

            # SNAP QC Result 
            f"In the application {''.join(applicant_status)}. ",
            f"Based on Quality Control the error made faulted the {''.join(responsibility_of_error)}. ",
            f"The error was an {''.join(over_under)} by an amount of {''.join(variance_dollar_amount)}. ",
            f"The error was found by {''.join(error_discovered_by)} and is because of the applicant's {''.join(element_driving_variance)} and {''.join(nature_of_variance)} and occured on {''.join(date_of_occurence)} ",
            f"Information given above was verified by {''.join(variance_verification)}. "

            # Demographics 

            # f"{num_over_60} people in the household over 60.",
            # f"{num_with_disability} people in the household with a disability."
            # f"{tanf_status}."
            # f"{homeless}",
            # f"Household spends {shelter_expenses} on shelter expenses.",
            # f"Household spends {dependent_care_expenses} on dependent care.", 
            # f"Household receives {child_support_payment} in child support.",
            # f"Household pays {utility_amount} in utilities.",
            # f"Household pays {rent} in rent."

            # # Countable Income 
            # f"The total gross income was: {final_gross_countable_unit_income}, while the net income was: {final_net_countable_unit_income}",
            # f"That gross and net income were calculated with multiple factors,",
            # f"the reported gross and net income were {reported_gross_countable_unit_income} and {reported_net_countable_unit_income} respectively. ",
            # f"Income was determined by various inputs, including wages ({countable_unit_wages_and_salaries}),",
            # f"earned income ({countable_unit_earned_income}),",
            # f"self employment income ({countable_unit_self_employment_income}),",
            # f"other earned income ({countable_unit_other_earned_income}),",
            # f"income from contributions ({countable_unit_income_from_contributions}),",
            # f"child support ({countable_unit_child_support_payment_income}),",
            # f"unearned income ({countable_unit_unearned_income}),",
            # f"other unearned income ({countable_unit_other_unearned_income}),",
            # f"deemed income ({countable_unit_deemed_income}),",
            # f"income from education grants and loans ({countable_unit_income_from_educational_grants_and_loans}),",
            # f"and income for families participating in foster care ({countable_unit_foster_care_income})",
            # f"Some payments may come from employers that are not part of regular wages. For this household, they received",
            # f"workers compensation ({countable_unit_workers_compensation_benefits}),",
            # f"and wage supplementation ({countable_unit_wage_supplementation_income})",
            # f"It also takes any government benefit payments into account, such as earned income tax credit ({countable_unit_income_from_earned_income_tax_credit}),",
            # f"energy assistance ({countable_unit_energy_assistance_income}),",
            # f"general assistance programs ({countable_unit_general_assistance_benefits}),",
            # f"social security ({countable_unit_social_security_income}),",
            # f"supplemental security benefits (ssi) (i.e. disability benefits) ({countable_unit_ssi_benefits}),",
            # f"countable payments through temporary assistance for needy families (tanf) ({countable_unit_tanf_payments}),",
            # f"unemployment insurance ({countable_unit_unemployment_compensation_benefits}),",
            # f"veterans benefits ({countable_unit_veterans_benefits}),",
            # f"diversion payment ({countable_unit_state_diversion_payments}),",
            # f"and any other government benefits ({countable_unit_income_from_other_government_benefits}). ",
            # f"A households' assets are also taken into account. The total assets were determined to be {total_countable_assets_under_state_rules}. ",
            # f"The value of vehicles was determined to be {reported_non_excluded_vehicles_value}. ",
            # f"It also includes reported liquid assets ({reported_liquid_assets}),",
            # f"countable liquid assets ({countable_liquid_assets_under_state_rules}),",
            # f"reported other nonliquid assets ({reported_other_nonliquid_assets}),",
            # f"countable other nonliquid assets ({countable_other_nonliquid_assets_under_state_rules}),",
            # f"reported real property ({reported_real_property}),",
            # f"and countable real property ({countable_real_property_under_state_rules}). ",
        ]

        return " ".join(
            story
            + [f"\n *** Final Calculated Benefit: ${final_calculated_benefit} *** "]
        )