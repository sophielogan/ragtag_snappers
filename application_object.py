class SnapApplication(object):

    # SNAP CASE AFFILIATION 1-16
    FSAFIL = {
        1: "Eligible member of SNAP case under review and entitled to receive benefits",
        2: "Eligible SNAP participant in another unit, not currently under review (code added by Matematica for use in certain SNAP-CAP units)",
        # no code 3 included 
        4: "Member is ineligible noncitizen and not participating in State-funded SNAP",
        5: "Member not paying/cooperating with child support agency",
        6: "Member is ineligible striker",
        7: "Member is ineligible student",
        8: "Member disqualified for program violation",
        9: "Member ineligible to participate due to disqualification or failure to meet work requirements (work registration, E&T, acceptance of employment, employment status/job availability, voluntary quit/reducing work effort, workfare/comparable workfare)",
        10: "ABAWD time limit exhausted and ABAWD ineligible to participate due to failure to meet ABAWD work requirements, to work at least 20 hours per week, to participate in at least 20 hours per week in qualifying educational training activities, or to participate in workfare",
        11: "Fleeing felon or parole and probation violator",
        # no code for 12 included 
        13: "Convicted drug felon",
        14: "Social Security Number disqualified",
        15: "SSI recipient in California",
        16: "Prisoner in detention center",
        17: "Foster care",
        18: "Member is ineligible noncitizen and participating in State-funded SNAP",
        19: "Individual in the home but not part of SNAP household",
        99: "Unknown"
    }

    AGENCY = {
        1: "Information not reported",
        2: "Incomplete or incorrect information provided; agency not required to verify",
        3: "Information withheld by client (case referred for Intentional Program Violation [IPV] investigation",
        4: "Incorrect information provided by client (case referred for IPV investigation)", 
        # no codes provided for 5 and 6
        7: "Inaccurate information reported by collateral contact",
        8: "Acted on incorrect Federal computer match information not requiring verification (such variance is excluded from error determination but must be recorded)",
        # no code provided for 9 
        10: "Policy incorrectly applied",
        # no code provided for 11 
        12: "Reported information disregarded or not applied",
        # no code provided for 13 
        14: "Agency failed to follow up on inconsistent or incomplete information",
        15: "Agency failed to follow up on impending changes",
        16: "Agency failed to verify required information",
        17: "Computer programming error", 
        18: "Data entry and/or coding error",
        19: "Mass change (error due to problem with computer- generated mass change)",
        20: "Arithmetic computation error", 
        21: "Computer user error",
        99: "Other"
    }

    def __init__(self, application):

        self.app = application

        kwargs = {
            "num_applicants": self.app.iloc[0:16].count(),
            "applicant_status": [
                f"one person is a(n) {self.FSAFIL[status]}"
                for status in self.app.loc["FSAFIL1":"FSAFIL16"] 
                if status > 0
            ],
            "responsbility_of_error": [
                f"{self.AGENCY[error]}"
                for error in self.app.loc["AGENCY1":"AGENCY9"] 
                if error > 0
            ],

            # benefit
            "final_calculated_benefit": self.app.loc["FSBEN"],

            # income 
            "countable_unit_income_from_contributions": self.app.loc["FSCONT"],
            "countable_unit_child_support_payment_income": self.app.loc["FSCSUPRT"],
            "countable_unit_deemed_income": self.app.loc["FSDEEM"],
            "countable_unit_state_diversion_payments": self.app.loc["FSDIVER"],
            "countable_unit_earned_income": self.app.loc["FSEARN"],
            "countable_unit_income_from_educational_grants_and_loans": self.app.loc["FSEDLOAN"],
            "countable_unit_income_from_earned_income_tax_credit": self.app.loc["FSEITC"],
            "countable_unit_energy_assistance_income": self.app.loc["FSENERGY"],
            "countable_unit_foster_care_income": self.app.loc["FSFOSTER"],
            "countable_unit_general_assistance_benefits": self.app.loc["FSGA"],
            "final_gross_countable_unit_income": self.app.loc["FSGRINC"], # if we do regression this might lead to multicollinearity 
            "final_net_countable_unit_income": self.app.loc["FSNETINC"], # if we do regression this might lead to multicollinearity 
            "countable_unit_other_earned_income": self.app.loc["FSOTHERN"],
            "countable_unit_income_from_other_government_benefits": self.app.loc["FSOTHGOV"],
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
            "countable_non_excluded_vehicles_values_under_state_rules": self.app.loc["FSVEHAST"],
            "countable_liquid_assets_under_state_rules": self.app.loc["LIQRESOR"],
            "countable_other_nonliquid_assets_under_state_rules": self.app.loc["OTHNLRES"],
            "reported_liquid_assets": self.app.loc["RAWLQRES"],
            "reported_other_nonliquid_assets": self.app.loc["RAWOTRES"],
            "reported_real_property": self.app.loc["RAWRPROP"],
            "reported_non_excluded_vehicles_value": self.app.loc["RAWVHAST"],
            "countable_real_property_under_state_rules": self.app.loc["REALPROP"],
            # DC often doesn't complete this line item
            # "impact_of_error": [f"the impact was an {impact}" for impact in self.app.loc["E_FINDG1":"E_FINDG9"], if impact>0]
        }

        text = self.generate_text_story(**kwargs)
        print(text)
        # write to csv

    def generate_text_story(
        self,
        num_applicants,
        applicant_status,
        responsbility_of_error,
        final_calculated_benefit,
        # income
        countable_unit_income_from_contributions, # michael
        countable_unit_child_support_payment_income,
        countable_unit_deemed_income, # michael
        countable_unit_state_diversion_payments, # one-time payment for families eligible for tanf 
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
        countable_non_excluded_vehicles_values_under_state_rules, # michael, how is this different from below
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
            f"{num_applicants} individual(s) listed in this SNAP application.",
            f"In the application {''.join(applicant_status)}.",
            f"Based on Quality Control findings the primary cause of variances were {''.join(responsbility_of_error)}.",
            f"The total gross income was: {final_gross_countable_unit_income}, while the net income was: {final_net_countable_unit_income}",
            f"That gross and net income were calculated with multiple factors,",
            f"the reported gross and net income were {reported_gross_countable_unit_income} and {reported_net_countable_unit_income} respectively.",
            f"Income was determined by various inputs, including wages ({countable_unit_wages_and_salaries}),", 
            f"earned income ({countable_unit_earned_income}),",
            f"self employment income ({countable_unit_self_employment_income}),", 
            f"other earned income ({countable_unit_other_earned_income}),", 
            f"income from contributions ({countable_unit_income_from_contributions}),",
            f"child support ({countable_unit_child_support_payment_income}),", 
            f"unearned income ({countable_unit_unearned_income}),",
            f"other unearned income ({countable_unit_other_unearned_income}),",
            f"deemed income ({countable_unit_deemed_income}),",
            f"income from education grants and loans ({countable_unit_income_from_educational_grants_and_loans}),", 
            f"and income for families participating in foster care ({countable_unit_foster_care_income})", 
            f"Some payments may come from employers that are not part of regular wages. For this household, they received",
            f"workers compensation ({countable_unit_workers_compensation_benefits}),",
            f"and wage supplementation ({countable_unit_wage_supplementation_income})",
            f"It also takes any government benefit payments into account, such as earned income tax credit ({countable_unit_income_from_earned_income_tax_credit}),",
            f"energy assistance ({countable_unit_energy_assistance_income}),",
            f"general assistance programs ({countable_unit_general_assistance_benefits}),",
            f"social security ({countable_unit_social_security_income}),",
            f"supplemental security benefits (ssi) (i.e. disability benefits) ({countable_unit_ssi_benefits}),",
            f"temporary assistance for needy families (tanf) ({countable_unit_tanf_payments}),",
            f"unemployment insurance ({countable_unit_unemployment_compensation_benefits}),",
            f"veterans benefits ({countable_unit_veterans_benefits}),",
            f"diversion payment ({countable_unit_state_diversion_payments}),",
            f"and any other government benefits ({countable_unit_income_from_other_government_benefits}).",
            f"A households' assets are also taken into account. The total assets were determined to be {total_countable_assets_under_state_rules}.",
            f"The value of vehicles was determined to be {reported_non_excluded_vehicles_value}.",
            f"It also includes reported liquid assets ({reported_liquid_assets}),", 
            f"countable liquid assets ({countable_liquid_assets_under_state_rules}),", 
            f"reported other nonliquid assets ({reported_other_nonliquid_assets}),",
            f"countable other nonliquid assets ({countable_other_nonliquid_assets_under_state_rules}),",
            f"reported real property ({reported_real_property}),",
            f"and countable real property ({countable_real_property_under_state_rules}).",
        ]

        return " ".join(story), f"***Final Calculated Benefit: {final_calculated_benefit}***"
