# Administrator's Guide for Usage of MOSIP's OpenG2P

This guide describes the administrator' functions. After installing the OpenG2P framework, Administrator user is auto created. 

## Glossary

This section describes the terminology used in OpenG2P.

* `Company`: A Company in OpenG2P is equivalent to an *Organization* that is providing benefits to beneficiaries.
* `Program`: A Program in OpenG2P is equivalent to a benefit scheme. Each organization could be running multiple such *programs* to benefit the beneficiaries.
* `Beneficiary`: A Beneficiary in OpenG2P is equivalent to a person who is eligible for (or one who is already) receiving benefit from some particular program from any organization.
* `Program Enrollment`: A beneficiary could be enrolled into multiple programs. The mapping of each *beneficiary* to a *program* that they are enrolled into is called  *Program Enrollment* in OpenG2P.
    * *Program Enrollment start date* describes the date on which the *beneficiary* started receiving the benefit under the given *program*.
    * *Program Enrollment end date* describes the date on which the *beneficiary* is going to stop receiving benefit under the given *program*.
    * *Program Enrollment amount* describes the amount that the *beneficiary* would receive for each benefit period under the given *program*.
    * *Program Enrollment total remuneration* describes the total amount that the *beneficiary* has received till date under the given *program*.
* `User`: A *user* in OpenG2P is equivalent to a Program Enrollment Officer under each *organization*  who is responsible for creating *programs*, creating/enrolling/disenrolling *beneficiaries* into/from their *organization programs*.
* `Administrator` or `admin` is also a *user* who has access to all the apps and settings on OpenG2P. Additionally, the admin also has access to all the organizations, users, programs, beneficiaries, and program enrollments.
* `Identification`- is an object in OpenG2P which is associated with a beneficiary. A beneficiary could be identified by multiple such IDs- passport, Tax ID, etc.

##  Identification creation

This section describes how to configure/create identifications for beneficiaries.

#### Prerequisite 

This identification should also be configured before installation using the following environment variables. To know more, refer [install instructions](https://github.com/mosip/openg2p-erp-docker/tree/develop#installation-on-kubernetes-cluster). 
  - `PROGRAM_ENROLLMENT_ON_IMPORT_BENEFICIARY_BASE_ID_LABEL`: `Tax ID`
  - `PROGRAM_ENROLLMENT_ON_IMPORT_BENEFICIARY_BASE_ID`: `taxid`

* Login as `admin`.
* Navigate to *Beneficiaries* app -> Configuration menu -> Identification
* Create a new Identification with the following properties.
  - ID Name: `Tax ID`
  - Code: `taxid`

![Create Identification](./images/identification.png)

### 3.2. Organization creation

Follow these instructions to create a new company/organization in OpenG2P.

- Login as `admin`.
- Navigate to *Settings* app.
- Click on *Users & Companies*, then on *Companies*.
- Create a new company here, with the required details.

![Create Company](./images/company.png)

- Since `admin` created the companies, `admin` is part of all of the companies/organizations by default.
- After creating companies, logout as `admin`, then login back as `admin` for the created companies to get reflected.
- The list of available companies/organizations for the currently logged in user (i.e., `admin`) will be reflected in the dropdown in the top right corner.
- For each company in the dropdown on the top right, navigate to *Settings* app, and then to *General Settings* Menu, and change the *Background Image* as required.

### 3.3. User creation

Following section describes how to create *users* (Program Enrollment Officers) within each company.

- Login as `admin`. Select the company/organization in which the user is to be created. (On the company dropdown on the top right corner).
- Create a new user with the required email and name.
- Assign only the `Program Enrollment Officer` role to the user, and remove all the other roles. The following image show how the final roles should look like.

![User Roles](./images/user-roles.png)

- Click *Save* to create the user.
- Upon creating user(s), select the user(s), click on *Action*. Then click *Change Password*.
- Assign some temporary password to each user, and instruct the required users to change their password immediately upon logging in.


