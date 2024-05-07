import binascii
import dataclasses
from enum import IntEnum
from typing import Optional, Union

from ledgerwallet.client import LedgerClient
from ledgerwallet.params import Bip32Path
from ledgerwallet.transport import enumerate_devices
from stellar_sdk import (
    Keypair,
    TransactionEnvelope,
    DecoratedSignature,
    FeeBumpTransactionEnvelope,
)
from stellar_sdk.xdr import HashIDPreimage, EnvelopeType

__all__ = [
    "get_default_client",
    "DeviceNotFoundException",
    "DEFAULT_KEYPAIR_INDEX",
    "Ins",
    "P1",
    "P2",
    "SW",
    "AppInfo",
    "StrLedger",
]

DEFAULT_KEYPAIR_INDEX = 0


class Ins(IntEnum):
    """Instruction enum for APDU commands."""

    GET_PK = 0x02
    SIGN_TX = 0x04
    GET_CONF = 0x06
    SIGN_HASH = 0x08
    SIGN_SOROBAN_AUTHORIZATION = 0x0A


class P1(IntEnum):
    """P1 parameter enum for APDU commands."""

    NONE = 0x00
    FIRST_APDU = 0x00
    MORE_APDU = 0x80


class P2(IntEnum):
    """P2 parameter enum for APDU commands."""

    NON_CONFIRM = 0x00
    CONFIRM = 0x01
    LAST_APDU = 0x00
    MORE_APDU = 0x80


class SW(IntEnum):
    """Status Words enum for APDU responses.

    See https://github.com/lightsail-network/app-stellar/blob/develop/docs/COMMANDS.md#status-words
    """

    # Status word for denied by user.
    DENY = 0x6985
    # Status word for hash signing model not enabled.
    TX_HASH_SIGNING_MODE_NOT_ENABLED = 0x6C66
    # Status word for data too large.
    SW_REQUEST_DATA_TOO_LARGE = 0x6C67
    # Status word for success.
    OK = 0x9000


class DeviceNotFoundException(Exception):
    """Exception raised when no Ledger device is found."""

    pass


def get_default_client() -> "StrLedger":
    """Get the default Ledger client.

    Returns:
        StrLedger: The default Ledger client instance.

    Raises:
        DeviceNotFoundException: If no Ledger device is found.
    """
    devices = enumerate_devices()
    if len(devices) == 0:
        raise DeviceNotFoundException
    client = LedgerClient(devices[0])
    return StrLedger(client)


@dataclasses.dataclass
class AppInfo:
    """App configuration information."""

    version: str
    """The version of the app."""
    hash_signing_enabled: bool
    """Whether hash signing is enabled."""


