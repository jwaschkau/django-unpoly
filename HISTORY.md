# History

## 0.1.2 (2021-08-13)

- Added server side support for Unpoly headers when redirecting.
- Added X-Up-Target support for Django class-based views.

## 0.1.1 (2021-06-23)

* Fixes `X-Up-Target` not considered in middleware.
* Fixes detection of django-debug-toolbar. Now no JavaScript-Errors will be triggered if djdt is not initialized.
* Renamed all UnpolyXXX classes to UpXXX.
* If a version tracked object was modified status code 410 will be set for UpException.

## 0.1.0 (2021-06-07)

* First release on PyPI.
