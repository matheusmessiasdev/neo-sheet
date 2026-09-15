# accounts/schema_hooks.py


def fix_djoser_security(result, generator, request, public, **kwargs):
    """
    Corrige a segurança dos endpoints do Djoser no schema OpenAPI gerado,
    já que o Djoser não expõe permissões por ação para o drf-spectacular.

    Também renomeia o esquema de segurança 'jwtAuth' para 'BearerAuth' para
    manter consistência com o SIMPLE_JWT.AUTH_HEADER_TYPES = ('Bearer',).
    """
    paths = result.get('paths', {})

    BEARER = [{'BearerAuth': []}]
    BEARER_OR_ANON = [{'BearerAuth': []}, {}]

    # ========== ENDPOINTS PÚBLICOS (sem autenticação) ==========
    public_paths = {
        '/api/v1/auth/jwt/create/': ['post'],
        '/api/v1/auth/jwt/refresh/': ['post'],
        '/api/v1/auth/jwt/verify/': ['post'],
        '/api/v1/auth/users/': ['post'],  # registro
        '/api/v1/auth/users/activation/': ['post'],
        '/api/v1/auth/users/resend_activation/': ['post'],
        '/api/v1/auth/users/reset_password/': ['post'],
        '/api/v1/auth/users/reset_password_confirm/': ['post'],
        '/api/v1/auth/users/reset_username/': ['post'],
        '/api/v1/auth/users/reset_username_confirm/': ['post'],
        '/api/v1/dice/rolls/base/': ['post'],
        '/api/v1/profiles/blank_profile/': ['get'],
        '/api/v1/profiles/generic_sheet/': ['get'],
        '/api/v1/profiles/profile_template/': ['get'],
    }

    # ========== ENDPOINTS PROTEGIDOS (exigem autenticação) ==========
    protected_paths = {
        '/api/v1/auth/users/': ['get'],
        '/api/v1/auth/users/{id}/': ['get', 'put', 'patch', 'delete'],
        '/api/v1/auth/users/me/': ['get', 'put', 'patch', 'delete'],
        '/api/v1/auth/users/set_password/': ['post'],
        '/api/v1/auth/users/set_username/': ['post'],
        '/api/v1/profiles/': ['post'],
        '/api/v1/profiles/{system_id}/': ['patch', 'delete'],
    }

    # ========== ENDPOINTS COM AUTENTICAÇÃO OPCIONAL ==========
    optional_paths = {
        '/api/v1/profiles/': ['get'],
        '/api/v1/profiles/{system_id}/': ['get'],
        '/api/v1/profiles/{system_id}/sheet/': ['get'],
        '/api/v1/schema/': ['get'],
    }

    # Aplica security = [] nos públicos
    for path, methods in public_paths.items():
        if path in paths:
            for method in methods:
                if method in paths[path]:
                    paths[path][method]['security'] = []

    # Aplica BearerAuth nos protegidos
    for path, methods in protected_paths.items():
        if path in paths:
            for method in methods:
                if method in paths[path]:
                    paths[path][method]['security'] = BEARER

    # Aplica BearerAuth OU anônimo nos opcionais
    for path, methods in optional_paths.items():
        if path in paths:
            for method in methods:
                if method in paths[path]:
                    paths[path][method]['security'] = BEARER_OR_ANON

    components = result.get('components', {})
    schemes = components.get('securitySchemes', {})
    if 'jwtAuth' in schemes:
        schemes['BearerAuth'] = schemes.pop('jwtAuth')

    return result
