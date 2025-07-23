#!/bin/bash
# OpenVPN client management script: add, revoke, and view clients via CLI args

function newClient() {
	CLIENT="$1"
	if [[ -z "$CLIENT" ]]; then
		echo "Error: No client name provided."
		echo "Usage: $0 add <client_name>"
		exit 1
	fi
	if ! [[ $CLIENT =~ ^[a-zA-Z0-9_-]+$ ]]; then
		echo "Error: Client name must be alphanumeric, underscore, or dash."
		exit 1
	fi
	CLIENTEXISTS=$(tail -n +2 /etc/openvpn/easy-rsa/pki/index.txt | grep -c -E "/CN=$CLIENT\$")
	if [[ $CLIENTEXISTS == '1' ]]; then
		echo "The specified client CN was already found in easy-rsa, please choose another name."
		exit 1
	else
		cd /etc/openvpn/easy-rsa/ || return
		EASYRSA_CERT_EXPIRE=3650 ./easyrsa --batch build-client-full "$CLIENT" nopass
		echo "Client $CLIENT added."
	fi

	# Home directory of the user, where the client configuration will be written
	if [ -e "/home/${CLIENT}" ]; then
		homeDir="/home/${CLIENT}"
	elif [ "${SUDO_USER}" ]; then
		if [ "${SUDO_USER}" == "root" ]; then
			homeDir="/root"
		else
			homeDir="/home/${SUDO_USER}"
		fi
	else
		homeDir="/root"
	fi

	# Determine if we use tls-auth or tls-crypt
	if grep -qs "^tls-crypt" /etc/openvpn/server.conf; then
		TLS_SIG="1"
	elif grep -qs "^tls-auth" /etc/openvpn/server.conf; then
		TLS_SIG="2"
	fi

	# Generates the custom client.ovpn
	cp /etc/openvpn/client-template.txt "$homeDir/$CLIENT.ovpn"
	{
		echo "<ca>"
		cat "/etc/openvpn/easy-rsa/pki/ca.crt"
		echo "</ca>"

		echo "<cert>"
		awk '/BEGIN/,/END CERTIFICATE/' "/etc/openvpn/easy-rsa/pki/issued/$CLIENT.crt"
		echo "</cert>"

		echo "<key>"
		cat "/etc/openvpn/easy-rsa/pki/private/$CLIENT.key"
		echo "</key>"

		case $TLS_SIG in
		1)
			echo "<tls-crypt>"
			cat /etc/openvpn/tls-crypt.key
			echo "</tls-crypt>"
			;;
		2)
			echo "key-direction 1"
			echo "<tls-auth>"
			cat /etc/openvpn/tls-auth.key
			echo "</tls-auth>"
			;;
		esac
	} >>"$homeDir/$CLIENT.ovpn"

	echo "The configuration file has been written to $homeDir/$CLIENT.ovpn."
	echo "Download the .ovpn file and import it in your OpenVPN client."

	exit 0
}

function revokeClient() {
	CLIENT="$1"
	if [[ -z "$CLIENT" ]]; then
		echo "Error: No client name provided."
		echo "Usage: $0 revoke <client_name>"
		exit 1
	fi
	NUMBEROFCLIENTS=$(tail -n +2 /etc/openvpn/easy-rsa/pki/index.txt | grep -c "^V")
	if [[ $NUMBEROFCLIENTS == '0' ]]; then
		echo "You have no existing clients!"
		exit 1
	fi
	CLIENT_EXISTS=$(tail -n +2 /etc/openvpn/easy-rsa/pki/index.txt | grep -c "^V.*CN=$CLIENT$")
	if [[ $CLIENT_EXISTS == '0' ]]; then
		echo "Client $CLIENT not found or already revoked."
		exit 1
	fi
	cd /etc/openvpn/easy-rsa/ || return
	./easyrsa --batch revoke "$CLIENT"
	EASYRSA_CRL_DAYS=3650 ./easyrsa gen-crl
	rm -f /etc/openvpn/crl.pem
	cp /etc/openvpn/easy-rsa/pki/crl.pem /etc/openvpn/crl.pem
	chmod 644 /etc/openvpn/crl.pem
	find /home/ -maxdepth 2 -name "$CLIENT.ovpn" -delete
	rm -f "/root/$CLIENT.ovpn"
	sed -i "/^$CLIENT,.*/d" /etc/openvpn/ipp.txt
	cp /etc/openvpn/easy-rsa/pki/index.txt{,.bk}
	echo "Certificate for client $CLIENT revoked."
}

function viewClient() {
	CLIENT="$1"
	if [[ -z "$CLIENT" ]]; then
		echo "Error: No client name provided."
		echo "Usage: $0 view <client_name>"
		exit 1
	fi
	NUMBEROFCLIENTS=$(tail -n +2 /etc/openvpn/easy-rsa/pki/index.txt | grep -c "^V")
	if [[ $NUMBEROFCLIENTS == '0' ]]; then
		echo "You have no existing clients!"
		exit 1
	fi
	CLIENT_EXISTS=$(tail -n +2 /etc/openvpn/easy-rsa/pki/index.txt | grep -c "^V.*CN=$CLIENT$")
	if [[ $CLIENT_EXISTS == '0' ]]; then
		echo "Client $CLIENT not found or revoked."
		exit 1
	fi

    # Home directory of the user, where the client configuration will be written
	if [ -e "/home/${CLIENT}" ]; then
		homeDir="/home/${CLIENT}"
	elif [ "${SUDO_USER}" ]; then
		if [ "${SUDO_USER}" == "root" ]; then
			homeDir="/root"
		else
			homeDir="/home/${SUDO_USER}"
		fi
	else
		homeDir="/root"
	fi

	if [ -e "$homeDir/$CLIENT.ovpn" ]; then
		OVPN_PATH="$homeDir/$CLIENT.ovpn"
	else
		echo "Could not find .ovpn file for $CLIENT."
		exit 1
	fi
	echo "Contents of $OVPN_PATH:"
	cat "$OVPN_PATH"
}

# CLI argument parsing
if [[ $# -lt 1 ]]; then
	echo "Usage: $0 <add|revoke|view> <client_name>"
	exit 1
fi

COMMAND="$1"
shift
case "$COMMAND" in
	add)
		newClient "$@"
		;;
	revoke)
		revokeClient "$@"
		;;
	view)
		viewClient "$@"
		;;
	*)
		echo "Unknown command: $COMMAND"
		echo "Usage: $0 <add|revoke|view> <client_name>"
		exit 1
		;;
esac