class StrLedger:
    """Stellar Ledger client class."""

    def __init__(self, client: LedgerClient) -> None:
        """Initialize the Stellar Ledger client.

        Args:
            client (LedgerClient): The Ledger client instance.
        """
        self.client = client

    def get_app_info(self) -> AppInfo:
        """Get the app configuration information.

        Returns:
            AppInfo: The app configuration information.
        """
        data = self.client.apdu_exchange(
            ins=Ins.GET_CONF, p1=P1.FIRST_APDU, p2=P2.LAST_APDU
        )
        hash_signing_enabled = bool(data[0])
        version = f"{data[1]}.{data[2]}.{data[3]}"
        return AppInfo(version=version, hash_signing_enabled=hash_signing_enabled)

    def get_keypair(
        self,
        keypair_index: int = DEFAULT_KEYPAIR_INDEX,
        confirm_on_device: bool = False,
    ) -> Keypair:
        """Get the public key for the specified keypair index.

        Args:
            keypair_index (int): The keypair index (default is 0).
            confirm_on_device (bool): Whether to confirm the action on the device (default is False).

        Returns:
            Keypair: The keypair instance.
        """
        path = Bip32Path.build(f"44'/148'/{keypair_index}'")
        data = self.client.apdu_exchange(
            ins=Ins.GET_PK,
            data=path,
            p1=P1.NONE,
            p2=P2.CONFIRM if confirm_on_device else P2.NON_CONFIRM,
        )
        keypair = Keypair.from_raw_ed25519_public_key(data)
        return keypair

    def sign_transaction(
        self,
        transaction_envelope: Union[TransactionEnvelope, FeeBumpTransactionEnvelope],
        keypair_index: int = DEFAULT_KEYPAIR_INDEX,
    ) -> None:
        """Sign a transaction envelope.

        Args:
            transaction_envelope (Union[TransactionEnvelope, FeeBumpTransactionEnvelope]): The transaction envelope to sign.
            keypair_index (int): The keypair index (default is 0).
        """
        sign_data = transaction_envelope.signature_base()
        keypair = self.get_keypair(keypair_index=keypair_index)

        path = Bip32Path.build(f"44'/148'/{keypair_index}'")
        payload = path + sign_data
        signature = self._send_payload(Ins.SIGN_TX, payload)
        assert isinstance(signature, bytes)
        decorated_signature = DecoratedSignature(keypair.signature_hint(), signature)
        transaction_envelope.signatures.append(decorated_signature)

    def sign_hash(
        self,
        transaction_hash: Union[str, bytes],
        keypair_index: int = DEFAULT_KEYPAIR_INDEX,
    ) -> bytes:
        """Sign a transaction hash.

        Args:
            transaction_hash (Union[str, bytes]): The transaction hash to sign.
            keypair_index (int): The keypair index (default is 0).

        Returns:
            bytes: The signature.
        """
        if isinstance(transaction_hash, str):
            transaction_hash = binascii.unhexlify(transaction_hash)
        path = Bip32Path.build(f"44'/148'/{keypair_index}'")
        payload = path + transaction_hash

        data = self.client.apdu_exchange(
            ins=Ins.SIGN_HASH, data=payload, p1=P1.FIRST_APDU, p2=P2.LAST_APDU
        )
        return data

    def sign_soroban_authorization(
        self,
        soroban_authorization: Union[str, bytes, HashIDPreimage],
        keypair_index: int = DEFAULT_KEYPAIR_INDEX,
    ) -> bytes:
        """Sign a Soroban authorization.

        Args:
            soroban_authorization (Union[str, bytes, HashIDPreimage]): The Soroban authorization to sign.
            keypair_index (int): The keypair index (default is 0).

        Returns:
            bytes: The signature.

        Raises:
            ValueError: If the Soroban authorization type is invalid.
        """
        if isinstance(soroban_authorization, str):
            soroban_authorization = HashIDPreimage.from_xdr(soroban_authorization)
        if isinstance(soroban_authorization, bytes):
            soroban_authorization = HashIDPreimage.from_xdr_bytes(soroban_authorization)

        if (
            soroban_authorization.type
            != EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION
        ):
            raise ValueError(
                f"Invalid type, expected {EnvelopeType.ENVELOPE_TYPE_SOROBAN_AUTHORIZATION}, but got {soroban_authorization.type}"
            )
        path = Bip32Path.build(f"44'/148'/{keypair_index}'")
        payload = path + soroban_authorization.to_xdr_bytes()
        signature = self._send_payload(Ins.SIGN_SOROBAN_AUTHORIZATION, payload)
        assert isinstance(signature, bytes)
        return signature

    def _send_payload(self, ins: Ins, payload) -> Optional[Union[int, bytes]]:
        """Send a payload to the Ledger device.

        Args:
            ins (Ins): The instruction for the APDU command.
            payload: The payload to send.

        Returns:
            Optional[Union[int, bytes]]: The response from the Ledger device.
        """
        chunk_size = 255
        first = True
        while payload:
            if first:
                p1 = P1.FIRST_APDU
                first = False
            else:
                p1 = P1.MORE_APDU

            size = min(len(payload), chunk_size)
            if size != len(payload):
                p2 = P2.MORE_APDU
            else:
                p2 = P2.LAST_APDU

            resp = self.client.apdu_exchange(ins, payload[:size], p1, p2)
            if resp:
                return resp
            payload = payload[size:]
