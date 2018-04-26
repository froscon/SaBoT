This is the **S**ponsoring **a**nd **Bo**oth **T**oolkit used by [FrOSCon](www.froscon.de) to manage their sponsors, exhibitors and devrooms.

Although everything is currently glued together, the three modules
can be used mostly independently of each other. The sponsoring module
can even be seen as two models - one to manage the sponsors and another
to manage invoices. It can very well be used without
the invoice functionalities.

The software was (and still is) designed with FrOSCon and its
organization processes in mind. Consequently, it may not fit
100% to your needs. However, we hope that it provides you with
a large codebase that is (more or less) easily adaptable to your
needs using Django's automagic generation features.

The development cycle of this project follows the preparation
of FrOSCon and thus often requires a fast implementation of
new features. This leads to a software quality that is in
some parts of the code lower than I would like it to be. Anyway,
I try to clean up the code when I find the time later on.
Nevertheless, I believe the basic ideas and concepts are clean.

Most of the software can be run standalone. Motivated by our
software environment, SaBoT integrates with RT as ticket service
for the sponsors functionality. Moreover, we use smskaufen.com
as a service provider to send out good old snail mails (hard copy
version of the invoices).

Additionally, we use [django-auth-ldap](https://github.com/django-auth-ldap/django-auth-ldap) in our production environment
to support LDAP user management for the organization team.

In case you're considering using SaBoT for your conference and still
have questions, feel free to [contact me](mailto:Martin.Lang@froscon.org).