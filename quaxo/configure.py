import os

CONFIG_PATH = os.path.expanduser("~/.quaxo/config")
CRED_ITEMS = [
    (
        "aws", [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "ZEPHYR_S3_BUCKET",
        ],
    ),
]
DEFAULTS = {
    "STUB_PREFIX": os.path.expanduser("~/.quaxo/"),
}
