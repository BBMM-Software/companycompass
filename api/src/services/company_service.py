from src.models.company_model import CompanyModel


def get_company(website):
    return CompanyModel("Netrom", website, "dummy_data@netrom.ro", "0721000000",
                        "Craiova, RO", "Netrom is a software company.")


def get_description(website):
    company = get_company(website)
    return (company.name + " located in " + company.address + ("with the following contact information:"
            "email (") + company.email + "), website (" + company.website + ") and phone (" + company.phone + ")."
            " A brief description of this company is: " + company.description + ".")
