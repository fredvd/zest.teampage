#!/bin/bash

# don't forget to activate your i18ndude workingenv before running this
# script.

I18NDUDE="i18ndude"
PRODUCTNAME="zest.teampage"
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
# Also merge it with generated.pot, which includes the items
# from schema.py

$I18NDUDE rebuild-pot --pot locales/${PRODUCTNAME}.pot --merge locales/manual.pot --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the .po files
for po in locales/*/LC_MESSAGES/${PRODUCTNAME}.po; do
    $I18NDUDE sync --pot locales/${PRODUCTNAME}.pot $po
done
