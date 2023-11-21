def get_saleor_app_identifier(environment_name: str, app_name: str) -> str:
    return f"{environment_name}.{app_name}"
