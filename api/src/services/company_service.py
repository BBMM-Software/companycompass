from src.models.company_model import CompanyModel


def get_company(company_website):
    return CompanyModel("Netrom", company_website, "dummy_data@netrom.ro", "0721000000", "Craiova, RO")


def get_company_description(company_website):
    company = get_company(company_website)
    return (company.company_name + " located in " + company.company_address + ("with the following contact information:"
                                                                               "email (") + company.company_email + "), website (" + company.company_website + ") and phone (" + company.company_phone + ").")
