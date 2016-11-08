Changelog of lizard-efcis
===================================================


0.2 (unreleased)
----------------
- Add 'omschrijving' field to MeetStatus, serializer.

- Added API for locations, including coloring of the points per value.

- Added option for csv export of opnames. Add ``format=csv`` to the API call.

- Split graph API into a separate /graphs listing all lines (without data) and
  separate views for individual line and boxplot data.

- Accepting POST in addition to GET in most of the API: this dirty hack works
  around issues with too-long URLs.

- Added scatterplot endpoints.

- Looking for photos with filenames (minus ``.jpg``) that match a Location's
  ``loc_id`` field. The photos should be placed in a ``photos/`` subdirectory
  of the ``MEDIA_ROOT``.

- Added 'Uitvoerende' model, related to activity.

- Admin improvements: better filtering, better string representations.

- Added several status domain tables, replacing string fields. Some status
  tables have been moved around and/or renamed (mostly only by editing
  ``verbose_name``, btw).

- Added security: Opnames that are not validated aren't shown to
  non-maintainers. "Thread local storage" is used for that.

- Huge (5x+) speed increase for the most expensive queries.

- KRW areas can now be loaded and shown.

- Using very quick count for opnames.

- Added indexerror-preventing safety valves.

- Added admin action to set opnames to 'validated' directly.


0.1 (2015-03-09)
----------------

- Initial project structure created with nensskel 1.34.

- Added django models for importing efcis data.

- Added csv imports for efcis data.

- Added API for graph lines, parameter trees and measurement data.
