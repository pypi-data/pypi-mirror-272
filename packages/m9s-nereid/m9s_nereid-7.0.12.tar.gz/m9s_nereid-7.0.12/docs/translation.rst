Translation
===========

Best practice for Nereid Translations is a little bit different from the
usual procedure in Tryton due to the different nature of the
translatable messages in Nereid.
For best results the following workflow is recommended:

- Import translations as usual by installing the module with the desired
  language.

- Run 'Set translations' to import new messages into the database.

- This is the additional step recommended in Nereid:
  Run 'Update translations' just once to get the new translations copied
  to your language *and* updated with the proposal evtl. found on an (old)
  existent string.

- Run 'Clean translations' to remove obsolete messages, that could lead
  to errors in translation mechanism and that are needless to translate.

- Now work on 'Update translations' the second time on a clean set of
  the actual messages. Don't forget to control and unmark fuzzy messages
  that got a proposal from an old string.

- When done, run as usual 'Export translations'.

- Enjoy!

.. note:: When working on translations to be included in the upstream
        package, please work on a clean template tree without
        customizations.


.. note:: As of version 7.0 the cleanup of unused database connections
        in trytond can interfere with the connection management of nereid.
        Pay attention to

        - either set the database timeout value in the trytond
          configuration to a high enough value to guarantee an access to the
          database in the meantime (e.g. 864000 for ten days)

        - or configure trytond to use the same database for default operations
          by setting the default_name in the database section of to the name
          of your database.
