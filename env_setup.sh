 #!/usr/bin/env bash

read -p "Your environment's base FQDN (e.g. example.bmp.ovhgoldorack.ovh): " FQDN_ENV

read -p 'Keycloak client ID: ' KC_CLIENT_ID
read -srp 'Keycloak client secret: ' KC_CLIENT_SECRET && echo

read -p 'Keycloak username: ' KC_USERNAME_INPUT
read -srp 'Keycloak password: ' KC_PASSWORD_INPUT && echo

read -p 'Openstack Project ID (not the name): ' PROJECT_ID

printf "\n\nHere is your configuration, paste it to your shell or use the generate openrc.sh file\n\n"
cat << EOM
export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3
export OS_AUTH_URL="https://keystone.${FQDN_ENV}"
export OS_AUTH_TYPE="v3oidcpassword"
export OS_PROTOCOL="openid"
export OS_IDENTITY_PROVIDER="keycloak-admin"
export OS_CLIENT_ID="$KC_CLIENT_ID"
export OS_CLIENT_SECRET="$KC_CLIENT_SECRET"
export OS_DISCOVERY_ENDPOINT="https://admin.keycloak.${FQDN_ENV}/realms/master/.well-known/openid-configuration"
export OS_USERNAME="$KC_USERNAME_INPUT"
export OS_PASSWORD="$KC_PASSWORD_INPUT"
export OS_PROJECT_ID="$PROJECT_ID"
EOM

echo "#!/usr/bin/env bash

export OS_INTERFACE=public
export OS_IDENTITY_API_VERSION=3
export OS_AUTH_URL="https://keystone.${FQDN_ENV}"
export OS_AUTH_TYPE="v3oidcpassword"
export OS_PROTOCOL="openid"
export OS_IDENTITY_PROVIDER="keycloak-admin"
export OS_CLIENT_ID="$KC_CLIENT_ID"
export OS_CLIENT_SECRET="$KC_CLIENT_SECRET"
export OS_DISCOVERY_ENDPOINT="https://admin.keycloak.${FQDN_ENV}/realms/master/.well-known/openid-configuration"
export OS_USERNAME="$KC_USERNAME_INPUT"
export OS_PASSWORD="$KC_PASSWORD_INPUT"
export OS_PROJECT_ID="$PROJECT_ID > $PROJECT_ID."-openrc.sh"