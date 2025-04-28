CHARITY DONATION TRACKING DATABASE

Features
Manage Donors, Businesses, Beneficiaries, Events, Volunteers, and Donations.
Search donations by donor, event, business, beneficiary, or volunteer.
Enforce database integrity with foreign keys and cascading deletions.
User-friendly error handling to avoid crashes and wrong input.
Clear menus, tips, and simple interface.

Important Notes
Foreign keys are enforced with PRAGMA foreign_keys = ON in SQLite.
Cascading deletes apply between Events and Volunteers only.
Manual checks are used to prevent deletion of donors, businesses, events, or beneficiaries that still have donations linked.
