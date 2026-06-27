"""
Role and Mapper API Tables 
"""

from enum import Enum as pyEnum

class RoleEnum(pyEnum):
    baker = "baker"  # Bakers in the workshop
    sales = "sales"  # Sales Department
    hr = "hr"  # Human Resources
    cofounder = "cofounder"  # Company Co-founder
    admin = "admin"  # Admin role for system management

# Actual source: role -> permitted Qdrant collections
ROLE_TO_QDRANT_COLLECTIONS: dict[RoleEnum, list[str]] = {
    RoleEnum.baker: ["recipes_procedures"],
    RoleEnum.hr: ["confidential"],
    RoleEnum.cofounder: ["cofounder_doc"],
    RoleEnum.sales: [],  # Sales dont have access to Qdrant, just to PostGres
    RoleEnum.admin: ["recipes_procedures", "confidential", "cofounder_doc"],
}

# Actual source: role -> acces to Postgres (Agent SQL)
ROLE_HAS_SQL_ACCESS: dict[RoleEnum, bool] = {
    RoleEnum.baker: False,
    RoleEnum.hr: False,
    RoleEnum.cofounder: False,
    RoleEnum.sales: True,
    RoleEnum.admin: True,
}