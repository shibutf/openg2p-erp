# Developer Installation and Setup

This document contains installation and setup instructions for running Openg2p Modules locally.

## Pre-requisites

- Install python3
- Then install `setuptools` and `wheel`.
    ```sh
    pip3 install setuptools wheel
    ```
- Install npm
-   ```sh
    sudo npm install -g rtlcss
    ```
- If OS is Linux; install the following modules:
    ```sh
    sudo apt install libxml2-dev libxslt1-dev libsasl2-dev libldap2-dev
    ```
- Install virtualenv.
- Install postgresql locally.
- Create a role/user in postgresql of name "openg2p" (with password atuhentication type, not peer type).
- Create a db of name "openg2p" with owner as "openg2p" role (created above)
- Create an extension within the "openg2p" db, called "pg_trgm"
    ```sql
    create extension pg_trgm;
    ```

## Installation

-   ```sh
    mkdir openg2p
    cd openg2p
    ```
- Create virtualenv. Example:
    ```sh
    virtualenv odooenv
    ```
- Clone `odoo` version 12.0, `openg2p-erp`, `openg2p-erp-community-addon` repositories.
    ```sh
    git clone https://github.com/odoo/odoo -b 12.0
    git clone https://github.com/mosip/openg2p-erp -b develop
    git clone https://github.com/mosip/openg2p-erp-community-addon -b 0.1-rc1
    ```
- Now the current folder structure should be similar to:
    ```
    openg2p
    |--odooenv
    |--odoo
    |--openg2p-erp
    |--openg2p-erp-community-addon
    ```
- Activate virtualenv:
    ```sh
    source odooenv/bin/activate
    ```
- Install python requirements. (The following might require the user to install the necessary development libraries when prompted)
    ```sh
    pip3 install -r odoo/requirements.txt
    pip3 install -r openg2p-erp/requirements.txt
    ```
- To run odoo (requires virtualenv to be active before running):
  - The following can also be done from the UI, in the "Apps" menu.
  - If running odoo for first time, (i.e., db not initialized), then run this
    ```sh
    python3 odoo/odoo-bin -r openg2p -d openg2p -w <password for openg2p role/db-user> --addons-path=odoo/addons,openg2p-erp,openg2p-erp-community-addon -i base,odk-connector,openg2p_package
    ```
  - If db already initialized, but there is a change in any `model` or `view` of any module, then run this:
    ```sh
    python3 odoo/odoo-bin -r openg2p -d openg2p -w <password for openg2p role/db-user> --addons-path=odoo/addons,openg2p-erp,openg2p-erp-community-addon -u <module list in which there are changes>
    ```
  - If there is no `model` or `view` change, but there is some other code change, then simply run this:
    ```sh
    python3 odoo/odoo-bin -r openg2p -d openg2p -w <password for openg2p role/db-user> --addons-path=odoo/addons,openg2p-erp,openg2p-erp-community-addon
    ```
- Launch `localhost:8069` on browser.

## Notes

- To increase odoo request timeout, use this following argument with the above run commands (Following limit is in seconds).
    ```
    --limit-time-real=10000
    ```