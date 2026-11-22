
"""A simplified income tax calculator with secure PAN encryption and XML parsing."""

import os
import re

from defusedxml import ElementTree
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


STANDARD_DEDUCTION_NEW = 75000
STANDARD_DEDUCTION_OLD = 50000
REBATE_LIMIT_NEW = 1200000
CESS = 0.04

OLD_SLABS = [
    (250000, 0.00),
    (500000, 0.05),
    (1000000, 0.20),
    (float("inf"), 0.30),
]

NEW_SLABS = [
    (400000, 0.00),
    (800000, 0.05),
    (1200000, 0.10),
    (1600000, 0.15),
    (2000000, 0.20),
    (2400000, 0.25),
    (float("inf"), 0.30),
]


def calculate_progressive_tax(taxable_income, slabs, lower_limit=0):
    """Calculate tax progressively using the supplied tax slabs."""
    total_tax = 0
    previous_limit = lower_limit

    for limit, rate in slabs:
        if taxable_income > previous_limit:
            slab_income = min(taxable_income, limit) - previous_limit
            total_tax += slab_income * rate

        previous_limit = max(previous_limit, limit)

        if taxable_income <= limit:
            break

    return total_tax


def calculate_new_regime_tax(salary):
    """Calculate simplified new-regime tax including cess and rebate."""
    taxable_income = max(0, salary - STANDARD_DEDUCTION_NEW)

    tax_amount = calculate_progressive_tax(
        taxable_income,
        NEW_SLABS
    )

    if taxable_income <= REBATE_LIMIT_NEW:
        tax_amount = 0

    return int(tax_amount * (1 + CESS))


def get_basic_exemption(age):
    """Return the basic exemption limit based on the taxpayer's age."""
    if age >= 80:
        return 500000

    if age >= 60:
        return 300000

    return 250000


def calculate_old_regime_tax(salary, age, deductions):
    """Calculate simplified old-regime tax after eligible deductions."""
    total_deductions = sum(deductions.values())

    taxable_income = max(
        0,
        salary - STANDARD_DEDUCTION_OLD - total_deductions
    )

    exemption_limit = get_basic_exemption(age)

    tax_amount = calculate_progressive_tax(
        taxable_income,
        OLD_SLABS,
        exemption_limit
    )

    return int(tax_amount * (1 + CESS))


def choose_better_regime(salary, age, deductions):
    """Return the regime that results in the lower calculated tax."""
    new_tax = calculate_new_regime_tax(salary)
    old_tax = calculate_old_regime_tax(salary, age, deductions)

    if new_tax <= old_tax:
        return "new"

    return "old"


def is_valid_pan(pan):
    """Check whether the complete PAN string follows the expected format."""
    if not isinstance(pan, str):
        return False

    return bool(re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan))


def get_pan_key():
    """Read and validate the AES encryption key from the environment."""
    key_hex = os.environ.get("PAN_KEY")

    if not key_hex:
        raise ValueError("PAN_KEY environment variable is not set")

    try:
        key = bytes.fromhex(key_hex)
    except ValueError as error:
        raise ValueError("PAN_KEY must contain valid hexadecimal data") from error

    if len(key) not in (16, 24, 32):
        raise ValueError("PAN_KEY must decode to 16, 24, or 32 bytes")

    return key


def encrypt_pan(pan):
    """Encrypt a PAN using AES-GCM with a fresh random nonce."""
    if not isinstance(pan, str):
        raise TypeError("PAN must be a string")

    aesgcm = AESGCM(get_pan_key())
    nonce = os.urandom(12)

    cipher_text = aesgcm.encrypt(
        nonce,
        pan.encode("utf-8"),
        None
    )

    return (nonce + cipher_text).hex()


def generate_signing_key():
    """Generate a 2048-bit RSA private signing key."""
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )


def parse_form16(xml_text):
    """Safely parse salary and TDS values from Form 16 XML."""
    if not isinstance(xml_text, str):
        raise TypeError("XML input must be a string")

    root = ElementTree.fromstring(xml_text)

    salary_element = root.find("salary")
    tds_element = root.find("tds")

    if salary_element is None or tds_element is None:
        raise ValueError("XML must contain salary and tds elements")

    if salary_element.text is None or tds_element.text is None:
        raise ValueError("Salary and TDS values cannot be empty")

    return int(salary_element.text), int(tds_element.text)


def main():
    """Run sample calculations and demonstrate security functions."""
    print(
        f"New regime, salary 12,75,000: "
        f"{calculate_new_regime_tax(1275000)}"
    )
    print(
        f"New regime, salary 18,00,000: "
        f"{calculate_new_regime_tax(1800000)}"
    )

    deductions = {"80C": 200000, "80D": 30000}

    print(
        f"Old regime, salary 18,00,000: "
        f"{calculate_old_regime_tax(1800000, 35, deductions)}"
    )

    print(
        f"Better regime: "
        f"{choose_better_regime(1800000, 35, deductions)}"
    )

    print(f"Basic exemption at age 80: {get_basic_exemption(80)}")

    pan = "ABCDE1234F"
    print(f"PAN '{pan}' valid? {is_valid_pan(pan)}")

    first_encryption = encrypt_pan(pan)
    second_encryption = encrypt_pan(pan)

    print(
        f"Same PAN encrypts differently? "
        f"{first_encryption != second_encryption}"
    )

    xml_data = (
        "<form16><salary>1800000</salary>"
        "<tds>150000</tds></form16>"
    )

    print(f"Form 16: {parse_form16(xml_data)}")

    signing_key = generate_signing_key()
    print(f"Signing key size: {signing_key.key_size}")


if __name__ == "__main__":
    main()
